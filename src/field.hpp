#ifndef REGILITE_FIELD_HPP
#define REGILITE_FIELD_HPP

#include <cstdint>
#include <type_traits>

#include "traits.hpp"
#include "utility.hpp"

namespace regilite {

namespace detail {
struct NoShift_t {};

template <typename UInt, UInt mask>
struct BitField {
    static_assert(std::is_unsigned<UInt>::value
                      and not std::is_same<UInt, bool>::value,
                  "Register<> type requires an unsigned integral as its "
                  "underlying representation.");

    UInt value;

    template <std::uint32_t rhs_mask>
    friend constexpr auto operator|(BitField lhs,
                                    BitField<UInt, rhs_mask> rhs) noexcept
        -> std::enable_if_t<!masks_overlap(mask, rhs_mask),
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


template <typename UInt, UInt mask>
class Field
{
    static_assert(std::is_unsigned<UInt>::value
                      and not std::is_same<UInt, bool>::value,
                  "Register<> type requires an unsigned integral as its "
                  "underlying representation.");

    UInt value_;

  public:
    constexpr explicit Field(std::uint32_t value) noexcept
        : Field(value << detail::lsb(mask), detail::NoShift_t{})
    {}

    constexpr explicit Field(std::uint32_t value, detail::NoShift_t) noexcept
        : value_(value)
    {}

    constexpr auto value() const noexcept { return value_; };

    constexpr auto as_bitfield() const noexcept -> detail::BitField<UInt, mask>
    {
        return detail::BitField<UInt, mask>{static_cast<UInt>(value_)};
    }
};

template <typename UInt, UInt mask>
constexpr auto operator==(const Field<UInt, mask>& lhs,
                          const traits::identity_t<Field<UInt, mask>>& rhs)
{
    return lhs.value() == rhs.value();
}


template <typename UInt, UInt mask>
constexpr auto operator!=(const Field<UInt, mask>& lhs,
                          const traits::identity_t<Field<UInt, mask>>& rhs)
    -> bool
{
    return not(lhs == rhs);
}


#ifndef __cpp_fold_expressions
template <typename UInt, UInt mask>
constexpr auto fold_fields(Field<UInt, mask> f)
{
    return f.as_bitfield();
}
#endif

template <typename UInt, std::uint32_t mask, std::uint32_t... masks>
constexpr auto fold_fields(Field<UInt, mask> f, Field<UInt, masks>... fs)
{
#ifndef __cpp_fold_expressions
    return fold_fields(f) | fold_fields(fs...);
#else
    return (f.as_bitfield() | ... | fs.as_bitfield());
#endif
}

} // namespace regilite

#endif // REGILITE_FIELD_HPP
