#ifndef REGILITE_BASIC_REGISTER_HPP
#define REGILITE_BASIC_REGISTER_HPP

#include "basic_field.hpp"
#include "register_proxy.hpp"
#include "traits.hpp"

namespace regilite {

template <typename UInt, UInt reset, typename... MemberFields>
class BasicRegister
    : public RegisterProxy<BasicRegister<UInt, reset, MemberFields...>,
                           MemberFields...>
{
    using Base = RegisterProxy<BasicRegister, MemberFields...>;
    friend Base;
    using typename Base::FieldSet;

  public:
    using storage_type =
        typename detail::register_traits<BasicRegister>::storage_type;

  private:
    storage_type state_;

  protected:
    template <typename Field>
    auto write_field(Field field)
    {
        // if (all other bits have safe static write value)
        //     detail::overwrite(field);
        // else if (all used bits read as zero)
        //     detail::or_with_register(field);
        // else

        const storage_type modified_state = detail::insert_bits(
            volatile_read(),
            (field
             | detail::BasicField<storage_type, FieldSet::safe_write_zero
                                                    & ~field.mask()>{0}));
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
template <typename UInt, UInt reset, typename... MemberFields>
struct register_traits<BasicRegister<UInt, reset, MemberFields...>> {
    using storage_type = UInt;
};
} // namespace detail

} // namespace regilite

#endif // REGILITE_BASIC_REGISTER_HPP