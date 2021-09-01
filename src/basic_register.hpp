// Copyright 2021 Daniel Way
// SPDX-License-Identifier: Apache-2.0

#ifndef REGILITE_BASIC_REGISTER_HPP
#define REGILITE_BASIC_REGISTER_HPP

#include <type_traits>

#include "basic_field.hpp"
#include "bitmask.hpp"
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
        return static_cast<storage_type>(detail::fold_masks(
                   mask, FieldSet::Reserved::mask(),
                   detail::mask_if<
                       MemberFields,
                       MemberFields::access::safe_write
                           != detail::SafeWriteDefault::Volatile>{}...))
               == static_cast<storage_type>(~storage_type{0u});
    }

  private:
    storage_type state_;

    template <typename Field>
    auto select_write(Field field, std::false_type) noexcept
    {
        const auto composite_field =
            fold_exclusive(field, typename FieldSet::SafeWriteZero{0});
        volatile_write(
            (volatile_read()
             & static_cast<storage_type>(~composite_field.mask()
                                         | FieldSet::AlwaysReadsZero::mask()
                                         | (FieldSet::AlwaysReadsReset::mask()
                                            & ~static_cast<mask_t>(reset))))
            | composite_field.value());
        return ReadModifyWrite{};
    }


    template <typename Field>
    auto select_write(Field field, std::true_type) noexcept
    {
        const auto overwrite_field = fold_exclusive(
            field, typename FieldSet::SafeWriteReset{
                       reset & FieldSet::SafeWriteReset::mask()});
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
        *static_cast<volatile storage_type*>(&state_) = s;
    }

    auto volatile_read() const noexcept -> storage_type
    {
        return *static_cast<const volatile storage_type*>(&state_);
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