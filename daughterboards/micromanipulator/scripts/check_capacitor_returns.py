"""Measure explicit front-copper capacitor-to-ground-via paths.

This deliberately excludes copper pours, so it reports the dedicated return
trace even when a shorter parallel path exists through the filled pour.
Lengths are pad-centre to via-centre; they do not measure loop inductance.
Run native DRC separately to check the complete filled copper connectivity.
"""
from pathlib import Path
import argparse
import csv
import heapq
import math
import pcbnew as p

BASE = Path(__file__).resolve().parents[1]


def xy(pos):
    return round(p.ToMM(pos.x), 5), round(p.ToMM(pos.y), 5)


def on_segment(q, a, b):
    return abs(math.dist(a, q) + math.dist(q, b) - math.dist(a, b)) < 1e-5


def inspect(path):
    board = p.LoadBoard(str(path))
    caps = {f.GetReference(): f for f in board.GetFootprints()
            if f.GetReference().startswith('C')}
    grounds = {ref: next(q for q in f.Pads() if q.GetNetname() == 'GND')
               for ref, f in caps.items()}
    vias = {xy(t.GetPosition()) for t in board.GetTracks()
            if isinstance(t, p.PCB_VIA) and t.GetNetname() == 'GND'}
    segments = [(xy(t.GetStart()), xy(t.GetEnd()))
                for t in board.GetTracks() if not isinstance(t, p.PCB_VIA)
                and t.GetLayer() == p.F_Cu and t.GetNetname() == 'GND']
    nodes = vias | {xy(q.GetPosition()) for q in grounds.values()}
    nodes |= {q for segment in segments for q in segment}
    graph = {q: [] for q in nodes}
    for a, b in segments:
        along = sorted((q for q in nodes if on_segment(q, a, b)),
                       key=lambda q: math.dist(a, q))
        for u, v in zip(along, along[1:]):
            d = math.dist(u, v)
            graph[u].append((d, v))
            graph[v].append((d, u))
    results = {}
    for ref, pad in grounds.items():
        queue, seen, answer = [(0., xy(pad.GetPosition()))], set(), None
        while queue:
            d, node = heapq.heappop(queue)
            if node in seen:
                continue
            seen.add(node)
            if node in vias:
                answer = (round(d, 3), node)
                break
            for delta, other in graph[node]:
                if other not in seen:
                    heapq.heappush(queue, (d + delta, other))
        results[ref] = {
            'value': caps[ref].GetValue(), 'pad': pad.GetNumber(),
            'length': answer[0] if answer else None,
            'via': answer[1] if answer else None,
            'solid': pad.GetLocalZoneConnection() == p.ZONE_CONNECTION_FULL,
        }
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--board', type=Path, default=BASE / 'hardware/daughterboard/FabNanoDaughterboard.kicad_pcb')
    parser.add_argument('--compare', type=Path)
    parser.add_argument('--output', type=Path, default=BASE / 'docs/capacitor-returns.csv')
    args = parser.parse_args()
    current = inspect(args.board)
    previous = inspect(args.compare) if args.compare else {}
    with args.output.open('w', newline='', encoding='utf-8') as output:
        writer = csv.writer(output)
        writer.writerow(['Capacitor', 'Value', 'Ground pad', 'Dedicated F.Cu return mm',
                         'Previous return mm', 'Ground via X mm', 'Ground via Y mm',
                         'Solid pad-to-pour setting'])
        for ref in sorted(current, key=lambda s: int(s[1:])):
            item = current[ref]
            writer.writerow([ref, item['value'], item['pad'], item['length'],
                             previous.get(ref, {}).get('length', ''),
                             *(item['via'] or ('', '')), item['solid']])
    missing = [ref for ref, item in current.items() if item['length'] is None]
    thermals = [ref for ref, item in current.items() if not item['solid']]
    print(f'{len(current)-len(missing)}/{len(current)} capacitors have explicit F.Cu ground-via returns; '
          f'{len(current)-len(thermals)}/{len(current)} ground pads are configured for solid pour connections.')
    if missing or thermals:
        raise SystemExit(f'Missing returns: {missing}; thermal/inherited connections: {thermals}')
