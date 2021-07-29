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

struct WriteOnly {};
using WO = WriteOnly;

struct ReadOnly {};
using RO = ReadOnly;

struct WriteOneToClear {};
using W1C = WriteOneToClear;

struct ReadWrite {};
using RW = ReadWrite;

} // namespace regilite
#endif // REGILITE_FIELD_ACCESS_HPP