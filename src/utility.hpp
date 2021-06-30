#ifndef REGILITE_UTILITY_HPP
#define REGILITE_UTILITY_HPP

#include <type_traits>

#include "traits.hpp"

namespace regilite {
namespace detail {

// Pre: value > 0
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

static_assert(lsb(0x00000001) == 0, "Only lowest bit set");
static_assert(lsb(0xFFFFFFFF) == 0, "All bits set");
static_assert(lsb(0xFFFFFFFE) == 1, "Only lowest bit cleared");
static_assert(lsb(0b00001010) == 1, "Bit gap has not effect");


// Pre: value > 0
template <typename Int>
constexpr auto msb(Int value) noexcept
    -> std::enable_if_t<std::is_integral<Int>::value, int>
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


template <typename UInt, bool test, UInt accum, UInt... masks>
struct masks_overlap_impl;

template <typename UInt, UInt accum>
struct masks_overlap_impl<UInt, false, accum> : std::false_type {};

template <typename UInt, UInt accum, UInt... masks>
struct masks_overlap_impl<UInt, true, accum, masks...> : std::true_type {};

template <typename UInt, UInt accum, UInt mask, UInt... masks>
struct masks_overlap_impl<UInt, false, accum, mask, masks...>
    : masks_overlap_impl<UInt, (accum | mask) != (accum ^ mask), accum | mask,
                         masks...> {};

template <typename UInt, UInt mask, UInt... masks>
using masks_overlap = masks_overlap_impl<UInt, false, mask, masks...>;


static_assert(!masks_overlap<std::uint32_t, 0x1234>{},
              "Single mask does not overlap");
static_assert(!masks_overlap<std::uint32_t, 0x0F, 0xF0>{},
              "These masks do not overlap");
static_assert(masks_overlap<std::uint32_t, 0x0F, 0xF8>{},
              "These masks do overlap");
static_assert(masks_overlap<std::uint32_t, 0x0F, 0xF0, 0x01>{},
              "Final mask overlaps");

template <typename Int>
constexpr auto fold_masks(Int m) noexcept
    -> std::enable_if_t<std::is_integral<Int>{}, std::make_unsigned_t<Int>>
{
    return static_cast<std::make_unsigned_t<Int>>(m);
}

template <typename Int, typename... Ints>
constexpr auto fold_masks(Int m, Ints... ms) noexcept -> std::enable_if_t<
    traits::conjunction<std::is_integral<Int>{}, std::is_integral<Ints>{}...>{},
    std::make_unsigned_t<Int>>
{
    return fold_masks(m) | fold_masks(ms...);
}

static_assert(fold_masks(0x0u) == 0x0u,
              "Single fold_masks argument is identity");
static_assert(fold_masks(0x0u, 0x1) == 0x1, "Can fold two fields");
static_assert(fold_masks(0x1, 0x0u, 0x1) == 0x1,
              "Folding multiple fields with same value is idempotent");


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