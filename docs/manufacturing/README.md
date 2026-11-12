# Manufacturing guide

These files cover the three active HackerFab boards at [design revision `1876353`](https://github.com/jonahsaunders/fab-computer-hackerfab/tree/1876353af80357d221325e103f67ee17cebcaeb5). The Gerbers, Excellon drills, and placement coordinates were exported with KiCad 10.0.6. The BOMs use the fitted parts in the corresponding KiCad schematics. See the [JLCPCB parts audit and replacement table](parts-sourcing.md) for catalog matches, stock, and separately reviewed alternatives.

| Board | Outline | Copper layers | Smallest via drill | Fabrication | Assembly |
| --- | --- | ---: | ---: | --- | --- |
| [HackerFab backplane](../../hardware/backplane/README.md) | 111.5 × 154 mm | 4 | 0.20 mm | [Gerbers and drills](backplane/Gerbers.zip) | [BOM](backplane/BOM.csv) · [CPL](backplane/CPL.csv) |
| [Motion controller](../../daughterboards/micromanipulator/README.md) | 100 × 60 mm | 4 | 0.20 mm | [Gerbers and drills](motion-controller/Gerbers.zip) · [Via-fill map](motion-controller/Via-Fill-Map.png) | [BOM](motion-controller/BOM.csv) · [CPL](motion-controller/CPL.csv) |
| [Slot-mounted encoder splitter](../../daughterboards/micromanipulator/hardware/encoder-backplane/README.md) | 100 × 26 mm | 4 | 0.25 mm | [Gerbers and drills](encoder-splitter/Gerbers.zip) | [BOM](encoder-splitter/BOM.csv) · [CPL](encoder-splitter/CPL.csv) |

## Place the PCB order

1. Upload one Gerber ZIP per board to the [JLCPCB quote page](https://cart.jlcpcb.com/quote). Select **FR-4, four layers, 1.6 mm**, and a via drill option that covers the smallest drill above. Check the outline, copper layers, and holes in the preview. [JLCPCB Gerber guide](https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-9)
2. For assembled boards, enable **top-side PCB Assembly**. Upload the corresponding `BOM.csv` and `CPL.csv` in the assembly step. Each design includes through-hole connectors. Confirm the connectors are selected and check their seating and orientation in the placement preview. [JLCPCB assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities)
3. Review the manufacturer part numbers, packages, and selected quantities against the [parts audit](parts-sourcing.md). A part may match by name and still be unchecked when stock is short. Confirm stock for your board quantity plus assembly attrition. Source the original or approve a listed alternative for that order before checkout. [JLCPCB matching and stock guide](https://jlcpcb.com/help/article/component-matching-guidelines-for-pcba-orders)
4. Review pin 1, connector alignment, diode and capacitor polarity, and the marked inductor orientation in the production preview before approving assembly. [JLCPCB orientation guidance](https://jlcpcb.com/help/article/pcb-assembly-faqs-part-2)

The CPL uses absolute coordinates in millimetres on the same origin as the Gerbers. Bare probe pads and mounting holes stay in the fabrication artwork. The assembly CSVs contain parts to be populated.

## Backplane

- Confirm the inner copper weight before ordering. The saved KiCad stackup shows 35 µm on each inner layer, while the supplied custom rules describe a 0.5 oz inner-copper process. Confirm the intended construction with the designer and JLCPCB. [Backplane project notes](../../hardware/backplane/README.md)
- Populate the three vertical female DIN96 sockets J1–J3 and the terminal blocks J4–J6. The plug-in cards use the mating right-angle male connector.
- Use the supplied [backplane CPL](backplane/CPL.csv) for the vertical DIN96 sockets. KiCad exports their positions at pad A1. JLCPCB expects the component center, so the supplied file moves each socket by +39.37 mm in X and +2.54 mm in Y from the KiCad export. If you already uploaded an earlier CPL, replace it and select **Process BOM&CPL** again. Check that the three contact rows and both mounting holes line up for each socket and that the connector's pin 1 matches A1. [JLCPCB CPL format](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly)
- The RP2350B uses Y1 Abracon **ABM8-272-T3** (`C20625731`) and L3 Abracon **AOTA-B201610S3R3-101-T** (`C42411119`). In the assembly preview, L3's winding mark faces pad 1 on `+1V1`. L1 and L2 are the separate 15 µH Sumida inductors for the external buck regulators. [Raspberry Pi's JLCPCB guidance](https://www.raspberrypi.com/news/rp2350-now-available-at-jlcpcb/)
- Review the prototype findings before ordering. The layout check reported zero errors and zero unconnected items, with 390 warnings including one front-copper sliver. The schematic check reported nine errors and five warnings. [Backplane validation](../validation.md)

## Motion controller

- Select **ENIG** and **JLC04161H-7628** to match the saved stackup. The USB geometry was designed for this stackup. Confirm construction and impedance requirements with JLCPCB. [Layout and stackup](../../daughterboards/micromanipulator/docs/layout-review.md)
- Use **Standard PCBA** for the 0201 resistors R7 and R8. Ask JLCPCB to add rails or panelize the board to meet the 70 × 70 mm Standard PCBA minimum. Have it check fixture clearance at the overhanging right-angle DIN96 connector J1. [JLCPCB Standard PCBA requirements](https://jlcpcb.com/blog/reduce-pcb-assembly-cost-prototype)
- Request epoxy fill and copper capping for the **11 marked Ø0.30 mm vias** at U1, U9 and U10. Attach the [via-fill map](motion-controller/Via-Fill-Map.png) and identify `FabNanoDaughterboard-via-fill-and-cap.sk` in the order notes. Follow the supplied mask artwork for the other vias. [JLCPCB via-covering guide](https://jlcpcb.com/help/article/pcb-via-covering)
- Verify U1's A4 stepping and QFN orientation, plus the switch-side and polarity markings around the motor drivers and the polymer capacitor. [Motion card BOM and validation](../../daughterboards/micromanipulator/docs/validation.md)

## Slot-mounted encoder splitter

- Select **ENIG** and **JLC04161H-7628**. Quote top-side Economic PCBA if the selected parts and finish qualify. Confirm fixture clearance at the overhanging male DIN96 connector J4.
- Populate three top-entry JST PH6 headers J1–J3 and the DIN96 plug J4. Check the JST key direction and DIN96 orientation in the preview. [Encoder card and pinout](../../daughterboards/micromanipulator/hardware/encoder-backplane/README.md)

## Source BOMs and order substitutions

The assembly BOMs preserve the KiCad manufacturer part numbers, footprint identities, and catalog codes recorded in the design. For generic-value backplane symbols whose library names carry the specified part number, the BOM uses that library part number. Blank catalog cells indicate that the design supplies no catalog code. The audit table lists verified exact catalog matches for these cells and any reviewed alternatives. Apply a replacement only to the specific order after reviewing its fit and electrical limits.

The board files and assembly CSVs are for prototype fabrication. At this revision, KiCad reported zero schematic electrical-rule, layout design-rule, unconnected, and schematic-parity findings on both plug-in cards. The [card validation notes](../../daughterboards/micromanipulator/docs/validation.md) describe the remaining physical fit, USB, current, thermal, and firmware work. [Enclosure and wiring](../enclosure/README.md) are documented separately.
