#ifndef REGILITE_REGISTER_HPP
#define REGILITE_REGISTER_HPP

#include <cstdint>
#include <type_traits>

#include "field.hpp"
#include "utility.hpp"

namespace regilite {

template <typename UInt, typename... MemberFields>
class Register
{
    static_assert(std::is_unsigned<UInt>{} and not std::is_same<UInt, bool>{},
                  "Register<> type requires an unsigned integral as its "
                  "underlying representation.");

    UInt state_;

    template <typename... Fields>
    using is_member_field =
        traits::conjunction<traits::is_one_of<Fields, MemberFields...>{}...>;

  public:
    class Snapshot
    {
        UInt state_;

        struct FieldExtractor {
            UInt state_;

            template <UInt mask, typename ValType,
                      typename = std::enable_if_t<
                          is_member_field<Field<UInt, mask, ValType>>{}>>
            constexpr operator Field<UInt, mask, ValType>() const noexcept
            {
                return Field<UInt, mask, ValType>{
                    static_cast<ValType>((state_ & mask) >> detail::lsb(mask))};
            }
        };

        template <UInt mask>
        auto match(detail::BitField<UInt, mask> f) const noexcept -> bool
        {
            return f.value == (state_ & mask);
        }


      public:
        explicit constexpr Snapshot(UInt s) : state_{s} {};

        constexpr auto raw() const noexcept -> UInt { return state_; }

        template <typename Field, typename... Fields>
        auto modify(Field f, Fields... fs) noexcept -> std::enable_if_t<
            is_member_field<Field>{}
                and !detail::fields_overlap<Field, Fields...>{},
            Snapshot&>
        {
            const auto fields = detail::fold_fields(f, fs...);
            state_ = detail::insert_bits(state_, fields);
            return *this;
        }


        constexpr auto extract() const noexcept
        {
            return FieldExtractor{state_};
        }


        template <typename Field>
        auto match(Field f) const noexcept
            -> std::enable_if_t<is_member_field<Field>{}, bool>
        {
            return f == decltype(f){extract()};
        }


        template <typename Field, typename... Fields>
        auto match_all(Field f, Fields... fs) const noexcept
            -> std::enable_if_t<
                is_member_field<Field, Fields...>{}
                    and !detail::fields_overlap<Field, Fields...>{},
                bool>
        {
            const auto fields = detail::fold_fields(f, fs...);
            return match(fields);
        }


        template <typename Field>
        auto match_any(Field f) const noexcept
            -> std::enable_if_t<is_member_field<Field>{}, bool>
        {
            return match(f);
        }

        template <typename Field, typename... Fields>
        auto match_any(Field f, Fields... fs) const noexcept
            -> std::enable_if_t<is_member_field<Field, Fields...>{}, bool>
        {
            return match_any(f) or match_any(fs...);
        }
    };


    auto write(Snapshot s) noexcept -> void
    {
        detail::make_volatile_ref(state_) = s.raw();
    }


    template <typename Field, typename... Fields>
    auto write(Field f, Fields... fs) noexcept
        -> std::enable_if_t<is_member_field<Field, Fields...>{}
                            and !detail::fields_overlap<Field, Fields...>{}>
    {
        write(read().modify(f, fs...));
    }


    auto read() const noexcept -> Snapshot
    {
        return Snapshot{detail::make_volatile_ref(state_)};
    }


    constexpr auto extract() const noexcept { return read().extract(); }


    template <typename Field>
    auto match(Field f) const noexcept
        -> std::enable_if_t<is_member_field<Field>{}, bool>
    {
        return read().match(f);
    }


    template <typename Field, typename... Fields>
    auto match_all(Field f, Fields... fs) const noexcept
        -> std::enable_if_t<is_member_field<Field, Fields...>{}
                                and !detail::fields_overlap<Field, Fields...>{},
                            bool>
    {
        return read().match_all(f, fs...);
    }


    template <typename Field, typename... Fields>
    auto match_any(Field f, Fields... fs) const noexcept
        -> std::enable_if_t<is_member_field<Field, Fields...>{}, bool>
    {
        return read().match_any(f, fs...);
    }
};

} // namespace regilite

#endif // REGILITE_REGISTER_HPP