import re,json
class S(str): pass
def parse(text):
    tokens=re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+',text)
    stack=[]; root=None
    for t in tokens:
        if t=='(':
            n=[]
            if stack: stack[-1].append(n)
            else: root=n
            stack.append(n)
        elif t==')': stack.pop()
        elif t.startswith('"'): stack[-1].append(json.loads(t))
        else:
            try: v=float(t) if '.' in t else int(t)
            except ValueError: v=S(t)
            stack[-1].append(v)
    return root
def dumps(v,depth=0):
    if isinstance(v,list):
        if not any(isinstance(x,list) for x in v): return '('+' '.join(dumps(x) for x in v)+')'
        s='('+str(v[0])
        for x in v[1:]: s+= ('\n'+'  '*(depth+1) if isinstance(x,list) else ' ')+dumps(x,depth+1)
        return s+')'
    if isinstance(v,S): return str(v)
    if isinstance(v,str): return json.dumps(v,ensure_ascii=False)
    return str(v)
def allof(v,key): return [x for x in v if isinstance(x,list) and x and x[0]==key]
def get(v,key,default=None): return next(iter(allof(v,key)),default)
def val(v,key,default=None):
    n=get(v,key)
    return n[1] if n else default
def walk(v,key):
    for x in v:
        if isinstance(x,list):
            if x and x[0]==key: yield x
            yield from walk(x,key)
if __name__=='__main__':
    from pathlib import Path
    base=Path('C:/Program Files/KiCad/10.0/share/kicad/symbols')
    for lib,names in {'MCU_RaspberryPi':['RP2350A'],'Driver_Motor':['TB6612FNG','DRV8837C'],'MCU_ST_STM32F1':['STM32F103C8Tx','STM32F103C6Tx'],'Memory_Flash':['W25Q32JVSS'],'Regulator_Linear':['AP2112K-3.3'],'Regulator_Switching':['TPS5450DDA'],'Connector':['DIN41612_3x32_A','DIN41612_3x32_ABC']}.items():
        doc=parse((base/(lib+'.kicad_sym')).read_text(encoding='utf-8'))
        for sym in allof(doc,'symbol'):
            if sym[1] in names:
                print(lib,sym[1], 'extends',val(sym,'extends'),[(p[1],p[2]) for p in allof(sym,'property') if p[1]=='Footprint'])
                print([(val(p,'number'),val(p,'name'),p[1],get(p,'at')[1:]) for p in walk(sym,'pin')])
