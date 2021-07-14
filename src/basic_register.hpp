#ifndef REGILITE_BASIC_REGISTER_HPP
#define REGILITE_BASIC_REGISTER_HPP

#include "register_proxy.hpp"

namespace regilite {

namespace detail {
template <typename UInt>
class BasicRegisterImpl
{
    static_assert(traits::is_storage_type<UInt>{},
                  "BasicRegister<> type requires an unsigned integral as its "
                  "underlying representation.");

  public:
    using storage_type = UInt;

  private:
    storage_type state_;

  protected:
    template <typename Field>
    auto write_field(Field f)
    {
        const storage_type modified_state =
            detail::insert_bits(volatile_read(), f);
        volatile_write(modified_state);
    }

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
    RegisterProxy<detail::BasicRegisterImpl<UInt>, MemberFields...>;

} // namespace regilite

#endif // REGILITE_BASIC_REGISTER_HPP