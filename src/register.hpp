#ifndef REGISTER_HPP
#define REGISTER_HPP

#include <cstdint>

namespace registex {

template <std::uintptr_t (&address)()>
struct Field {
    explicit constexpr Field(int){};

    static void write()
    {
        *reinterpret_cast<volatile std::uint32_t*>(address()) = 1u;
    }
};

template <std::uint32_t& reg>
auto make_addr() -> std::uintptr_t
{
    return reinterpret_cast<std::uintptr_t>(&reg);
};

template <typename F>
void write(F field)
{
    field.write();
};

} // namespace registex

#endif // REGISTER_HPP