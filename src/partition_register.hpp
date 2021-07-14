#ifndef REGILITE_PARTITION_REGISTER_HPP
#define REGILITE_PARTITION_REGISTER_HPP

#include "basicfield.hpp"
#include "register_proxy.hpp"
#include "traits.hpp"
#include "utility.hpp"


namespace regilite {

template <typename UInt>
class Write
{
    static_assert(traits::is_storage_type<UInt>{},
                  "Write<> type requires an unsigned integral as its "
                  "underlying representation.");

    std::uintptr_t addr_;

  public:
    explicit Write(const UInt* ptr)
        : addr_(reinterpret_cast<std::uintptr_t>(ptr))
    {}

    constexpr auto address() -> std::uintptr_t { return addr_; }
};

template <int max_partition>
struct Block;

template <>
struct Block<1> {
    using type = std::uint8_t;
};
template <>
struct Block<2> {
    using type = std::uint16_t;
};

template <int msb, int lsb = 0>
using Block_t = typename Block<(1 << (detail::msb((msb ^ lsb) / 8) + 1))>::type;


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
        using WriteBlock =
            Block_t<detail::msb(f.mask()), detail::lsb(f.mask())>;
        constexpr int offset = detail::lsb(f.mask()) / (sizeof(WriteBlock) * 8);
        constexpr int offset_bits = offset * sizeof(WriteBlock) * 8;
        auto* state_segment_ptr =
            reinterpret_cast<WriteBlock*>(&state_) + offset;
        const WriteBlock modified_state =
            (volatile_read(state_segment_ptr)
             & ~static_cast<WriteBlock>(f.mask() >> offset_bits))
            | static_cast<WriteBlock>(f.value() >> offset_bits);
        return volatile_write(state_segment_ptr, modified_state);
    }

    auto volatile_write(storage_type s) noexcept -> void
    {
        *const_cast<volatile storage_type*>(&state_) = s;
    }

    template <typename T>
    auto volatile_write(T* address, T state) noexcept
        -> std::enable_if_t<traits::is_storage_type<T>{}, Write<T>>
    {
        *const_cast<volatile T*>(address) = state;
        return Write<T>{address};
    }

    auto volatile_read() const noexcept -> storage_type
    {
        return *const_cast<const volatile storage_type*>(&state_);
    }

    template <typename T>
    auto volatile_read(T* address)
        -> std::enable_if_t<traits::is_storage_type<T>{}, T>
    {
        return *const_cast<volatile T*>(address);
    }
};

} // namespace detail

template <typename UInt, typename AccessType, typename... MemberFields>
using PartitionRegister = RegisterProxy<
    detail::PartitionRegisterImpl<UInt, AccessType, MemberFields...>,
    MemberFields...>;

} // namespace regilite

#endif // REGILITE_PARTITION_REGISTER_HPP