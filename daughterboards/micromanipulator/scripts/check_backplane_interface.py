"""Compare the saved card's DIN contacts with the actual host PCB.

This checks electrical allocation and hole geometry, not mating tolerances,
cable bend space, connector current derating, or assembled hardware.
Run using KiCad's pcbnew Python.
"""
from pathlib import Path
import argparse
import csv
import json
import math
import pcbnew as p
from sexp import parse, allof, get, val, walk

B = Path(__file__).resolve().parents[1]
REPO = B.parents[1]


def pads(fp):
    return {q.GetNumber(): q for q in fp.Pads() if q.GetNumber()}


def mm(v):
    return round(p.ToMM(v), 5)


def local(fp, pad):
    # Both DIN footprints have zero board rotation in this assembly.
    assert fp.GetOrientationDegrees() == 0
    v = pad.GetPosition() - fp.GetPosition()
    return (mm(v.x), mm(v.y))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host',type=Path,default=REPO/'hardware/backplane/HackerfabBackplane.kicad_pcb')
    args=parser.parse_args()
    if not args.host.is_file():
        parser.error('Host PCB not found. Run from the repository checkout or supply --host PATH.')
    card = p.LoadBoard(str(B/'hardware/daughterboard/FabNanoDaughterboard.kicad_pcb'))
    host = p.LoadBoard(str(args.host))
    cf = {f.GetReference(): f for f in card.GetFootprints()}
    hf = {f.GetReference(): f for f in host.GetFootprints()}
    cp = pads(cf['J1'])
    pin_names = {f'{r}{n}' for r in 'ABC' for n in range(1,33)}
    assert set(cp) == pin_names
    rows = []
    for ref in ('J1','J2','J3'):
        hp = pads(hf[ref]); assert set(hp) == pin_names
        for row in 'ABC':
            for n in range(1,33):
                number = f'{row}{n}'
                a,z = cp[number],hp[number]
                assert local(cf['J1'],a) == (round((n-1)*2.54,5),round('ABC'.index(row)*2.54,5))
                assert local(hf[ref],z) == (round((n-1)*2.54,5),round(-'ABC'.index(row)*2.54,5))
                assert mm(a.GetDrillSize().x) == 1.0
                assert mm(z.GetDrillSize().x) == 1.0
                an,zn = a.GetNetname(),z.GetNetname()
                if an.startswith('unconnected-'):
                    assert not any(t.GetNetCode()==a.GetNetCode() for t in card.GetTracks()),number
                    status = 'Unused on card'
                else:
                    expected = {'GND':'GND','+12V_BP':'+12V','+5V_BP':'+5V',
                                '/HOST_SCL':'/I2C0_SCL','/HOST_SDA':'/I2C0_SDA',
                                '/HOST_TX':'/UART_TX' if ref=='J1' else '/UART2_TX',
                                '/HOST_RX':'/UART_RX' if ref=='J1' else '/UART2_RX'}[an]
                    if ref=='J3' and an in ('/HOST_TX','/HOST_RX'):
                        assert zn.startswith('unconnected-')
                        status='UART absent on host slot 3'
                    else:
                        assert zn == expected,(ref,number,an,zn,expected)
                        status='Matches'
                rows.append({'Host slot':ref,'Contact':number,'Host net':zn,'Card net':an,'Result':status})

    # Check direction through the actual four series links to named MCU pins.
    sch=parse((B/'hardware/daughterboard/MotionController.kicad_sch').read_text(encoding='utf8'))
    symbols=allof(sch,'symbol')
    u1=next(s for s in symbols if any(q[1:3]==['Reference','U1'] for q in allof(s,'property')))
    lib=next(s for s in allof(get(sch,'lib_symbols'),'symbol') if s[1]==val(u1,'lib_id'))
    pin_by_name={val(pin,'name'):val(pin,'number') for pin in walk(lib,'pin')}
    for net,ref,gpio in [('/HOST_TX','R3','GPIO29'),('/HOST_RX','R4','GPIO28'),
                         ('/HOST_SCL','R5','GPIO31'),('/HOST_SDA','R6','GPIO30')]:
        rp=pads(cf[ref]); up=pads(cf['U1'])[pin_by_name[gpio]]
        assert {q.GetNetname() for q in rp.values()} == {net,up.GetNetname()},(ref,gpio)

    mount=sorted(local(cf['J1'],q) for q in cf['J1'].Pads() if not q.GetNumber())
    assert mount == [(-5.08,-2.54),(83.82,-2.54)]
    assert all(2.7 <= mm(q.GetDrillSize().x) <= 2.9 for q in cf['J1'].Pads() if not q.GetNumber())
    ph={'J3':4,'J4':4,'J5':4,'J6':8,'J13':3,'J14':4,'J15':5,'J16':2,'J17':2}
    for ref,n in ph.items():
        q=pads(cf[ref]); assert set(q)=={str(i) for i in range(1,n+1)}
        for i in range(1,n):
            a,z=q[str(i)].GetPosition(),q[str(i+1)].GetPosition()
            assert abs(math.hypot(mm(a.x-z.x),mm(a.y-z.y))-2.0)<1e-5
        assert all(0.70 <= mm(a.GetDrillSize().x) <= 0.80 for a in q.values())
    headers={'J2':(5,1.27,0.65),'J19':(4,1.27,0.65),'J12':(6,2.54,1.0)}
    for ref,(n,pitch,drill) in headers.items():
        q=pads(cf[ref]); assert set(q)=={str(i) for i in range(1,n+1)}
        for i in range(1,n):
            a,z=q[str(i)].GetPosition(),q[str(i+1)].GetPosition()
            assert abs(math.hypot(mm(a.x-z.x),mm(a.y-z.y))-pitch)<1e-5,(ref,i)
        assert all(mm(a.GetDrillSize().x)==drill and mm(a.GetDrillSize().y)==drill for a in q.values()),ref
    slot_spacing=abs(mm(hf['J1'].GetPosition().y-hf['J2'].GetPosition().y))
    assert slot_spacing == 26.0
    assert abs(mm(hf['J2'].GetPosition().y-hf['J3'].GetPosition().y)) == slot_spacing
    report={'host_contacts_compared':len(rows),'full_interface_slots':['J1','J2'],
            'slot_J3_uart_available':False,'host_slot_spacing_mm':slot_spacing,
            'DIN_hole_pattern':'matches WingTAT drawing 9001D11001 R7',
            'JST_PH_footprints_checked':len(ph),'unshrouded_header_footprints_checked':len(headers),
            'card_power_contacts':{
                net:sum(q.GetNetname()==net for q in cp.values()) for net in ('GND','+12V_BP','+5V_BP')},
            'unused_card_contacts':sum(q.GetNetname().startswith('unconnected-') for q in cp.values()),
            'mechanical_mating_and_cable_clearance_verified':False}
    out=B/'build';out.mkdir(exist_ok=True)
    with (out/'host-interface-check.csv').open('w',newline='',encoding='utf8') as stream:
        writer=csv.DictWriter(stream,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    (out/'host-interface-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__': main()
