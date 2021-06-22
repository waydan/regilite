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

static_assert(lsb(0x00000001) == 0, "Only lowest bit set");
static_assert(lsb(0xFFFFFFFF) == 0, "All bits set");
static_assert(lsb(0xFFFFFFFE) == 1, "Only lowest bit cleared");


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


} // namespace detail
} // namespace regilite

#endif // REGILITE_UTILITY_HPP