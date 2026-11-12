# Plug-in card placement check

View the boards from the component side with the long DIN41612 footprint at the top. Both cards use the WingTAT **9001-11961C00A** (`C5173361`) right-angle male plug. The CPL uses the catalog placement origin and 180° rotation so A1 is the **upper-left** signal contact and the mating face projects past the top edge. The placement matches all 96 contact holes and the two mounting holes on each board. [JLCPCB catalog part](https://jlcpcb.com/partdetail/C5173361) · [Connector drawing and board fit](../../daughterboards/micromanipulator/docs/connector-review.md)

After uploading the BOM and CPL, run **Process BOM&CPL**. In **Select Parts**, confirm the DIN plug is checked against `C5173361`. JLCPCB lists it as a through-hole assembly part. Confirm its seating, keying and overhang in the production DFM even if the initial preview leaves the housing blank. [JLCPCB assembly terms](https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service)

## Motion controller

[BOM](motion-controller/BOM.csv) · [CPL](motion-controller/CPL.csv) · [Gerbers and drills](motion-controller/Gerbers.zip)

| Designators | CPL rotation | Check in the top view |
| --- | ---: | --- |
| J1 | 180° | A1 upper left. Center is `(100.000, -56.350)` mm in the CPL. |
| J2, J12 | 270° | Pin rows run vertically with pin 1 at the top. |
| J3–J5 | 0° | Center the four pins across each row. Pin 1 is at the right end. |
| J13, J16, J17 | 180° | Center the pins over their rows. Pin 1 is at the left end. |
| J14, J15 | 270° | Pin rows run vertically with pin 1 at the bottom. |
| J18 | 270° | USB-C opening faces left. The placement moves 1.409 mm right from the KiCad origin to align the shell slots, locating holes and signal lands. |
| J19 | 0° | The four pins run horizontally with pin 1 at the left end. |
| U1 | 90° | RP2350B dot at lower left, on the bottom edge. Check the A4 lot when ordering. |
| U2 | 90° | AP2112M pin 1 at lower right, with four leads on each side. |
| U4 | 0° | Pin 1 at lower left. Four leads along the top and bottom. Select **W25Q128JVSIQ** (`C97521`), 16 MiB. |
| U5–U7 | 0° | TB6612FNG pin 1 at lower left, with twelve leads along the top and bottom. [Toshiba pinout](https://toshiba.semicon-storage.com/info/datasheet_en_20141001.pdf?did=10660) |
| U9, U10 | 180° | DRV8837C pin 1 at lower right. [TI pinout](https://www.ti.com/lit/ds/symlink/drv8837c.pdf) |
| U11, U12 | 270° | Pin 1 at upper left on each part. |
| Q1, Q2 | 180° | Gate (pin 1) at upper left. Two leads on the left and one on the right. |
| D2 | 180° | Cathode stripe faces right. |
| D3 | 90° | Cathode faces down. |
| C5, C33, C37, C41 | 0° | Positive end faces left. |
| Y1 | 0° | Crystal electrodes are lower left and upper right. Case ground is on the opposite diagonal. [Abracon drawing](https://abracon.com/datasheets/ABM8-272-T3.pdf) |

The assembly CSVs contain 117 fitted positions. The flash change preserves U4's eight nets and the fabrication artwork, including the via-fill instructions. Verify each manually selected alternative against the same board lands after processing. [Flash pin mapping](parts-sourcing.md#motion-controller-u4-flash)

## Slot-mounted encoder splitter

[BOM](encoder-splitter/BOM.csv) · [CPL](encoder-splitter/CPL.csv) · [Gerbers and drills](encoder-splitter/Gerbers.zip)

| Designators | CPL rotation | Check in the top view |
| --- | ---: | --- |
| J1–J3 | 180° | Pin 1 is at the left end of each top-entry JST PH6 header. All six pins should be centered over the hole row. |
| J4 | 180° | DIN96 A1 is upper left. Center is `(99.370, -56.350)` mm in the CPL. |
| U1 | 90° | AP2112M pin 1 is lower right, with four leads on each side. |

The assembly CSVs contain 11 fitted positions. [Encoder card pinout](../../daughterboards/micromanipulator/hardware/encoder-backplane/README.md)
