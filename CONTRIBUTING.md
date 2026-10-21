# Contributing

Open the complete project in KiCad 10 and keep hardware changes focused on one circuit or layout task at a time.

## Hardware changes

1. Describe the reason for the change and which schematic sheets or interfaces it affects.
2. Keep custom symbols and footprints in `hardware/libraries/`. Preserve library names so existing references continue to resolve.
3. Use `${KIPRJMOD}` paths in project library tables. Do not add paths to a personal desktop or global library configuration.
4. Run ERC and DRC, including schematic/PCB parity. Review new findings against the [import baseline](docs/validation.md); document deliberate exclusions rather than silently hiding them.
5. Regenerate the previews with `python scripts/export_design.py` when the design changes. Keep local reports in `build/` and summarize meaningful changes in the review.
6. Run `python scripts/check_repo.py` before submitting.

Include a schematic or layout image and the relevant ERC/DRC results with a proposed change. Do not commit autosaves, editor history, personal settings, or raw archive copies.

## Manufacturing and bring-up

The initial import is not fabrication-ready. Before preparing a manufacturing release, complete the outline and routing, review component footprints and connector orientation, resolve or justify ERC/DRC findings, and check assembly data against the reviewed design. Record the exact commit and KiCad version used for exported files.

Keep bench results separate from design intent: record the board revision, setup, measurements, and any modifications made during testing. Add daughter boards and firmware when their actual source files are available.
