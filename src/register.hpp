#ifndef REGISTER_HPP
#define REGISTER_HPP

#include <cstdint>
#include <type_traits>

#include "field.hpp"

namespace regilite {


class Register
{
    std::uint32_t raw_;

  public:
    template <std::uint32_t mask, std::uint32_t... masks>
    auto write(Field<mask> f, Field<masks>... fs) noexcept -> void
    {
        const auto fields = fold_fields(f, fs...);
        raw_ = (raw_ & ~fields.msk()) | fields.value();
    }
};

} // namespace regilite


#endif // REGISTER_HPP