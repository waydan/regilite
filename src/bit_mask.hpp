#ifndef REGILITE_BIT_MASK_HPP
#define REGILITE_BIT_MASK_HPP

namespace regilite {

using mask_t = std::uint64_t;


namespace detail {

template <bool test, mask_t accum, mask_t... masks>
struct masks_overlap_impl;

template <mask_t accum>
struct masks_overlap_impl<false, accum> : std::false_type {};

template <mask_t accum, mask_t... masks>
struct masks_overlap_impl<true, accum, masks...> : std::true_type {};

template <mask_t accum, mask_t mask, mask_t... masks>
struct masks_overlap_impl<false, accum, mask, masks...>
    : masks_overlap_impl<(accum | mask) != (accum ^ mask), accum | mask,
                         masks...> {};

template <mask_t mask, mask_t... masks>
using masks_overlap = masks_overlap_impl<false, mask, masks...>;


// Test masks_overlap
static_assert(!masks_overlap<0x1234>{}, "Single mask does not overlap");
static_assert(!masks_overlap<0x0F, 0xF0>{}, "These masks do not overlap");
static_assert(masks_overlap<0x0F, 0xF8>{}, "These masks do overlap");
static_assert(masks_overlap<0x0F, 0xF0, 0x01>{}, "Final mask overlaps");


template <typename Int>
constexpr auto fold_masks(Int m) noexcept
    -> std::enable_if_t<std::is_integral<Int>{}, mask_t>
{
    return static_cast<mask_t>(m);
}

template <typename Int, typename... Ints>
constexpr auto fold_masks(Int m, Ints... ms) noexcept -> decltype(fold_masks(m))
{
    return fold_masks(m) | fold_masks(ms...);
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