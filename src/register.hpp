#ifndef REGISTER_HPP
#define REGISTER_HPP

#include <bit>
#include <cstdint>
#include <type_traits>
#include <utility>

namespace registex {

// [Pre => mask > 0]
constexpr auto lsb(std::uint32_t mask) noexcept -> unsigned char
{
    return std::countr_zero(mask);
}

// [Pre => mask > 0]
constexpr auto msb(std::uint32_t mask) noexcept -> unsigned char
{
    return sizeof(mask) * 8 - (std::countl_zero(mask) + 1);
}

constexpr auto mask_from_range(unsigned char msb, unsigned char lsb) noexcept
    -> std::uint32_t
{
    return (~std::uint32_t{1u} << msb) ^ (~std::uint32_t{0u} << lsb);
}

constexpr auto min_pow_8(std::uint32_t mask) noexcept -> unsigned char
{
    return (msb(mask) ^ lsb(mask)) / 8;
}

template <unsigned char exp>
struct Block;

template <>
struct Block<0> {
    using type = std::uint8_t;
};

template <>
struct Block<1> {
    using type = std::uint16_t;
};

template <>
struct Block<2> {
    using type = std::uint32_t;
};

template <unsigned char exp>
using Block_t = typename Block<exp>::type;


template <typename Uint, typename>
struct Action {
    Uint value;
    std::uintptr_t address;

    explicit constexpr Action(Uint val, std::uintptr_t addr)
        : value{val}, address{addr}
    {}
};

template <typename Uint>
using WriteAction = Action<Uint, struct Write_t>;


struct NoShift_t {};
constexpr inline NoShift_t no_shift{};


template <typename Reg, std::uint32_t mask>
struct Field {
    explicit constexpr Field(std::uint32_t value, NoShift_t) : value_(value) {}
    explicit constexpr Field(std::uint32_t value)
        : Field{value << lsb(mask), no_shift}
    {}

    std::uint32_t value_;

    template <std::uint32_t other_mask>
    constexpr auto operator|(const Field<Reg, other_mask>& other) const noexcept
    {
        return Field<Reg, mask | other_mask>{value_ | other.value_, no_shift};
    }
};

template <std::uintptr_t (&address)()>
struct Register {

    template <std::uint32_t mask>
    static auto write(Field<Register, mask> field)
    {
        const auto write_address = address();
        const std::uint32_t write_value =
            *reinterpret_cast<volatile std::uint32_t*>(write_address) & ~mask
            | field.value_;
        *reinterpret_cast<volatile std::uint32_t*>(write_address) = write_value;
        return WriteAction<std::uint8_t>(write_value, write_address + 1);
    }
};


template <std::uint32_t& reg>
auto make_addr() -> std::uintptr_t
{
    return reinterpret_cast<std::uintptr_t>(&reg);
};


template <typename Reg, std::uint32_t... masks>
auto write(Field<Reg, masks>... fields)
{
    return Reg::write((fields | ...));
};

} // namespace registex

#endif // REGISTER_HPP