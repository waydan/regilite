#ifndef REGILITE_REGISTER_HPP
#define REGILITE_REGISTER_HPP

#include <cstdint>
#include <type_traits>

#include "basicfield.hpp"
#include "field_access.hpp"
#include "utility.hpp"

namespace regilite {
namespace detail {

template <typename R>
struct register_traits;
}

template <typename Impl, typename... MemberFields>
class RegisterProxy
{
  protected:
    template <typename... Fields>
    static constexpr bool is_member_field = traits::conjunction(
        traits::is_pack_element<Fields, MemberFields...>{}...);

    static constexpr mask_t static_zero =
        detail::SafeWrite<detail::SafeWriteDefault::Zero, MemberFields...>{};

  public:
    using storage_type = typename detail::register_traits<Impl>::storage_type;
    static_assert(traits::is_storage_type<storage_type>{},
                  "BasicRegister<> type requires an unsigned integral as its "
                  "underlying representation.");


    class Snapshot
    {
        storage_type state_;

        class FieldExtractor
        {
            storage_type state_;

            // Prevent user code from creating named FieldExtractor object
            FieldExtractor(FieldExtractor&&) = default;
            // RegisterProxy and Snapshot are friends which enables passing
            // FieldExtractor&&
            friend class RegisterProxy;

          public:
            constexpr FieldExtractor(storage_type s) noexcept : state_{s} {}

            template <typename Field,
                      typename = std::enable_if_t<is_member_field<Field>>>
            constexpr operator Field() const noexcept
            {
                return Field{static_cast<typename Field::value_type>(
                    (state_ & Field::mask()) >> detail::lsb(Field::mask()))};
            }
        };

        template <mask_t mask>
        auto match(detail::BasicField<storage_type, mask> f) const noexcept
            -> bool
        {
            return f.value() == (state_ & mask);
        }


      public:
        explicit constexpr Snapshot(storage_type s) : state_{s} {};

        constexpr auto raw() const noexcept -> storage_type { return state_; }

        template <typename Field, typename... Fields>
        auto modify(Field f, Fields... fs) noexcept -> std::enable_if_t<
            is_member_field<
                Field> and !detail::fields_overlap<Field, Fields...>{},
            Snapshot&>
        {
            const auto fields = detail::fold_fields<storage_type>(f, fs...);
            state_ = detail::insert_bits(state_, fields);
            return *this;
        }


        constexpr auto extract_field() const noexcept
        {
            return FieldExtractor{state_};
        }


        template <typename Field>
        auto match(Field f) const noexcept
            -> std::enable_if_t<is_member_field<Field>, bool>
        {
            return f == decltype(f){extract_field()};
        }


        template <typename Field, typename... Fields>
        auto match_all(Field f, Fields... fs) const noexcept
            -> std::enable_if_t<
                is_member_field<
                    Field,
                    Fields...> and !detail::fields_overlap<Field, Fields...>{},
                bool>
        {
            const auto fields = detail::fold_fields<storage_type>(f, fs...);
            return match(fields);
        }


        template <typename Field>
        auto match_any(Field f) const noexcept
            -> std::enable_if_t<is_member_field<Field>, bool>
        {
            return match(f);
        }

        template <typename Field, typename... Fields>
        auto match_any(Field f, Fields... fs) const noexcept
            -> std::enable_if_t<is_member_field<Field, Fields...>, bool>
        {
            return match_any(f) or match_any(fs...);
        }
    }; // class Snapshot


    auto write(Snapshot s) noexcept -> void
    {
        static_cast<Impl*>(this)->volatile_write(s.raw());
    }


    template <
        typename Field, typename... Fields,
        typename = std::enable_if_t<
            is_member_field<
                Field,
                Fields...> and !detail::fields_overlap<Field, Fields...>{}>>
    auto write(Field f, Fields... fs) noexcept
    {
        const auto fields = detail::fold_fields<storage_type>(f, fs...);
        return static_cast<Impl*>(this)->write_field(
            fields
            | detail::BasicField<storage_type, static_zero & ~fields.mask()>{
                0});
    }


    auto read() const noexcept -> Snapshot
    {
        return Snapshot{static_cast<const Impl*>(this)->volatile_read()};
    }


    constexpr auto extract_field() const noexcept
    {
        return read().extract_field();
    }


    template <typename Field>
    auto match(Field f) const noexcept
        -> std::enable_if_t<is_member_field<Field>, bool>
    {
        return read().match(f);
    }


    template <typename Field, typename... Fields>
    auto match_all(Field f, Fields... fs) const noexcept -> std::enable_if_t<
        is_member_field<
            Field, Fields...> and !detail::fields_overlap<Field, Fields...>{},
        bool>
    {
        return read().match_all(f, fs...);
    }


    template <typename Field, typename... Fields>
    auto match_any(Field f, Fields... fs) const noexcept
        -> std::enable_if_t<is_member_field<Field, Fields...>, bool>
    {
        return read().match_any(f, fs...);
    }
};

} // namespace regilite

#endif // REGILITE_REGISTER_HPP