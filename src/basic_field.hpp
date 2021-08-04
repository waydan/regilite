#ifndef REGILITE_BASIC_FIELD_HPP
#define REGILITE_BASIC_FIELD_HPP

#include <cassert>
#include <type_traits>


#include "bitmask.hpp"

namespace regilite {
namespace detail {

template <typename UInt, mask_t bit_mask>
class BasicField
{
    static_assert(std::is_unsigned<UInt>{} and not std::is_same<UInt, bool>{},
                  "Register<> type requires an unsigned integral as its "
                  "underlying representation.");

  public:
    using value_type = UInt;

  private:
    UInt value_;

  public:
    explicit constexpr BasicField(value_type val) noexcept : value_(val) {}

    static constexpr auto mask() -> mask_t { return bit_mask; }
    static constexpr auto offset() -> mask_t { return 0; }

    constexpr auto value() const noexcept -> UInt { return value_; }

    template <mask_t rhs_mask>
    friend constexpr auto
    operator+(BasicField lhs, BasicField<value_type, rhs_mask> rhs) noexcept
        -> std::enable_if_t<!masks_overlap(mask(), rhs_mask),
                            BasicField<value_type, mask() | rhs_mask>>
    {
        return BasicField<value_type, mask() | rhs_mask>{
            static_cast<value_type>(lhs.value() | rhs.value())};
    }

    template <mask_t rhs_mask>
    friend constexpr auto operator-(BasicField lhs,
                                    BasicField<value_type, rhs_mask>) noexcept
    {
        return BasicField<value_type, mask() & ~rhs_mask>{
            static_cast<value_type>(lhs.value() & ~rhs_mask)};
    }
};

template <typename UInt, typename Field>
constexpr auto to_basicfield(Field f) noexcept
{
    return detail::BasicField<UInt, f.mask()>{
        static_cast<UInt>(static_cast<UInt>(f.value()) << f.offset())};
}

// This cannot be a function: it must be evaluated without instantiated objects
template <typename F, typename... Fs>
using fields_overlap =
    std::integral_constant<bool, masks_overlap(F::mask(), Fs::mask()...)>;


template <typename UInt, typename Field>
constexpr auto fold_fields(Field f) noexcept -> BasicField<UInt, Field::mask()>
{
    return to_basicfield<UInt>(f);
}

template <typename UInt, typename Field, typename... Fields>
constexpr auto fold_fields(Field f, Fields... fs) noexcept -> std::enable_if_t<
    not fields_overlap<Field, Fields...>{},
    BasicField<UInt, fold_masks(Field::mask(), Fields::mask()...)>>
{
    return fold_fields<UInt>(f) + fold_fields<UInt>(fs...);
}

template <typename FieldA, typename FieldB>
constexpr auto fold_exclusive(FieldA a, FieldB b) noexcept
{
    return a + (b - a);
}

template <typename FieldA, typename FieldB, typename... Fields>
constexpr auto fold_exclusive(FieldA a, FieldB b, Fields... fs) noexcept
{
    return fold_exclusive(fold_exclusive(a, b), fs...);
}


template <typename UInt, mask_t mask>
constexpr auto insert_bits(UInt value, BasicField<UInt, mask> field) noexcept
    -> UInt
{
    return (value & ~static_cast<UInt>(mask)) | field.value();
}


} // namespace detail
} // namespace regilite
#endif // REGILITE_BASIC_FIELD_HPP