#include "basic_register.hpp"
#include "check_register.hpp"
#include "field.hpp"
#include "traits.hpp"
#include <CppUTest/TestHarness.h>


TEST_GROUP(basic_register_write)
{
    using F0 = regilite::Field<std::uint8_t, regilite::Mask<0>{}>;
    using F1 = regilite::Field<std::uint8_t, regilite::Mask<2, 1>{}>;

    // +--+--+--+--+--+--+--+--+
    // |   Reserved   |  F1 |F0|
    // +--+--+--+--+--+--+--+--+
    //   7  6  5  4  3  2  1  0
    regilite::BasicRegister<std::uint8_t, 0, F0, F1> test_register;
};

TEST(basic_register_write, set_one_bit)
{
    test_register.write(F0{1});
    REGISTER_EQUALS(0x1, test_register);
}

TEST(basic_register_write, clear_one_bit)
{
    test_register.raw_write(0b10);
    test_register.write(F1{0});
    REGISTER_EQUALS(0x0, test_register);
}

TEST(basic_register_write, set_two_adjacent_fields)
{
    test_register.write(F1{2});
    test_register.write(F0{1});
    REGISTER_EQUALS(0b101, test_register);
}

TEST(basic_register_write, simultaneously_write_fields)
{
    test_register.raw_write(0b111);
    test_register.write(F0{0}, F1{1});
    REGISTER_EQUALS(0b010, test_register);
}

TEST(basic_register_write,
     unspecified_readable_writeable_fields_are_not_overwritten)
{
    test_register.raw_write(0b100u);
    test_register.write(F0{1});
    REGISTER_EQUALS(0b101, test_register);
}


TEST_GROUP(write_w1c_field)
{
    using Fx = regilite::Field<std::uint8_t, regilite::Mask<0>{}, regilite::RW>;
    using Fy = regilite::Field<bool, regilite::Mask<7>{}, regilite::W1C>;

    // +--+--+--+--+--+--+--+--+
    // |Fy|    Reserved     |Fx|
    // +--+--+--+--+--+--+--+--+
    //   7  6  5  4  3  2  1  0
    regilite::BasicRegister<std::uint8_t, 0, Fx, Fy> test_register;
};

TEST(write_w1c_field, implicitly_write_0_to_w1c)
{
    test_register.raw_write(0x80);
    test_register.write(Fx{1});
    REGISTER_EQUALS(0x01, test_register);
}

TEST(write_w1c_field, explicit_write_prevents_implicit_write)
{
    test_register.write(Fx{1}, Fy{true});
    REGISTER_EQUALS(0x81, test_register);
}


TEST_GROUP(optimized_register_write)
{
    using Fx = regilite::Field<std::uint8_t, regilite::Mask<0>{}, regilite::RW>;
    using Fy = regilite::Field<bool, regilite::Mask<7>{}, regilite::W1C>;

    // +--+--+--+--+--+--+--+--+
    // |Fy|    Reserved     |Fx|
    // +--+--+--+--+--+--+--+--+
    //   7  6  5  4  3  2  1  0
    regilite::BasicRegister<std::uint8_t, 0, Fx, Fy> test_register;
};

TEST(optimized_register_write,
     reserved_fields_reset_when_all_volatile_fields_written)
{
    test_register.raw_write(0b01111110);
    const auto audit = test_register.write(Fx{1});
    static_assert(regilite::traits::match_unqualified<decltype(audit),
                                                      regilite::Overwrite>{},
                  "Whole field should be overwritten");
    REGISTER_EQUALS(0x01, test_register);
}

TEST(optimized_register_write,
     preserve_reserved_dynamic_value_when_volatile_field_is_unwritten)
{
    test_register.raw_write(0b1011);
    const auto audit = test_register.write(Fy{true});
    static_assert(
        regilite::traits::match_unqualified<decltype(audit),
                                            regilite::ReadModifyWrite>{},
        "Test expects reserved fields will keep dynamic value");
    REGISTER_EQUALS(0b10001011, test_register);
}