# Tool-output component review

The following exact parts are assigned in the schematic, PCB and BOM. Manufacturer package drawings and pin functions were compared with the saved footprints on 2026-11-07. Catalog listings establish part identity and assembly support; available inventory must be checked when ordering.

| References | Selected manufacturer / part | JLCPCB | Saved footprint |
| --- | --- | --- | --- |
| U9, U10 | Texas Instruments DRV8837CDSGR | [C191000](https://jlcpcb.com/partdetail/C191000) | WSON-8, 2 × 2 mm, 0.5 mm pitch, exposed pad |
| U11 | Microchip TC4427AEOA | [C18690](https://jlcpcb.com/partdetail/C18690) | SOIC-8, 3.9 × 4.9 mm, 1.27 mm pitch |
| Q1, Q2 | Alpha & Omega Semiconductor AO3400A | [C20917](https://jlcpcb.com/partdetail/C20917) | SOT-23 |
| D2 | MDD SS34 | [C8678](https://jlcpcb.com/partdetail/C8678) | SMA / DO-214AC |

## Pin and land checks

- **U9/U10:** [TI's DSG0008A drawing](https://www.ti.com/lit/ds/symlink/drv8837c.pdf) has rows 1.9 mm apart and a 0.9 × 1.6 mm exposed pad. The footprint matches these locations and the 0.5 mm pitch. Its 0.6 × 0.25 mm signal lands extend 0.05 mm farther at each end than TI's 0.5 × 0.25 mm example. Pin 1 is fused 5 V VM, pins 2/3 are winding outputs, pin 4 and pad 9 are ground, pins 5/6 are IN2/IN1, pin 7 is enable, and pin 8 is 3.3 V logic. Both exposed pads have two filled/capped ground vias. The existing nominal 3D model represents this package.
- **U11:** [Microchip's OA drawing](https://ww1.microchip.com/downloads/en/DeviceDoc/20001423J.pdf), pages 18–19, specifies a 3.9 × 4.9 mm body, 6.0 mm lead span and 1.27 mm pitch. The saved SOIC lands cover the leads and retain the correct pin sequence: inputs 2/4, ground 3, outputs 7/5 and supply 6; pins 1/8 are NC. Its supply now follows the [upstream logic-power domain](power-budget.md#gate-driver-supply-and-an-open-load-fuse).
- **Q1/Q2:** The [AOS pinout](https://www.aosmd.com/sites/default/files/res/datasheets/AO3400A.pdf) and [SOT23 drawing](https://www.aosmd.com/sites/default/files/res/package/SOT23.pdf) agree with gate 1, source 2 and drain 3. The generic KiCad SOT-23 lands retain the 0.95 mm pitch and cover the specified leads. These are generic package models, not manufacturer tolerance models.
- **D2:** The [MDD drawing supplied by LCSC](https://www.lcsc.com/datasheet/C8678.pdf) specifies SMA with a 4.7–5.3 mm lead span and 1.3–1.7 mm terminal width. The saved 2.5 × 1.8 mm lands at ±2.0 mm cover those terminals. The cathode band is pad 1, connected to the fused load supply; pad 2 connects to the vacuum switch node.

## Electrical limits

The DRV8837C uses separate motor and logic supplies, compatible with the board's 5 V and 3.3 V domains. Its 1 A maximum output specification is not a guaranteed continuous winding-current rating for this layout. Thermal and motor-stall checks remain necessary.

AO3400A is a 30 V device with ±12 V gate limits; the 5 V buffer drive is within those limits. Its datasheet gives 32 mΩ maximum on-resistance at 4.5 V gate drive. MDD SS34 is a 40 V, 3 A device under its specified test conditions. Neither package's headline current rating establishes the allowed heater or pump current on this board; the final load, fuse and thermal budget remain separate checks.

This selection changes hidden procurement fields only. Parsed schematic/PCB comparisons prove unchanged values, pin assignments, placement, pads, models and routing.
