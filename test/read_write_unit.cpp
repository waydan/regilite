#include "CppUTest/TestHarness.h"

#include "register.hpp"
#include <cstdint>
#include <type_traits>

std::uint32_t virtual_register;

using Writeable = registex::Register<registex::make_addr<virtual_register>>;
using Enable = registex::Field<Writeable, registex::mask_from_range(0, 0)>;
using Execute = registex::Field<Writeable, registex::mask_from_range(1, 1)>;
using Mode = registex::Field<Writeable, registex::mask_from_range(4, 2)>;
using Config = registex::Field<Writeable, registex::mask_from_range(11, 8)>;

TEST_GROUP(WriteToRegister)
{
    void setup() { virtual_register = 0u; };
};


TEST(WriteToRegister, WriteSingleBit)
{
    write(Enable{1});
    LONGS_EQUAL(1u, virtual_register);
}


TEST(WriteToRegister, WriteMultipleBits)
{
    write(Enable{1}, Execute{1});
    LONGS_EQUAL(3u, virtual_register);
}

TEST(WriteToRegister, WritesDoNotAffectOtherBits)
{
    virtual_register = 0xFFF0;
    write(Enable{1}, Execute{1});
    LONGS_EQUAL(0xFFF0 | 3u, virtual_register);
}


TEST(WriteToRegister, MultibitFieldClearsUnsetBits)
{
    virtual_register = 0xFF;
    write(Mode{5});
    LONGS_EQUAL(0b11110111, virtual_register);
}


template <typename A, typename B>
constexpr auto is_same_non_cv_type =
    std::is_same_v<std::remove_cv_t<A>, std::remove_cv_t<B>>;

TEST(WriteToRegister, WritesMinimalSizeWhenPossible)
{
    const auto action = write(Config{0b1111});
    static_assert(is_same_non_cv_type<decltype(action),
                                      registex::WriteAction<std::uint8_t>>);
    LONGS_EQUAL(0b1111 << 8, virtual_register);
    LONGS_EQUAL(reinterpret_cast<std::uintptr_t>(&virtual_register) + 1,
                action.address);
}
