// Copyright 2021 Daniel Way
// SPDX-License-Identifier: Apache-2.0

#ifndef REGILITE_FIELD_HPP
#define REGILITE_FIELD_HPP

#include <cassert>
#include <type_traits>

#include "bitmask.hpp"
#include "field_traits.hpp"
#include "traits.hpp"
#include "utility.hpp"

namespace regilite {


template <typename ValType, mask_t bit_mask, typename FieldAccess = RW,
          typename = void /*shadow type*/>
class Field
{
    static_assert(std::is_unsigned<ValType>{} or std::is_enum<ValType>{},
                  "Field only supports unsigned integrals, booleans or "
                  "enumeration types");

  public:
    using value_type = ValType;
    using access = FieldAccess;

  private:
    value_type value_;

  public:
    constexpr explicit Field(value_type value) noexcept : value_(value)
    {
        assert((~static_cast<mask_t>(mask() >> offset())
                & static_cast<mask_t>(value))
                   == 0u
               and "Value overflows the field boundary");
    }
    static constexpr auto mask() noexcept -> mask_t { return bit_mask; }
    static constexpr auto offset() noexcept { return detail::lsb(mask()); }

    constexpr auto value() const noexcept -> value_type { return value_; };


    template <typename Other>
    friend constexpr auto operator==(const Field& lhs,
                                     const Other& rhs) noexcept
        -> std::enable_if_t<std::is_convertible<Other, Field>{}, bool>
    {
        return lhs.value() == static_cast<Field>(rhs).value();
    }

    template <typename Other>
    friend constexpr auto operator!=(const Field& lhs,
                                     const Other& rhs) noexcept
        -> std::enable_if_t<std::is_convertible<Other, Field>{}, bool>
    {
        return not(lhs == static_cast<Field>(rhs));
    }
};

} // namespace regilite

#endif // REGILITE_FIELD_HPP
