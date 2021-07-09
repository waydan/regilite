#ifndef REGILITE_BASIC_REGISTER_HPP
#define REGILITE_BASIC_REGISTER_HPP

#include "register.hpp"

namespace regilite {

namespace detail {
template <typename UInt>
class BasicRegisterImpl
{
    static_assert(std::is_unsigned<UInt>{} and not std::is_same<UInt, bool>{},
                  "BasicRegister<> type requires an unsigned integral as its "
                  "underlying representation.");

  public:
    using storage_type = UInt;

  private:
    storage_type state_;

  protected:
    auto volatile_write(storage_type s) noexcept -> void
    {
        *const_cast<volatile storage_type*>(&state_) = s;
    }

    auto volatile_read() const noexcept -> storage_type
    {
        return *const_cast<const volatile storage_type*>(&state_);
    }
};
} // namespace detail

template <typename UInt, typename... MemberFields>
using BasicRegister =
    Register<detail::BasicRegisterImpl<UInt>, MemberFields...>;

} // namespace regilite

#endif // REGILITE_BASIC_REGISTER_HPP