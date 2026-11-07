"""Check supply domains against the load-fuse-open fault case.

Run with KiCad's pcbnew Python. Native ERC/DRC and schematic parity are also
required: these net assertions do not prove physical copper connectivity.
"""
from pathlib import Path
import pcbnew as p

BASE = Path(__file__).resolve().parents[1]
board = p.LoadBoard(str(BASE / 'hardware/daughterboard/FabNanoDaughterboard.kicad_pcb'))
pads = {f'{fp.GetReference()}.{pad.GetNumber()}': pad.GetNetname()
        for fp in board.GetFootprints() for pad in fp.Pads()}

# U11 has no powered-off input tolerance: MCU outputs must not remain powered
# while the load fuse disconnects its supply. Feed the buffer before that fuse.
for pin in ('F1.1', 'U2.8', 'U11.6', 'C64.1', 'C65.1'):
    assert pads[pin] == '+5V_BP', (pin, pads[pin])

# Keep the load-side motor supply and pump clamp behind the same fuse.
for pin in ('F1.2', 'U9.1', 'U10.1', 'D2.1'):
    assert pads[pin] == '+5V_LOAD', (pin, pads[pin])
for pin in ('U2.1', 'U9.8', 'U10.8'):
    assert pads[pin] == '+3V3', (pin, pads[pin])
print('Load-fuse-open supply-domain check passed: gate buffer stays with logic; loads remain fused.')
