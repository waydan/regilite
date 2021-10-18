#ifndef CHECK_REGISTER_HPP
#define CHECK_REGISTER_HPP

#include <CppUTest/TestHarness.h>

template <typename Register>
void REGISTER_EQUALS(typename Register::storage_type value, Register& reg)
{
    LONGS_EQUAL(value, reg.raw_read());
}

#endif // CHECK_REGISTER_HPP