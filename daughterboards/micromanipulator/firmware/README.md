# Firmware integration requirements

These headers are configuration aids for the new hardware, not a completed or hardware-tested firmware port. The source motion and rotation applications still need consolidation onto the single RP2350B.

The **motion card owns SPI0** and reads all three XYZ encoders. Use [board_config.h](board_config.h): MISO GPIO0, SCK GPIO2, MOSI GPIO3, and software chip selects GPIO44/45/46. GPIO20/21/22 are no longer encoder selects. Initialize all three CS outputs high before selecting the SPI function on GPIO0/2/3. Keep only one CS low at a time. Preserve the original MT6835 protocol, SPI mode and command framing.

Start at **1 MHz** for bench bring-up. The original firmware uses 8 MHz; the new backplane path, shared-slot stubs and sensor harnesses require oscilloscope checks before restoring that rate. Five 33-ohm source resistors on clock, MOSI and selects control edge rate; their values may need adjustment after measurement. MISO is driven by the selected sensor.

The **backplane CPU must leave GPIO16–21 as inputs with all pulls disabled**. Integrate [host_spi0_reservation.h](host_spi0_reservation.h) early in host startup and ensure no later code enables SPI0, changes the mux or drives these pins. The helper alone cannot enforce this across an application. This requirement applies during boot, normal operation and firmware updates. Use SPI1 for other host SPI peripherals. All three SPI0 chip selects are reserved for this pair; other cards must leave these signals undriven.

Power the complete assembly down before inserting/removing cards. There is no hot-swap isolation between independently powered sensor and controller logic. The files have been checked against the saved board pin map; no firmware binary or hardware runtime validation is included.

GPIO API reference: [Raspberry Pi Pico SDK](https://www.raspberrypi.com/documentation/pico-sdk/hardware.html#hardware_gpio).
