#ifndef REGILITE_PARTITION_REGISTER_HPP
#define REGILITE_PARTITION_REGISTER_HPP

#include "register_proxy.hpp"

namespace regilite {
namespace detail {

template <typename UInt, typename AccessType, typename... MemberFields>
class PartitionRegisterImpl
{
    static_assert(std::is_unsigned<UInt>{} and not std::is_same<UInt, bool>{},
                  "BasicRegister<> type requires an unsigned integral as its "
                  "underlying representation.");

  protected:
    using storage_type = UInt;

  private:
    storage_type state_;
};
} // namespace detail

template <typename UInt, typename AccessType, typename... MemberFields>
using PartitionRegister = RegisterProxy<
    detail::PartitionRegisterImpl<UInt, AccessType, MemberFields...>,
    MemberFields...>;

} // namespace regilite

#endif // REGILITE_PARTITION_REGISTER_HPP