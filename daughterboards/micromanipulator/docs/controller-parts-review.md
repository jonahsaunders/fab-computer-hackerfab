# Controller and axis-driver package review

The following parts now have exact manufacturer and JLCPCB ordering codes in the schematic, PCB and BOM. Catalog identities were checked on 2026-11-07; confirm inventory at order time.

| References | Manufacturer part | JLCPCB |
| --- | --- | --- |
| U4 | Winbond W25Q32JVSSIQ | [C82344](https://jlcpcb.com/partdetail/C82344) |
| Y1 | Abracon ABM8-272-T3 | [C20625731](https://jlcpcb.com/partdetail/C20625731) |
| L2 | Murata DFE252012F-3R3M=P2 | [C2041573](https://jlcpcb.com/partdetail/C2041573) |
| SW1, SW2 | E-Switch TL3305AF160QG | [C2886899](https://jlcpcb.com/partdetail/C2886899) |
| D3 | Lite-On LTST-C190KGKT | [C125094](https://jlcpcb.com/partdetail/C125094) |
| U5, U6, U7 | Toshiba TB6612FNG(O,C,8,EL | [C88224](https://jlcpcb.com/partdetail/C88224) |

## Controller support

- **Flash:** The [Winbond drawing](https://datasheet.lcsc.com/datasheet/pdf/5e9d1528bd9ff612cdac1a3e34dc8d43.pdf?productCode=C179173), section 10.2, specifies the SS 208-mil package: 5.28 mm nominal body, 7.9 mm nominal lead span and 1.27 mm pitch. The local SOIC-8 5.3 x 5.3 mm footprint has 1.625 x 0.65 mm lands at x = +/-3.5875 mm. Pins 1/2/3/4/5/6/7/8 map to CS/D1/D2/GND/D0/CLK/D3/3V3. The 2.7-3.6 V device and 32 Mbit density retain the existing 3.3 V, 4 MiB design.
- **Crystal:** [Abracon drawing 456603](https://datasheet.lcsc.com/datasheet/pdf/d5520a242c89eeaef42f6496027f72da.pdf?productCode=C20625731), revision IR, specifies 12 MHz, 10 pF load, 50 ohm maximum ESR and a 3.2 x 2.5 mm body. Pins 1/3 are the crystal and 2/4 are case ground. The existing lands are 1.4 x 1.2 mm at x = +/-1.1 mm, y = +/-0.85 mm, slightly larger than the drawing's 1.4 x 1.1 mm reflow pads. C14/C15 remain 15 pF C0G. Two equal 15 pF capacitors provide 7.5 pF series load before pin/board parasitics; frequency/startup still need checking on the assembled board.
- **Core inductor:** The [Murata specification](https://taoic.oss-cn-hangzhou.aliyuncs.com/sku/pdf/816901e1ecbf66b9c6d207df4e9d77e76cb0ddd2.pdf) gives 3.3 uH, 2.5 x 2.0 x 1.2 mm nominal dimensions, 0.135 ohm maximum DCR, 2.5 A saturation criterion and 1.8 A temperature-rise criterion. This retains the part and embedded model from the RP2350 reference. Existing 0.8 x 2.0 mm lands at x = +/-1.0 mm fit its end terminations.
- **Switches:** [E-Switch P010468 revision C](https://configured-product-images.s3.amazonaws.com/2D/specs/TL3305AF160QG.pdf) specifies 4.5 x 4.5 mm body, 3.8 mm actuator height and 7.5 mm overall terminal span. The local footprint uses 1.6 x 1.4 mm pads at x = +/-3.6 mm, y = +/-1.5 mm, matching the drawing. Each horizontal pair is internally common; the two KiCad pad-number groups follow those pairs, so pressing closes RUN/BOOTSEL to ground. The switches are rated 12 V / 50 mA and operate from -20 to +70 C.
- **Status LED:** The [Lite-On specification](https://www.tme.com/Document/02bca468f5ec2519e3018913b2ddaf5e/LTST-C190KGKT.pdf) specifies a 1.6 x 0.8 x 0.8 mm green 0603 LED. Pad 1 is cathode/GND. Its approximately 2 V forward drop and existing 1 kohm resistor give roughly 1.3 mA from a 3.3 V GPIO; this is an indicator, not a 20 mA load.

These six selections change hidden procurement fields only. Parsed comparisons confirm unchanged visible schematic content and all PCB geometry.

## Toshiba axis-driver footprint correction

[Toshiba's package table](https://toshiba.semicon-storage.com/jp/semiconductor/design-development/package/sop.html) identifies SSOP24-P-300-0.65A as 7.8 x 5.6 mm, 0.65 mm pitch and 1.6 mm maximum height. The detailed TB6612FNG package drawing (2007-06-30, page 8, retained in the upstream design) shows a 7.6 +/-0.3 mm lead span and 0.22 +/-0.1 mm lead width. The [current package page](https://toshiba.semicon-storage.com/eu/semiconductor/design-development/package/detail.SSOP24-P-300-0.65A.html) provides the manufacturer's outline and land-pattern references.

The previous generic SSOP footprint represented a 5.3 x 8.2 mm body. Its existing copper lands already fit the Toshiba leads: centres at x = +/-3.5 mm, 1.9 x 0.4 mm pad size, 0.65 mm pitch. Those lands and all routing are retained. A project-local derivative, `FabNano:SSOP-24_Toshiba_5.6x7.8mm_P0.65mm`, now has the correct nominal fabrication outline and a courtyard widened around the body and extended for the 8.3 mm maximum end envelope. The original generic library entry remains intact.

The new nominal VRML model has a 5.6 x 7.8 x 1.2 mm body at 0.1 mm standoff and 24 leads on the correct pitch/span, with a pin-1 marker. It is deliberately a low-fidelity assembly aid, not a manufacturer tolerance model. No component moves, copper changes or pin swaps accompany the correction. Native comparisons verify every pad, net, component position and track, and DRC checks the revised courtyards.

The pin check retains the parallel AO/BO output contacts, VM on 13/14/24, VCC20, GND18 and PGND3/4/9/10, with the original PWM/input/STBY mapping. Driver current and thermal limits are separate from this package correction; the 3.2 A transient rating must not be treated as a continuous board rating.
