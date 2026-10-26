# Source provenance

## Supplied inputs

The initial repository import was prepared on 2026-10-21 from:

- `Backplane.zip`: the `Backplane/HackerfabBackplane/` KiCad project.
- `LibraryHackerfab.zip`: custom symbols and footprint libraries under `LibraryHackerfab/`.
- *Hackerfab Progress Report 1 - FAB Computer.pdf*: background only, including Jonah Saunders' modular backplane/nanopositioner section and Jacob Rohozen's fab computer/sputtering section. The PDF is not redistributed in this repository.

The report describes early requirements and plans. The supplied KiCad files are the source for the repository's hardware inventory and validation baseline; the report's milestone statuses are not presented as current test results.

## 2026-10-26 source update

Replacement `Backplane.zip` and `LibraryHackerfab.zip` archives were supplied on 2026-10-26 and imported into the same repository locations. The update includes nine backplane design files (project, PCB, and seven schematic sheets) and 29 library files (seven symbol libraries and 22 footprints).

The root schematic and project now include `Protection.kicad_sch`; the libraries add protection components, connectors, and seven footprints. The PCB and the five pre-existing subsheets match the initial import after line-ending normalization.

The repository's portable `fp-lib-table` and `sym-lib-table` were retained. The replacement footprint table still contains absolute desktop paths and the unused `Hack_Osicllators` typo. The new fuse reference named an absent `Hack_Passives_Power` library, so it was corrected to `Hack_Passives:Fuse_Littelfuse-NANO2-451_453` in the library symbol and both cached/placed symbol properties in `Protection.kicad_sch`. The footprint itself was supplied in `Hack_Passives.pretty`. These reference corrections and line-ending normalization are the only changes to the imported design contents; circuit connections were preserved.

Schematic previews, the board image, and validation notes were refreshed with KiCad 10.0.6. The new schematic has 109 components, while the unchanged PCB has 93 footprints; see the [current validation results](validation.md).

## Import mapping

| Original location | Repository location |
| --- | --- |
| `Backplane/HackerfabBackplane/` | `hardware/backplane/` |
| `LibraryHackerfab/` | `hardware/libraries/` |

The initial 2026-10-21 import retained eight backplane design files (project, PCB, and six schematic sheets) and 22 library files (seven symbol libraries and 15 footprints). Source filenames, component identifiers, embedded models, and electrical connections were preserved. Git normalizes text line endings.

The original footprint table used absolute desktop paths. It was replaced with relative `${KIPRJMOD}/../libraries/` entries, and a matching project-local symbol table was added. An unused `Hack_Osicllators` typo entry was removed; references use the supplied `Hack_Oscillators` library.

## Omitted local state

- The backplane's `.history/` directory, including its nested Git database and save snapshots.
- The personal `.kicad_prl` settings file.
- Seven `.bak` library copies. Some differ from current library files; they remain available in the original archive rather than being treated as active source.

The original archives are unchanged. They are not committed as duplicate project copies. Generated schematic SVGs and the board PNG come directly from KiCad and can be refreshed using `scripts/export_design.py`.

## Archive fingerprints

SHA-256 identifies the exact supplied archives used for each import.

### Current update: 2026-10-26

| Input | SHA-256 |
| --- | --- |
| `Backplane.zip` | `cb402ce35c35c4ca89653b3e4fa78799b7c20a86cc4a859fcf68cb515b5bb651` |
| `LibraryHackerfab.zip` | `fae4f7f1eb39ee0c3e7f227d90205d20042f0cc822c55a51ffbe870fe86c5a20` |

### Initial import: 2026-10-21

| Input | SHA-256 |
| --- | --- |
| `Backplane.zip` | `98cf0ab542ad3de3d64e1f620149b67db82f9fa043ab19333f574d06d6231985` |
| `LibraryHackerfab.zip` | `9b7ce8772d420b50c1afcbc9ea5139d51ee581ea7fd56a7c9e4cf8f526473748` |
