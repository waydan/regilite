#ifndef REGILITE_FIELD_HPP
#define REGILITE_FIELD_HPP

#include <cstdint>
#include <type_traits>

#include "traits.hpp"
#include "utility.hpp"

namespace regilite {

namespace detail {

template <typename UInt, UInt mask>
struct BitField {
    static_assert(std::is_unsigned<UInt>{} and not std::is_same<UInt, bool>{},
                  "Register<> type requires an unsigned integral as its "
                  "underlying representation.");

    UInt value;

    template <UInt rhs_mask>
    friend constexpr auto operator|(BitField lhs,
                                    BitField<UInt, rhs_mask> rhs) noexcept
        -> std::enable_if_t<!masks_overlap<UInt, mask, rhs_mask>{},
                            BitField<UInt, mask | rhs_mask>>
    {
        return BitField<UInt, mask | rhs_mask>{
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
struct Mask {
    static_assert(msb >= lsb, "Most significant bit may not be less than the "
                              "least significant");
    static_assert(lsb >= 0 and msb >= 0, "Bit positions may not be negative");

    static constexpr unsigned long value = (~1ul << msb) ^ (~0ul << lsb);
};


template <typename UInt, UInt mask_, typename ValType>
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

    ValType value_;

  public:
    static constexpr auto mask() noexcept -> UInt { return mask_; }

    constexpr explicit Field(ValType value) noexcept : value_(value) {}


    constexpr auto value() const noexcept { return value_; };

    constexpr auto as_bitfield() const noexcept
        -> detail::BitField<UInt, mask()>
    {
        return detail::BitField<UInt, mask()>{static_cast<UInt>(value_)
                                              << detail::lsb(mask())};
    }

    constexpr auto operator==(const Field& rhs) const noexcept -> bool
    {
        return value_ == rhs.value_;
    }


    constexpr auto operator!=(const Field& rhs) const noexcept -> bool
    {
        return not(*this == rhs);
    }
};

namespace detail {

template <typename UInt, UInt mask, typename ValType>
constexpr auto fold_fields(Field<UInt, mask, ValType> f)
{
    return f.as_bitfield();
}

template <typename UInt, UInt mask, typename ValType, UInt... masks,
          typename... ValTypes>
constexpr auto fold_fields(Field<UInt, mask, ValType> f,
                           Field<UInt, masks, ValTypes>... fs)
{
    return fold_fields(f) | fold_fields(fs...);
}

} // namespace detail
} // namespace regilite

#endif // REGILITE_FIELD_HPP
