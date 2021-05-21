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

    UInt state_;

    class Snapshot
    {
        UInt state_;

      public:
        constexpr auto raw() const -> UInt { return state_; }
    };

  public:
    template <UInt mask, UInt... masks>
    auto write(Field<UInt, mask> f, Field<UInt, masks>... fs) noexcept -> void
    {
        const auto fields = fold_fields(f, fs...);
        state_ = (state_ & ~fields.msk()) | fields.value();
    }


    template <typename F>
    auto read() const noexcept
        -> std::enable_if_t<std::is_same<F, Field<UInt, F::msk()>>::value,
                            Field<UInt, F::msk()>>
    {
        return Field<UInt, F::msk()>{state_ & F::msk(), detail::NoShift_t{}};
    }


    auto read() const noexcept -> Snapshot { return Snapshot{}; }


    template <UInt mask>
    auto match(Field<UInt, mask> f) const noexcept -> bool
    {
        return read<decltype(f)>() == f;
    }


    template <UInt mask, UInt... masks>
    auto match_all(Field<UInt, mask> f, Field<UInt, masks>... fs) const noexcept
        -> bool
    {
        const auto fields = fold_fields(f, fs...);
        return match(fields);
    }

#ifndef __cpp_fold_expressions
    template <UInt mask>
    auto match_any(Field<UInt, mask> f) const noexcept -> bool
    {
        return match(f);
    }
#endif

    template <UInt mask, UInt... masks>
    auto match_any(Field<UInt, mask> f, Field<UInt, masks>... fs) const noexcept
        -> bool
    {

#ifndef __cpp_fold_expressions
        return match_any(f) or match_any(fs...);
#else
        return (match(f) or ... or match(fs));
#endif
    }
};

} // namespace regilite


#endif // REGILITE_REGISTER_HPP