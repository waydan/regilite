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
    auto write(Field<UInt, mask> f, Field<UInt, masks>... fs) noexcept -> void
    {
        const auto fields = fold_fields(f, fs...);
        raw_ = (raw_ & ~fields.msk()) | fields.value();
    }

    template <typename F>
    auto read() const noexcept -> F
    {
        return F{raw_ & F::msk(), detail::NoShift_t{}};
    }
};

} // namespace regilite


#endif // REGISTER_HPP