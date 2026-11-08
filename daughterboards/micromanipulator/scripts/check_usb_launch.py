"""Measure USB launch geometry and sample its adjacent ground references.

Requires KiCad's pcbnew Python. This is a geometric check, not an impedance
solver, propagation-delay model or USB compliance test. Signal-via antipads
within 0.6 mm are reported separately, not treated as a plane split.
"""
from pathlib import Path
import argparse, math, json, heapq
import pcbnew as p

B=Path(__file__).resolve().parents[1]
def xy(q):return (round(p.ToMM(q.x),6),round(p.ToMM(q.y),6))
def pt(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def on(q,a,z):return abs(math.dist(a,q)+math.dist(q,z)-math.dist(a,z))<1e-5

def inspect(file,reference_check=True):
    b=p.LoadBoard(str(file));fps={f.GetReference():f for f in b.GetFootprints()}
    planes={layer:[z.GetFilledPolysList(layer) for z in b.Zones() if z.GetLayer()==layer and z.GetNetname()=='GND'] for layer in [p.In1_Cu,p.In2_Cu]}
    all_vias=[xy(t.GetPosition()) for t in b.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetNetname() in ['/USB_D+','/USB_D-']]
    rows=[]
    for net,contacts,r in [('/USB_D+',['A6','B6'],'R7'),('/USB_D-',['A7','B7'],'R8')]:
        items=[t for t in b.GetTracks() if t.GetNetname()==net]
        vias=[t for t in items if isinstance(t,p.PCB_VIA)]
        tracks=[t for t in items if not isinstance(t,p.PCB_VIA)]
        missing=[];counts={'F.Cu':0,'B.Cu':0};skipped=0
        for t in tracks:
            layer=t.GetLayer();a,z=xy(t.GetStart()),xy(t.GetEnd())
            if layer==p.F_Cu and max(a[0],z[0])>66:continue  # MCU fanout checked separately.
            assert layer in (p.F_Cu,p.B_Cu)
            reference=p.In1_Cu if layer==p.F_Cu else p.In2_Cu
            length=math.dist(a,z);steps=max(1,math.ceil(length/.05))
            for i in range(steps+1):
                x,y=(a[j]+(z[j]-a[j])*i/steps for j in [0,1])
                if min(math.dist((x,y),v) for v in all_vias)<.6:skipped+=1;continue
                for off in [0,-p.ToMM(t.GetWidth())/2,p.ToMM(t.GetWidth())/2]:
                    q=(x-(z[1]-a[1])/length*off,y+(z[0]-a[0])/length*off)
                    counts[b.GetLayerName(layer)]+=1
                    if not any(poly.Contains(pt(*q)) for poly in planes[reference]):missing.append([b.GetLayerName(layer),*map(lambda v:round(v,4),q)])
        # Shortest copper path between connector and resistor, with layer changes
        # counted separately. Do not substitute branched copper totals for delay.
        segs=[(t.GetLayer(),xy(t.GetStart()),xy(t.GetEnd())) for t in tracks]
        nodes={(layer,q) for layer,a,z in segs for q in (a,z)}
        points={c:xy(next(q for q in fps['J18'].Pads() if q.GetNumber()==c).GetPosition()) for c in contacts}
        target=xy(next(q for q in fps[r].Pads() if q.GetNumber()=='2').GetPosition())
        nodes|={(p.F_Cu,q) for q in [*points.values(),target]}
        for v in vias:nodes|={(layer,xy(v.GetPosition())) for layer in (p.F_Cu,p.B_Cu)}
        graph={q:[] for q in nodes}
        for layer,a,z in segs:
            pts=sorted((q for q in nodes if q[0]==layer and on(q[1],a,z)),key=lambda q:math.dist(a,q[1]))
            for u,v in zip(pts,pts[1:]):
                d=math.dist(u[1],v[1]);graph[u].append((v,d,0));graph[v].append((u,d,0))
        for v in vias:
            a,z=(p.F_Cu,xy(v.GetPosition())),(p.B_Cu,xy(v.GetPosition()))
            graph[a].append((z,0,1));graph[z].append((a,0,1))
        paths={}
        for contact,point in points.items():
            queue=[(0.,0,(p.F_Cu,point))];seen=set();answer=None
            while queue:
                distance,transitions,node=heapq.heappop(queue)
                if node in seen:continue
                seen.add(node)
                if node==(p.F_Cu,target):answer={'copper_mm':round(distance,3),'signal_layer_changes':transitions};break
                for other,d,v in graph[node]:
                    if other not in seen:heapq.heappush(queue,(distance+d,transitions+v,other))
            assert answer,(net,contact);paths[contact+' to '+r+'.2']=answer
        if reference_check:assert not missing,(net,missing[:12])
        rows.append({'net':net,'signal_vias':len(vias),'copper_inventory_mm':round(sum(p.ToMM(t.GetLength()) for t in tracks),3),
                     'connector_to_termination':paths,'ground_reference_samples':counts,'skipped_via_launch_samples':skipped,'missing_ground_samples':len(missing)})
    zones=[{'net':z.GetNetname(),'layer':b.GetLayerName(z.GetLayer()),'regions':z.GetFilledPolysList(z.GetLayer()).OutlineCount()} for z in b.Zones() if z.GetLayer() in [p.In1_Cu,p.In2_Cu]]
    if reference_check:assert all(q['regions']==1 for q in zones),zones
    return {'data_nets':rows,'inner_zones':zones,'reference_check_enabled':reference_check}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--board',type=Path,default=B/'hardware/daughterboard/FabNanoDaughterboard.kicad_pcb')
    parser.add_argument('--compare',type=Path)
    args=parser.parse_args();report={'current':inspect(args.board)}
    if args.compare:report['previous']=inspect(args.compare,False)
    (B/'build').mkdir(exist_ok=True)
    (B/'build/usb-launch-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
