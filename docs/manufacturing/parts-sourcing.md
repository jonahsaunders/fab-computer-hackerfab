# JLCPCB BOM stock and manual replacements

**Stock snapshot November 12, 2026, 11:39:43–11:40:05 EST.** Counts came from JLCPCB’s public assembly catalog. The three BOMs share this inventory pool. Confirm the current quantities in your quote. [JLCPCB matching guidance](https://jlcpcb.com/help/article/component-matching-guidelines-for-pcba-orders)

The shared DIN96 plug `C5173361` and flash `C97521` were rechecked at 12:32:43 EST on November 12.

**Need for 5** estimates one five-PCB order per board. It is the greater of the catalog minimum or the fitted quantity plus the catalog spare count. The quote determines the final quantity. The checked listing uses the project’s C-code when specified, or an exact catalog match for the original part. The TPS2116DRL listing uses TI’s orderable tape-and-reel suffix `TPS2116DRLR`. [TI ordering information](https://www.ti.com/product/TPS2116/part-details/TPS2116DRLR)

For JLCPCB assembly, use the search icon on the matching row and enter the C-code listed for that designator. For parts you plan to solder yourself, leave those rows unselected in the assembly quote and buy the exact MPN shown. The [manufacturing guide](README.md) links to the original KiCad BOMs and placement files.

[Backplane](#backplane) · [Motion controller](#motion-controller) · [Slot-mounted encoder splitter](#slot-mounted-encoder-splitter)

## Backplane

[Original KiCad BOM CSV](backplane/BOM.csv) for 136 fitted positions.

### Manual entries for shortages

| Designators | Original part and listing | Original stock / need for 5 | Enter or source this part | Alternate stock / need for 5 | Compatibility |
| --- | --- | --- | --- | ---: | --- |
| C3, C4, C7, C10, C11, C14 | `C1608X7R1H103M080AA` [`C3832102`](https://jlcpcb.com/partdetail/C3832102) | 0 / 36 | [`C1589`](https://jlcpcb.com/partdetail/C1589) · Samsung Electro-Mechanics `CL10B103KB8NNNC` | 1,644,654 / 46 | Same two-terminal 0603 land pattern, 10 nF, 50 V, X7R. ±10% tightens the original ±20%. [TDK original](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1H103M080AA) |
| C15, C16, C37, C38 | `C1608X7R1E105K080AB` [`C2170660`](https://jlcpcb.com/partdetail/C2170660) | 3 / 22 | [`C701259`](https://jlcpcb.com/partdetail/C701259) · Murata Electronics `GRT188R71E105KE13D` | 4,812 / 24 | Same two-terminal 0603, 1 µF, 25 V, X7R, ±10% for the 3.3 V and 5 V rail bypass positions. TDK identifies [`C2167089`](https://jlcpcb.com/partdetail/C2167089) as an automotive equivalent. That listing showed 4 in stock and needs 22 for five boards. [TDK original](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1E105K080AB) |
| C18, C19, C20, C21, C22, C23, C24, C26, C27, C28, C30, C31, C33, C35, C41 | `0402B104K500HI`  | Exact listing unverified / 75 | [`C152814`](https://jlcpcb.com/partdetail/C152814) · Walsin Tech Corp `0402B104K500CT` | 739,623 / 85 | Same two-terminal 0402, 100 nF, 50 V, X7R, ±10%. [NextGen original](https://www.nextgencomponent.com/uploads/soft/20241220/1-2412201F0061O.pdf) |
| C29, C34 | `CC0603JRNPO0BN150` [`C327117`](https://jlcpcb.com/partdetail/C327117) | 0 / 20 | [`C1644`](https://jlcpcb.com/partdetail/C1644) · Samsung Electro-Mechanics `CL10C150JB8NNNC` | 1,042,822 / 20 | Same two-terminal 0603, 15 pF, C0G, ±5%. The 50 V rating covers the 3.3 V crystal circuit. Fit both C29 and C34 with the same part. The 100 V option [`C472783`](https://jlcpcb.com/partdetail/C472783) showed 13 in stock and needs 20 for five boards. |
| R4, R9, R10, R12, R13, R14, R20, R21, R53, R54 | `RT0603FRE071K13L` [`C863632`](https://jlcpcb.com/partdetail/C863632) | 0 / 55 | [`C861190`](https://jlcpcb.com/partdetail/C861190) · YAGEO `RT0603BRD071K13L` | 3,214 / 58 | Same Yageo RT thin-film 0603 package, 1.13 kΩ, 100 mW. The ±0.1% tolerance and ±25 ppm/°C TCR are tighter than the original. [Yageo RT series data](https://datasheet.lcsc.com/datasheet/pdf/46d7760c582640714d605308a25a220a.pdf?productCode=C728599) |
| R8 | `RT0603FRE073K16L` [`C863780`](https://jlcpcb.com/partdetail/C863780) | 0 / 10 | [`C326747`](https://jlcpcb.com/partdetail/C326747) · YAGEO `RT0603BRE073K16L` | 1,927 / 20 | Same Yageo RT thin-film 0603 package, 3.16 kΩ, 100 mW and ±50 ppm/°C TCR. The ±0.1% tolerance is tighter than the original ±1%. [Yageo RT series data](https://datasheet.lcsc.com/datasheet/pdf/46d7760c582640714d605308a25a220a.pdf?productCode=C728599) |
| R22, R23 | `RMEF0603JT5K10` [`C6981465`](https://jlcpcb.com/partdetail/C6981465) | 0 / 15 | [`C144594`](https://jlcpcb.com/partdetail/C144594) · YAGEO `AC0603JR-075K1L` | 1,292 / 20 | Same two-terminal 0603, 5.1 kΩ, ±5%, 100 mW, AEC-Q200 thick-film resistor for the USB-C CC pull-downs. |
| R55 | `RC0402JR-0733RP` [`C851857`](https://jlcpcb.com/partdetail/C851857) | 0 / 20 | [`C25105`](https://jlcpcb.com/partdetail/C25105) · UNI-ROYAL(Uniroyal Elec) `0402WGF330JTCE` | 3,585,480 / 20 | Same two-terminal 0402, 33 Ω, ±5%, 62.5 mW thick-film resistor. This MPN is already used in the motion design. |
| R58, R59, R60, R61 | `RC0402FR-132K2L` [`C4332914`](https://jlcpcb.com/partdetail/C4332914) | 0 / 30 | [`C144773`](https://jlcpcb.com/partdetail/C144773) · YAGEO `AC0402FR-072K2L` | 211,888 / 30 | Same two-terminal 0402, 2.2 kΩ, ±1%, 62.5 mW thick-film resistor. The Yageo AC series adds AEC-Q200 qualification. |
| SW1, SW2 | `B3U-1000P` [`C271754`](https://jlcpcb.com/partdetail/C271754) | 0 / 10 | [`C231329`](https://jlcpcb.com/partdetail/C231329) · Omron Electronics `B3U-1000P` | 74,642 / 12 | Same Omron MPN through a different catalog listing. Same top-actuated SPST-NO contacts, 3 × 2.5 mm body, no locating boss and no ground terminal. [Omron B3U data](https://components.omron.com/system/files/2025-01/datasheet_pdf/CDMA-006.pdf) |
| Y1 | `ABM8-272-T3` [`C20625731`](https://jlcpcb.com/partdetail/C20625731) | 1 / 5 | Preorder or hand-fit the exact `ABM8-272-T3` | — | Raspberry Pi recommends this exact 12 MHz, 10 pF crystal for the oscillator. Source the exact part to keep the reference design’s specified crystal and load capacitance. [RP2350 hardware design guide](https://pip-assets.raspberrypi.com/categories/1214-rp2350/documents/RP-008280-DS-1-hardware-design-with-rp2350.pdf?disposition=inline) |

### Detailed BOM and assembly stock

| Designators | Manufacturer part number | KiCad value | KiCad footprint | Qty per PCB | Checked JLCPCB listing | In stock | Need for 5 |
| --- | --- | --- | --- | ---: | --- | ---: | ---: |
| C1, C2, C8, C9, C17, C25 | `CL31A106KBHNNNE` | 10u 50V | `C_1206_3216Metric` | 6 | [`C13585`](https://jlcpcb.com/partdetail/C13585) | 3,475,143 | 34 |
| C3, C4, C7, C10, C11, C14 | `C1608X7R1H103M080AA` | 10n 50V | `C_0603_1608Metric` | 6 | [`C3832102`](https://jlcpcb.com/partdetail/C3832102) | 0 | 36 |
| C5, C6, C12, C13 | `217EC0037` | 220u 25V | `CP_Elec_6.3x7.7` | 4 | [`C42371908`](https://jlcpcb.com/partdetail/C42371908) | 3,795 | 20 |
| C15, C16, C37, C38 | `C1608X7R1E105K080AB` | 1u 25V | `C_0603_1608Metric` | 4 | [`C2170660`](https://jlcpcb.com/partdetail/C2170660) | 3 | 22 |
| C18, C19, C20, C21, C22, C23, C24, C26, C27, C28, C30, C31, C33, C35, C41 | `0402B104K500HI` | 100n 50V | `C_0402_1005Metric` | 15 | — | Exact listing unverified | 75 |
| C29, C34 | `CC0603JRNPO0BN150` | 15p 100V | `C_0603_1608Metric` | 2 | [`C327117`](https://jlcpcb.com/partdetail/C327117) | 0 | 20 |
| C32, C36 | `GRM155R60J475ME47D` | 4u7 6V3 | `C_0402_1005Metric_VREG` | 2 | [`C82453`](https://jlcpcb.com/partdetail/C82453) | 414,218 | 20 |
| C39, C40 | `GRT188R61C106KE13D` | 10u 16V | `C_0603_1608Metric` | 2 | [`C711098`](https://jlcpcb.com/partdetail/C711098) | 60,168 | 12 |
| C42 | `CL05A475MO5NUNC` | 4u7 16V | `C_0402_1005Metric` | 1 | [`C318563`](https://jlcpcb.com/partdetail/C318563) | 606,688 | 20 |
| D1, D3, D5, D6, D9, D10 | `KT-0603R` | KT-0603R | `LED_0603_1608Metric` | 6 | [`C2286`](https://jlcpcb.com/partdetail/C2286) | 5,986,031 | 40 |
| D2, D4 | `B540C-13-F` | B540C-13-F | `D_SMC` | 2 | [`C72264`](https://jlcpcb.com/partdetail/C72264) | 79,596 | 12 |
| D7 | `TVS2700DRVR` | TVS2700DRVR | `WSON-6_TVS2700DRV_2x2mm` | 1 | [`C523797`](https://jlcpcb.com/partdetail/C523797) | 276 | 5 |
| D8 | `BZT52C12` | BZT52C12 12V | `D_SOD-123` | 1 | [`C43491`](https://jlcpcb.com/partdetail/C43491) | 201,290 | 15 |
| F1 | `0451005.MRL` | 5A 125V | `Fuse_Littelfuse-NANO2-451_453` | 1 | [`C48467`](https://jlcpcb.com/partdetail/C48467) | 28,518 | 7 |
| J1, J2, J3 | `9001-12961C00A` | 9001-12961C00A | `WingTAT_9001-12961C00A_DIN41612_C_3x32_Vertical` | 3 | [`C5173363`](https://jlcpcb.com/partdetail/C5173363) | 1,677 | 15 |
| J4, J5, J6 | `KF128-5.08-2P-AA` | KF128-5.08-2P-AA | `KF128-5.08-2P-AA` | 3 | [`C474952`](https://jlcpcb.com/partdetail/C474952) | 66,103 | 15 |
| J7 | `TYPE-C-31-M-12` | TYPE-C-31-M-12 | `USB_C_Receptacle_HRO_TYPE-C-31-M-12` | 1 | [`C165948`](https://jlcpcb.com/partdetail/C165948) | 544,500 | 5 |
| J9 | `ZX-SH1.0-3PWT` | ZX-SH1.0-3PWT | `Megastar_ZX-SH1.0-3PWT_1x03_P1.00mm_Horizontal` | 1 | [`C7430445`](https://jlcpcb.com/partdetail/C7430445) | 90,324 | 9 |
| L1, L2 | `CDRH127/LDNP-150MC` | 15uH | `L_Sumida_CDRH127_LD_12.0x12.0mm` | 2 | [`C879410`](https://jlcpcb.com/partdetail/C879410) | 2,173 | 10 |
| L3 | `AOTA-B201610S3R3-101-T` | 3u3 | `L_Abracon_AOTA-B201610S3R3-101-T` | 1 | [`C42411119`](https://jlcpcb.com/partdetail/C42411119) | 816 | 6 |
| Q1 | `DMP6023LE-13` | DMP6023LE-13 | `SOT-223-3_TabPin4` | 1 | [`C154901`](https://jlcpcb.com/partdetail/C154901) | 3,762 | 5 |
| R1, R2, R3, R5, R7 | `CRCW060310K0FKEA` | 10k | `R_0603_1608Metric` | 5 | [`C844918`](https://jlcpcb.com/partdetail/C844918) | 1,049,814 | 35 |
| R4, R9, R10, R12, R13, R14, R20, R21, R53, R54 | `RT0603FRE071K13L` | 1k13 | `R_0603_1608Metric` | 10 | [`C863632`](https://jlcpcb.com/partdetail/C863632) | 0 | 55 |
| R6, R11 | `PT1206-R-070RL` | 0R | `R_1206_3216Metric` | 2 | [`C858810`](https://jlcpcb.com/partdetail/C858810) | 2,650 | 14 |
| R8 | `RT0603FRE073K16L` | 3k16 | `R_0603_1608Metric` | 1 | [`C863780`](https://jlcpcb.com/partdetail/C863780) | 0 | 10 |
| R15, R16 | `RC0402FR-0727RL` | 27R | `R_0402_1005Metric` | 2 | [`C138021`](https://jlcpcb.com/partdetail/C138021) | 38,089 | 22 |
| R17 | `RC0603JR-071KL` | 1k | `R_0603_1608Metric` | 1 | [`C14676`](https://jlcpcb.com/partdetail/C14676) | 5,397,474 | 20 |
| R18 | `RT0603FRE07330KL` | 330k | `R_0603_1608Metric` | 1 | [`C863745`](https://jlcpcb.com/partdetail/C863745) | 164 | 20 |
| R19 | `CRCW0603100KFKEA` | 100k | `R_0603_1608Metric` | 1 | [`C844916`](https://jlcpcb.com/partdetail/C844916) | 1,021,497 | 20 |
| R22, R23 | `RMEF0603JT5K10` | 5k1 | `R_0603_1608Metric` | 2 | [`C6981465`](https://jlcpcb.com/partdetail/C6981465) | 0 | 15 |
| R24, R25 | `RNCP0603FTD100R` | 100R | `R_0603_1608Metric` | 2 | [`C2479153`](https://jlcpcb.com/partdetail/C2479153) | 4,906 | 20 |
| R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38, R39, R40, R41, R42, R43, R44, R45, R46, R47, R48, R49, R50, R51, R52, R56, R57 | `AA0402JR-070RL` | 0R | `R_0402_1005Metric` | 29 | [`C1882573`](https://jlcpcb.com/partdetail/C1882573) | 5,595 | 153 |
| R55 | `RC0402JR-0733RP` | 33R | `R_0402_1005Metric` | 1 | [`C851857`](https://jlcpcb.com/partdetail/C851857) | 0 | 20 |
| R58, R59, R60, R61 | `RC0402FR-132K2L` | 2k2 | `R_0402_1005Metric` | 4 | [`C4332914`](https://jlcpcb.com/partdetail/C4332914) | 0 | 30 |
| SW1, SW2 | `B3U-1000P` | — | `B3U-1000P` | 2 | [`C271754`](https://jlcpcb.com/partdetail/C271754) | 0 | 10 |
| U1, U2 | `TPS5450DDAR` | TPS5450DDAR | `Texas_HSOP-8-1EP_3.9x4.9mm_P1.27mm` | 2 | [`C114425`](https://jlcpcb.com/partdetail/C114425) | 16,983 | 10 |
| U3 | `AP2112K-3.3TRG1` | AP2112K-3.3TRG1 | `SOT-23-5` | 1 | [`C51118`](https://jlcpcb.com/partdetail/C51118) | 5,845 | 5 |
| U4 | `USBLC6-2SC6` | USBLC6-2SC6 | `SOT-23-6` | 1 | [`C7519`](https://jlcpcb.com/partdetail/C7519) | 45,081 | 7 |
| U5 | `RP2350B` | RP2350B | `QFN-80-1EP_10x10mm_P0.4mm_EP3.4x3.4mm` | 1 | [`C42415655`](https://jlcpcb.com/partdetail/C42415655) | 1,523 | 5 |
| U6 | `TPS2116DRL` | TPS2116DRL | `SOT-583-8` | 1 | [`C3235557`](https://jlcpcb.com/partdetail/C3235557) | 65,135 | 5 |
| U7 | `W25Q128JVSIQ` | W25Q128JVSIQ | `W25Q128JVSIQ_SOIC-8_5.3x5.3mm_P1.27mm` | 1 | [`C97521`](https://jlcpcb.com/partdetail/C97521) | 70,815 | 5 |
| Y1 | `ABM8-272-T3` | 12MHz | `generic_xtalcc320x250x80-4` | 1 | [`C20625731`](https://jlcpcb.com/partdetail/C20625731) | 1 | 5 |

## Motion controller

[Original KiCad BOM CSV](motion-controller/BOM.csv) for 117 fitted positions.

### Manual entries for shortages

| Designators | Original part and listing | Original stock / need for 5 | Enter or source this part | Alternate stock / need for 5 | Compatibility |
| --- | --- | --- | --- | ---: | --- |
| C31, C35, C39 | `C0805X7R106K250NT` [`C2835529`](https://jlcpcb.com/partdetail/C2835529) | 0 / 17 | [`C237493`](https://jlcpcb.com/partdetail/C237493) · Murata Electronics `GRM21BZ71E106KE15L` | 74,524 / 17 | Same two-terminal 0805, 10 µF, 25 V, X7R, ±10%. Check effective capacitance at 12 V for the motor-driver bypass positions. [Murata data via its distributor](https://www.lcsc.com/product-detail/C237493.html) |
| U1 | `RP2350B A4` [`C9900208890`](https://jlcpcb.com/partdetail/C9900208890) | 0 / 5 | [`C42415655`](https://jlcpcb.com/partdetail/C42415655) · Raspberry Pi `RP2350B` · confirm A4 lot first | 1,523 / 5 | Conditional sourcing option. This listing has the RP2350B QFN-80 pinout and 10 × 10 mm footprint. Ask JLCPCB to confirm an A4 lot before selecting it for motion U1. The explicitly named A4 listing [C50090805](https://jlcpcb.com/partdetail/C50090805) also reported zero. The exact Raspberry Pi ordering code SC1510-A4 can be quoted for [Global Sourcing](https://jlcpcb.com/help/article/pcba-parts-sourcing-instruction) or consigned. [Raspberry Pi stepping guidance](https://www.raspberrypi.com/news/rp2350-a4-rp2354-and-a-new-hacking-challenge/) |
| Y1 | `ABM8-272-T3` [`C20625731`](https://jlcpcb.com/partdetail/C20625731) | 1 / 5 | Preorder or hand-fit the exact `ABM8-272-T3` | — | Raspberry Pi recommends this exact 12 MHz, 10 pF crystal for the oscillator. Source the exact part to keep the reference design’s specified crystal and load capacitance. [RP2350 hardware design guide](https://pip-assets.raspberrypi.com/categories/1214-rp2350/documents/RP-008280-DS-1-hardware-design-with-rp2350.pdf?disposition=inline) |

### Motion controller U4 flash

Motion U4 now specifies Winbond `W25Q128JVSIQ` (`C97521`) in KiCad and the assembly BOM. It is the same part as backplane U7. JLCPCB showed **70,815** in assembly stock at the recheck. [JLCPCB listing](https://jlcpcb.com/partdetail/C97521)

The device uses a wide 208-mil SOIC-8 body, 1.27 mm lead pitch and a 2.7–3.6 V supply. It fits the existing motion-card lands and preserves all eight signal connections. [Winbond specifications](https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/w25q-jv/?__locale=en&partNo=W25Q128JVSIQ)

| Pin | Winbond function | Motion U4 and backplane U7 |
| ---: | --- | --- |
| 1 | `/CS` | QSPI chip select |
| 2 | `IO1` | QSPI data 1 |
| 3 | `IO2` | QSPI data 2 |
| 4 | `GND` | Ground |
| 5 | `IO0` | QSPI data 0 |
| 6 | `CLK` | QSPI clock |
| 7 | `IO3` | QSPI data 3 |
| 8 | `VCC` | 3.3 V |

The device provides **16 MiB** and reports JEDEC ID `EF 40 18`. Configure the target for 16 MiB before using the full address space. Verify that the programmer recognizes the ID and that the first board boots. [Winbond W25Q128JV documentation](https://www.winbond.com/hq/support/documentation/?__locale=en&category=%2F.categories%2Fresources%2Fdatasheet%2F&family=%2Fproduct%2Fcode-storage-flash%2Fserial-nor-flash%2Findex.html&line=%2Fproduct%2Fcode-storage-flash%2Findex.html&pno=W25Q128JV)

### Detailed BOM and assembly stock

| Designators | Manufacturer part number | KiCad value | KiCad footprint | Qty per PCB | Checked JLCPCB listing | In stock | Need for 5 |
| --- | --- | --- | --- | ---: | --- | ---: | ---: |
| C1, C2, C10 | `CL10A475KO8NNNC` | 4.7uF 16V X5R | `C_0603_1608Metric` | 3 | [`C19666`](https://jlcpcb.com/partdetail/C19666) | 3,674,982 | 25 |
| C3, C61, C63 | `CL10A106KP8NNNC` | 10uF 10V X5R | `C_0603_1608Metric` | 3 | [`C19702`](https://jlcpcb.com/partdetail/C19702) | 9,821,462 | 25 |
| C4, C6, C30, C34, C38, C59 | `CC0603KRX7R9BB104` | 100nF 50V | `C_0603_1608Metric` | 6 | [`C14663`](https://jlcpcb.com/partdetail/C14663) | 36,461,209 | 45 |
| C5, C33, C37, C41 | `217EC0037` | 220uF 25V | `CP_Elec_6.3x7.7` | 4 | [`C42371908`](https://jlcpcb.com/partdetail/C42371908) | 3,795 | 20 |
| C11, C12 | `GRM155R60J475ME47D` | 4.7uF 6.3V X5R | `C_0402_RP2350_Regulator` | 2 | [`C82453`](https://jlcpcb.com/partdetail/C82453) | 414,218 | 20 |
| C13, C16, C17, C18, C19, C20, C21, C22, C23, C24, C25, C26, C27, C53, C54 | `CL05B104KA5NNNC` | 100nF 25V | `C_0402_1005Metric` | 15 | [`C155422`](https://jlcpcb.com/partdetail/C155422) | 290,962 | 89 |
| C14, C15 | `0402CG150J500NT` | 15pF C0G | `C_0402_1005Metric` | 2 | [`C1548`](https://jlcpcb.com/partdetail/C1548) | 1,095,157 | 20 |
| C31, C35, C39 | `C0805X7R106K250NT` | 10uF 25V X7R | `C_0805_2012Metric` | 3 | [`C2835529`](https://jlcpcb.com/partdetail/C2835529) | 0 | 17 |
| C32, C36, C40, C60, C62, C64, C66, C67, C68 | `CL05B104KO5NNNC` | 100nF 16V | `C_0402_1005Metric` | 9 | [`C1525`](https://jlcpcb.com/partdetail/C1525) | 33,153,908 | 60 |
| C65 | `CL10A105KB8NNNC` | 1uF 50V X5R | `C_0603_1608Metric` | 1 | [`C15849`](https://jlcpcb.com/partdetail/C15849) | 14,215,200 | 20 |
| D2 | `SS34` | SS34 | `D_SMA` | 1 | [`C8678`](https://jlcpcb.com/partdetail/C8678) | 2,784,347 | 13 |
| D3 | `LTST-C190KGKT` | STATUS | `LED_0603_1608Metric` | 1 | [`C125094`](https://jlcpcb.com/partdetail/C125094) | 467,402 | 20 |
| F1, F2 | `0466004.NRHF` | 4A 32V | `Fuse_Littelfuse_0466_1206` | 2 | [`C187596`](https://jlcpcb.com/partdetail/C187596) | 14,725 | 12 |
| J1 | `9001-11961C00A` | DIN96 / male right-angle | `DIN96_Male_Horizontal` | 1 | [`C5173361`](https://jlcpcb.com/partdetail/C5173361) | 945 | 5 |
| J2 | `PH1.27-01-05PZD` | SWD / RP2350 | `PinHeader_1x05_P1.27mm_Vertical` | 1 | [`C41360740`](https://jlcpcb.com/partdetail/C41360740) | 2,008 | 5 |
| J3, J4, J5, J14 | `B4B-PH-K-S(LF)(SN)` | MOTOR 1 / MOTOR 2 / MOTOR 3 / ROTATION MOTOR | `JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical` | 4 | [`C131334`](https://jlcpcb.com/partdetail/C131334) | 87,018 | 21 |
| J12 | `2.54-1x6PStraight pin` | ROTATION ENCODER | `PinHeader_1x06_P2.54mm_Vertical` | 1 | [`C37208`](https://jlcpcb.com/partdetail/C37208) | 220,371 | 5 |
| J13 | `B3B-PH-K-S(LF)(SN)` | ENDSTOP | `JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical` | 1 | [`C131339`](https://jlcpcb.com/partdetail/C131339) | 95,353 | 6 |
| J15 | `B5B-PH-K-S(LF)(SN)` | HEATER + TEMP | `JST_PH_B5B-PH-K_1x05_P2.00mm_Vertical` | 1 | [`C157993`](https://jlcpcb.com/partdetail/C157993) | 54,752 | 5 |
| J16, J17 | `B2B-PH-K-S(LF)(SN)` | VACUUM / 5 V / THERMAL CUTOFF | `JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical` | 2 | [`C131337`](https://jlcpcb.com/partdetail/C131337) | 292,370 | 11 |
| J18 | `TYPE-C-31-M-12` | USB-C / SERVICE | `USB_C_Receptacle_HRO_TYPE-C-31-M-12` | 1 | [`C165948`](https://jlcpcb.com/partdetail/C165948) | 544,500 | 5 |
| J19 | `PH1.27-01-04PZD` | TOOL PWM | `PinHeader_1x04_P1.27mm_Vertical` | 1 | [`C41360739`](https://jlcpcb.com/partdetail/C41360739) | 597 | 6 |
| L2 | `DFE252012F-3R3M=P2` | 3.3uH | `L_Murata_DFE252012F_2.5x2.0mm` | 1 | [`C2041573`](https://jlcpcb.com/partdetail/C2041573) | 2,220 | 7 |
| Q1, Q2 | `AO3400A` | AO3400A | `SOT-23` | 2 | [`C20917`](https://jlcpcb.com/partdetail/C20917) | 1,044,774 | 14 |
| R1, R42, R44, R50 | `0603WAF1003T5E` | 100kR 1% / 100kR | `R_0603_1608Metric` | 4 | [`C25803`](https://jlcpcb.com/partdetail/C25803) | 15,164,359 | 30 |
| R2 | `0603WAF2202T5E` | 22kR 1% | `R_0603_1608Metric` | 1 | [`C31850`](https://jlcpcb.com/partdetail/C31850) | 2,472,282 | 20 |
| R3, R4 | `0603WAF1000T5E` | 100R | `R_0603_1608Metric` | 2 | [`C22775`](https://jlcpcb.com/partdetail/C22775) | 9,928,457 | 20 |
| R5, R6 | `0603WAF0000T5E` | 0R | `R_0603_1608Metric` | 2 | [`C21189`](https://jlcpcb.com/partdetail/C21189) | 17,747,168 | 20 |
| R7, R8 | `RC0201FR-0727RL` | 27R | `R_0201_Yageo_Reflow` | 2 | [`C273268`](https://jlcpcb.com/partdetail/C273268) | 30,006 | 20 |
| R9, R36 | `0603WAF1001T5E` | 1kR | `R_0603_1608Metric` | 2 | [`C21190`](https://jlcpcb.com/partdetail/C21190) | 28,780,068 | 20 |
| R10, R52, R53, R54, R55, R56 | `0402WGF330JTCE` | 33R | `R_0402_1005Metric` | 6 | [`C25105`](https://jlcpcb.com/partdetail/C25105) | 3,585,480 | 45 |
| R11, R13 | `0402WGF1002TCE` | 10kR | `R_0402_1005Metric` | 2 | [`C25744`](https://jlcpcb.com/partdetail/C25744) | 22,064,260 | 25 |
| R12, R14 | `0402WGF1001TCE` | 1kR | `R_0402_1005Metric` | 2 | [`C11702`](https://jlcpcb.com/partdetail/C11702) | 31,991,958 | 20 |
| R20, R21, R34, R35, R40, R45, R46 | `0603WAF1002T5E` | 10kR | `R_0603_1608Metric` | 7 | [`C25804`](https://jlcpcb.com/partdetail/C25804) | 42,823,804 | 45 |
| R41, R43 | `0603WAF330JT5E` | 33R | `R_0603_1608Metric` | 2 | [`C23140`](https://jlcpcb.com/partdetail/C23140) | 3,401,871 | 20 |
| R47 | `0603WAF1004T5E` | 1MR | `R_0603_1608Metric` | 1 | [`C22935`](https://jlcpcb.com/partdetail/C22935) | 3,896,202 | 20 |
| R48, R49 | `0603WAF5101T5E` | 5.1kR 1% | `R_0603_1608Metric` | 2 | [`C23186`](https://jlcpcb.com/partdetail/C23186) | 19,560,403 | 20 |
| R51 | `0603WAF1503T5E` | 150kR 1% | `R_0603_1608Metric` | 1 | [`C22807`](https://jlcpcb.com/partdetail/C22807) | 975,169 | 20 |
| SW1, SW2 | `TL3305AF160QG` | RESET / BOOTSEL | `SW_SPST_TL3305A` | 2 | [`C2886899`](https://jlcpcb.com/partdetail/C2886899) | 128 | 10 |
| U1 | `RP2350B A4` | RP2350B | `QFN-80-1EP_10x10mm_P0.4mm_EP3.4x3.4mm` | 1 | [`C9900208890`](https://jlcpcb.com/partdetail/C9900208890) | 0 | 5 |
| U2 | `AP2112M-3.3TRG1` | AP2112M-3.3TRG1 | `SOIC-8_3.9x4.9mm_P1.27mm` | 1 | [`C5290219`](https://jlcpcb.com/partdetail/C5290219) | 2,486 | 5 |
| U4 | `W25Q128JVSIQ` | W25Q128JVSIQ / 16 MiB | `SOIC-8_5.3x5.3mm_P1.27mm` | 1 | [`C97521`](https://jlcpcb.com/partdetail/C97521) | 70,815 | 5 |
| U5, U6, U7 | `TB6612FNG(O,C,8,EL` | TB6612FNG | `SSOP-24_Toshiba_5.6x7.8mm_P0.65mm` | 3 | [`C88224`](https://jlcpcb.com/partdetail/C88224) | 2,893 | 15 |
| U9, U10 | `DRV8837CDSGR` | DRV8837CDSGR | `Texas_DSG0008A_WSON-8-1EP_2x2mm_P0.5mm_EP0.9x1.6mm` | 2 | [`C191000`](https://jlcpcb.com/partdetail/C191000) | 56,230 | 14 |
| U11 | `TC4427AEOA` | TC4427AEOA | `SOIC-8_3.9x4.9mm_P1.27mm` | 1 | [`C18690`](https://jlcpcb.com/partdetail/C18690) | 160 | 5 |
| U12 | `USBLC6-2SC6` | USBLC6-2SC6 | `SOT-23-6` | 1 | [`C7519`](https://jlcpcb.com/partdetail/C7519) | 45,081 | 7 |
| Y1 | `ABM8-272-T3` | 12MHz / 10pF | `Crystal_SMD_3225-4Pin_3.2x2.5mm` | 1 | [`C20625731`](https://jlcpcb.com/partdetail/C20625731) | 1 | 5 |

## Slot-mounted encoder splitter

[Original KiCad BOM CSV](encoder-splitter/BOM.csv) for 11 fitted positions.

All original parts cover the five-board estimate at this snapshot.

### Detailed BOM and assembly stock

| Designators | Manufacturer part number | KiCad value | KiCad footprint | Qty per PCB | Checked JLCPCB listing | In stock | Need for 5 |
| --- | --- | --- | --- | ---: | --- | ---: | ---: |
| C1, C2 | `CL10A475KO8NNNC` | 4.7uF 16V X5R | `C_0603_1608Metric` | 2 | [`C19666`](https://jlcpcb.com/partdetail/C19666) | 3,674,982 | 20 |
| C3 | `CL10A106KP8NNNC` | 10uF 10V X5R | `C_0603_1608Metric` | 1 | [`C19702`](https://jlcpcb.com/partdetail/C19702) | 9,821,462 | 20 |
| J1, J2, J3 | `B6B-PH-K-S(LF)(SN)` | ENCODER 1 / ENCODER 2 / ENCODER 3 | `JST_PH_B6B-PH-K_1x06_P2.00mm_Vertical` | 3 | [`C131342`](https://jlcpcb.com/partdetail/C131342) | 447 | 15 |
| J4 | `9001-11961C00A` | DIN96 / male right-angle | `DIN96_Male_Horizontal` | 1 | [`C5173361`](https://jlcpcb.com/partdetail/C5173361) | 945 | 5 |
| R1, R2, R3 | `0603WAF1002T5E` | 10kR | `R_0603_1608Metric` | 3 | [`C25804`](https://jlcpcb.com/partdetail/C25804) | 42,823,804 | 25 |
| U1 | `AP2112M-3.3TRG1` | AP2112M-3.3TRG1 | `SOIC-8_3.9x4.9mm_P1.27mm` | 1 | [`C5290219`](https://jlcpcb.com/partdetail/C5290219) | 2,486 | 5 |
