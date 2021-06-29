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


template <typename Elem, typename... Pack>
struct is_pack_element;

template <typename Elem>
struct is_pack_element<Elem> : std::false_type {};

template <typename Elem, typename... Pack>
struct is_pack_element<Elem, Elem, Pack...> : std::true_type {};

template <typename Elem, typename NotElem, typename... Pack>
struct is_pack_element<Elem, NotElem, Pack...> : is_pack_element<Elem, Pack...> {};


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