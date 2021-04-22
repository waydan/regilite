#include "CppUTest/TestHarness.h"

#include "register.hpp"
#include <cstdint>

std::uint32_t virtual_register;

using Enable = registex::Field<registex::make_addr<virtual_register>, 0>;
using Execute = registex::Field<registex::make_addr<virtual_register>, 1>;

TEST_GROUP(WriteToRegister)
{
    void setup() { virtual_register = 0u; };
};

TEST(WriteToRegister, WriteSingleBit)
{
    write(Enable{1});
    CHECK_EQUAL(1u, virtual_register);
}

TEST(WriteToRegister, WriteMultipleBits)
{
    write(Enable{1}, Execute{1});
    CHECK_EQUAL(3u, virtual_register);
}
