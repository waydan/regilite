#ifndef REGILITE_TRAITS_HPP
#define REGILITE_TRAITS_HPP

namespace regilite {
namespace traits {
template <typename T>
struct identity {
    using type = T;
};

template <typename T>
using identity_t = typename identity<T>::type;

template <typename T, typename... Ts>
struct is_one_of;

template <typename T>
struct is_one_of<T> {
    static constexpr bool value = false;
};

template <typename T, typename... Ts>
struct is_one_of<T, T, Ts...> {
    static constexpr bool value = true;
    using type = T;
};

template <typename T, typename NotT, typename... Ts>
struct is_one_of<T, NotT, Ts...> : is_one_of<T, Ts...> {};

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