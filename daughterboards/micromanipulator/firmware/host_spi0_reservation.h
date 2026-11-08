#pragma once
#include "hardware/gpio.h"
// Backplane CPU only. Call early at boot, before enabling any shared buses.
// No other code may configure these pins or enable the host SPI0 peripheral.
static inline void fab_reserve_spi0_for_motion(void) {
    for (unsigned int pin = 16; pin <= 21; ++pin) {
        gpio_init(pin);
        gpio_set_dir(pin, GPIO_IN);
        gpio_disable_pulls(pin);
    }
}
