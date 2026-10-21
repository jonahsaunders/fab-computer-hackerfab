# Validation baseline

Checked on **2026-10-21** with **KiCad 10.0.6**, after organizing the supplied files and registering the local libraries. Electrical and PCB design sources were preserved.

## Repository and export checks

- All five hierarchical subsheets resolve from the root schematic.
- All seven custom symbol libraries and seven footprint-library directories resolve through relative project paths.
- The library archive contributes 15 custom footprint files.
- Schematic SVG export succeeds for all six sheets.
- XML netlist export succeeds and contains 93 components.
- The PCB contains 93 footprints and zero routed track segments.
- Schematic/PCB parity check reports zero findings.
- The board preview renders, but KiCad reports a missing or malformed outline. Its rendered substrate is not evidence of a valid fabrication outline.

## Existing electrical-rule findings

ERC reports **82 findings: 63 errors and 19 warnings**.

| Type | Count |
| --- | ---: |
| Unconnected pins | 54 |
| Power-input pins not driven | 7 |
| Other input pin not driven | 1 |
| Pin-to-pin conflict | 1 |
| Isolated pin labels | 15 |
| Library symbol mismatches | 3 |
| Multiple net names | 1 |

These are tool findings on the imported design, not independently confirmed electrical defects. They require design review. Cached schematic symbols were not automatically replaced from the libraries because doing so could change the circuit.

The exported netlist also differs from the report's first-slot-only UART intent: `/UART_RX` reaches `J1:C22` and `J3:C22`, while `/UART_TX` reaches `J1:A22`. This is documented for review; no net connections were changed during cleanup.

## Existing design-rule findings

DRC reports **151 findings**, plus **413 unconnected items**:

| Type | Count |
| --- | ---: |
| Missing or malformed board outline | 1 |
| Silkscreen over exposed copper | 82 |
| Overlapping silkscreen | 68 |
| Unconnected PCB items, reported separately | 413 |
| Schematic/PCB parity findings | 0 |

The design is at the component-placement stage. Manufacturing outputs are intentionally not included in this import.

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
