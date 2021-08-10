#ifndef REGILITE_BASIC_FIELD_HPP
#define REGILITE_BASIC_FIELD_HPP

#include <cassert>
#include <type_traits>


#include "bitmask.hpp"
#include "partition_type.hpp"

namespace regilite {
namespace detail {

template <mask_t bit_mask>
class BasicField
{
  public:
    using value_type = typename Bytes<min_bytes(bit_mask)>::type;

  private:
    value_type value_;

  public:
    explicit constexpr BasicField(value_type val) noexcept : value_(val) {}

    static constexpr auto mask() -> mask_t { return bit_mask; }
    static constexpr auto offset() -> mask_t { return 0u; }

    constexpr auto value() const noexcept { return value_; }

    template <mask_t rhs_mask>
    friend constexpr auto operator+(BasicField lhs,
                                    BasicField<rhs_mask> rhs) noexcept
        -> std::enable_if_t<!masks_overlap(mask(), rhs_mask),
                            BasicField<mask() | rhs_mask>>
    {
        using ResultField = BasicField<mask() | rhs_mask>;
        return ResultField{static_cast<typename ResultField::value_type>(
            lhs.value() | rhs.value())};
    }

    template <mask_t rhs_mask>
    friend constexpr auto operator-(BasicField lhs,
                                    BasicField<rhs_mask>) noexcept
    {
        using ResultField = BasicField<mask() & ~rhs_mask>;
        return ResultField{static_cast<typename ResultField::value_type>(
            lhs.value() & ~rhs_mask)};
    }
};

template <typename Field>
constexpr auto to_basicfield(Field f) noexcept
    -> std::enable_if_t<sizeof(typename Field::value_type) <= sizeof(mask_t),
                        detail::BasicField<Field::mask()>>
{
    using ResultField = BasicField<f.mask()>;
    return ResultField{static_cast<typename ResultField::value_type>(
        static_cast<typename ResultField::value_type>(f.value())
        << f.offset())};
}

// This cannot be a function: it must be evaluated without instantiated objects
template <typename F, typename... Fs>
using fields_overlap =
    std::integral_constant<bool, masks_overlap(F::mask(), Fs::mask()...)>;


template <typename Field>
constexpr auto fold_fields(Field f) noexcept -> decltype(to_basicfield(f))
{
    return to_basicfield(f);
}

template <typename Field, typename... Fields>
constexpr auto fold_fields(Field f, Fields... fs) noexcept -> std::enable_if_t<
    not fields_overlap<Field, Fields...>{},
    BasicField<fold_masks(Field::mask(), Fields::mask()...)>>
{
    return to_basicfield(f) + fold_fields(fs...);
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
constexpr auto insert_bits(UInt value, BasicField<mask> field) noexcept
    -> std::enable_if_t<sizeof(UInt) <= sizeof(mask_t), UInt>
{
    return (value & ~static_cast<UInt>(mask))
           | static_cast<UInt>(field.value() << field.offset());
}


} // namespace detail
} // namespace regilite
#endif // REGILITE_BASIC_FIELD_HPP