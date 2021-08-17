#ifndef TEST_REGISTER_HPP
#define TEST_REGISTER_HPP

#include "CppUTest/TestHarness.h"
#include "basic_register.hpp"
#include "field.hpp"
#include "partition_register.hpp"
#include "traits.hpp"


// TestReg layout
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
// |  |  |  |  |     F3    |  |   F2   |  |  F1 |F0|
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
//  15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0

enum class F3Val
{
    A = 1,
    B = 2,
    C = 4,
    D = 8
};

using F0 = regilite::Field<std::uint16_t, regilite::Mask<0>{}>;
using F1 = regilite::Field<std::uint16_t, regilite::Mask<2, 1>{}>;
using F2 = regilite::Field<std::uint16_t, regilite::Mask<6, 4>{}>;
using F3 = regilite::Field<F3Val, regilite::Mask<11, 8>{}>;


using TestReg = regilite::BasicRegister<std::uint16_t, 0, F0, F1, F2, F3>;

static_assert(std::is_standard_layout<TestReg>{},
              "BasicRegister<> type must be standard layout.");

static_assert(
    std::is_standard_layout<TestReg::Snapshot>{},
    "Unnameable type RegisterProxy<>::Snapshot must be standard layout.");


// PartableReg layout
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
// |  |  |  |  |     F3    |  |   F2   |  |  F1 |F0|
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
//  15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0

using PartableReg =
    regilite::PartitionRegister<std::uint16_t, 0, F0, F1, F2, F3>;

#endif // TEST_REGISTER_HPP