#ifndef REGILITE_FIELD_HPP
#define REGILITE_FIELD_HPP

#include "utility.hpp"

namespace regilite {

namespace detail {
struct NoShift_t {};
} // namespace detail


template <typename UInt, UInt mask>
class Field
{
    static_assert(std::is_unsigned<UInt>::value
                      and not std::is_same<UInt, bool>::value,
                  "Register<> type requires an unsigned integral as its "
                  "underlying representation.");

    UInt value_;

  public:
    constexpr explicit Field(std::uint32_t value) noexcept
        : Field(value << detail::lsb(mask), detail::NoShift_t{})
    {}

    constexpr explicit Field(std::uint32_t value, detail::NoShift_t) noexcept
        : value_(value)
    {}

    constexpr auto value() const noexcept { return value_; };
    static constexpr auto msk() noexcept -> std::uint32_t { return mask; }

    template <std::uint32_t o_mask>
    constexpr auto operator|(Field<UInt, o_mask> other_f) const noexcept
        -> std::enable_if_t<!detail::masks_overlap(mask, o_mask),
                            Field<UInt, mask | o_mask>>
    {
        return Field<UInt, mask | o_mask>{value() | other_f.value(),
                                          detail::NoShift_t{}};
    }
};

template <typename UInt, UInt mask>
constexpr auto operator==(const Field<UInt, mask>& lhs,
                          const Field<UInt, mask>& rhs)
{
    return lhs.value() == rhs.value();
}

template <typename UInt, UInt mask>
constexpr auto operator!=(const Field<UInt, mask>& lhs,
                          const Field<UInt, mask>& rhs)
{
    return not (lhs == rhs);
}

#ifndef __cpp_fold_expressions

template <typename UInt, std::uint32_t mask>
constexpr auto fold_fields(Field<UInt, mask> f)
{
    return f;
}

#endif

template <typename UInt, std::uint32_t mask, std::uint32_t... masks>
constexpr auto fold_fields(Field<UInt, mask> f, Field<UInt, masks>... fs)
{
#ifndef __cpp_fold_expressions
    return f | fold_fields(fs...);
#else
    return (f | ... | fs);
#endif
}

} // namespace regilite

#endif // REGILITE_FIELD_HPP
