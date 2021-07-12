#ifndef REGILITE_FIELD_HPP
#define REGILITE_FIELD_HPP

#include <cassert>
#include <cstdint>
#include <type_traits>

#include "bit_mask.hpp"
#include "traits.hpp"
#include "utility.hpp"

namespace regilite {

namespace detail {

template <typename UInt, mask_t bit_mask>
struct BitField {
    static_assert(std::is_unsigned<UInt>{} and not std::is_same<UInt, bool>{},
                  "Register<> type requires an unsigned integral as its "
                  "underlying representation.");

    UInt value;

    static constexpr auto mask() -> mask_t { return bit_mask; }

    template <mask_t rhs_mask>
    friend constexpr auto operator|(BitField lhs,
                                    BitField<UInt, rhs_mask> rhs) noexcept
        -> std::enable_if_t<!masks_overlap<bit_mask, rhs_mask>{},
                            BitField<UInt, bit_mask | rhs_mask>>
    {
        return BitField<UInt, bit_mask | rhs_mask>{
            lhs.value | rhs.value,
        };
    }
};


template <typename UInt, mask_t mask>
constexpr auto insert_bits(UInt value, BitField<UInt, mask> field) noexcept
    -> UInt
{
    return (value & ~static_cast<UInt>(mask)) | field.value;
}

} // namespace detail

template <int msb, int lsb = msb>
struct Mask : std::integral_constant<mask_t, (~1ul << msb) ^ (~0ul << lsb)> {
    static_assert(msb >= lsb, "Most significant bit may not be less than the "
                              "least significant");
    static_assert(lsb >= 0 and msb >= 0, "Bit positions may not be negative");
};


template <typename ValType, mask_t bit_mask>
class Field
{
    static_assert(
        std::is_unsigned<ValType>{} or std::is_enum<ValType>{},
        "Field only supports unsigned integrals or enumeration types");

  public:
    using value_type = ValType;

  private:
    value_type value_;

  public:
    static constexpr auto mask() noexcept -> mask_t { return bit_mask; }

    constexpr explicit Field(value_type value) noexcept : value_(value)
    {
        assert(0u
                   == (~static_cast<decltype(traits::to_uint(value))>(
                           mask() >> detail::lsb(mask()))
                       & traits::to_uint(value))
               and "Value overflows the field boundary");
    }

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

namespace detail {

template <typename UInt, typename ValType, mask_t mask>
constexpr auto to_bitfield(Field<ValType, mask> f) noexcept
{
    return detail::BitField<UInt, mask>{static_cast<UInt>(f.value())
                                        << detail::lsb(mask)};
}

template <typename F, typename... Fs>
using fields_overlap = masks_overlap<F::mask(), Fs::mask()...>;


template <typename UInt, typename ValType, mask_t mask>
constexpr auto fold_fields(Field<ValType, mask> f) noexcept
    -> BitField<UInt, mask>
{
    return to_bitfield<UInt>(f);
}

template <typename UInt, typename ValType, mask_t mask, typename... ValTypes,
          mask_t... masks>
constexpr auto fold_fields(Field<ValType, mask> f,
                           Field<ValTypes, masks>... fs) noexcept
    -> BitField<UInt, fold_masks(mask, masks...)>
{
    return fold_fields<UInt>(f) | fold_fields<UInt>(fs...);
}

} // namespace detail
} // namespace regilite

#endif // REGILITE_FIELD_HPP
