#ifndef REGILITE_BASIC_REGISTER_HPP
#define REGILITE_BASIC_REGISTER_HPP

#include "basicfield.hpp"
#include "register_proxy.hpp"
#include "traits.hpp"

namespace regilite {

template <typename UInt, typename... MemberFields>
class BasicRegister : public RegisterProxy<BasicRegister<UInt, MemberFields...>,
                                           MemberFields...>
{
    friend RegisterProxy<BasicRegister, MemberFields...>;

  public:
    using storage_type =
        typename detail::register_traits<BasicRegister>::storage_type;

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

namespace detail {
template <typename UInt, typename... MemberFields>
struct register_traits<BasicRegister<UInt, MemberFields...>> {
    using storage_type = UInt;
};
} // namespace detail

} // namespace regilite

#endif // REGILITE_BASIC_REGISTER_HPP