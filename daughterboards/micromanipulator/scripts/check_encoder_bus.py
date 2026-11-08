"""Check actual slot SPI nets, series resistors, GPIO allocation and host ties.
This does not prove signal integrity or that the required host firmware is running.
"""
from pathlib import Path
import json, re
import pcbnew as p
from sexp import parse, allof, val, walk
B=Path(__file__).resolve().parents[1];R=B.parents[1]
def load(file):
    b=p.LoadBoard(str(file))
    return b,{f.GetReference():{q.GetNumber():q.GetNetname() for q in f.Pads() if q.GetNumber()} for f in b.GetFootprints()}
main,m=load(B/'hardware/daughterboard/FabNanoDaughterboard.kicad_pcb')
enc,e=load(B/'hardware/encoder-backplane/EncoderBackplane.kicad_pcb')
host,h=load(R/'hardware/backplane/HackerfabBackplane.kicad_pcb')
spec=[('A12','ENC1_CS','SPI0_CS1',44,'R52'),('C10','ENC2_CS','SPI0_CS2',45,'R53'),
      ('A10','ENC3_CS','SPI0_CS3',46,'R54'),('C11','ENC_SCK','SPI0_CLK',2,'R55'),
      ('A11','ENC_MOSI','SPI0_MOSI',3,'R56'),('C12','ENC_MISO','SPI0_MISO',0,None)]
lib=parse((B/'hardware/libraries/FabNano.kicad_sym').read_text())
rp=next(s for s in allof(lib,'symbol') if s[1]=='RP2350B')
pin={val(q,'name').split('/')[0]:val(q,'number') for q in walk(rp,'pin')}
config=(B/'firmware/board_config.h').read_text()
for contact,name,host_name,gpio,resistor in spec:
    net='/'+name
    assert m['J1'][contact]==e['J4'][contact]==net
    assert all(h[slot][contact]=='/'+host_name for slot in ('J1','J2','J3'))
    up=m['U1'][pin[f'GPIO{gpio}']]
    if resistor:
        assert set(m[resistor].values())=={up,net} and up!=net
        assert next(f for f in main.GetFootprints() if f.GetReference()==resistor).GetValue()=='33R'
    else:assert up==net
    assert re.search(rf'#define\s+FAB_{name}_PIN\s+{gpio}\b',config),name
for gpio in (20,21,22):assert m['U1'][pin[f'GPIO{gpio}']].startswith('unconnected-')
for gpio,resistor,signal in [(16,'R32','MISO'),(19,'R33','MOSI'),(18,'R34','CLK'),
                             (17,'R35','CS1'),(20,'R36','CS2'),(21,'R37','CS3')]:
    assert set(h[resistor].values())=={h['U5'][pin[f'GPIO{gpio}']],'/SPI0_'+signal}
assert 'J6' not in m
assert len(list(main.GetFootprints()))==121 and len(list(enc.GetFootprints()))==15
report={'shared_SPI_contacts_verified':18,'motion_CS_GPIOs':[44,45,46],'source_series_resistors':5,
        'host_GPIOs_requiring_input_no_pulls':list(range(16,22)),'host_runtime_firmware_verified':False}
(B/'build/encoder-bus-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
