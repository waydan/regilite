#ifndef REGILITE_REGISTER_HPP
#define REGILITE_REGISTER_HPP

#include <cstdint>
#include <type_traits>

#include "field.hpp"

namespace regilite {

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
    auto read() const noexcept
        -> std::enable_if_t<std::is_same<F, Field<UInt, F::msk()>>::value,
                            Field<UInt, F::msk()>>
    {
        return Field<UInt, F::msk()>{raw_ & F::msk(), detail::NoShift_t{}};
    }
};

} // namespace regilite


#endif // REGILITE_REGISTER_HPP