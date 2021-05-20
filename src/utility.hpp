#ifndef REGILITE_UTILITY_HPP
#define REGILITE_UTILITY_HPP

namespace regilite::detail {

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

} // namespace regilite::detail

#endif // REGILITE_UTILITY_HPP