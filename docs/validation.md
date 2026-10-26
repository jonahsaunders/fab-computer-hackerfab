# Validation baseline

Checked on **2026-10-26** with **KiCad 10.0.6**, after importing the updated archives. The existing relative library tables were retained, and the fuse footprint reference was corrected to the supplied `Hack_Passives` library. Circuit connections and the PCB were preserved.

## Repository and export checks

- All six hierarchical subsheets resolve from the root schematic, including the new protection sheet.
- All seven custom symbol libraries and seven footprint-library directories resolve through relative project paths.
- The library archive contributes 22 custom footprint files.
- Schematic SVG export succeeds for all seven sheets.
- XML netlist export succeeds and contains 109 components.
- The PCB contains 93 footprints and zero routed track segments.
- Schematic/PCB parity check reports 59 findings: 16 missing footprints and 43 net conflicts.
- The board preview renders, but KiCad reports a missing or malformed outline. Its rendered substrate is not evidence of a valid fabrication outline.
- All 38 imported source files were compared against the archives. They match after line-ending normalization and the documented fuse-library correction.

The supplied PCB is unchanged from the initial import after line-ending normalization. Its 93 footprints do not yet include the 16 additional schematic components. The update preserves this supplied design state; it does not automatically synchronize, route, or refill the PCB.

## Existing electrical-rule findings

ERC reports **74 findings: 58 errors and 16 warnings** (initial import: 82 findings).

| Type | Count |
| --- | ---: |
| Unconnected pins | 49 |
| Power-input pins not driven | 8 |
| Pin-to-pin conflict | 1 |
| Isolated pin labels | 11 |
| Library symbol mismatches | 4 |
| Multiple net names | 1 |

These are tool findings on the imported design, not independently confirmed electrical defects. They require design review. Cached schematic symbols were not automatically replaced from the libraries because doing so could change the circuit.

The exported netlist also differs from the report's first-slot-only UART intent: `/UART_RX` reaches `J1:C22` and `J3:C22`, while `/UART_TX` reaches `J1:A22`. This is documented for review; no net connections were changed during cleanup.

## Existing design-rule findings

DRC reports **151 findings**, plus **413 unconnected items** and **59 schematic/PCB parity findings**:

| Type | Count |
| --- | ---: |
| Missing or malformed board outline | 1 |
| Silkscreen over exposed copper | 82 |
| Overlapping silkscreen | 68 |
| Unconnected PCB items, reported separately | 413 |
| Missing footprints, parity report | 16 |
| Net conflicts, parity report | 43 |

The design is at the component-placement stage. The DRC and unconnected-item counts are unchanged from the initial import; parity findings have increased from zero because the schematic has advanced beyond the supplied PCB. Manufacturing outputs are intentionally not included in this import.

## Reproduce

Run from the repository root with `kicad-cli` from KiCad 10 on your PATH:

```sh
python scripts/check_repo.py
python scripts/export_design.py
```

The export script updates the committed previews and writes JSON reports and an XML netlist under ignored `build/`. It preserves the design files and does not save or refill the PCB. KiCad can return success for report generation while still finding violations; read the report contents.

For an individual check that returns a nonzero exit code when findings exist:

```sh
kicad-cli sch erc --exit-code-violations --output build/erc.rpt hardware/backplane/HackerfabBackplane.kicad_sch
kicad-cli pcb drc --schematic-parity --exit-code-violations --output build/drc.rpt hardware/backplane/HackerfabBackplane.kicad_pcb
```

Create `build/` first if you have not run the export script. No bench testing, power-up, manufacturing review, or firmware validation is implied by these checks.
