#ifndef TEST_REGISTER_HPP
#define TEST_REGISTER_HPP

auto register_view(regilite::Register& reg) noexcept -> std::uint32_t&
{
    return *reinterpret_cast<std::uint32_t*>(&reg);
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

using TestReg = regilite::Register;

static_assert(std::is_standard_layout<TestReg>::value,
              "Register<> type must always be standard layout.");

using F0 = regilite::Field<0b001>;
using F1 = regilite::Field<0b110>;


#endif // TEST_REGISTER_HPP