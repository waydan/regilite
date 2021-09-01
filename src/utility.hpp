// Copyright 2021 Daniel Way
// SPDX-License-Identifier: Apache-2.0

#ifndef REGILITE_UTILITY_HPP
#define REGILITE_UTILITY_HPP

#include <type_traits>

namespace regilite {
namespace detail {

// Pre: value != 0
template <typename Int>
constexpr auto lsb(Int value) noexcept
    -> std::enable_if_t<std::is_integral<Int>{}, int>
{
    auto x = static_cast<std::make_unsigned_t<Int>>(value);
    int lsb = sizeof(x) * 8;
    for (; x != 0; x <<= 1u)
        --lsb;
    return lsb;
}

static_assert(lsb(0x00000001) == 0, "Only lowest bit set");
static_assert(lsb(0xFFFFFFFF) == 0, "All bits set");
static_assert(lsb(0xFFFFFFFE) == 1, "Only lowest bit cleared");
static_assert(lsb(0b00001010) == 1, "Bit gap has not effect");


// Pre: value > 0
template <typename Int>
constexpr auto msb(Int value) noexcept
    -> std::enable_if_t<std::is_integral<Int>{}, int>
{
    auto x = static_cast<std::make_unsigned_t<Int>>(value);
    int msb = -1;
    for (; x != 0; x >>= 1u)
        ++msb;
    return msb;
}

static_assert(msb(0x00000001) == 0, "Only lowest bit set");
static_assert(msb(0xFFFFFFFF) == 31, "All bits set");
static_assert(msb(0xFFFFFFFE) == 31, "Only lowest bit cleared");
static_assert(msb(0b00001010) == 3, "Bit gap has not effect");


template <typename Int>
constexpr auto min_alignment(Int mask) noexcept
    -> std::enable_if_t<std::is_integral<Int>{}, int>
{
    return 1 << (msb((msb(mask) ^ lsb(mask)) / 8) + 1);
}

static_assert(min_alignment(0x01) == 1u, "Single byte");
static_assert(min_alignment(0x0101) == 2u, "Half-word");
static_assert(min_alignment(0x018000) == 4u, "Spanning bit 16:15 gap");


} // namespace detail
} // namespace regilite

#endif // REGILITE_UTILITY_HPP