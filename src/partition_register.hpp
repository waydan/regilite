#ifndef REGILITE_PARTITION_REGISTER_HPP
#define REGILITE_PARTITION_REGISTER_HPP

#include "basic_field.hpp"
#include "partition_type.hpp"
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

    constexpr auto address() const noexcept { return addr_; }
};


template <typename UInt, UInt reset, typename... MemberFields>
class PartitionRegister
    : public RegisterProxy<PartitionRegister<UInt, reset, MemberFields...>,
                           MemberFields...>
{
    friend RegisterProxy<PartitionRegister, MemberFields...>;

  public:
    using storage_type =
        typename detail::register_traits<PartitionRegister>::storage_type;

  private:
    storage_type state_;

  protected:
    template <typename Field>
    auto write_field(Field f)
    {
        using WriteBlock = detail::Partition<f.mask()>;
        using WriteBlock_t = typename WriteBlock::type;
        static_assert(sizeof(WriteBlock_t) <= sizeof(storage_type),
                      "Partition may not be larger than the register itself.");

        auto* state_segment_ptr =
            reinterpret_cast<WriteBlock_t*>(&state_) + WriteBlock::offset();
        const WriteBlock_t modified_state =
            (volatile_read(state_segment_ptr)
             & ~static_cast<WriteBlock_t>(
                 f.mask() >> (WriteBlock::offset() * WriteBlock::size())))
            | static_cast<WriteBlock_t>(f.value() >> WriteBlock::offset()
                                                         * WriteBlock::size());
        return volatile_write(state_segment_ptr, modified_state);
    }

    auto volatile_write(storage_type s) noexcept -> void
    {
        *static_cast<volatile storage_type*>(&state_) = s;
    }

    template <typename T>
    auto volatile_write(T* address, T state) noexcept
        -> std::enable_if_t<traits::is_storage_type<T>{}, Write<T>>
    {
        *static_cast<volatile T*>(address) = state;
        return Write<T>{address};
    }

    auto volatile_read() const noexcept -> storage_type
    {
        return *static_cast<const volatile storage_type*>(&state_);
    }

    template <typename T>
    auto volatile_read(T* address)
        -> std::enable_if_t<traits::is_storage_type<T>{}, T>
    {
        return *static_cast<volatile T*>(address);
    }
};

namespace detail {
template <typename UInt, UInt reset, typename... MemberFields>
struct register_traits<PartitionRegister<UInt, reset, MemberFields...>> {
    using storage_type = UInt;
};
} // namespace detail

} // namespace regilite

#endif // REGILITE_PARTITION_REGISTER_HPP