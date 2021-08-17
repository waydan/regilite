#include "CppUTest/TestHarness.h"
#include "test_registers.hpp"

TestReg test_register;

TEST_GROUP(ReadRegisterSnapshot)
{
    void setup() override { test_register.raw_write(0u); };
};

TEST(ReadRegisterSnapshot, SnapshotMatchesState)
{
    const auto snapshot = test_register.read();
    LONGS_EQUAL(0u, snapshot.raw());
}

TEST(ReadRegisterSnapshot, SnapshotCopiedBeforWriteNotUpdated)
{
    const auto snapshot = test_register.read();
    test_register.write(F1{3});
    CHECK(test_register.raw_read() != snapshot.raw());
}

TEST(ReadRegisterSnapshot, SnapshotCopiedAfterWriteIsUpdated)
{
    test_register.write(F1{3});
    const auto snapshot = test_register.read();
    LONGS_EQUAL(test_register.raw_read(), snapshot.raw());
}
