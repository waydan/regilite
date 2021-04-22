#ifndef REGISTER_HPP
#define REGISTER_HPP

#include <cstdint>

namespace registex {

template <std::uintptr_t (&address)(), std::size_t lsb>
struct Field {
    explicit constexpr Field(std::uint32_t value) : value_(value << lsb){};

    void write()
    {
        *reinterpret_cast<volatile std::uint32_t*>(address()) = value_;
    }

    std::uint32_t value_;

    template <std::size_t lsb_other>
    constexpr auto
    operator|(const Field<address, lsb_other>& other) const noexcept
    {
        return Field<address, lsb>{value_ | other.value_};
    }
};

template <std::uint32_t& reg>
auto make_addr() -> std::uintptr_t
{
    return reinterpret_cast<std::uintptr_t>(&reg);
};

template <typename F, typename... Fs>
void write(F field, Fs... fields)
{
    auto joined_fields = (field | ... | fields);
    joined_fields.write();
};

} // namespace registex

#endif // REGISTER_HPP