#ifndef REGILITE_BASIC_REGISTER_HPP
#define REGILITE_BASIC_REGISTER_HPP

#include <type_traits>

#include "basic_field.hpp"
#include "register_proxy.hpp"
#include "traits.hpp"

namespace regilite {

struct Overwrite {};

struct ReadModifyWrite {};

template <typename UInt, UInt reset, typename... MemberFields>
class BasicRegister
    : public RegisterProxy<BasicRegister<UInt, reset, MemberFields...>,
                           MemberFields...>
{
    using Base = RegisterProxy<BasicRegister, MemberFields...>;
    friend Base;
    using typename Base::FieldSet;

  public:
    using storage_type =
        typename detail::register_traits<BasicRegister>::storage_type;

    static constexpr auto can_safely_overwrite(mask_t mask) noexcept -> bool
    {
        constexpr auto static_write_mask = FieldSet::safe_write_zero
                                           | FieldSet::safe_write_one
                                           | FieldSet::safe_write_reset;
        constexpr storage_type storage_mask = ~storage_type{0u};

        return static_cast<storage_type>(static_write_mask | mask)
               == storage_mask;
    }

  private:
    storage_type state_;

    template <typename Field>
    auto select_write(Field field, std::false_type) noexcept
    {
        constexpr auto zero_field =
            detail::BasicField<storage_type,
                               FieldSet::safe_write_zero & ~field.mask()>{0};
        const storage_type modified_state =
            detail::insert_bits(volatile_read(), field + zero_field);
        volatile_write(modified_state);
        return ReadModifyWrite{};
    }


    template <typename Field>
    auto select_write(Field field, std::true_type) noexcept
    {
        const auto overwrite_field = fold_exclusive(
            field, detail::BasicField<storage_type, FieldSet::safe_write_reset>{
                       reset & FieldSet::safe_write_reset});
        volatile_write(static_cast<storage_type>(overwrite_field.value()
                                                 << field.offset()));
        return Overwrite{};
    }

  protected:
    template <typename Field>
    auto write_field(Field field) noexcept
    {
        return select_write(
            field,
            std::integral_constant<bool, can_safely_overwrite(field.mask())>{});
    }

    auto volatile_write(storage_type s) noexcept -> void
    {
        *const_cast<volatile storage_type*>(&state_) = s;
    }

    auto volatile_read() const noexcept -> storage_type
    {
        return *const_cast<const volatile storage_type*>(&state_);
    }
};

namespace detail {
template <typename UInt, UInt reset, typename... MemberFields>
struct register_traits<BasicRegister<UInt, reset, MemberFields...>> {
    using storage_type = UInt;
};
} // namespace detail

} // namespace regilite

#endif // REGILITE_BASIC_REGISTER_HPP