#ifndef REGILITE_FIELD_TRAITS_HPP
#define REGILITE_FIELD_TRAITS_HPP

#include <type_traits>

#include "basic_field.hpp"
#include "bitmask.hpp"

namespace regilite {

namespace detail {

enum class SafeWriteDefault
{
    Zero,
    One,
    Reset,
    Volatile
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


template <typename... Fields>
struct FieldGroup {
    using Reserved = detail::BasicField<~detail::fold_masks(Fields::mask()...)>;

    static constexpr mask_t safe_write_zero =
        detail::SafeWrite<detail::SafeWriteDefault::Zero, Fields...>{};
    static constexpr mask_t safe_write_one =
        detail::SafeWrite<detail::SafeWriteDefault::One, Fields...>{};
    static constexpr mask_t safe_write_reset =
        detail::SafeWrite<detail::SafeWriteDefault::Reset, Fields...>{}
        | Reserved::mask();
};
} // namespace detail

struct WriteOnly {
    static constexpr auto reads_as = detail::SafeWriteDefault::Reset;
    static constexpr auto safe_write = detail::SafeWriteDefault::Zero;
};
using WO = WriteOnly;

struct ReadOnly {
    static constexpr auto reads_as = detail::SafeWriteDefault::Volatile;
    static constexpr auto safe_write = detail::SafeWriteDefault::Volatile;
};
using RO = ReadOnly;

struct WriteOneToClear {
    static constexpr auto reads_as = detail::SafeWriteDefault::Volatile;
    static constexpr auto safe_write = detail::SafeWriteDefault::Zero;
};
using W1C = WriteOneToClear;

struct ReadWrite {
    static constexpr auto reads_as = detail::SafeWriteDefault::Volatile;
    static constexpr auto safe_write = detail::SafeWriteDefault::Volatile;
};
using RW = ReadWrite;

} // namespace regilite
#endif // REGILITE_FIELD_TRAITS_HPP