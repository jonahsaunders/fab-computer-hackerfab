# USB placement and routing review

The 27 Ω termination resistors now sit beside the RP2350B USB pins. Their output-side tracks are direct on F.Cu; four signal vias and the long under-MCU detours have been removed. The saved-board measurements are in [usb-termination-paths.csv](usb-termination-paths.csv).

| Connection | Previous copper length | Current copper length | Current vias |
| --- | ---: | ---: | ---: |
| R7.1 → U1.67, D+ | 14.407 mm | 2.652 mm | 0 |
| R8.1 → U1.66, D− | 15.731 mm | 0.987 mm | 0 |

This implements the placement guidance in [Raspberry Pi's hardware guide, section 5.1](https://pip-assets.raspberrypi.com/categories/1214-rp2350/documents/RP-008280-DS-1-hardware-design-with-rp2350.pdf?disposition=inline). The under-3-mm check is this project's layout target, not a USB compliance specification.

The main pair stays on B.Cu over the In2 ground plane, with 0.26 mm width and 0.15 mm nominal edge gap. The final split feeds the two resistors. Short connector, ESD and resistor launches use narrower tracks; the two short resistor-to-MCU stubs are not continuously coupled. B.Cu coplanar ground remains excluded from this corridor. Three ground-transfer vias were added beside the connector/ESD launches. Existing nearby capacitor ground vias serve the MCU end.

U12's equivalent ESD channels are exchanged: I/O1, pins 1/6, protects D−; I/O2, pins 3/4, protects D+. This keeps the long pair in the correct order. The [ST functional diagram](https://www.st.com/resource/en/datasheet/usblc6-2.pdf) shows the two matching channels and their common GND/VBUS connections. Native netlist comparison confirms those four U12 pins are the only electrical net-membership changes. USB connector pins, resistor-to-MCU polarity, backplane and harness connections are unchanged.

## Parts and local placement

R7/R8 use YAGEO RC0201FR-0727RL, 27 Ω, 1%, 50 mW, listed as [JLCPCB C273268](https://jlcpcb.com/partdetail/YAGEO-RC0201FR0727RL/C273268) for Standard assembly. Order-time inventory must still be checked. The [manufacturer part specification](https://www.yageogroup.com/component-documentation/download/specsheet/RC0201FR-0727RL) gives a 0.6 × 0.3 mm body.

The self-contained `FabNano:R_0201_Yageo_Reflow` footprint uses the recommended 0.35 × 0.40 mm rectangular lands, 0.30 mm inner gap and 1.00 mm overall land span from [YAGEO's mounting guide, table 1](https://yageogroup.com/content/Resource%20Library/Product%20Guide-Catalog/yageo_PYu-R_Mount_10_19050818_343.pdf). Its courtyard adds 0.15 mm around the lands. A bundled KiCad STEP model represents the package. Both resistors remain on the component side.

C11/C12 move 0.1 mm upward and 0.1 mm apart; C53 moves 0.1 mm downward. The core-power traces are adjusted with them, and C53's supply via moves to the nearby same-net fork. C11/C12 supply and ground paths become slightly shorter. C53's supply path increases by 0.004 mm and its ground path by 0.008 mm. All 35 direct supply paths and all 48 dedicated capacitor ground returns remain present. Ground-pad pour connections remain solid.

## Validation and limits

Native KiCad DRC, unconnected-item and schematic/PCB parity counts are zero. The seven-page schematic visual audit and connector-only hierarchy check pass. No clearance rule or manufacturing constraint was relaxed. The local 3D model and routing views were reviewed for placement and access.

These are geometric and connectivity checks. They do not establish 90 Ω impedance or USB compliance. Fabricator stackup/impedance confirmation and electrical testing remain required for release.

[![USB front-layer detail](usb-front-detail.svg)](usb-front-detail.svg)

[![USB back-layer pair, viewed from the top](usb-back-detail.svg)](usb-back-detail.svg)
