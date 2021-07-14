#ifndef REGILITE_TRAITS_HPP
#define REGILITE_TRAITS_HPP

#include <type_traits>

namespace regilite {
namespace traits {
template <typename T>
struct identity {
    using type = T;
};

template <typename T>
using identity_t = typename identity<T>::type;


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


template <typename T>
constexpr auto as_uint(const T& x) -> std::make_unsigned_t<T>
{
    return static_cast<std::make_unsigned_t<T>>(x);
}


template <typename Elem, typename... Pack>
struct is_pack_element;

template <typename Elem>
struct is_pack_element<Elem> : std::false_type {};

template <typename Elem, typename... Pack>
struct is_pack_element<Elem, Elem, Pack...> : std::true_type {};

template <typename Elem, typename NotElem, typename... Pack>
struct is_pack_element<Elem, NotElem, Pack...>
    : is_pack_element<Elem, Pack...> {};


template <bool pred, bool... preds>
struct conjunction;

template <bool... preds>
struct conjunction<false, preds...> : std::false_type {};

template <bool... preds>
struct conjunction<true, preds...> : conjunction<preds...> {};

template <>
struct conjunction<true> : std::true_type {};


} // namespace traits
} // namespace regilite

#endif // REGILITE_TRAITS_HPP