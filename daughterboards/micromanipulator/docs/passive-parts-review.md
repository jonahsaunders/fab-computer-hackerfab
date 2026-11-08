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

## Remaining capacitor selections

The final ten capacitor placeholders have now been resolved. Visible ratings reflect the actual selected parts; capacitance values and all pad/net/trace geometry are retained.

| References | Part / JLCPCB | Selection |
| --- | --- | --- |
| C31, C35, C39 | SANYEAR C0805X7R106K250NT / [C2835529](https://jlcpcb.com/partdetail/SANYEAR-C0805X7R106K250NT/C2835529) | 10 uF, 25 V, X7R, 0805 |
| C4, C6, C59 | YAGEO CC0603KRX7R9BB104 / [C14663](https://jlcpcb.com/partdetail/C14663) | 100 nF, 50 V, X7R, 0603; same part as C30/C34/C38 |
| C3, C61, C63 | Samsung CL10A106KP8NNNC / [C19702](https://jlcpcb.com/partdetail/C19702) | 10 uF, 10 V, X5R, 0603 |
| C65 | Samsung CL10A105KB8NNNC / [C15849](https://jlcpcb.com/partdetail/C15849) | 1 uF, 50 V, X5R, 0603 |

The SANYEAR manufacturer drawing linked from its catalog gives a 2.00 +/-0.20 by 1.25 +/-0.20 mm body, maximum 1.45 mm height. The existing 0805 lands accommodate it. These ceramics supplement each axis's 220 uF bulk capacitor and direct 100 nF bypass; no claim is made that their effective capacitance remains 10 uF at 12 V because an individual bias curve was not supplied.

[YAGEO's exact-part specification](https://www.yageogroup.com/download/specsheet/CC0603KRX7R9BB104) and the Samsung specifications give 1.6 by 0.8 by 0.8 mm nominal bodies, all dimensions +/-0.1 mm. Existing 0603 footprints and nominal models fit. Samsung's typical bias curves for [10 uF](https://product.samsungsem.com/mlcc/CL10A106KP8NNN.do) and [1 uF](https://product.samsungsem.com/mlcc/CL10A105KB8NNN.do) give approximately 4.29 uF at 3.4 V, 2.67 uF at 5.25 V, and 0.63 uF at 5.25 V respectively. These are typical interpolated values, not guaranteed combined-condition minima.

C3 is supplementary output bulk; C2 independently provides the regulator's required local capacitance. C61/C63 supplement the direct C60/C62 bypasses and shared 220 uF load-rail bulk. C65 supplements C64 at the gate driver. X5R's 85 C temperature limit applies to these parts; it must be respected during thermal bring-up. C3's old unselected X7R label has therefore been corrected explicitly, rather than assigning an X5R part under an X7R description.

F1/F2 are selected separately in the [load-power review](load-power-review.md). All 117 BOM entries now carry manufacturer and supplier codes.

## Existing bulk and core capacitors

C5/C33/C37/C41 retain KNSCHA 217EC0037, the same 220 uF / 25 V polymer part used by the host. The [manufacturer specification](https://atta.szlcsc.com/upload/public/pdf/source/20241030/2EF4F6A017619059DDD7BBE6E6FCD6C8.pdf), pages 5-6, gives 35 milliohm maximum ESR and 1.95 A RMS ripple at 100 kHz. Its frequency factor is 0.7 from 10 to 100 kHz, giving 1.365 A for that range. These figures do not establish the complete system's ripple or startup behavior.

The drawing specifies a nominal 6.3 mm can, 6.6 mm square base, 7.7 +/-0.3 mm height and 0.5-0.8 mm lead width. The existing footprint's two 3.5 by 1.6 mm lands, centered at +/-2.7 mm, encompass the lead envelope and leave solder fillets. Its courtyard clears the maximum body/base, and the nominal local model is retained. [LCSC C42371908](https://item.szlcsc.com/44253490.html) confirms the exact ordering code and SMT extended-library designation; confirm JLCPCB order availability, since its direct catalog page did not load during the final check.

C11/C12 retain Murata GRM155R60J475ME47D, [JLCPCB C82453](https://jlcpcb.com/partdetail/MurataElectronics-GRM155R60J475ME47D/C82453), 4.7 uF / 6.3 V / X5R / 0402. The code was already in the BOM and is now also present in the hidden schematic and PCB fields. Their specially checked core-regulator footprints, values and routing are unchanged.
