#include "CppUTest/TestHarness.h"

#include "register.hpp"
#include <cstdint>

std::uint32_t virtual_register;

using Writeable = registex::Register<registex::make_addr<virtual_register>>;
using Enable = registex::Field<Writeable, registex::mask_from_range<0, 0>>;
using Execute = registex::Field<Writeable, registex::mask_from_range<1, 1>>;
using Mode = registex::Field<Writeable, registex::mask_from_range<4, 2>>;

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
    virtual_register = 0xFFFF'FFF0;
    write(Enable{1}, Execute{1});
    LONGS_EQUAL(0xFFFF'FFF0 | 3u, virtual_register);
}

TEST(WriteToRegister, MultibitFieldClearsUnsetBits)
{
    virtual_register = 0xFF;
    write(Mode{5});
    LONGS_EQUAL(0b11110111, virtual_register);
}
