// Copyright 2021 Daniel Way
// SPDX-License-Identifier: Apache-2.0

#ifndef REGILITE_FIELD_TRAITS_HPP
#define REGILITE_FIELD_TRAITS_HPP

#include <type_traits>

#include "basic_field.hpp"
#include "bitmask.hpp"

namespace regilite {

namespace detail {

enum class BitState
{
    Zero,
    One,
    Reset,
    Volatile
};

template <typename Field, bool predicate>
using mask_if = std::integral_constant<mask_t, predicate ? Field::mask() : 0u>;


template <typename... Fields>
struct FieldGroup {
    using Reserved = BasicField<~fold_masks(Fields::mask()...)>;

    using SafeWriteZero = BasicField<fold_masks(
        mask_if<Fields, Fields::access::safe_write == BitState::Zero>{}...)>;
    using SafeWriteReset = BasicField<fold_masks(
        Reserved::mask(),
        mask_if<Fields, Fields::access::safe_write == BitState::Reset>{}...)>;
    using SafeWriteVolatile = BasicField<fold_masks(
        Reserved::mask(), mask_if<Fields, Fields::access::safe_write
                                              == BitState::Volatile>{}...)>;
    using AlwaysReadsZero = BasicField<fold_masks(
        mask_if<Fields, Fields::access::always_reads == BitState::Zero>{}...)>;
    using AlwaysReadsReset = BasicField<fold_masks(
        Reserved::mask(),
        mask_if<Fields, Fields::access::always_reads == BitState::Reset>{}...)>;
};
} // namespace detail

template <detail::BitState read, detail::BitState write>
struct AccessType {
    static constexpr auto always_reads = read;
    static constexpr auto safe_write = write;
};

using WriteOnly = AccessType<detail::BitState::Reset, detail::BitState::Zero>;
using WO = WriteOnly;

using ReadOnly =
    AccessType<detail::BitState::Volatile, detail::BitState::Volatile>;
using RO = ReadOnly;

using WriteOneToClear =
    AccessType<detail::BitState::Volatile, detail::BitState::Zero>;
using W1C = WriteOneToClear;

using ReadWrite =
    AccessType<detail::BitState::Volatile, detail::BitState::Volatile>;
using RW = ReadWrite;

} // namespace regilite
#endif // REGILITE_FIELD_TRAITS_HPP