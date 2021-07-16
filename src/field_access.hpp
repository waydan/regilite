#ifndef REGILITE_FIELD_ACCESS_HPP
#define REGILITE_FIELD_ACCESS_HPP

namespace regilite {

namespace detail {

enum class SafeWriteDefault
{
    Zero,
    One,
    Readback
};

}

struct WriteOnly {
    static constexpr auto safe_value = detail::SafeWriteDefault::Zero;
};
using WO = WriteOnly;

struct ReadOnly {
    static constexpr auto safe_value = detail::SafeWriteDefault::Readback;
};
using RO = ReadOnly;

struct WriteOneToClear {
    static constexpr auto safe_value = detail::SafeWriteDefault::One;
};
using W1C = WriteOneToClear;

struct ReadWrite {
    static constexpr auto safe_value = detail::SafeWriteDefault::Readback;
};
using RW = ReadWrite;

} // namespace regilite
#endif // REGILITE_FIELD_ACCESS_HPP