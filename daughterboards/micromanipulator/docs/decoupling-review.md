# Capacitor placement and return-path review

This pass reviews all **48 capacitors**, including IC bypassing, supply bulk, input filters and crystal loads. It shortens local supply and ground paths, adds ground vias where useful, and sets every capacitor ground pad to connect solidly wherever the front ground pour reaches it. The comparison baseline is published commit `29b7a7d6dc5006305a6a5237972ac0a1ec5680e8`.

## MCU and clock

C10, C18, C19, C23, C53 and C54 move closer to their served pins. C12 gains a nearby ground via. C26's previous long ground lead is replaced by a local return. C53 and C54 now have separate ground vias. The already-close top and bottom MCU bypass capacitors retain their pin-facing placement, with the plane-entry vias brought closer. Less-sensitive control routes on the back move aside to make space for these returns.

| Capacitor | Served pin | Supply trace before → after | Ground-via trace before → after |
| --- | --- | ---: | ---: |
| C10 | U1.61, VREG_AVDD | 3.011 → 1.875 mm | 1.026 → 0.667 mm |
| C12 | U1.64, VREG_FB | 1.298 → 1.298 mm | 2.135 → 0.485 mm |
| C18 | U1.24, IOVDD | 3.194 → 2.173 mm | 1.100 → 1.157 mm |
| C19 | U1.29, IOVDD | 3.694 → 2.594 mm | 0.974 → 0.570 mm |
| C26 | U1.32, DVDD | 1.253 → 1.253 mm | 2.127 → 0.608 mm |
| C53 | U1.68, USB_VDD | 1.570 → 1.170 mm | 0.720 → 0.620 mm |
| C54 | U1.69, QSPI_IOVDD | 2.307 → 1.460 mm | 1.798 → 1.331 mm |

The table shows the tradeoff for C18: its ground trace is 0.057 mm longer, while its supply path is 1.021 mm shorter. C54 still needs an angled return around nearby copper. The core-converter capacitor traces to PGND remain direct; its switching loop remains excluded from the front ground pour.

Y1 is rotated, with R12 and both load capacitors placed around its signal pads. Each load capacitor has a short local ground return, and both crystal ground pads have nearby vias. The crystal traces remain on F.Cu with no signal vias.

## Drivers, protection and supply

- C60/C62 and C67/C68 move beside the rotation-driver supply pins. Their direct supply traces fall to 1.17 mm and 1.12 mm respectively. C64 at the vacuum driver and C66 at USB protection also move closer.
- C32/C36/C40 use smaller 0402 parts and connect to the adjacent driver ground-pin return. Their supply paths increase by 0.075 mm, while the dedicated ground-via paths shorten from 0.900 to 0.591 mm. This is an intentional whole-loop placement choice.
- C30/C34/C38 use 0603, 100 nF, 50 V parts; C31/C35/C39 rotate beside the opposite motor-supply pins. Supply paths are direct, with local supply and ground vias.
- Bulk capacitors C5/C33/C37/C41 gain paired supply and ground vias and 0.6 mm ground leads. Their trace-centre lengths are unchanged; the wider copper and parallel vias are the improvement.
- C1/C2/C3, C4/C6/C59 and the remaining tool-supply capacitors receive closer ground vias. C3 has its own return. U2 is now the SO-8 AP2112M-3.3TRG1, using the existing backplane 5 V rail; see the [supply budget](power-budget.md).

The nine new 0402 bypass selections are Samsung CL05B104KO5NNNC, [JLCPCB C1525](https://jlcpcb.com/partdetail/1877-CL05B104KO5NNNC/C1525), 100 nF / 16 V / X7R. The three 0603 motor bypass selections are YAGEO CC0603KRX7R9BB104, [C14663](https://jlcpcb.com/partdetail/Yageo-CC0603KRX7R9BB104/C14663), 100 nF / 50 V / X7R. Their schematic, PCB, BOM and bundled models agree. Catalog/package identity was checked; stock at ordering time is not guaranteed.

## Other annotated routing

R34 moves beside rotation-encoder connector J12 and connects directly to CS pin 5. The former signal-side via and long pull-up stub are removed; a supply via remains. The two vias above/right of U1 carry **HEATER_PWM**, bridging across debug-clock routing. They are signal layer transitions, not unused ground vias.

Sixty-eight right-angle track bends are chamfered. The three encoder SPI escapes at the MCU's lower-left side have 0.8 mm copper tapers between their 0.10 and 0.20 mm sections. These tapers remove abrupt width shoulders; they do not establish controlled impedance. The DIN96 and all 14 external connector placements, pad geometry and pin assignments are unchanged.

## Saved-board checks

All **35 local supply-to-pin paths** remain entirely on F.Cu. All **48 capacitor ground pads** have an explicit F.Cu path to a ground via and a solid pad-to-pour setting. The core-converter pour exclusion deliberately leaves its local return traces exposed. The [supply table](decoupling-paths.csv) and [ground-return table](capacitor-returns.csv) are measured from the saved native PCB, independently of the route manifest.

Lengths are trace centrelines from pad centre to pin/via centre. The ground audit deliberately excludes parallel copper-pour paths; it does not model plane spreading, mutual inductance, impedance or EMI. The filled In2.Cu ground plane is one connected region. Native DRC reports zero violations, unconnected items and schematic-parity issues. See the [layout review](layout-review.md) for stackup, USB and prototype-validation limits.

Run with KiCad's Python and `pcbnew` available:

```sh
python scripts/check_decoupling.py
python scripts/check_capacitor_returns.py
```

The previews hide copper pours to expose the dedicated traces. The canonical board retains all filled zones.

[![MCU, crystal and capacitor detail](decoupling-detail.svg)](decoupling-detail.svg)

[![Axis-driver capacitor detail](axis-decoupling-detail.svg)](axis-decoupling-detail.svg)

[![Tool-driver capacitor detail](tool-decoupling-detail.svg)](tool-decoupling-detail.svg)

Reference: [Raspberry Pi hardware design guide, section 2.2.1](https://pip-assets.raspberrypi.com/categories/1214-rp2350/documents/RP-008280-DS-1-hardware-design-with-rp2350.pdf?disposition=inline).
