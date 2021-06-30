#ifndef REGILITE_FIELD_HPP
#define REGILITE_FIELD_HPP

#include <cassert>
#include <cstdint>
#include <type_traits>

#include "traits.hpp"
#include "utility.hpp"

namespace regilite {

namespace detail {

template <typename UInt, UInt bit_mask>
struct BitField {
    static_assert(std::is_unsigned<UInt>{} and not std::is_same<UInt, bool>{},
                  "Register<> type requires an unsigned integral as its "
                  "underlying representation.");

    UInt value;

    static constexpr auto mask() -> UInt { return bit_mask; }

    template <UInt rhs_mask>
    friend constexpr auto operator|(BitField lhs,
                                    BitField<UInt, rhs_mask> rhs) noexcept
        -> std::enable_if_t<!masks_overlap<UInt, bit_mask, rhs_mask>{},
                            BitField<UInt, bit_mask | rhs_mask>>
    {
        return BitField<UInt, bit_mask | rhs_mask>{
            lhs.value | rhs.value,
        };
    }
};


template <typename UInt, UInt mask>
constexpr auto insert_bits(UInt value, BitField<UInt, mask> field) noexcept
    -> UInt
{
    return (value & ~mask) | field.value;
}

} // namespace detail

template <int msb, int lsb = msb>
struct Mask
    : std::integral_constant<unsigned long, (~1ul << msb) ^ (~0ul << lsb)> {
    static_assert(msb >= lsb, "Most significant bit may not be less than the "
                              "least significant");
    static_assert(lsb >= 0 and msb >= 0, "Bit positions may not be negative");
};


template <typename UInt, UInt bit_mask, typename ValType>
class Field
{
    static_assert(std::is_unsigned<UInt>{} and not std::is_same<UInt, bool>{},
                  "Register<> type requires an unsigned integral as its "
                  "underlying representation.");
    static_assert(
        sizeof(UInt) >= sizeof(ValType),
        "Value type may not be larger than storage type for a register");
    static_assert(
        std::is_unsigned<ValType>{} or std::is_enum<ValType>{},
        "Field only supports unsigned integrals or enumeration types");

  public:
    using value_type = ValType;

  private:
    value_type value_;

  public:
    static constexpr auto mask() noexcept -> UInt { return bit_mask; }

    constexpr explicit Field(value_type value) noexcept : value_(value)
    {
        assert(
            0u == (~(mask() >> detail::lsb(mask())) & static_cast<UInt>(value))
            and "Value overflows the field boundary");
    }

    constexpr auto value() const noexcept -> value_type { return value_; };

    constexpr operator detail::BitField<UInt, mask()>() const noexcept
    {
        return detail::BitField<UInt, mask()>{static_cast<UInt>(value_)
                                              << detail::lsb(mask())};
    }


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

namespace detail {

template <typename F, typename... Fs>
using fields_overlap =
    masks_overlap<decltype(F::mask()), F::mask(), Fs::mask()...>;

template <typename UInt, UInt mask, typename ValType>
constexpr auto fold_fields(Field<UInt, mask, ValType> f) noexcept
    -> BitField<UInt, mask>
{
    return f;
}

template <typename UInt, UInt mask, typename ValType, UInt... masks,
          typename... ValTypes>
constexpr auto fold_fields(Field<UInt, mask, ValType> f,
                           Field<UInt, masks, ValTypes>... fs) noexcept
{
    return fold_fields(f) | fold_fields(fs...);
}

} // namespace detail
} // namespace regilite

#endif // REGILITE_FIELD_HPP
