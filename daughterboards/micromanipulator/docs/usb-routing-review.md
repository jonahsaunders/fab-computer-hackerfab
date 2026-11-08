# USB routing review — 2026-11-08

The connector-end routing has been simplified while preserving the USB-C position, every electrical pin assignment, the two 27 Ω resistors beside the RP2350B, and the 100 × 60 mm board outline. No schematic, component selection, manufacturing rule or backplane interface changed.

## Connector and ESD launch

U12 is aligned with the connector's data contacts. D+ joins its two reversible USB-C contacts directly on front copper; D− uses one short back-layer jumper for the unavoidable crossing. Each protection-channel output then makes one transition to the paired back-layer route. New bends are 45 degrees.

| Saved-board measurement | Before | Current |
| --- | ---: | ---: |
| D+ signal vias | 5 | **2** |
| D− signal vias | 5 | **4** |
| Total data-net copper inventory, D+ | 31.242 mm | **28.804 mm** |
| Total data-net copper inventory, D− | 30.562 mm | **30.052 mm** |
| J18.A6 → R7.2 copper / layer changes | 29.487 mm / 4 | **26.949 mm / 2** |
| J18.B6 → R7.2 copper / layer changes | 28.487 mm / 4 | **26.183 mm / 2** |
| J18.A7 → R8.2 copper / layer changes | 29.407 mm / 4 | **28.897 mm / 4** |
| J18.B7 → R8.2 copper / layer changes | 28.407 mm / 4 | **27.897 mm / 2** |

Copper inventory includes branches. Endpoint measurements follow the shortest connected PCB route and count layer changes separately; they exclude via-barrel length, packages and cable contacts. They are not propagation-delay estimates. The D− crossover accounts for the two remaining extra vias; no length-matching meander was added to compensate this short full-speed launch.

The front-layer connector/ESD tracks now have a **9.3 × 3.6 mm local In1 ground region** directly underneath, tied to the continuous In2 ground plane through nearby ground vias. The five surrounding supply regions each remain connected. The main pair stays on B.Cu over In2 ground; B.Cu coplanar ground remains excluded from this corridor. MCU fanout is unchanged. Short launches and component pads are not uniform controlled-impedance transmission lines.

U12 has two short explicit ground returns. Its shortest pad-center-to-via-center front-copper path falls from 1.270 to **0.963 mm**. C66 rotates beside the VBUS pin: its ground lead falls from 0.672 to **0.544 mm**; its direct VBUS lead is 1.862 mm, previously 1.583 mm. This is a geometric placement tradeoff, not a measured ESD clamping improvement. [ST's USBLC6-2 datasheet, section 2.3](https://www.st.com/resource/en/datasheet/usblc6-2.pdf) emphasizes short protection connections and placement at the connector.

[![USB connector and protection, front copper](usb-front-detail.svg)](usb-front-detail.svg)

[![USB back-layer pair, viewed from the top](usb-back-detail.svg)](usb-back-detail.svg)

## MCU termination and parts

R7/R8 remain beside the MCU. R7.1 → U1.67 is **2.652 mm**, and R8.1 → U1.66 is **0.987 mm**, both direct on F.Cu with no signal vias. The short output stubs are not continuously coupled. [Raspberry Pi's RP2350 hardware guide, section 5.1](https://pip-assets.raspberrypi.com/categories/1214-rp2350/documents/RP-008280-DS-1-hardware-design-with-rp2350.pdf?disposition=inline) requires 27 Ω termination near the chip and recommends a nominal 90 Ω differential route for its full-speed USB interface. The under-3-mm check is this project's target, not a USB compliance limit.

R7/R8 are YAGEO RC0201FR-0727RL, 27 Ω, 1%, [JLCPCB C273268](https://jlcpcb.com/partdetail/YAGEO-RC0201FR0727RL/C273268). The local `FabNano:R_0201_Yageo_Reflow` footprint uses 0.35 × 0.40 mm rectangular lands, 0.30 mm inner gap and 1.00 mm overall span from the [YAGEO mounting guide](https://yageogroup.com/content/Resource%20Library/Product%20Guide-Catalog/yageo_PYu-R_Mount_10_19050818_343.pdf). Models and footprints remain self-contained.

U12 remains ST USBLC6-2SC6, [C7519](https://jlcpcb.com/partdetail/C7519), in SOT-23-6. Its two equivalent channels retain the previous assignment: pins 1/6 protect D−; pins 3/4 protect D+. Pin 2 is GND and pin 5 is USB VBUS. Its footprint remains unchanged. Confirm current supplier stock when ordering.

## Impedance estimate and validation

The uniform back-layer pair remains **0.26 mm wide with a 0.15 mm edge gap**. For the saved nominal stackup (0.2104 mm dielectric, 35 µm outer copper, Er 4.4), the microstrip approximation from [TI DP83816, section 6.2.2.2](https://www.ti.com/lit/ds/symlink/dp83816.pdf) gives:

`Z0 = 87/sqrt(Er + 1.41) * ln(5.98*h/(0.8*w + t)) = 59.35 Ω`

`Zdiff = 2*Z0*(1 - 0.48*exp(-0.96*s/h)) = 89.96 Ω`

Varying dielectric height from 0.19 to 0.23 mm and Er from 4.2 to 4.6 gives approximately 84.9–94.7 Ω with unchanged copper. This is a sensitivity example, not a fabrication tolerance or field-solver result. Mask, copper shape, connector/ESD loading, launches and vias are omitted. The short front-layer launch does not inherit this impedance estimate.

`scripts/check_usb_launch.py` samples the center and both trace edges every 0.05 mm: **3,000 points** across the connector-side F.Cu routes and all USB B.Cu routes have adjacent-layer ground underneath. Samples within 0.6 mm of either data net's signal vias are counted separately because of their antipads. The MCU-side front fanout is outside this reference check. Each inner supply region, the new local ground region and In2 ground remains one connected region.

Native DRC, connectivity and schematic parity report zero findings. The schematic and ERC result are unchanged. Native comparison verifies that only U12/C66 moved; all pad nets, the connector position, MCU decouplers, unrelated signal routes, board outline and project rules are preserved. All 35 direct capacitor-to-pin supply paths and all 48 explicit capacitor ground returns remain present.

These checks establish geometry and connectivity, not USB compliance or measured ESD immunity. Fabricator impedance confirmation and prototype electrical testing remain required.
