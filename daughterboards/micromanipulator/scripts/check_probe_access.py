"""Validate bare surface probe pads and the original encoder-splitter harness.

Run using KiCad 10's pcbnew Python. Native ERC/DRC and parity remain required.
"""
from pathlib import Path
import json, math
import pcbnew as p

B = Path(__file__).resolve().parents[1]
card = p.LoadBoard(str(B / 'hardware/daughterboard/FabNanoDaughterboard.kicad_pcb'))
splitter = p.LoadBoard(str(B / 'hardware/encoder-splitter/EncoderBoard.kicad_pcb'))
fps = {f.GetReference(): f for f in card.GetFootprints()}
expected = {'TP1': '+5V_BP', 'TP2': '+3V3', 'TP3': 'GND', 'TP4': 'GND'}
assert {r for r in fps if r.startswith('TP')} == set(expected)
points = {}
for ref, net in expected.items():
    f = fps[ref]
    pads = list(f.Pads())
    assert len(pads) == 1
    q = pads[0]
    assert q.GetNetname() == net
    assert q.GetAttribute() == p.PAD_ATTRIB_SMD
    assert q.GetDrillSize().x == q.GetDrillSize().y == 0
    assert q.GetSize().x == q.GetSize().y == p.FromMM(.8)
    assert set(q.GetLayerSet().Seq()) == {p.F_Cu, p.F_Mask}
    assert f.IsExcludedFromBOM() and f.IsExcludedFromPosFiles()
    points[ref] = (p.ToMM(q.GetPosition().x), p.ToMM(q.GetPosition().y))
distances = {rail: round(math.dist(points[rail], points[gnd]), 3)
             for rail, gnd in [('TP1', 'TP3'), ('TP2', 'TP4')]}
assert all(distance <= 2 for distance in distances.values())
assert card.GetCopperLayerCount() == 4

def pins(board, ref):
    fp = next(f for f in board.GetFootprints() if f.GetReference() == ref)
    return {int(q.GetNumber()): q.GetNetname() for q in fp.Pads()}

card_bus = ['GND', '+3V3', '/ENC_MOSI', '/ENC_MISO', '/ENC_SCK',
            '/ENC1_CS', '/ENC2_CS', '/ENC3_CS']
upstream_bus = ['GND', '+3.3V', '/Encoder_MOSI', '/Encoder_MISO', '/Encoder_SCK',
                '/Encoder1_CS', '/Encoder2_CS', '/Encoder3_CS']
assert pins(card, 'J6') == dict(enumerate(card_bus, 1))
assert pins(splitter, 'J4') == dict(enumerate(upstream_bus, 1))
for axis in range(1, 4):
    assert pins(splitter, f'J{axis}') == dict(enumerate([
        'GND', f'/Encoder{axis}_CS', '/Encoder_SCK', '/Encoder_MOSI',
        '/Encoder_MISO', '+3.3V'], 1))

report = {'probe_diameter_mm': .8, 'probe_pad_count': 4,
          'rail_testpoints': {'TP1': '+5V_BP', 'TP2': '+3V3'},
          'ground_pad_distance_mm': distances, 'no_drill_or_paste': True,
          'encoder_splitter_input_pinout_matches': True,
          'encoder_output_pinouts_match_upstream': True}
(B / 'build').mkdir(exist_ok=True)
(B / 'build/probe-access-check.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
