# Local bypass routing review

The six MCU capacitors that previously depended on a via-to-via power-layer connection now have continuous front-copper paths to their supply pins. The comparison baseline is commit `ea3916893235fc1fc28f32656f90d6fa9a8904a1`.

| Capacitor | RP2350B pin | Direct front-copper path, pad centre to pin centre |
| --- | --- | --- |
| C18 | 24, IOVDD | 3.194 mm |
| C19 | 29, IOVDD | 3.694 mm |
| C26 | 32, DVDD | 1.253 mm |
| C27 | 51, DVDD | 1.907 mm |
| C53 | 68, USB_VDD | 1.570 mm |
| C54 | 69, QSPI_IOVDD | 2.307 mm |

C26 moved beside pin 32, with the debug-clock escape moved inward to make room. C53 and C54 moved beside the USB and QSPI supply pins. The USB series resistors moved out of that local bypass area. C18, C19 and C27 retain their positions and now connect directly on the component side; unnecessary pin-end supply vias were removed. C53 and C54 share a nearby ground return, while each has its own direct supply-pin trace. The fixed backplane and harness interfaces are unchanged.

C66 now also connects directly to the USB protection device's supply pin. It was previously unrouted. All 35 checked local supply/bypass connections now have a continuous F.Cu path, without using an inner-layer shortcut. The [measured paths](decoupling-paths.csv) come from the saved native board, not from an intended route list.

This check measures supply-trace connectivity and centreline length. It does not measure loop inductance, establish controlled impedance, or replace ground-return, stackup and electrical review. Ground returns use the filled In2.Cu plane. Further routing and the final return-path review remain open.

Run with KiCad's Python and `pcbnew` available:

```sh
python scripts/check_decoupling.py --output build/decoupling-paths.csv
```

Native DRC at this revision reports zero violations and zero schematic-parity issues. There are 28 other unconnected items; this is still an unfinished layout. The newly opened flash routing corridor is now routed manually.

[![Front copper detail showing the direct bypass traces](decoupling-detail.svg)](decoupling-detail.svg)

Reference: [Raspberry Pi hardware design guide, section 2.2.1](https://pip-assets.raspberrypi.com/categories/1214-rp2350/documents/RP-008280-DS-1-hardware-design-with-rp2350.pdf?disposition=inline).
