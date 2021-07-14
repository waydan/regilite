#ifndef REGILITE_ACCESS_PARTITION_HPP
#define REGILITE_ACCESS_PARTITION_HPP

#include <cstdint>

#include "bitmask.hpp"
#include "utility.hpp"


namespace regilite {
namespace detail {

template <int size>
struct Block;

template <>
struct Block<1> {
    using type = std::uint8_t;
};
template <>
struct Block<2> {
    using type = std::uint16_t;
};
template <>
struct Block<4> {
    using type = std::uint32_t;
};
template <>
struct Block<8> {
    using type = std::uint64_t;
};


template <mask_t mask>
struct Partition {
    static_assert(mask != 0, "Mask must include at least one set bit.");

    using type =
        typename Block<(1 << (msb((msb(mask) ^ lsb(mask)) / 8) + 1))>::type;
    static constexpr auto size() noexcept -> int { return sizeof(type) * 8; }
    static constexpr auto offset() noexcept -> int
    {
        return lsb(mask) / size();
    }
};

} // namespace detail
} // namespace regilite
#endif // REGILITE_ACCESS_PARTITION_HPP