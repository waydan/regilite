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

} // namespace traits
} // namespace regilite

#endif // REGILITE_TRAITS_HPP