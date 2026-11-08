"""Audit bare surface probes on both active cards and original PH6 compatibility."""
from pathlib import Path
import json, math
import pcbnew as p
B = Path(__file__).resolve().parents[1]
files = ['daughterboard/FabNanoDaughterboard', 'encoder-backplane/EncoderBackplane']
boards = [p.LoadBoard(str(B/'hardware'/(name+'.kicad_pcb'))) for name in files]
reports = {}
for name, board in zip(files, boards):
    fps = {f.GetReference():f for f in board.GetFootprints()}
    expected = {'TP1':'+5V_BP','TP2':'+3V3','TP3':'GND','TP4':'GND'}
    assert {r for r in fps if r.startswith('TP')} == set(expected)
    points={}
    for ref,net in expected.items():
        f=fps[ref]; pads=list(f.Pads()); assert len(pads)==1
        q=pads[0]
        assert q.GetNetname()==net and q.GetAttribute()==p.PAD_ATTRIB_SMD
        assert q.GetDrillSize().x==q.GetDrillSize().y==0
        assert q.GetSize().x==q.GetSize().y==p.FromMM(.8)
        assert set(q.GetLayerSet().Seq())=={p.F_Cu,p.F_Mask}
        assert f.IsExcludedFromBOM() and f.IsExcludedFromPosFiles()
        points[ref]=(p.ToMM(q.GetPosition().x),p.ToMM(q.GetPosition().y))
    distances={rail:round(math.dist(points[rail],points[gnd]),3) for rail,gnd in [('TP1','TP3'),('TP2','TP4')]}
    assert all(d<=2 for d in distances.values()) and board.GetCopperLayerCount()==4
    reports[name]={'diameter_mm':.8,'ground_pad_distance_mm':distances,'no_drill_or_paste':True,'probe_count':4}
def pins(board,ref):
    fp=next(f for f in board.GetFootprints() if f.GetReference()==ref)
    return {int(q.GetNumber()):q.GetNetname() for q in fp.Pads()}
old=p.LoadBoard(str(B/'hardware/encoder-splitter/EncoderBoard.kicad_pcb'))
rename={'+3.3V':'+3V3','/Encoder_SCK':'/ENC_SCK','/Encoder_MOSI':'/ENC_MOSI','/Encoder_MISO':'/ENC_MISO',
        **{f'/Encoder{i}_CS':f'/ENC{i}_CS' for i in range(1,4)}}
for axis in range(1,4):
    expected={n:rename.get(net,net) for n,net in pins(old,f'J{axis}').items()}
    assert pins(boards[1],f'J{axis}')==expected
reports['all_three_PH6_pinouts_match_original']=True
(B/'build').mkdir(exist_ok=True)
(B/'build/probe-access-check.json').write_text(json.dumps(reports,indent=2)+'\n')
print(json.dumps(reports))
