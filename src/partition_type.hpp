#ifndef REGILITE_ACCESS_PARTITION_HPP
#define REGILITE_ACCESS_PARTITION_HPP

#include <cstdint>

#include "bitmask.hpp"
#include "utility.hpp"


namespace regilite {
namespace detail {

template <int size>
struct Bytes;

template <>
struct Bytes<1> {
    using type = std::uint8_t;
};
template <>
struct Bytes<2> {
    using type = std::uint16_t;
};
template <>
struct Bytes<4> {
    using type = std::uint32_t;
};
template <>
struct Bytes<8> {
    using type = std::uint64_t;
};

// Returns the minimum number of bytes to contain an integral value
template <typename T>
constexpr auto min_bytes(T x)
    -> std::enable_if_t<std::is_integral<T>{}, std::uint8_t>
{
    constexpr auto type_size = static_cast<std::uint8_t>(sizeof(T));
    for (unsigned char n_bytes = 1u; n_bytes < type_size; n_bytes *= 2)
        if (x <= (T{1} << (n_bytes * 8)) - 1)
            return n_bytes;
    return type_size;
}

static_assert(min_bytes(0) == 1, "One byte needed to hold value zero");
static_assert(min_bytes(1) == 1, "One byte needed to hold value one");
static_assert(min_bytes(255) == 1, "2^8 - 1 = 255");
static_assert(min_bytes(256) == 2, "2^8 = 256");
static_assert(min_bytes(65536) == 4, "2^16 = 65536");


template <mask_t mask>
struct Partition {
    static_assert(mask != 0, "Mask must include at least one set bit.");

    using type =
        typename Bytes<(1 << (msb((msb(mask) ^ lsb(mask)) / 8) + 1))>::type;
    static constexpr auto size() noexcept -> int { return sizeof(type) * 8; }
    static constexpr auto offset() noexcept -> int
    {
        return lsb(mask) / size();
    }
};

} // namespace detail
} // namespace regilite
#endif // REGILITE_ACCESS_PARTITION_HPP