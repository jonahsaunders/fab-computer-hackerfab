# JLCPCB parts sourcing

Stock checked on **November 12, 2026** against JLCPCB’s public assembly catalog. Quantities below are assembly inventory, separate from LCSC retail inventory. They can change between this check and checkout. A shortfall can leave a matched part unchecked, so confirm the selected quantities and attrition in the live quote. [JLCPCB matching guidance](https://jlcpcb.com/help/article/component-matching-guidelines-for-pcba-orders)

The [manufacturing guide](README.md) links to the original-design BOMs. The table below gives choices for an individual order. The checked catalog code is the original code where the project specifies one, or an exact catalog match where the project leaves it blank. The TPS2116DRL listing uses TI’s tape-and-reel orderable suffix `TPS2116DRLR`. [TI orderable part](https://www.ti.com/product/TPS2116/part-details/TPS2116DRLR)

## Parts to review before checkout

| Board and designators | Original part | JLCPCB assembly stock | Order option and stock | Fit and electrical check |
| --- | --- | --- | --- | --- |
| Backplane C3, C4, C7, C10, C11, C14 | `C1608X7R1H103M080AA` | [`C3832102`](https://jlcpcb.com/partdetail/C3832102) · 0 (out of stock) | Samsung Electro-Mechanics `CL10B103KB8NNNC` [`C1589`](https://jlcpcb.com/partdetail/C1589) · 1,644,472 | Same two-terminal 0603 land pattern, 10 nF, 50 V, X7R. ±10% tightens the original ±20%. [TDK original](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1H103M080AA) |
| Backplane C15, C16, C37, C38 | `C1608X7R1E105K080AB` | [`C2170660`](https://jlcpcb.com/partdetail/C2170660) · 3 (short for two boards or order minimum) | Murata Electronics `GRT188R71E105KE13D` [`C701259`](https://jlcpcb.com/partdetail/C701259) · 4,812 | Same two-terminal 0603, 1 µF, 25 V, X7R, ±10% for the 3.3 V and 5 V rail bypass positions. TDK also identifies its [CGA3E1X7R1E105K080AC](https://jlcpcb.com/partdetail/C2167089) as an automotive equivalent. That listing had 4 pieces at a 5-piece minimum. [TDK original](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1E105K080AB) |
| Backplane C18, C19, C20, C21, C22, C23, C24, C26, C27, C28, C30, C31, C33, C35, C41 | `0402B104K500HI` | No exact listing verified | Walsin Tech Corp `0402B104K500CT` [`C152814`](https://jlcpcb.com/partdetail/C152814) · 739,623 | Same two-terminal 0402, 100 nF, 50 V, X7R, ±10%. [NextGen original](https://www.nextgencomponent.com/uploads/soft/20241220/1-2412201F0061O.pdf) |
| Backplane C29, C34 | `CC0603JRNPO0BN150` | [`C327117`](https://jlcpcb.com/partdetail/C327117) · 0 (out of stock) | Samsung Electro-Mechanics `CL10C150JB8NNNC` [`C1644`](https://jlcpcb.com/partdetail/C1644) · 1,042,822 | Same two-terminal 0603, 15 pF, C0G, ±5%. The 50 V rating covers the 3.3 V crystal circuit. Fit both C29 and C34 with the same part. For the original 100 V rating, [C472783](https://jlcpcb.com/partdetail/C472783) has the same nominal value, dielectric and tolerance, with 13 pieces at a 20-piece minimum. |
| Backplane R4, R9, R10, R12, R13, R14, R20, R21, R53, R54 | `RT0603FRE071K13L` | [`C863632`](https://jlcpcb.com/partdetail/C863632) · 0 (out of stock) | YAGEO `RT0603BRD071K13L` [`C861190`](https://jlcpcb.com/partdetail/C861190) · 3,214 | Same Yageo RT thin-film 0603 package, 1.13 kΩ, 100 mW. The ±0.1% tolerance and ±25 ppm/°C TCR are tighter than the original. [Yageo RT series data](https://datasheet.lcsc.com/datasheet/pdf/46d7760c582640714d605308a25a220a.pdf?productCode=C728599) |
| Backplane R8 | `RT0603FRE073K16L` | [`C863780`](https://jlcpcb.com/partdetail/C863780) · 0 (out of stock) | YAGEO `RT0603BRE073K16L` [`C326747`](https://jlcpcb.com/partdetail/C326747) · 1,927 | Same Yageo RT thin-film 0603 package, 3.16 kΩ, 100 mW and ±50 ppm/°C TCR. The ±0.1% tolerance is tighter than the original ±1%. [Yageo RT series data](https://datasheet.lcsc.com/datasheet/pdf/46d7760c582640714d605308a25a220a.pdf?productCode=C728599) |
| Backplane R22, R23 | `RMEF0603JT5K10` | [`C6981465`](https://jlcpcb.com/partdetail/C6981465) · 0 (out of stock) | YAGEO `AC0603JR-075K1L` [`C144594`](https://jlcpcb.com/partdetail/C144594) · 1,292 | Same two-terminal 0603, 5.1 kΩ, ±5%, 100 mW, AEC-Q200 thick-film resistor for the USB-C CC pull-downs. |
| Backplane R55 | `RC0402JR-0733RP` | [`C851857`](https://jlcpcb.com/partdetail/C851857) · 0 (out of stock) | UNI-ROYAL(Uniroyal Elec) `0402WGF330JTCE` [`C25105`](https://jlcpcb.com/partdetail/C25105) · 3,562,934 | Same two-terminal 0402, 33 Ω, ±5%, 62.5 mW thick-film resistor. This MPN is already used in the motion design. |
| Backplane R58, R59, R60, R61 | `RC0402FR-132K2L` | [`C4332914`](https://jlcpcb.com/partdetail/C4332914) · 0 (out of stock) | YAGEO `AC0402FR-072K2L` [`C144773`](https://jlcpcb.com/partdetail/C144773) · 211,888 | Same two-terminal 0402, 2.2 kΩ, ±1%, 62.5 mW thick-film resistor. The Yageo AC series adds AEC-Q200 qualification. |
| Backplane SW1, SW2 | `B3U-1000P` | [`C271754`](https://jlcpcb.com/partdetail/C271754) · 0 (out of stock) | Omron Electronics `B3U-1000P` [`C231329`](https://jlcpcb.com/partdetail/C231329) · 74,738 | Same Omron MPN through a different catalog listing. Same top-actuated SPST-NO contacts, 3 × 2.5 mm body, no locating boss and no ground terminal. [Omron B3U data](https://components.omron.com/system/files/2025-01/datasheet_pdf/CDMA-006.pdf) |
| Backplane Y1<br>Motion controller Y1 | `ABM8-272-T3` | [`C20625731`](https://jlcpcb.com/partdetail/C20625731) · 1 (short for two boards or order minimum) | Preorder or consign the exact crystal | Source the original 12 MHz, 10 pF crystal. One piece is below the quantity for two boards. Raspberry Pi recommends this exact crystal for the RP2350 oscillator circuit. [Raspberry Pi hardware design guide](https://pip-assets.raspberrypi.com/categories/1214-rp2350/documents/RP-008280-DS-1-hardware-design-with-rp2350.pdf?disposition=inline) |
| Motion controller C31, C35, C39 | `C0805X7R106K250NT` | [`C2835529`](https://jlcpcb.com/partdetail/C2835529) · 0 (out of stock) | Murata Electronics `GRM21BZ71E106KE15L` [`C237493`](https://jlcpcb.com/partdetail/C237493) · 74,524 | Same two-terminal 0805, 10 µF, 25 V, X7R, ±10%. Check effective capacitance at 12 V for the motor-driver bypass positions. [Murata data via its distributor](https://www.lcsc.com/product-detail/C237493.html) |
| Motion controller U1 | `RP2350B A4` | [`C9900208890`](https://jlcpcb.com/partdetail/C9900208890) · 0 (out of stock) | Raspberry Pi `RP2350B` [`C42415655`](https://jlcpcb.com/partdetail/C42415655) · 1,523 | Conditional sourcing option. This listing has the RP2350B QFN-80 pinout and 10 × 10 mm footprint. Ask JLCPCB to confirm an A4 lot before selecting it for motion U1. The explicitly named A4 listing [C50090805](https://jlcpcb.com/partdetail/C50090805) also reported zero. The exact Raspberry Pi ordering code SC1510-A4 can be quoted for [Global Sourcing](https://jlcpcb.com/help/article/pcba-parts-sourcing-instruction) or consigned. [Raspberry Pi stepping guidance](https://www.raspberrypi.com/news/rp2350-a4-rp2354-and-a-new-hacking-challenge/) |
| Motion controller U4 | `W25Q32JVSSIQ` | [`C82344`](https://jlcpcb.com/partdetail/C82344) · 0 (out of stock) | Winbond Elec `W25Q128JVSIQ` [`C97521`](https://jlcpcb.com/partdetail/C97521) · 70,827 | Same Winbond JV family, 2.7–3.6 V supply, wide 208-mil SOIC-8 with 1.27 mm pitch, and the same `/CS`, IO0–IO3, SCLK, VCC and GND pin positions. The Q variant has QE fixed to 1. This option has 16 MiB instead of 4 MiB. Keep the image in the first 4 MiB with the existing memory layout and verify programming and boot on the first assembled board. [Winbond QSPI family and datasheets](https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/) · [Winbond QE guidance](https://www.winbond.com/hq/support/faq/technical/index.html) |

Capacitor and resistor alternatives were screened for pad size, value, tolerance, and the voltage or power needed at their actual circuit positions. For the flash, the wider package suffix, I/O mapping and quad-enable behavior matter in addition to capacity. The crystal and MCU sourcing notes identify the conditions that need confirmation before an order.

## Complete BOM stock check

Each row covers all listed designators on one PCB. The minimum shown is the catalog part minimum, before the quote accounts for assembly attrition. If a project leaves the C-code blank, use the exact match in this table when reviewing the order.

### Backplane

[42 BOM rows](backplane/BOM.csv) covering 136 fitted positions.

| Designators | Manufacturer part number | Qty per PCB | Checked JLCPCB listing | Assembly stock | Part minimum |
| --- | --- | ---: | --- | ---: | ---: |
| C1, C2, C8, C9, C17, C25 | `CL31A106KBHNNNE` | 6 | [`C13585`](https://jlcpcb.com/partdetail/C13585) | 3,462,309 | 5 |
| C3, C4, C7, C10, C11, C14 | `C1608X7R1H103M080AA` | 6 | [`C3832102`](https://jlcpcb.com/partdetail/C3832102) | 0 (out of stock) | 20 |
| C5, C6, C12, C13 | `217EC0037` | 4 | [`C42371908`](https://jlcpcb.com/partdetail/C42371908) | 3,798 | 2 |
| C15, C16, C37, C38 | `C1608X7R1E105K080AB` | 4 | [`C2170660`](https://jlcpcb.com/partdetail/C2170660) | 3 (short for two boards or order minimum) | 5 |
| C18, C19, C20, C21, C22, C23, C24, C26, C27, C28, C30, C31, C33, C35, C41 | `0402B104K500HI` | 15 | — | No exact listing verified | — |
| C29, C34 | `CC0603JRNPO0BN150` | 2 | [`C327117`](https://jlcpcb.com/partdetail/C327117) | 0 (out of stock) | 20 |
| C32, C36 | `GRM155R60J475ME47D` | 2 | [`C82453`](https://jlcpcb.com/partdetail/C82453) | 414,318 | 20 |
| C39, C40 | `GRT188R61C106KE13D` | 2 | [`C711098`](https://jlcpcb.com/partdetail/C711098) | 60,174 | 5 |
| C42 | `CL05A475MO5NUNC` | 1 | [`C318563`](https://jlcpcb.com/partdetail/C318563) | 606,688 | 20 |
| D1, D3, D5, D6, D9, D10 | `KT-0603R` | 6 | [`C2286`](https://jlcpcb.com/partdetail/C2286) | 5,986,272 | 20 |
| D2, D4 | `B540C-13-F` | 2 | [`C72264`](https://jlcpcb.com/partdetail/C72264) | 79,596 | 2 |
| D7 | `TVS2700DRVR` | 1 | [`C523797`](https://jlcpcb.com/partdetail/C523797) | 276 | 2 |
| D8 | `BZT52C12` | 1 | [`C43491`](https://jlcpcb.com/partdetail/C43491) | 201,272 | 15 |
| F1 | `0451005.MRL` | 1 | [`C48467`](https://jlcpcb.com/partdetail/C48467) | 28,518 | 5 |
| J1, J2, J3 | `9001-12961C00A` | 3 | [`C5173363`](https://jlcpcb.com/partdetail/C5173363) | 1,677 | 1 |
| J4, J5, J6 | `KF128-5.08-2P-AA` | 3 | [`C474952`](https://jlcpcb.com/partdetail/C474952) | 66,306 | 2 |
| J7 | `TYPE-C-31-M-12` | 1 | [`C165948`](https://jlcpcb.com/partdetail/C165948) | 544,544 | 2 |
| J9 | `ZX-SH1.0-3PWT` | 1 | [`C7430445`](https://jlcpcb.com/partdetail/C7430445) | 90,324 | 5 |
| L1, L2 | `CDRH127/LDNP-150MC` | 2 | [`C879410`](https://jlcpcb.com/partdetail/C879410) | 2,173 | 1 |
| L3 | `AOTA-B201610S3R3-101-T` | 1 | [`C42411119`](https://jlcpcb.com/partdetail/C42411119) | 816 | 5 |
| Q1 | `DMP6023LE-13` | 1 | [`C154901`](https://jlcpcb.com/partdetail/C154901) | 3,762 | 2 |
| R1, R2, R3, R5, R7 | `CRCW060310K0FKEA` | 5 | [`C844918`](https://jlcpcb.com/partdetail/C844918) | 1,049,814 | 20 |
| R4, R9, R10, R12, R13, R14, R20, R21, R53, R54 | `RT0603FRE071K13L` | 10 | [`C863632`](https://jlcpcb.com/partdetail/C863632) | 0 (out of stock) | 10 |
| R6, R11 | `PT1206-R-070RL` | 2 | [`C858810`](https://jlcpcb.com/partdetail/C858810) | 2,650 | 5 |
| R8 | `RT0603FRE073K16L` | 1 | [`C863780`](https://jlcpcb.com/partdetail/C863780) | 0 (out of stock) | 10 |
| R15, R16 | `RC0402FR-0727RL` | 2 | [`C138021`](https://jlcpcb.com/partdetail/C138021) | 38,089 | 20 |
| R17 | `RC0603JR-071KL` | 1 | [`C14676`](https://jlcpcb.com/partdetail/C14676) | 5,397,639 | 20 |
| R18 | `RT0603FRE07330KL` | 1 | [`C863745`](https://jlcpcb.com/partdetail/C863745) | 164 | 20 |
| R19 | `CRCW0603100KFKEA` | 1 | [`C844916`](https://jlcpcb.com/partdetail/C844916) | 1,021,497 | 20 |
| R22, R23 | `RMEF0603JT5K10` | 2 | [`C6981465`](https://jlcpcb.com/partdetail/C6981465) | 0 (out of stock) | 5 |
| R24, R25 | `RNCP0603FTD100R` | 2 | [`C2479153`](https://jlcpcb.com/partdetail/C2479153) | 4,906 | 20 |
| R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R56, R57 | `AA0402JR-070RL` | 29 | [`C1882573`](https://jlcpcb.com/partdetail/C1882573) | 5,595 | 20 |
| R55 | `RC0402JR-0733RP` | 1 | [`C851857`](https://jlcpcb.com/partdetail/C851857) | 0 (out of stock) | 20 |
| R58, R59, R60, R61 | `RC0402FR-132K2L` | 4 | [`C4332914`](https://jlcpcb.com/partdetail/C4332914) | 0 (out of stock) | 20 |
| SW1, SW2 | `B3U-1000P` | 2 | [`C271754`](https://jlcpcb.com/partdetail/C271754) | 0 (out of stock) | 1 |
| U1, U2 | `TPS5450DDAR` | 2 | [`C114425`](https://jlcpcb.com/partdetail/C114425) | 16,983 | 1 |
| U3 | `AP2112K-3.3TRG1` | 1 | [`C51118`](https://jlcpcb.com/partdetail/C51118) | 5,850 | 5 |
| U4 | `USBLC6-2SC6` | 1 | [`C7519`](https://jlcpcb.com/partdetail/C7519) | 45,128 | 5 |
| U5 | `RP2350B` | 1 | [`C42415655`](https://jlcpcb.com/partdetail/C42415655) | 1,523 | 1 |
| U6 | `TPS2116DRL` | 1 | [`C3235557`](https://jlcpcb.com/partdetail/C3235557) | 64,773 | 2 |
| U7 | `W25Q128JVSIQ` | 1 | [`C97521`](https://jlcpcb.com/partdetail/C97521) | 70,827 | 1 |
| Y1 | `ABM8-272-T3` | 1 | [`C20625731`](https://jlcpcb.com/partdetail/C20625731) | 1 (short for two boards or order minimum) | 5 |

### Motion controller

[47 BOM rows](motion-controller/BOM.csv) covering 117 fitted positions.

| Designators | Manufacturer part number | Qty per PCB | Checked JLCPCB listing | Assembly stock | Part minimum |
| --- | --- | ---: | --- | ---: | ---: |
| C1, C2, C10 | `CL10A475KO8NNNC` | 3 | [`C19666`](https://jlcpcb.com/partdetail/C19666) | 3,674,026 | 20 |
| C3, C61, C63 | `CL10A106KP8NNNC` | 3 | [`C19702`](https://jlcpcb.com/partdetail/C19702) | 9,812,448 | 20 |
| C4, C6, C30, C34, C38, C59 | `CC0603KRX7R9BB104` | 6 | [`C14663`](https://jlcpcb.com/partdetail/C14663) | 36,455,496 | 20 |
| C5, C33, C37, C41 | `217EC0037` | 4 | [`C42371908`](https://jlcpcb.com/partdetail/C42371908) | 3,798 | 2 |
| C11, C12 | `GRM155R60J475ME47D` | 2 | [`C82453`](https://jlcpcb.com/partdetail/C82453) | 414,318 | 20 |
| C13, C16, C17, C18, C19, C20, C21, C22, C23, C24, C25, C26, C27, C53, C54 | `CL05B104KA5NNNC` | 15 | [`C155422`](https://jlcpcb.com/partdetail/C155422) | 290,888 | 20 |
| C14, C15 | `0402CG150J500NT` | 2 | [`C1548`](https://jlcpcb.com/partdetail/C1548) | 1,092,194 | 20 |
| C31, C35, C39 | `C0805X7R106K250NT` | 3 | [`C2835529`](https://jlcpcb.com/partdetail/C2835529) | 0 (out of stock) | 5 |
| C32, C36, C40, C60, C62, C64, C66, C67, C68 | `CL05B104KO5NNNC` | 9 | [`C1525`](https://jlcpcb.com/partdetail/C1525) | 33,113,834 | 20 |
| C65 | `CL10A105KB8NNNC` | 1 | [`C15849`](https://jlcpcb.com/partdetail/C15849) | 14,201,832 | 20 |
| D2 | `SS34` | 1 | [`C8678`](https://jlcpcb.com/partdetail/C8678) | 2,784,174 | 5 |
| D3 | `LTST-C190KGKT` | 1 | [`C125094`](https://jlcpcb.com/partdetail/C125094) | 467,321 | 20 |
| F1, F2 | `0466004.NRHF` | 2 | [`C187596`](https://jlcpcb.com/partdetail/C187596) | 14,725 | 5 |
| J1 | `9001-11961C00A` | 1 | [`C5173361`](https://jlcpcb.com/partdetail/C5173361) | 945 | 1 |
| J2 | `PH1.27-01-05PZD` | 1 | [`C41360740`](https://jlcpcb.com/partdetail/C41360740) | 2,008 | 2 |
| J3, J4, J5, J14 | `B4B-PH-K-S(LF)(SN)` | 4 | [`C131334`](https://jlcpcb.com/partdetail/C131334) | 87,012 | 2 |
| J12 | `2.54-1x6PStraight pin` | 1 | [`C37208`](https://jlcpcb.com/partdetail/C37208) | 220,371 | 2 |
| J13 | `B3B-PH-K-S(LF)(SN)` | 1 | [`C131339`](https://jlcpcb.com/partdetail/C131339) | 95,373 | 2 |
| J15 | `B5B-PH-K-S(LF)(SN)` | 1 | [`C157993`](https://jlcpcb.com/partdetail/C157993) | 54,747 | 2 |
| J16, J17 | `B2B-PH-K-S(LF)(SN)` | 2 | [`C131337`](https://jlcpcb.com/partdetail/C131337) | 292,390 | 2 |
| J18 | `TYPE-C-31-M-12` | 1 | [`C165948`](https://jlcpcb.com/partdetail/C165948) | 544,544 | 2 |
| J19 | `PH1.27-01-04PZD` | 1 | [`C41360739`](https://jlcpcb.com/partdetail/C41360739) | 597 | 2 |
| L2 | `DFE252012F-3R3M=P2` | 1 | [`C2041573`](https://jlcpcb.com/partdetail/C2041573) | 2,220 | 5 |
| Q1, Q2 | `AO3400A` | 2 | [`C20917`](https://jlcpcb.com/partdetail/C20917) | 1,045,156 | 5 |
| R1, R42, R44, R50 | `0603WAF1003T5E` | 4 | [`C25803`](https://jlcpcb.com/partdetail/C25803) | 15,153,090 | 20 |
| R2 | `0603WAF2202T5E` | 1 | [`C31850`](https://jlcpcb.com/partdetail/C31850) | 2,471,687 | 20 |
| R3, R4 | `0603WAF1000T5E` | 2 | [`C22775`](https://jlcpcb.com/partdetail/C22775) | 9,929,485 | 20 |
| R5, R6 | `0603WAF0000T5E` | 2 | [`C21189`](https://jlcpcb.com/partdetail/C21189) | 17,731,393 | 20 |
| R7, R8 | `RC0201FR-0727RL` | 2 | [`C273268`](https://jlcpcb.com/partdetail/C273268) | 30,006 | 20 |
| R9, R36 | `0603WAF1001T5E` | 2 | [`C21190`](https://jlcpcb.com/partdetail/C21190) | 28,778,587 | 20 |
| R10, R52, R53, R54, R55, R56 | `0402WGF330JTCE` | 6 | [`C25105`](https://jlcpcb.com/partdetail/C25105) | 3,562,934 | 20 |
| R11, R13 | `0402WGF1002TCE` | 2 | [`C25744`](https://jlcpcb.com/partdetail/C25744) | 22,051,180 | 20 |
| R12, R14 | `0402WGF1001TCE` | 2 | [`C11702`](https://jlcpcb.com/partdetail/C11702) | 31,963,937 | 20 |
| R20, R21, R34, R35, R40, R45, R46 | `0603WAF1002T5E` | 7 | [`C25804`](https://jlcpcb.com/partdetail/C25804) | 42,780,380 | 20 |
| R41, R43 | `0603WAF330JT5E` | 2 | [`C23140`](https://jlcpcb.com/partdetail/C23140) | 3,399,257 | 20 |
| R47 | `0603WAF1004T5E` | 1 | [`C22935`](https://jlcpcb.com/partdetail/C22935) | 3,896,131 | 20 |
| R48, R49 | `0603WAF5101T5E` | 2 | [`C23186`](https://jlcpcb.com/partdetail/C23186) | 19,558,204 | 20 |
| R51 | `0603WAF1503T5E` | 1 | [`C22807`](https://jlcpcb.com/partdetail/C22807) | 975,249 | 20 |
| SW1, SW2 | `TL3305AF160QG` | 2 | [`C2886899`](https://jlcpcb.com/partdetail/C2886899) | 128 | 2 |
| U1 | `RP2350B A4` | 1 | [`C9900208890`](https://jlcpcb.com/partdetail/C9900208890) | 0 (out of stock) | 1 |
| U2 | `AP2112M-3.3TRG1` | 1 | [`C5290219`](https://jlcpcb.com/partdetail/C5290219) | 2,486 | 1 |
| U4 | `W25Q32JVSSIQ` | 1 | [`C82344`](https://jlcpcb.com/partdetail/C82344) | 0 (out of stock) | 1 |
| U5, U6, U7 | `TB6612FNG(O,C,8,EL` | 3 | [`C88224`](https://jlcpcb.com/partdetail/C88224) | 2,898 | 1 |
| U9, U10 | `DRV8837CDSGR` | 2 | [`C191000`](https://jlcpcb.com/partdetail/C191000) | 56,230 | 5 |
| U11 | `TC4427AEOA` | 1 | [`C18690`](https://jlcpcb.com/partdetail/C18690) | 160 | 1 |
| U12 | `USBLC6-2SC6` | 1 | [`C7519`](https://jlcpcb.com/partdetail/C7519) | 45,128 | 5 |
| Y1 | `ABM8-272-T3` | 1 | [`C20625731`](https://jlcpcb.com/partdetail/C20625731) | 1 (short for two boards or order minimum) | 5 |

### Slot-mounted encoder splitter

[6 BOM rows](encoder-splitter/BOM.csv) covering 11 fitted positions.

| Designators | Manufacturer part number | Qty per PCB | Checked JLCPCB listing | Assembly stock | Part minimum |
| --- | --- | ---: | --- | ---: | ---: |
| C1, C2 | `CL10A475KO8NNNC` | 2 | [`C19666`](https://jlcpcb.com/partdetail/C19666) | 3,674,026 | 20 |
| C3 | `CL10A106KP8NNNC` | 1 | [`C19702`](https://jlcpcb.com/partdetail/C19702) | 9,812,448 | 20 |
| J1, J2, J3 | `B6B-PH-K-S(LF)(SN)` | 3 | [`C131342`](https://jlcpcb.com/partdetail/C131342) | 547 | 2 |
| J4 | `9001-11961C00A` | 1 | [`C5173361`](https://jlcpcb.com/partdetail/C5173361) | 945 | 1 |
| R1, R2, R3 | `0603WAF1002T5E` | 3 | [`C25804`](https://jlcpcb.com/partdetail/C25804) | 42,780,380 | 20 |
| U1 | `AP2112M-3.3TRG1` | 1 | [`C5290219`](https://jlcpcb.com/partdetail/C5290219) | 2,486 | 1 |
