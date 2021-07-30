#ifndef REGILITE_FIELD_ACCESS_HPP
#define REGILITE_FIELD_ACCESS_HPP

#include <type_traits>

#include "bitmask.hpp"

namespace regilite {

namespace detail {

enum class SafeWriteDefault
{
    Zero,
    One,
    Readback
};

template <typename Field>
constexpr auto safe_write(SafeWriteDefault type) noexcept -> mask_t
{
    return (Field::access_type::safe_write == type) ? Field::mask() : 0u;
}

template <SafeWriteDefault type, typename Field, typename... Fields>
struct SafeWrite
    : std::integral_constant<mask_t, SafeWrite<type, Fields...>{}
                                         | safe_write<Field>(type)> {};

template <SafeWriteDefault type, typename Field>
struct SafeWrite<type, Field>
    : std::integral_constant<mask_t, safe_write<Field>(type)> {};


} // namespace detail

struct WriteOnly {};
using WO = WriteOnly;

struct ReadOnly {};
using RO = ReadOnly;

struct WriteOneToClear {
    static constexpr auto reads_as = detail::SafeWriteDefault::Readback;
    static constexpr auto safe_write = detail::SafeWriteDefault::Zero;
};
using W1C = WriteOneToClear;

struct ReadWrite {
    static constexpr auto reads_as = detail::SafeWriteDefault::Readback;
    static constexpr auto safe_write = detail::SafeWriteDefault::Readback;
};
using RW = ReadWrite;

} // namespace regilite
#endif // REGILITE_FIELD_ACCESS_HPP