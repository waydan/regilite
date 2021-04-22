#ifndef REGISTER_HPP
#define REGISTER_HPP

#include <bit>
#include <cstdint>
#include <type_traits>
#include <utility>

namespace registex {

template <std::uint32_t mask>
struct BitMask {

    template <std::uint32_t other_mask>
    constexpr auto operator|(BitMask<other_mask>) noexcept
        -> BitMask<mask | other_mask>;

    static constexpr std::uint32_t value = mask;
    static constexpr unsigned char lsb = std::countr_zero(mask);
    static constexpr unsigned char msb = std::countl_zero(mask);
};

template <unsigned char msb, unsigned char lsb>
using mask_from_range =
    std::enable_if_t<(lsb <= msb) and (msb < sizeof(std::uint32_t) * 8),
                     BitMask<((1u << msb - lsb + 1) - 1) << lsb>>;


struct NoShift_t {};
constexpr inline NoShift_t no_shift{};


template <typename Reg, typename Mask>
struct Field {
    explicit constexpr Field(std::uint32_t value, NoShift_t) : value_(value) {}
    explicit constexpr Field(std::uint32_t value)
        : Field{value << Mask::lsb, no_shift}
    {}

    std::uint32_t value_;

    template <typename OtherMask>
    constexpr auto operator|(const Field<Reg, OtherMask>& other) const noexcept
    {
        return Field<Reg, decltype(std::declval<Mask>()
                                   | std::declval<OtherMask>())>{
            value_ | other.value_, no_shift};
    }
};

template <std::uintptr_t (&address)()>
struct Register {

    template <typename Mask>
    static auto write(Field<Register, Mask> field)
    {
        const auto write_address = address();
        const std::uint32_t write_value =
            *reinterpret_cast<volatile std::uint32_t*>(write_address)
                & ~Mask::value
            | field.value_;
        *reinterpret_cast<volatile std::uint32_t*>(write_address) = write_value;
        return std::make_pair(write_value, write_address);
    }
};


template <std::uint32_t& reg>
auto make_addr() -> std::uintptr_t
{
    return reinterpret_cast<std::uintptr_t>(&reg);
};


template <typename Reg, typename... Masks>
auto write(Field<Reg, Masks>... fields)
{
    const auto joined_fields = (fields | ...);
    return Reg::write(joined_fields);
};

} // namespace registex

#endif // REGISTER_HPP