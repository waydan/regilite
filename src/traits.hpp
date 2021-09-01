// Copyright 2021 Daniel Way
// SPDX-License-Identifier: Apache-2.0

#ifndef REGILITE_TRAITS_HPP
#define REGILITE_TRAITS_HPP

#include <type_traits>

namespace regilite {
namespace traits {

template <typename T>
using remove_cvref_t = std::remove_cv_t<std::remove_reference_t<T>>;

template <typename T, typename U>
using match_unqualified = std::is_same<remove_cvref_t<T>, remove_cvref_t<U>>;

static_assert(match_unqualified<int volatile&&, int const&>{},
              "Only checks unqualified type");


template <typename T, typename = void>
struct is_storage_type : std::integral_constant<bool, false> {};
template <typename T>
struct is_storage_type<
    T, std::enable_if_t<std::is_unsigned<T>{} and not std::is_same<T, bool>{}>>
    : std::integral_constant<bool, true> {};

static_assert(not is_storage_type<float>{},
              "Floating-point types may not be used for register storage.");
static_assert(is_storage_type<unsigned char>{},
              "Unsigned integral types may be used for register storage.");
static_assert(not is_storage_type<bool>{},
              "Boolean types may not be used for register storage.");
static_assert(not is_storage_type<signed int>{},
              "Storage types must be unsigned.");


template <typename Elem, typename... Pack>
struct is_pack_element;

template <typename Elem>
struct is_pack_element<Elem> : std::false_type {};

template <typename Elem, typename... Pack>
struct is_pack_element<Elem, Elem, Pack...> : std::true_type {};

template <typename Elem, typename NotElem, typename... Pack>
struct is_pack_element<Elem, NotElem, Pack...>
    : is_pack_element<Elem, Pack...> {};


constexpr auto conjunction(bool pred) noexcept -> bool { return pred; }

template <typename... Bs>
constexpr auto conjunction(bool pred, Bs... preds) noexcept -> bool
{
    return pred and conjunction(static_cast<bool>(preds)...);
}


} // namespace traits
} // namespace regilite

#endif // REGILITE_TRAITS_HPP