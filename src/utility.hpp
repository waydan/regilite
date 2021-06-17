#ifndef REGILITE_UTILITY_HPP
#define REGILITE_UTILITY_HPP

#include <type_traits>

namespace regilite {
namespace detail {

template <typename Int>
constexpr auto lsb(Int value) noexcept
    -> std::enable_if_t<std::is_integral<Int>::value, int>
{
    auto x = static_cast<std::make_unsigned_t<Int>>(value);
    int lsb = sizeof(x) * 8;
    for (; x != 0; x <<= 1u)
        --lsb;
    return lsb;
}

template <typename UInt>
constexpr auto masks_overlap(UInt a, UInt b) noexcept
    -> std::enable_if_t<std::is_unsigned<UInt>::value, bool>
{
    return (a ^ b) != (a | b);
}

template <typename T>
constexpr auto make_volatile_ref(T& x) noexcept -> volatile T&
{
    return *const_cast<volatile T*>(&x);
}

template <typename T>
constexpr auto make_volatile_ref(const T& x) noexcept -> const volatile T&
{
    return *const_cast<const volatile T*>(&x);
}

} // namespace detail
} // namespace regilite

#endif // REGILITE_UTILITY_HPP