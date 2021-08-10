.. default-role:: code

.. role:: c-code(code)
    :language: C

.. role:: cpp-code(code)
    :language: Cpp

.. include:: <isonum.txt>

Introduction
------------

**Regilite** provides concise, robust abstractions for interacting with memory-mapped hardware registers. It's goals are to:

- Lighten user burden and improve readability with a simple, expressive interface
- Flag most programming errors at compile-time
- Generate assebly at-least as efficient as hand-written C code

Examples
--------
The most common operation for a memory-mapped hardware register is probably read-modify-write. This is expressed idiomatically in C as :c-code:`register = (register & ~mask) | value;` (assuming `mask` and `value` are both appropriately shifted and `register` has been declared :c-code:`volatile`).

Read-modify-write, however, is actually an implementation detail. Usually a user just wants to update one or more fields in a register. In Regilite, this is expressed as :cpp-code:`register.write(field)`. Here, `field` is an object of some `Field`-like type defined in the library, and it carries metadata to perform all bit-shifting and masking behind the scenes.




.. csv-table:: Port Control Register
    :header: "Bits", "Field", "Access"
    :align: center

    31-8, *Reserved*, *n/a*
    7, LowPowerCfg, r/w
    6-5, ClkDivSel, r/w
    4, SampleTimeCfg, r/w
    3-2, Mode, r/w
    1-0, InputClkSel, r/w

*This register definition is based on the `Kinetis KV1x`_ PORT_PCRx register.*

.. _`Kinetis KV1x`: https://www.nxp.com/files-static/32bit/doc/ref_manual/KV11P64M75RM.pdf



Writing to a Register
~~~~~~~~~~~~~~~~~~~~~
.. code-block:: Cpp

    // Writing a single field to the register
    reg.write(SlewRate::Fast);
    // Writing multiple fields to the register
    reg.write(Mux{5}, DriveStrength::Low);

    // Error: Cannot write the same field twice in one expression
    reg.write(SlewRate::Fast, SlewRate::Slow);

Capturing Register State
~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: Cpp

    // Saves the state of a register as non-volatile value
    auto snapshot = reg.read();

Sometimes a piece of code will need to refer to the same register state multiple times while assuming it has not changed. `Register::read()` copies the state of the volatile register to a non-volatile object for later processing.


Extracting a Field
~~~~~~~~~~~~~~~~~~
.. code-block:: Cpp

    // Extract field value directly from register
    PullEnable pull_state = reg.extract();

    // Extract field value from saved register state
    PullSelect selector = snapshot.extract();


Testing Field Values
~~~~~~~~~~~~~~~~~~~~
.. code-block:: Cpp

    // Check if single field matches register state
    reg.match(DummyField::Enable);
    snapshot.match(DummyField::Enable);

    // Check if multiple fields match register state
    reg.match_all(DummyField::Enable, SillyField{42});
    snapshot.match_all(DummyField::Enable, SillyField{42});

    // Check if any of the fields match register state
    reg.match_any(DummyField::Enable, SillyField{42});
    reg.match_any(DummyField::Enable, DummyField::Disable); // Always evaluates as true
    snapshot.match_any(DummyField::Enable, SillyField{42});

Passing a single field object to `match_any` or `match_all` is valid and semantically equivalent to calling `match` with that field.

A single call to `Register::match` will result in exactly one read to the memory-mapped hardware.

Notes
-----

Rationale
---------
Traditional C-style access and manipulation of hardware registers is manual, tedeous, and error prone. There are well documented patterns to reduce errors and make code more obvious, e.g. `Barr Group`_.

.. _`Barr Group`: https://barrgroup.com/embedded-systems/books/programming-embedded-systems/peripherals-device-drivers

Often silicon vendors will provide a header file which groups registers into a struct and `#define`\ s pointers and constants to ease access.

.. code-block:: C

    typedef struct {
        uint8_t volatile CONFIG;
        uint8_t volatile MISSILE_COMMAND;
        } FROB;

    #define FROB0 ((FROB* const)(0x1000))
    #define GIBBLE_SHIFT    (5)
    #define GIBBLE_MASK     ((uint8_t)(7u << GIBBLE_SHIFT))
    #define GIBBLE(x)       ((uint8_t)((x) << GIBBLE_SHIFT))


    A function in the hardware abstraction layer may then contain code which looks like:

.. code-block:: C

        FROB0->CONFIG = (FROB0->CONFIG & ~GIBBLE_MASK) | GIBBLE(2u);

Prior Art
---------
This library is not breaking new ground; others have also used the expressive power of C++ to simplify register access and reduce errors.

- Kvasir_
- regbits_

.. _Kvasir: https://github.com/kvasir-io/Kvasir
.. _regbits: https://github.com/thanks4opensource/regbits

These libraries are interesting and readers should take a look to consider which option is the best fit for their application or usecase.

- Write a single field to a register
- Write multiple fields to a register
- Read a single field from a register
- Read multiple fields from a register

Reduce Errors
~~~~~~~~~~~~~

- Only Predefined ``Field``\ s may be written to a ``Register``
- Overlapping ``Field``\ s can be detected at compile-time


Copyright |copy| 2021 by Daniel Way