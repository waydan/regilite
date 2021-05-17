#ifndef REGISTER_HPP
#define REGISTER_HPP

#include <cstdint>

namespace regilite {


class Field
{
    std::uint32_t value_;

  public:
    constexpr explicit Field(std::uint32_t value) noexcept : value_(value) {}

    constexpr auto value() const noexcept { return value_; };
};


class Register
{
    std::uint32_t raw_;

  public:
    auto write(Field f) noexcept -> void { raw_ = f.value(); }
};

} // namespace regilite


#endif // REGISTER_HPP