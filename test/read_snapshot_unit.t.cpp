#include "CppUTest/TestHarness.h"
#include "register.hpp"
#include "test_register.hpp"

TestReg test_register;

TEST_GROUP(ReadRegisterSnapshot)
{
    void setup() { register_view(test_register) = 0u; };
};

TEST(ReadRegisterSnapshot, SnapshotMatchesState)
{
    const auto snapshot = test_register.read();
    LONGS_EQUAL(0u, snapshot.raw());
}

TEST(ReadRegisterSnapshot, SnapshotNotUpdatedByRegisterWrite)
{
    const auto snapshot = test_register.read();
    test_register.write(F1{3});
    CHECK(register_view(test_register) != snapshot.raw());
}
