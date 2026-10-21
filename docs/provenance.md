# Source provenance

## Supplied inputs

The initial repository import was prepared on 2026-10-21 from:

- `Backplane.zip`: the `Backplane/HackerfabBackplane/` KiCad project.
- `LibraryHackerfab.zip`: custom symbols and footprint libraries under `LibraryHackerfab/`.
- *Hackerfab Progress Report 1 - FAB Computer.pdf*: background only, including Jonah Saunders' modular backplane/nanopositioner section and Jacob Rohozen's fab computer/sputtering section. The PDF is not redistributed in this repository.

The report describes early requirements and plans. The supplied KiCad files are the source for the repository's hardware inventory and validation baseline; the report's milestone statuses are not presented as current test results.

## Import mapping

| Original location | Repository location |
| --- | --- |
| `Backplane/HackerfabBackplane/` | `hardware/backplane/` |
| `LibraryHackerfab/` | `hardware/libraries/` |

Eight backplane design files (project, PCB, and six schematic sheets) and 22 library files (seven symbol libraries and 15 footprints) were retained. Source filenames, component identifiers, embedded models, and electrical connections were preserved. Git normalizes text line endings.

The original footprint table used absolute desktop paths. It was replaced with relative `${KIPRJMOD}/../libraries/` entries, and a matching project-local symbol table was added. An unused `Hack_Osicllators` typo entry was removed; references use the supplied `Hack_Oscillators` library.

## Omitted local state

- The backplane's `.history/` directory, including its nested Git database and save snapshots.
- The personal `.kicad_prl` settings file.
- Seven `.bak` library copies. Some differ from current library files; they remain available in the original archive rather than being treated as active source.

The original archives are unchanged. They are not committed as duplicate project copies. Generated schematic SVGs and the board PNG come directly from KiCad and can be refreshed using `scripts/export_design.py`.

## Archive fingerprints

SHA-256 identifies the exact supplied archives used for this import:

| Input | SHA-256 |
| --- | --- |
| `Backplane.zip` | `98cf0ab542ad3de3d64e1f620149b67db82f9fa043ab19333f574d06d6231985` |
| `LibraryHackerfab.zip` | `9b7ce8772d420b50c1afcbc9ea5139d51ee581ea7fd56a7c9e4cf8f526473748` |
