#ifndef REGISTER_HPP
#define REGISTER_HPP

#include <cstdint>
#include <type_traits>

namespace regilite {

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

struct NoShift_t {};

template <std::uint32_t mask>
class Field
{
    std::uint32_t value_;

  public:
    constexpr explicit Field(std::uint32_t value) noexcept
        : Field(value << lsb(mask), NoShift_t{})
    {}

    constexpr explicit Field(std::uint32_t value, NoShift_t) noexcept
        : value_(value)
    {}

    constexpr auto value() const noexcept { return value_; };
    static constexpr auto msk() noexcept -> std::uint32_t { return mask; }

    template <std::uint32_t o_mask>
    constexpr auto operator|(Field<o_mask> other_f) const noexcept
    {
        return Field<mask | o_mask>{value() | other_f.value(), NoShift_t{}};
    }
};

template <std::uint32_t mask>
constexpr auto fold(Field<mask> f)
{
    return f;
}

template <std::uint32_t mask, std::uint32_t... masks>
constexpr auto fold(Field<mask> f, Field<masks>... fs)
{
    return f | fold(fs...);
}

class Register
{
    std::uint32_t raw_;

  public:
    template <std::uint32_t mask, std::uint32_t... masks>
    auto write(Field<mask> f, Field<masks>... fs) noexcept -> void
    {
        const auto fields = fold(f, fs...);
        raw_ = (raw_ & ~fields.msk()) | fields.value();
    }
};

} // namespace regilite


#endif // REGISTER_HPP