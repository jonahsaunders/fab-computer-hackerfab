# Source provenance

## Supplied inputs

The initial repository import was prepared on 2026-10-21 from:

- `Backplane.zip`: the `Backplane/HackerfabBackplane/` KiCad project.
- `LibraryHackerfab.zip`: custom symbols and footprint libraries under `LibraryHackerfab/`.
- *Hackerfab Progress Report 1 - FAB Computer.pdf*: background only, including Jonah Saunders' modular backplane/nanopositioner section and Jacob Rohozen's fab computer/sputtering section. The PDF is not redistributed in this repository.

The report describes early requirements and plans. The supplied KiCad files are the source for the repository's hardware inventory and validation baseline; the report's milestone statuses are not presented as current test results.

## Latest 2026-10-30 source update

The corrected supplied archives were imported: nine backplane design files and 31 custom-library files. The root schematic and PCB implement the V6 pin order, with J1 nearest the MCU and UART only on J1. The libraries are unchanged from the October 29 archive. All 40 active source files match the archives after line-ending normalization; the repository retains its portable library tables. History, backups, personal settings, and lock files are omitted.

All 288 connector pad assignments were compared with V6 in the schematic and PCB. Updated schematic/board previews and current ERC/DRC results accompany the import; see [validation](validation.md). The PCB contains the author’s routing progress.

| Input | SHA-256 |
| --- | --- |
| `Backplane.zip` | `e90955123a6e66318d26df3ff379cbae10a63ccf3329a530b0bd17e33bcbb435` |
| `LibraryHackerfab.zip` | `db5c3d66d2a99bcd8b0e6b4c48f858e088cf05453cb7b19b771d245ed7039d63` |

## Previous 2026-10-29 source update

The supplied archives were imported into the existing repository locations: nine backplane design files and 31 library files (seven symbol libraries and 24 footprints). Compared with the previous import, the PCB, project, root schematic, and microcontroller sheet changed. The library update adds W25Q128JVSIQ flash-memory and DFE252012F-3R3M=P2 inductor symbols and their footprints, and revises the QFN-80 and Texas HSOP-8 footprints. The other active files match after line-ending normalization.

The repository's portable `fp-lib-table` and `sym-lib-table` were retained. The archive's footprint table still contains absolute desktop paths and an unused `Hack_Osicllators` entry. All 40 imported design and library files match the supplied active sources after line-ending normalization; no electrical or footprint changes were made during import. The supplied sources already contain the earlier fuse reference correction. Local history, backup files, personal settings, and editor lock files were omitted.

| Input | SHA-256 |
| --- | --- |
| `Backplane.zip` | `2831c1ed387e02acf5ddecc946eb71cafc70bb48188b46764c5f6404acc80a21` |
| `LibraryHackerfab.zip` | `db5c3d66d2a99bcd8b0e6b4c48f858e088cf05453cb7b19b771d245ed7039d63` |

All seven schematic previews and the board image were regenerated with KiCad 10.0.6. The design has 144 schematic components and 144 PCB footprints, with partial routing. See [validation](validation.md) for the current ERC/DRC results.

## Later 2026-10-26 source update

The latest supplied archives were imported into the same locations. The PCB, project, microcontroller sheet, 12 V and 5 V sheets, and passive symbol library changed. Other active source files match the previous import after line-ending normalization and the documented fuse reference correction. The portable library tables remain in place. The archives also contain local history, personal settings, and backup files, which are omitted as described below. The library archive contains another copy of the backplane; the dedicated backplane archive is the source for the project.

| Input | SHA-256 |
| --- | --- |
| `Backplane.zip` | `5d5989b9b181786cb4872330af4dc332807218ec35e0b4a389b25ffbf5ee654a` |
| `LibraryHackerfab.zip` | `67145490204cabcd166149f126d37eebc9a72dfa01b24410629074def56f428e` |

Previews and validation were regenerated with KiCad 10.0.6; see [validation](validation.md).

## Earlier 2026-10-26 source update

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
- Editor `.lck` files.
- Seven `.bak` library copies. Some differ from current library files; they remain available in the original archive rather than being treated as active source.

The original archives are unchanged. They are not committed as duplicate project copies. Generated schematic SVGs and the board PNG come directly from KiCad and can be refreshed using `scripts/export_design.py`.

## Archive fingerprints

SHA-256 identifies the exact supplied archives used for each import.

### Earlier update: 2026-10-26

| Input | SHA-256 |
| --- | --- |
| `Backplane.zip` | `cb402ce35c35c4ca89653b3e4fa78799b7c20a86cc4a859fcf68cb515b5bb651` |
| `LibraryHackerfab.zip` | `fae4f7f1eb39ee0c3e7f227d90205d20042f0cc822c55a51ffbe870fe86c5a20` |

### Initial import: 2026-10-21

| Input | SHA-256 |
| --- | --- |
| `Backplane.zip` | `98cf0ab542ad3de3d64e1f620149b67db82f9fa043ab19333f574d06d6231985` |
| `LibraryHackerfab.zip` | `9b7ce8772d420b50c1afcbc9ea5139d51ee581ea7fd56a7c9e4cf8f526473748` |
