#ifndef REGILITE_PARTITION_REGISTER_HPP
#define REGILITE_PARTITION_REGISTER_HPP

#include "register_proxy.hpp"

namespace regilite {

template <typename UInt>
class Write
{
    static_assert(traits::is_storage_type<UInt>{},
                  "Write<> type requires an unsigned integral as its "
                  "underlying representation.");
};

template <int max_partition>
struct Block;

template <>
struct Block<0> {
    using type = std::uint8_t;
};
template <>
struct Block<1> {
    using type = std::uint16_t;
};

template <int msb>
using Block_t = std::enable_if_t<(msb >= 0), typename Block<msb / 8>::type>;


namespace detail {

template <typename UInt, typename AccessType, typename... MemberFields>
class PartitionRegisterImpl
{
    static_assert(
        traits::is_storage_type<UInt>{},
        "PartitionRegister<> type requires an unsigned integral as its "
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
        return Write<Block_t<detail::msb(f.mask())>>{};
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

template <typename UInt, typename AccessType, typename... MemberFields>
using PartitionRegister = RegisterProxy<
    detail::PartitionRegisterImpl<UInt, AccessType, MemberFields...>,
    MemberFields...>;

} // namespace regilite

#endif // REGILITE_PARTITION_REGISTER_HPP