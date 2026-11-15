# Sputtering cards: PR review and validation

Reviewed November 15, 2026 using KiCad **10.0.6** on Windows. Current source: [PR #16](https://github.com/jonahsaunders/fab-computer-hackerfab/pull/16), commit [`0c6d404d303cf7dc25ea720b2cbbe8fff10cb81f`](https://github.com/jonahsaunders/fab-computer-hackerfab/commit/0c6d404d303cf7dc25ea720b2cbbe8fff10cb81f). The submitted hardware, schematic PDFs and manufacturing exports are retained unchanged. The two standalone renders and both installed assembly views were regenerated from this revision using the repository's established view and lighting settings.

## Connector update

PR #16 replaces pump-card J2/J3 with Kangnex WJ124-3.81-04P-14-00A screw terminals (`C69809`) and Alicat J2/J3 with CONNFLY DS1037-09MNAKT74-0CC male DB9 connectors (`C75750`) for the lab's female-to-female cables. The supplied BOMs and placement files reflect these changes.

Comparing exported schematic netlists with the PR #15 revision found identical electrical connectivity on all 72 nets of each card. The DIN96 plug and external connector pad numbers also retain their PCB net assignments. Actual cable wiring and mechanical fit still require verification. The screw-terminal render uses the supplied nominal Phoenix model; it is not an exact Kangnex mechanical model.

The [initial PR #15 review](https://github.com/jonahsaunders/fab-computer-hackerfab/blob/b2cfac5ee008dcd296017fc3f7fbc75bfcf77d37/daughterboards/sputtering/docs/validation.md) recorded 22 pump-card warnings and 24 Alicat-card warnings. The table below records the current connector revision.

## Automated design checks

| Check | Pump + gauge + USB | Alicat |
| --- | ---: | ---: |
| ERC errors / warnings | 0 / 0 | 0 / 0 |
| DRC errors | 0 | 0 |
| DRC warnings | 9 | 24 |
| Unconnected items | 0 | 0 |
| Schematic/PCB parity findings | 0 | 0 |
| BOM designators / CPL entries | 43 / 43 | 22 / 22 |
| Copper layers / board thickness | 2 / 1.6 mm | 2 / 1.6 mm |

DRC was run with zone refill, schematic parity and all severities enabled. ERC was run with all severities enabled. Neither project lists ERC or DRC exclusions.

The pump card's warnings are 9 footprint/library mismatches. The Alicat card has 22 silkscreen-over-copper warnings and 2 silkscreen-to-edge clearance warnings. Warning counts may depend on the installed standard KiCad libraries.

Pump-card footprint mismatches affect C4, C5, C6, C7, C9, J1, J4, R18 and R20. Compare the embedded board footprints against their library definitions before updating footprints or releasing fabrication. These findings have been recorded, not suppressed or treated as resolved. Resolve or justify the silkscreen findings against the actual assembly and fabrication process.

BOM quantities and designators match the PCB footprint inventory and the CPL designator sets. Both Gerber ZIPs pass archive integrity checks and contain front/back copper, mask, paste, silkscreen, outline and drill outputs. This does not certify catalog part equivalence, placement rotations or Gerber-to-source geometry.

## Host interface review

All 192 DIN96 contacts were checked for host-slot compatibility, including each connected signal and power/ground contact, using the current [host connector reference](../../../docs/connector-pinout.md), host PCB and exported card netlists. The host's `+24V_P` contacts feed the cards' `+24V` nets. Slot labels refer to host connectors; the DIN96 plug on each daughtercard is named J1.

| Host slot | DIN96 contact | Card function | Host assignment |
| --- | --- | --- | --- |
| J1 | A20 / C20 | Pump UART RX / TX | UART0, GPIO1 / GPIO0 |
| J1 | A14 | RS-485 direction | AUX1, GPIO40 |
| J1 | A16 / C16 | Gauge ADC SCL / SDA | I2C0 |
| J1 | A19 / C18 | USB D+ / D- | AUX2 / AUX3, GPIO22 / GPIO23 |
| J2 | A20 / C20 | Argon UART RX / TX | UART1, GPIO37 / GPIO36 |
| J2 | A18 / C15 | Oxygen UART RX / TX | AUX5 / AUX6, GPIO24 / GPIO25 |

The ADC address selection is grounded (0x48). Both cards leave SPI0 and SPI1 unconnected. Slot-specific connections mean the pump card belongs in host J1 and the Alicat card in host J2. Firmware must configure these interfaces; this PR supplies no sputtering firmware or bench results.

## Initial integration notes (PR #15)

- The shared ordering instructions previously told readers to choose four layers for every board, contradicting these two-layer designs. The instructions now use each board's listed layer count.
- The shared guide's statement about zero findings on "both plug-in cards" referred to the earlier motion and encoder cards. Their validation is now explicitly separated from this sputtering review, including the warnings above.
- The root README now links to this dedicated section and shows both boards. Manufacturing exports remain in the shared `docs/manufacturing/sputtering-*` directories and are linked from the section.

## Reproduce the checks

From the repository root, with KiCad 10 and its standard libraries installed, run `python scripts/check_repo.py`. This existing repository check covers the backplane and shared documentation; it is not a replacement for the card-specific checks below. Create `build/sputtering-review/`, then run these commands for each card, replacing `<card>` with `pump-gauge-usb` or `alicat`:

```sh
kicad-cli sch erc --severity-all --format json --output build/sputtering-review/<card>-erc.json daughterboards/sputtering/hardware/<card>/sputtering-<card>.kicad_sch
kicad-cli pcb drc --schematic-parity --refill-zones --severity-all --format json --output build/sputtering-review/<card>-drc.json daughterboards/sputtering/hardware/<card>/sputtering-<card>.kicad_pcb
kicad-cli sch export netlist --format kicadxml --output build/sputtering-review/<card>-netlist.xml daughterboards/sputtering/hardware/<card>/sputtering-<card>.kicad_sch
```

The review also checked the new section's relative links and local library targets. Reports are local build artifacts; summarize new results here against the exact design revision.

## Remaining validation

This is a source and automated design review, not a manufacturing release or a full circuit qualification. Physical mating and enclosure fit, connector orientation and cable pinouts, manufacturer part matching, assembly placement previews, power/current/thermal measurements, gauge calibration, RS-485/RS-232 operation, USB signal integrity and host firmware integration remain to be verified. The combined 5 V load must stay within the host's documented [2.5 A power-mux limit](../../micromanipulator/docs/load-power-review.md). Record actual bench results separately with board revision and test setup.
