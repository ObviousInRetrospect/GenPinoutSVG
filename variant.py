import re,sys,csv
from pprint import pprint
apins={}
apin2pin={}
anapins={}
fake_pins=[]
pinswap={} #'SPI':{},'WIRE':{}
fns={}
pin2timer={}
mode="std"
timer_dpin=0
with open(sys.argv[1],'r') as f:
    for l in f:
        l=l.strip()
        m=re.search('#define PIN_(P[ABCDEFG][0-7])\s+\(([0-9]*)\)',l)
        if m:
            apins[m.group(1)]=int(m.group(2))
            apin2pin[int(m.group(2))]=m.group(1)
        m=re.search('#define FAKE_PIN_(P[ABCDEFG][0-7])',l)
        if m:
            fake_pins.append(m.group(1))
        """ generalized this
        m=re.search('#define PIN_SPI_([A-Z]*)(?:_PINSWAP_([0-9]))?\s+PIN_(P[ABCDEFG][0-7])',l)
        if m:
            pos=m.group(2)
            if not pos:
                pos='0'
            pos=int(pos)
            if not m.group(1) in pinswap['SPI']:
                pinswap['SPI'][m.group(1)]={}
            pinswap['SPI'][m.group(1)][int(pos)]=m.group(3)
            if not m.group(3) in fns:
                fns[m.group(3)]=[]
            fns[m.group(3)].append(('SPI',m.group(1),pos))
        m=re.search('#define PIN_WIRE_([A-Z]*)(?:_PINSWAP_([0-9]))?\s+PIN_(P[ABCDEFG][0-7])',l)
        if m:
            pos=m.group(2)
            if not pos:
                pos='0'
            pos=int(pos)
            if not m.group(1) in pinswap['WIRE']:
                pinswap['WIRE'][m.group(1)]={}
            pinswap['WIRE'][m.group(1)][pos]=m.group(3)
            if not m.group(3) in fns:
                fns[m.group(3)]=[]
            fns[m.group(3)].append(('WIRE',m.group(1),pos))
        m=re.search('#define PIN_(HWSERIAL[0-9])_([A-Z]*)(?:_PINSWAP_([0-9]))?\s+PIN_(P[ABCDEFG][0-7])',l)
        if m:
            pos=m.group(3)
            if not pos:
                pos='0'
            pos=int(pos)
            if not m.group(1) in pinswap:
                pinswap[m.group(1)]={}
            if not m.group(2) in pinswap[m.group(1)]:
                pinswap[m.group(1)][m.group(2)]={}
            pinswap[m.group(1)][m.group(2)][pos]=m.group(4)
            if not m.group(4) in fns:
                fns[m.group(4)]=[]
            fns[m.group(4)].append((m.group(1),m.group(2),pos))
        """
        for dev in ['WIRE','SPI','HWSERIAL']:
            m=re.search('#define PIN_('+dev+'(?:[0-9])?)_([A-Z]*)(?:_PINSWAP_([0-9]))?\s+PIN_(P[ABCDEFG][0-7])',l)
            if m:
                pos=m.group(3)
                if not pos:
                    pos='0'
                pos=int(pos)
                if not m.group(1) in pinswap:
                    pinswap[m.group(1)]={}
                if not m.group(2) in pinswap[m.group(1)]:
                    pinswap[m.group(1)][m.group(2)]={}
                pinswap[m.group(1)][m.group(2)][pos]=m.group(4)
                if not pos in pinswap[m.group(1)]:
                    pinswap[m.group(1)][pos]={}
                pinswap[m.group(1)][pos][m.group(2)]=m.group(4)
                if not m.group(4) in fns:
                    fns[m.group(4)]=[]
                fns[m.group(4)].append((m.group(1),m.group(2),pos))
        m=re.search('#define PIN_A([0-7]+)\s+PIN_(P[ABCDEFG][0-7])',l)
        if m:
            anapins[m.group(2)]=int(m.group(1))
        if mode=='timer':
            if re.search('};',l):
                mode='std'
            if not re.search('NOT_ON_TIMER',l):
                m=re.search('([A-Za-z0-9_]+)',l)
                if m:
                    pin2timer[apin2pin[timer_dpin]]=m.group(1)
            timer_dpin+=1
        if re.search('const uint8_t digital_pin_to_timer',l):
            mode='timer'
            timer_dpin=0
            
        #todo: parse digital_pin_to_timer[]

for p in fake_pins:
    if p in apins:
        print("fake",p)
        del apins[p]

print('apins',apins)
print('anapins',anapins)
print('pin2timer',pin2timer)
print('fake_pins',fake_pins)
#define PIN_(P[ABCDEFG][0-7])\w+\(([0-9]*))\)
print('pinswap=')
pprint(pinswap)
print('fns=')
pprint(fns)
#pprint(apin2pin)

mux2var='SS'
field2pos=None
hdr=None

if(len(sys.argv)>2):
    with open(sys.argv[2],'r') as f:
        muxread=csv.reader(f)
        for row in muxread:
            if not field2pos: #header
                field2pos={}
                hdr=row
                for i in range(0,len(row)):
                    field2pos[row[i]]=i
            print(row)
            for k in field2pos:
                me=row[field2pos[k]]
                mes=me.split('\\\\n')
                #print(me,mes)
                for e in mes:
                    m=re.search('(?:([0-9]),)?([A-Za-z])+\(3\)')
                    if m:
                        pass
print(field2pos)
