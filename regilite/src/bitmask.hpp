// Copyright 2021 Daniel Way
// SPDX-License-Identifier: Apache-2.0

#ifndef REGILITE_BIT_MASK_HPP
#define REGILITE_BIT_MASK_HPP

#include <cstdint>
#include <type_traits>

#include "traits.hpp"

namespace regilite {

using mask_t = std::uintptr_t;


template <int msb, int lsb = msb>
struct Mask : std::integral_constant<mask_t, (~1ul << msb) ^ (~0ul << lsb)> {
    static_assert(msb >= lsb, "Most significant bit may not be less than the "
                              "least significant");
    static_assert(lsb >= 0 and msb >= 0, "Bit positions may not be negative");
};


namespace detail {

constexpr auto masks_overlap(mask_t) noexcept { return false; }

constexpr auto masks_overlap(mask_t a, mask_t b) noexcept
{
    return mask_t{0u} != (a & b);
}

template <typename... M>
constexpr auto masks_overlap(mask_t a, mask_t b, M... c) noexcept
    -> std::enable_if_t<
        traits::conjunction(std::is_convertible<M, mask_t>{}...), bool>
{
    return masks_overlap(a, b)
           or masks_overlap(a | b, static_cast<mask_t>(c)...);
}

// Test masks_overlap
static_assert(!masks_overlap(0x1234), "Single mask does not overlap");
static_assert(!masks_overlap(0x0F, 0xF0), "These masks do not overlap");
static_assert(masks_overlap(0x0F, 0xF8), "These masks do overlap");
static_assert(masks_overlap(0x0F, 0xF0, 0x01), "Final mask overlaps");


constexpr auto fold_masks(mask_t m) noexcept { return m; }

template <typename... Ints>
constexpr auto fold_masks(mask_t m, Ints... ms) noexcept
{
    return static_cast<mask_t>(m | fold_masks(ms...));
}


// Test fold_masks
static_assert(fold_masks(0x0u) == 0x0u,
              "Single fold_masks argument is identity");
static_assert(fold_masks(0x0u, 0x1) == 0x1, "Can fold two fields");
static_assert(fold_masks(0x1, 0x0u, 0x1) == 0x1,
              "Folding multiple fields with same value is idempotent");

} // namespace detail
} // namespace regilite

#endif // REGILITE_BIT_MASK_HPP