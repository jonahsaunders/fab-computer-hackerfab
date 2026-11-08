"""Enforce connector-only top level and reachable lower-level circuitry."""
from pathlib import Path
import json
from sexp import parse, allof, val

B = Path(__file__).resolve().parent.parent
H = B / 'hardware/daughterboard'
root = H / 'FabNanoDaughterboard.kicad_sch'
seen = set()
connectors = set()
components = set()
issues = []


def inspect(path, top=False):
    if path in seen:
        issues.append(f'Repeated sheet or hierarchy cycle: {path.name}')
        return
    seen.add(path)
    doc = parse(path.read_text(encoding='utf8'))
    libraries = {s[1]: s for s in allof(next(n for n in doc if isinstance(n, list) and n[0] == 'lib_symbols'), 'symbol')}
    for sym in allof(doc, 'symbol'):
        props = {p[1]: p[2] for p in allof(sym, 'property')}
        ref = props['Reference']
        lib = libraries[val(sym, 'lib_id')]
        if ref.startswith('#'):
            if not allof(lib, 'power') or val(sym, 'on_board') != 'no':
                issues.append(f'{path.name}: non-power symbol hidden behind {ref}')
            continue
        components.add(ref)
        if top:
            if not ref.startswith('J') or not val(sym, 'lib_id').startswith(('Connector', 'FabNano:DIN96')):
                issues.append(f'{path.name}: {ref} is not an external connector')
            else:
                connectors.add(ref)
        elif ref.startswith('J'):
            issues.append(f'{path.name}: external connector {ref} must be on the root')
    for sheet in allof(doc, 'sheet'):
        props = {p[1]: p[2] for p in allof(sheet, 'property')}
        child = (path.parent / props['Sheetfile']).resolve()
        if not child.is_relative_to(H.resolve()) or not child.exists():
            issues.append(f'Missing or external sheet: {child}')
        else:
            inspect(child)


inspect(root.resolve(), True)
unreachable = {p.resolve() for p in H.glob('*.kicad_sch')} - seen
issues.extend(f'Unreachable sheet: {p.name}' for p in sorted(unreachable))
if len(connectors) != 13:
    issues.append(f'Expected 13 external connectors after removing the PH8 cable; found {len(connectors)}')
result = {'sheets': len(seen), 'root_connectors': sorted(connectors),
          'component_count': len(components), 'issues': issues}
(B / 'build').mkdir(exist_ok=True)
(B / 'build/hierarchy-audit.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
raise SystemExit(bool(issues))
