# Passive part selection

The 49 previously unselected resistors and small capacitors below now have exact ordering codes in the schematic, PCB properties and BOM. This change adds hidden procurement fields only. A parsed comparison against the preceding board and all affected schematic sheets verifies unchanged values, nets, pads, placement, models, copper and visible drawing geometry. Project design rules are unchanged.

JLCPCB catalog identities were checked on 2026-11-07. Catalog presence does not reserve stock; verify inventory when ordering.

| References | Part | JLCPCB | Rating / package |
| --- | --- | --- | --- |
| R5, R6 | Uniroyal 0603WAF0000T5E | [C21189](https://jlcpcb.com/partdetail/C21189) | 0 ohm jumper, 0603 |
| R3, R4 | Uniroyal 0603WAF1000T5E | [C22775](https://jlcpcb.com/partdetail/C22775) | 100 ohm, 1%, 0603 |
| R9, R36 | Uniroyal 0603WAF1001T5E | [C21190](https://jlcpcb.com/partdetail/C21190) | 1 kohm, 1%, 0603 |
| R20-R24, R34, R35, R40, R45, R46 | Uniroyal 0603WAF1002T5E | [C25804](https://jlcpcb.com/partdetail/C25804) | 10 kohm, 1%, 0603 |
| R1, R42, R44, R50 | Uniroyal 0603WAF1003T5E | [C25803](https://jlcpcb.com/partdetail/C25803) | 100 kohm, 1%, 0603 |
| R47 | Uniroyal 0603WAF1004T5E | [C22935](https://jlcpcb.com/partdetail/C22935) | 1 Mohm, 1%, 0603 |
| R48, R49 | Uniroyal 0603WAF5101T5E | [C23186](https://jlcpcb.com/partdetail/C23186) | 5.1 kohm, 1%, 0603 |
| R2 | Uniroyal 0603WAF2202T5E | [C31850](https://jlcpcb.com/partdetail/C31850) | 22 kohm, 1%, 0603 |
| R41, R43 | Uniroyal 0603WAF330JT5E | [C23140](https://jlcpcb.com/partdetail/C23140) | 33 ohm, 1%, 0603 |
| R51 | Uniroyal 0603WAF1503T5E | [C22807](https://jlcpcb.com/partdetail/C22807) | 150 kohm, 1%, 0603 |
| R11, R13 | Uniroyal 0402WGF1002TCE | [C25744](https://jlcpcb.com/partdetail/C25744) | 10 kohm, 1%, 0402 |
| R12, R14 | Uniroyal 0402WGF1001TCE | [C11702](https://jlcpcb.com/partdetail/C11702) | 1 kohm, 1%, 0402 |
| R10 | Uniroyal 0402WGF330JTCE | [C25105](https://jlcpcb.com/partdetail/C25105) | 33 ohm, 1%, 0402 |
| C13, C16-C27, C53, C54 | Samsung CL05B104KA5NNNC | [C155422](https://jlcpcb.com/partdetail/C155422) | 100 nF, 25 V, X7R, 10%, 0402 |
| C14, C15 | Fenghua 0402CG150J500NT | [C1548](https://jlcpcb.com/partdetail/C1548) | 15 pF, 50 V, C0G, 5%, 0402 |

## Package and circuit checks

The [Uniroyal manufacturer datasheet](https://robu-prod-media.s3.ap-south-1.amazonaws.com/uploads/2024/06/C38522.pdf), pages 4-5, specifies nominal 1.0 x 0.5 mm bodies for 0402 and 1.6 x 0.8 mm bodies for 0603. Existing project footprints use 0.54 x 0.64 mm pads at x = +/-0.51 mm and 0.80 x 0.95 mm pads at x = +/-0.825 mm respectively. These are the KiCad IPC nominal lands, with larger fillet allowance than the manufacturer's compact reflow examples. No land or courtyard change is required. The 0402 parts are rated 62.5 mW / 50 V and the 0603 parts 100 mW / 75 V at or below 70 C; the power-derived voltage limit also applies. The 0 ohm links carry I2C signals, not supply current. They are rated 1 A by the family datasheet.

[Samsung's specification](https://product.samsungsem.com/mlcc/CL05B104KA5NNN.do) and [Fenghua's specification](https://www.fhcomp.com/en/product_info/?prod_code=0402CG150J500NT) both give 1.00 +/-0.05 by 0.50 +/-0.05 mm bodies and 0.50 +/-0.05 mm thickness. Existing 0402 capacitor lands are 0.56 x 0.62 mm at x = +/-0.48 mm. The crystal capacitors retain C0G dielectric and 15 pF values. The 100 nF capacitors retain their 25 V rating and use X7R dielectric; these are local logic/core bypass parts, not the motor bulk-energy reservoir.

Nominal project-local 0402/0603 models remain appropriate for these standard chip packages. The previously selected USB 0201 termination resistors, regulator capacitors and motor bulk capacitors are covered in their separate reviews.
