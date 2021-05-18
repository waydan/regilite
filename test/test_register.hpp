#ifndef TEST_REGISTER_HPP
#define TEST_REGISTER_HPP

#include "CppUTest/TestHarness.h"
#include "traits.hpp"

template <typename UInt>
auto register_view(regilite::Register<UInt>& reg) noexcept -> UInt&
{
    return *reinterpret_cast<UInt*>(&reg);
}

template <typename UInt>
auto REGISTER_EQUALS(regilite::traits::identity_t<UInt> value,
                     regilite::Register<UInt>& reg) noexcept -> void
{
    LONGS_EQUAL(value, register_view(reg));
}


// TestReg layout
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
// |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
//  31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 15
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
// |  |  |  |  |  |  |  |  |  |  |  |  |  |  F1 |F0|
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
//  15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0

using TestReg = regilite::Register<std::uint32_t>;

static_assert(std::is_standard_layout<TestReg>::value,
              "Register<> type must always be standard layout.");

using F0 = regilite::Field<0b001>;
using F1 = regilite::Field<0b110>;


#endif // TEST_REGISTER_HPP