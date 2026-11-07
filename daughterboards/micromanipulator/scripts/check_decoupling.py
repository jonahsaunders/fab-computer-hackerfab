"""Measure actual same-layer supply paths, excluding inner-layer shortcuts.

Run with KiCad's pcbnew Python. This supplements, not replaces, native DRC.
It checks supply traces only; ground-loop/placement review remains separate.
"""
from pathlib import Path
import argparse
import csv
import heapq
import math
import pcbnew as p

BASE = Path(__file__).resolve().parents[1]
PAIRS = [('C1', 'U2.1'), ('C2', 'U2.5'), ('C10', 'U1.61'),
         ('C11', 'L2.2'), ('C12', 'U1.64'), ('C13', 'U4.8')]
PAIRS += [(f'C{c}', f'U1.{pin}') for c, pin in
          [(16, 5), (17, 15), (18, 24), (19, 29), (20, 41),
           (21, 50), (22, 60), (23, 76), (24, 59), (25, 10),
           (26, 32), (27, 51), (53, 68), (54, 69)]]
for chip, first in [('U5', 30), ('U6', 34), ('U7', 38)]:
    PAIRS += [(f'C{first + offset}', f'{chip}.{pin}')
              for offset, pin in [(0, 24), (1, 13), (2, 20)]]
PAIRS += [('C60', 'U9.1'), ('C62', 'U10.1'), ('C67', 'U9.8'),
          ('C68', 'U10.8'), ('C64', 'U11.6'), ('C66', 'U12.5')]


def xy(pos):
    return round(p.ToMM(pos.x), 6), round(p.ToMM(pos.y), 6)


def on_segment(q, a, b):
    return abs(math.dist(a, q) + math.dist(q, b) - math.dist(a, b)) < 1e-6


def inspect(path):
    board = p.LoadBoard(str(path))
    pads = {f'{f.GetReference()}.{q.GetNumber()}': q
            for f in board.GetFootprints() for q in f.Pads()}
    results = {}
    for cap, pin in PAIRS:
        start, end = pads[cap + '.1'], pads[pin]
        assert start.GetNetCode() == end.GetNetCode(), (cap, pin)
        # Vias are deliberately absent: a route must exist entirely on F.Cu.
        segments = [(xy(t.GetStart()), xy(t.GetEnd()))
                    for t in board.GetTracks()
                    if not isinstance(t, p.PCB_VIA)
                    and t.GetLayer() == p.F_Cu
                    and t.GetNetCode() == start.GetNetCode()]
        source, target = xy(start.GetPosition()), xy(end.GetPosition())
        nodes = {source, target} | {q for s in segments for q in s}
        graph = {q: [] for q in nodes}
        for a, b in segments:
            along = sorted((q for q in nodes if on_segment(q, a, b)),
                           key=lambda q: math.dist(a, q))
            for u, v in zip(along, along[1:]):
                d = math.dist(u, v)
                graph[u].append((d, v))
                graph[v].append((d, u))
        queue, seen = [(0., source)], set()
        length = None
        while queue:
            d, node = heapq.heappop(queue)
            if node in seen:
                continue
            seen.add(node)
            if node == target:
                length = round(d, 3)
                break
            for delta, other in graph[node]:
                if other not in seen:
                    heapq.heappush(queue, (d + delta, other))
        results[cap] = (pin, length)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--board', type=Path, default=BASE / 'hardware/daughterboard/FabNanoDaughterboard.kicad_pcb')
    parser.add_argument('--compare', type=Path)
    parser.add_argument('--output', type=Path, default=BASE / 'docs/decoupling-paths.csv')
    args = parser.parse_args()
    current = inspect(args.board)
    previous = inspect(args.compare) if args.compare else {}
    with args.output.open('w', newline='', encoding='utf-8') as output:
        writer = csv.writer(output)
        writer.writerow(['Capacitor', 'Supply pad', 'Served pin', 'Front copper length mm',
                         'Previous front copper length mm', 'Path layers'])
        for cap, (pin, length) in current.items():
            old = previous.get(cap, ('', None))[1]
            writer.writerow([cap, '1', pin, length if length is not None else 'NO DIRECT PATH',
                             old if old is not None else 'NO DIRECT PATH' if previous else 'not compared',
                             'F.Cu only' if length is not None else 'unverified'])
    missing = [cap for cap, (_, length) in current.items() if length is None]
    print(f'{len(current) - len(missing)}/{len(current)} local supply paths remain entirely on F.Cu')
    if missing:
        raise SystemExit('Missing direct paths: ' + ', '.join(missing))
