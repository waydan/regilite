#ifndef REGILITE_REGISTER_HPP
#define REGILITE_REGISTER_HPP

#include <cstdint>
#include <type_traits>

#include "field.hpp"
#include "utility.hpp"

namespace regilite {

template <typename UInt, typename... Fields>
class Register
{
    static_assert(std::is_unsigned<UInt>{} and not std::is_same<UInt, bool>{},
                  "Register<> type requires an unsigned integral as its "
                  "underlying representation.");

    UInt state_;

    template <typename... Fs>
    using is_member_field =
        traits::conjunction<traits::is_one_of<Fs, Fields...>{}...>;

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
        auto match(detail::BitField<UInt, mask> field) const noexcept -> bool
        {
            return field.value == (state_ & mask);
        }


      public:
        explicit constexpr Snapshot(UInt s) : state_{s} {};

        constexpr auto raw() const noexcept -> UInt { return state_; }

        template <typename F, typename... Fs>
        auto modify(F field, Fs... fields) noexcept
            -> std::enable_if_t<is_member_field<F>{}, Snapshot&>
        {
            const auto joined_fields = detail::fold_fields(field, fields...);
            state_ = detail::insert_bits(state_, joined_fields);
            return *this;
        }


        constexpr auto extract() const noexcept
        {
            return FieldExtractor{state_};
        }


        template <typename F>
        auto match(F field) const noexcept
            -> std::enable_if_t<is_member_field<F>{}, bool>
        {
            return field == decltype(field){extract()};
        }


        template <typename F, typename... Fs>
        auto match_all(F field, Fs... fields) const noexcept
            -> std::enable_if_t<is_member_field<F, Fs...>{}, bool>
        {
            const auto joined_fields = detail::fold_fields(field, fields...);
            return match(joined_fields);
        }


        template <typename F>
        auto match_any(F field) const noexcept
            -> std::enable_if_t<is_member_field<F>{}, bool>
        {
            return match(field);
        }

        template <typename F, typename... Fs>
        auto match_any(F field, Fs... fields) const noexcept
            -> std::enable_if_t<is_member_field<F, Fs...>{}, bool>
        {
            return match_any(field) or match_any(fields...);
        }
    };


    auto write(Snapshot s) noexcept -> void
    {
        detail::make_volatile_ref(state_) = s.raw();
    }


    template <typename F, typename... Fs>
    auto write(F field, Fs... fields) noexcept -> std::enable_if_t<
        is_member_field<F, Fs...>{}
        and !detail::masks_overlap<UInt, F::mask(), Fs::mask()...>{}>
    {
        write(read().modify(field, fields...));
    }


    auto read() const noexcept -> Snapshot
    {
        return Snapshot{detail::make_volatile_ref(state_)};
    }


    constexpr auto extract() const noexcept { return read().extract(); }


    template <typename F>
    auto match(F field) const noexcept
        -> std::enable_if_t<is_member_field<F>{}, bool>
    {
        return read().match(field);
    }


    template <typename F, typename... Fs>
    auto match_all(F field, Fs... fields) const noexcept
        -> std::enable_if_t<is_member_field<F, Fs...>{}, bool>
    {
        return read().match_all(field, fields...);
    }


    template <typename F, typename... Fs>
    auto match_any(F field, Fs... fields) const noexcept
        -> std::enable_if_t<is_member_field<F, Fs...>{}, bool>
    {
        return read().match_any(field, fields...);
    }
};

} // namespace regilite


#endif // REGILITE_REGISTER_HPP