#ifndef TEST_REGISTER_HPP
#define TEST_REGISTER_HPP

#include "CppUTest/TestHarness.h"
#include "field.hpp"
#include "register.hpp"
#include "traits.hpp"

template <typename UInt, UInt mask>
SimpleString StringFrom(regilite::Field<UInt, mask> f)
{
    return SimpleString{"Field value: "} + StringFrom(f.value());
}

template <typename UInt>
auto register_view(regilite::Register<UInt>& reg) -> UInt&
{
    return *reinterpret_cast<UInt*>(&reg);
}

template <typename UInt>
auto REGISTER_EQUALS(regilite::traits::identity_t<UInt> value,
                     regilite::Register<UInt>& reg) -> void
{
    LONGS_EQUAL(value, register_view(reg));
}


// TestReg layout
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
// |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
//  31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 15
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
// |  |  |  |  |  |  |  |  |  |   F2   |  |  F1 |F0|
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
//  15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0

using TestReg = regilite::Register<std::uint32_t>;

static_assert(std::is_standard_layout<TestReg>::value,
              "Register<> type must be standard layout.");

static_assert(
    std::is_standard_layout<decltype(std::declval<TestReg>().read())>::value,
    "Unnameable type Register<>::Snapshot must be standard layout.");

using F0 = regilite::Field<std::uint32_t, regilite::Mask<0>::value>;
using F1 = regilite::Field<std::uint32_t, regilite::Mask<2, 1>::value>;
using F2 = regilite::Field<std::uint32_t, regilite::Mask<6, 4>::value>;


#endif // TEST_REGISTER_HPP