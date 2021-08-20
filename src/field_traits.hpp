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
    : std::integral_constant<mask_t,
                             detail::fold_masks(safe_write<Field>(type),
                                                safe_write<Fields>(type)...)> {
};


template <typename Field>
constexpr auto always_reads(SafeWriteDefault type) noexcept -> mask_t
{
    return (Field::access_type::always_reads == type) ? Field::mask() : 0u;
}

template <SafeWriteDefault type, typename Field, typename... Fields>
struct ReadsAs
    : std::integral_constant<mask_t, detail::fold_masks(
                                         always_reads<Field>(type),
                                         always_reads<Fields>(type)...)> {};


template <typename... Fields>
struct FieldGroup {
    using Reserved = BasicField<~fold_masks(Fields::mask()...)>;

    using SafeWriteZero =
        BasicField<SafeWrite<SafeWriteDefault::Zero, Fields...>{}>;
    using SafeWriteOne =
        BasicField<SafeWrite<SafeWriteDefault::One, Fields...>{}>;
    using SafeWriteReset =
        BasicField<SafeWrite<SafeWriteDefault::Reset, Fields...>{}
                   | Reserved::mask()>;
    using SafeWriteVolatile =
        BasicField<SafeWrite<SafeWriteDefault::Volatile, Fields...>{}
                   | Reserved::mask()>;
    using AlwaysReadsZero =
        BasicField<ReadsAs<SafeWriteDefault::Zero, Fields...>{}>;
    // using AlwaysReadsOne =
    //     BasicField<ReadsAs<SafeWriteDefault::One, Fields...>{}>;
    using AlwaysReadsReset =
        BasicField<ReadsAs<SafeWriteDefault::Reset, Fields...>{}
                   | Reserved::mask()>;
    // using AlwaysReadsVolatile =
    //     BasicField<ReadsAs<SafeWriteDefault::Volatile, Fields...>{}>;
};
} // namespace detail

struct WriteOnly {
    static constexpr auto always_reads = detail::SafeWriteDefault::Reset;
    static constexpr auto safe_write = detail::SafeWriteDefault::Zero;
};
using WO = WriteOnly;

struct ReadOnly {
    static constexpr auto always_reads = detail::SafeWriteDefault::Volatile;
    static constexpr auto safe_write = detail::SafeWriteDefault::Volatile;
};
using RO = ReadOnly;

struct WriteOneToClear {
    static constexpr auto always_reads = detail::SafeWriteDefault::Volatile;
    static constexpr auto safe_write = detail::SafeWriteDefault::Zero;
};
using W1C = WriteOneToClear;

struct ReadWrite {
    static constexpr auto always_reads = detail::SafeWriteDefault::Volatile;
    static constexpr auto safe_write = detail::SafeWriteDefault::Volatile;
};
using RW = ReadWrite;

} // namespace regilite
#endif // REGILITE_FIELD_TRAITS_HPP