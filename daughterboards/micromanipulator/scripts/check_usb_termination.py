"""Measure USB source-termination stubs on the saved board (not SI simulation)."""
from pathlib import Path
import argparse, csv, heapq, math
import pcbnew as p

B = Path(__file__).resolve().parent.parent


def inspect(path):
    board = p.LoadBoard(str(path))
    pads = {f'{fp.GetReference()}.{pad.GetNumber()}': pad
            for fp in board.GetFootprints() for pad in fp.Pads()}
    xy = lambda q: (round(p.ToMM(q.x), 5), round(p.ToMM(q.y), 5))
    rows = []
    for resistor, pin in [('R7', 'U1.67'), ('R8', 'U1.66')]:
        a, z = pads[resistor + '.1'], pads[pin]
        assert a.GetNetCode() == z.GetNetCode(), (resistor, pin)
        tracks = [t for t in board.GetTracks() if t.GetNetCode() == a.GetNetCode()]
        segments = [(xy(t.GetStart()), xy(t.GetEnd())) for t in tracks
                    if not isinstance(t, p.PCB_VIA) and t.GetLayer() == p.F_Cu]
        source, target = xy(a.GetPosition()), xy(z.GetPosition())
        nodes = {source, target} | {q for seg in segments for q in seg}
        graph = {q: [] for q in nodes}
        for start, end in segments:
            along = sorted((q for q in nodes if abs(math.dist(start, q) + math.dist(q, end) - math.dist(start, end)) < 1e-5),
                           key=lambda q: math.dist(start, q))
            for u, v in zip(along, along[1:]):
                graph[u].append((math.dist(u, v), v)); graph[v].append((math.dist(u, v), u))
        queue, seen, direct = [(0., source)], set(), None
        while queue:
            length, q = heapq.heappop(queue)
            if q in seen: continue
            seen.add(q)
            if q == target:
                direct = round(length, 3); break
            for delta, other in graph[q]:
                if other not in seen: heapq.heappush(queue, (length + delta, other))
        rows.append({'resistor': resistor, 'MCU pin': pin,
                     'direct F.Cu stub mm': direct,
                     'total stub copper mm': round(sum(p.ToMM(t.GetLength()) for t in tracks if not isinstance(t, p.PCB_VIA)), 3),
                     'stub vias': sum(isinstance(t, p.PCB_VIA) for t in tracks)})
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--board', type=Path, default=B / 'hardware/daughterboard/FabNanoDaughterboard.kicad_pcb')
    parser.add_argument('--compare', type=Path)
    parser.add_argument('--output', type=Path, default=B / 'build/usb-termination-check.csv')
    args = parser.parse_args()
    rows = inspect(args.board)
    if args.compare:
        old = {r['resistor']: r for r in inspect(args.compare)}
        for row in rows:
            row['previous total stub copper mm'] = old[row['resistor']]['total stub copper mm']
            row['previous stub vias'] = old[row['resistor']]['stub vias']
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', newline='', encoding='utf8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    for row in rows:
        print(row)
        # A local design target, not a claimed USB compliance limit.
        assert row['direct F.Cu stub mm'] is not None and row['direct F.Cu stub mm'] < 3
        assert row['stub vias'] == 0
