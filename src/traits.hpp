#ifndef REGILITE_TRAITS_HPP
#define REGILITE_TRAITS_HPP

namespace regilite::traits {
template <typename T>
struct identity {
    using type = T;
};

template <typename T>
using identity_t = typename identity<T>::type;

} // namespace regilite::traits

#endif // REGILITE_TRAITS_HPP