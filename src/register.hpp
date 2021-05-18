#ifndef REGISTER_HPP
#define REGISTER_HPP

#include <cstdint>
#include <type_traits>

#include "field.hpp"

namespace regilite {

template <typename UInt>
class Register;

template <typename UInt>
class Register
{
    static_assert(std::is_unsigned<UInt>::value
                      and not std::is_same<UInt, bool>::value,
                  "Register<> type requires an unsigned integral as its "
                  "underlying representation.");

    UInt raw_;

  public:
    template <UInt mask, UInt... masks>
    auto write(Field<mask> f, Field<masks>... fs) noexcept -> void
    {
        const auto fields = fold_fields(f, fs...);
        raw_ = (raw_ & ~fields.msk()) | fields.value();
    }
};

} // namespace regilite


#endif // REGISTER_HPP