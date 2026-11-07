#!/usr/bin/env python3
"""Render nominal host/card assembly views with KiCad's pcbnew Python.

Run with KiCad 10's Python. This creates review assemblies in build/, never
changes either source PCB, and does not certify seating or cable clearance.
"""
from pathlib import Path
import argparse
import hashlib
import shutil
import subprocess
import pcbnew as pcb

ROOT = Path(__file__).resolve().parents[1]
CARD = ROOT / 'daughterboards/micromanipulator'
HOST_PCB = ROOT / 'hardware/backplane/HackerfabBackplane.kicad_pcb'
CARD_PCB = CARD / 'hardware/daughterboard/FabNanoDaughterboard.kicad_pcb'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kicad-cli', default='kicad-cli')
    args = parser.parse_args()
    build = CARD / 'build/assembly'
    build.mkdir(parents=True, exist_ok=True)
    watched = [HOST_PCB, CARD_PCB, HOST_PCB.with_suffix('.kicad_pro'), CARD_PCB.with_suffix('.kicad_pro')]
    hashes = {f: hashlib.sha256(f.read_bytes()).digest() for f in watched}

    def run(arguments, name):
        result = subprocess.run([args.kicad_cli, *map(str, arguments)], capture_output=True, text=True, encoding='utf8', errors='replace')
        (build / (name + '.log')).write_text(result.stdout + result.stderr, encoding='utf8')
        if result.returncode:
            raise RuntimeError(f'{name} failed; see {build / (name + ".log")}')

    card = pcb.LoadBoard(str(CARD_PCB))
    plug = next(f for f in card.GetFootprints() if f.GetReference() == 'J1')
    a1 = next(p for p in plug.Pads() if p.GetNumber() == 'A1').GetPosition()
    origin = f'{pcb.ToMM(a1.x)}x{pcb.ToMM(a1.y)}mm'
    model = build / 'daughterboard.wrl'
    run(['pcb', 'export', 'vrml', '--force', '--units', 'tenths', '--user-origin', origin, '--output', model, CARD_PCB], 'card-model')

    for slots, name in [(('J1',), 'single'), (('J1', 'J2'), 'adjacent')]:
        board = pcb.LoadBoard(str(HOST_PCB))
        sockets = {f.GetReference(): f for f in board.GetFootprints() if f.GetReference() in slots}
        for fp in board.GetFootprints():
            models = list(fp.Models())
            fp.Models().clear()
            for item in models:
                item.m_Filename = item.m_Filename.replace('${KIPRJMOD}', HOST_PCB.parent.as_posix())
                fp.Models().push_back(item)
        for slot in slots:
            socket = sockets[slot]
            a1 = next(p for p in socket.Pads() if p.GetNumber() == 'A1').GetPosition()
            assert socket.GetOrientationDegrees() == 0, 'Review placement for rotated host socket'
            fp = pcb.FOOTPRINT(board)
            fp.SetReference('REVIEW_' + slot)
            fp.SetValue('Nominal assembly only')
            fp.SetPosition(a1)
            fp.Reference().SetVisible(False)
            fp.Value().SetVisible(False)
            item = pcb.FP_3DMODEL()
            item.m_Filename = model.as_posix()
            item.m_Rotation = pcb.VECTOR3D(90, 0, 0)
            # Inferred from supplied mating models; not a vendor seating datum.
            item.m_Offset = pcb.VECTOR3D(0, -2.01, 17.74)
            fp.Models().push_back(item)
            board.Add(fp)
        assembly = build / (name + '.kicad_pcb')
        shutil.copy2(HOST_PCB.with_suffix('.kicad_pro'), assembly.with_suffix('.kicad_pro'))
        pcb.SaveBoard(str(assembly), board)
        for side, rotation in [('front', '325,0,205'), ('back', '325,0,25')]:
            destination = CARD / 'docs' / f'host-{name}-{side}.png'
            run(['pcb', 'render', '--width', '2000', '--height', '1600', '--quality', 'high', '--background', 'opaque', '--perspective', '--rotate', rotation, '--zoom', '.75', '--output', destination, assembly], name + '-' + side)
            print(f'Rendered {destination.relative_to(ROOT)}', flush=True)
    assert all(hashlib.sha256(f.read_bytes()).digest() == digest for f, digest in hashes.items()), 'Source design changed during rendering'
    print('Source boards and project settings unchanged. Seating and harnesses remain nominal.')


if __name__ == '__main__':
    main()
