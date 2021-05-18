#include "utility.hpp"

namespace regilite {

namespace detail {
struct NoShift_t {};
} // namespace detail


template <std::uint32_t mask>
class Field
{
    std::uint32_t value_;

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
    constexpr auto operator|(Field<o_mask> other_f) const noexcept
    {
        return Field<mask | o_mask>{value() | other_f.value(),
                                    detail::NoShift_t{}};
    }
};


#ifndef __cpp_fold_expressions

template <std::uint32_t mask>
constexpr auto fold_fields(Field<mask> f)
{
    return f;
}

#endif

template <std::uint32_t mask, std::uint32_t... masks>
constexpr auto fold_fields(Field<mask> f, Field<masks>... fs)
{
#ifndef __cpp_fold_expressions
    return f | fold_fields(fs...);
#else
    return (f | ... | fs);
#endif
}

} // namespace regilite