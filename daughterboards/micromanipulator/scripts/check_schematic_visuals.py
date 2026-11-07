"""Audit actual plotted text bounds against schematic wires, plus crossings."""
from pathlib import Path
import re,json,xml.etree.ElementTree as ET
from sexp import *
B=Path(__file__).resolve().parent.parent;H=B/'hardware/daughterboard'
ns={'s':'http://www.w3.org/2000/svg'}
result={}
def cross(b,c,pad=0):return b[0]<c[2]+pad and c[0]<b[2]+pad and b[1]<c[3]+pad and c[1]<b[3]+pad
for f in H.glob('*.kicad_sch'):
    svg=B/'docs/schematics'/('FabNanoDaughterboard'+('' if f.stem=='FabNanoDaughterboard' else '-'+f.stem)+'.svg')
    root=ET.parse(svg).getroot();d=parse(f.read_text(encoding='utf8'))
    wires=[tuple(tuple(q[1:]) for q in allof(get(w,'pts'),'xy')) for w in allof(d,'wire')]
    ts=[]
    for g in root.findall('.//s:g[@class="stroked-text"]',ns):
        name=g.findtext('s:desc',namespaces=ns)
        xy=[]
        for p in g.findall('.//s:path',ns):
            nums=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',p.get('d',''))]
            xy+=list(zip(nums[::2],nums[1::2]))
        if xy:ts.append((name,(min(x for x,y in xy)-.0762,min(y for x,y in xy)-.0762,max(x for x,y in xy)+.0762,max(y for x,y in xy)+.0762)))
    ts=list(dict.fromkeys(ts)) # Identical overprinted glyphs are visually one text.
    tw=[];tt=[];wc=[];ol=[]
    for text,bb in ts:
        for a,b in wires:
            wb=(min(a[0],b[0])-.0762,min(a[1],b[1])-.0762,max(a[0],b[0])+.0762,max(a[1],b[1])+.0762)
            if cross(bb,wb):tw.append({'text':text,'bbox':bb,'wire':[a,b]})
    for i,(text,bb) in enumerate(ts):
        for other,ob in ts[i+1:]:
            if cross(bb,ob):tt.append({'texts':[text,other],'bboxes':[bb,ob]})
    js={tuple(get(n,'at')[1:3]) for n in allof(d,'junction')}
    for i,(a,b) in enumerate(wires):
        for c,e in wires[i+1:]:
            if abs(a[1]-b[1])<.0001 and abs(c[0]-e[0])<.0001 and min(a[0],b[0])+.001<c[0]<max(a[0],b[0])-.001 and min(c[1],e[1])+.001<a[1]<max(c[1],e[1])-.001:
                wc.append({'at':[c[0],a[1]],'junction':(c[0],a[1]) in js,'wires':[[a,b],[c,e]]})
            if abs(a[0]-b[0])<.0001 and abs(c[1]-e[1])<.0001 and min(c[0],e[0])+.001<a[0]<max(c[0],e[0])-.001 and min(a[1],b[1])+.001<c[1]<max(a[1],b[1])-.001:
                wc.append({'at':[a[0],c[1]],'junction':(a[0],c[1]) in js,'wires':[[a,b],[c,e]]})
            for axis in [0,1]:
                o=1-axis
                if max(abs(a[o]-b[o]),abs(a[o]-c[o]),abs(a[o]-e[o]))<.0001:
                    overlap=min(max(a[axis],b[axis]),max(c[axis],e[axis]))-max(min(a[axis],b[axis]),min(c[axis],e[axis]))
                    if overlap>.001:ol.append([[a,b],[c,e]])
    result[f.stem]={'text_wire':tw,'text_text':tt,'wire_crossings':wc,'wire_overlaps':ol}
    print(f.stem,':',len(tw),'text/wire,',len(tt),'text/text,',len(wc),'crossings,',len(ol),'overlaps')
    for issue in tw:print('  text/wire',issue)
    for issue in tt:print('  text/text',issue)
    for issue in wc:print('  crossing',issue)
    for issue in ol:print('  overlap',issue)
(B/'build/schematic-visual-audit.json').write_text(json.dumps(result,indent=2)+'\n')

raise SystemExit(any(any(v.values()) for v in result.values()))
