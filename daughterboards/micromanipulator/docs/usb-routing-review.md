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

U12 retains ST USBLC6-2SC6, [JLCPCB C7519](https://jlcpcb.com/partdetail/C7519). The [ST package drawing](https://www.st.com/resource/en/datasheet/usblc6-2.pdf), pages 12-13, specifies 0.95 mm pitch and 2.6-3.0 mm lead span. The existing SOT-23-6 footprint has 1.325 by 0.60 mm pads centered at +/-1.1375 mm; these provide slightly larger fillets than ST's 1.20 by 0.60 mm recommendation. Pin 2 is ground, pin 5 is VBUS, and the paired signal pins are 1/6 and 3/4. The footprint and its nominal model remain appropriate.

C11/C12 move 0.1 mm upward and 0.1 mm apart; C53 moves 0.1 mm downward. The core-power traces are adjusted with them, and C53's supply via moves to the nearby same-net fork. C11/C12 supply and ground paths become slightly shorter. C53's supply path increases by 0.004 mm and its ground path by 0.008 mm. All 35 direct supply paths and all 48 dedicated capacitor ground returns remain present. Ground-pad pour connections remain solid.

## Validation and limits

Native KiCad DRC, unconnected-item and schematic/PCB parity counts are zero. The seven-page schematic visual audit and connector-only hierarchy check pass. No clearance rule or manufacturing constraint was relaxed. The local 3D model and routing views were reviewed for placement and access.

These are geometric and connectivity checks. They do not establish 90 Ω impedance or USB compliance. Fabricator stackup/impedance confirmation and electrical testing remain required for release.

## Nominal impedance and return-plane screen

The uniform 0.26 mm / 0.15 mm back-layer pair was screened using the microstrip approximations in [TI's DP83816 datasheet, section 6.2.2.2](https://www.ti.com/lit/ds/symlink/dp83816.pdf). This uses a transmission-line formula from that reference, not the Ethernet circuit itself. With the saved stackup's 0.2104 mm dielectric, 35 um outer copper and relative permittivity 4.4:

`Z0 = 87/sqrt(Er + 1.41) * ln(5.98*h/(0.8*w + t)) = 59.35 ohm`

`Zdiff = 2*Z0*(1 - 0.48*exp(-0.96*s/h)) = 89.96 ohm`

Varying the assumed dielectric height from 0.19 to 0.23 mm and permittivity from 4.2 to 4.6 gives approximately 84.9-94.7 ohm with unchanged copper. This is a sensitivity example, not a fabrication tolerance or a field-solver result. Solder mask, copper shape, short launches, ESD/connector loading and vias are omitted.

The saved filled In2 ground polygon was also sampled beneath the center and both edges of every back-layer USB data segment at 0.05 mm intervals. All 2,337 checked points have ground beneath them. Samples within 0.6 mm of that net's signal vias are excluded because the required antipads interrupt the plane there. This confirms no plane split under the checked route; it does not model the launch return current.

Each connector-side USB net contains five signal-via objects, including connector/ESD branches. Total copper inventory is 31.242 mm for D+ and 30.562 mm for D-, of which 22.614/23.227 mm is on B.Cu. These totals include branches and are not endpoint propagation-delay measurements. The resistor-to-MCU routes remain separate, direct and via-free. The combination is a reasonable nominal 90 ohm full-speed layout, with the short launches and actual fabrication still requiring electrical validation.

[![USB front-layer detail](usb-front-detail.svg)](usb-front-detail.svg)

[![USB back-layer pair, viewed from the top](usb-back-detail.svg)](usb-back-detail.svg)
