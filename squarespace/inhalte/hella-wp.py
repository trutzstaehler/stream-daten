import numpy as np, json
from PIL import Image, ImageDraw
im=np.array(Image.open('hella-map.png').convert('RGB')).astype(int); H,W,_=im.shape
dark=im.sum(2)/3; blue=im[:,:,2]-im[:,:,0]
W_=lambda pts,ox,oy:[(ox+x/2,oy+y/2) for x,y in pts]
C=lambda pts,ox,oy:[(ox+x/4,oy+y/4) for x,y in pts]
# Start → Reeperbahn → Königstraße → Holländische Reihe → (3) → Palmaille → Breite Straße → St. Pauli Hafenstraße
west=C([(1180,92),(1010,90),(900,100),(820,118),(700,150),(560,168),(420,170),(280,170),(180,148),(90,140),(85,190),(85,240),(180,232),(400,225),(650,228),(880,225),(920,230),(970,262),(1030,236),(1100,222),(1240,220)],30,360)
# Landungsbrücken → Vorsetzen → Speicherstadt → (9)
hafen=C([(40,95),(110,108),(180,125),(260,150),(340,185),(430,188),(500,152),(570,160),(660,162),(730,155),(845,85),(935,75),(1005,40)],320,390)
# Hauptbahnhof-Bogen → Lombardsbrücke (11) → Kennedybrücke → (12)
hbf=C([(415,500),(420,430),(412,365),(395,305),(368,258),(332,218),(290,184),(240,152),(195,130),(160,120),(152,104),(195,108),(240,122),(285,136),(330,150),(420,125),(500,90)],470,270)
HBF=set(hbf)
# Ostufer: (12) → (13) → (14) → (15) → (16)
ost=C([(140,1010),(245,905),(295,835),(320,800),(308,718),(298,650),(236,596),(152,532),(116,437),(95,362),(165,325),(147,232),(117,140),(55,30)],560,40)
# Norden: (16) → Diagonale → (17) → Westufer runter
nord=C([(300,38),(235,95),(170,152),(180,182),(255,283),(195,335),(130,352),(160,365),(198,380),(225,420),(232,480),(235,600)],480,0)
# Westufer → (19) → Dammtor → Schleife → Esplanade → (21) → Ziel
damm=C([(580,0),(580,90),(465,100),(447,160),(412,312),(345,378),(385,398),(408,440),(410,485),(360,475),(280,466),(200,470),(150,482),(135,437)],400,180)
P=west+hafen+hbf+ost+nord+damm
def snap(x,y,r=4):
    best=None
    for yy in range(int(y)-r,int(y)+r+1):
        for xx in range(int(x)-r,int(x)+r+1):
            if 0<=xx<W and 0<=yy<H and blue[yy,xx]>=10:
                s=dark[yy,xx]+((xx-x)**2+(yy-y)**2)*3
                if best is None or s<best[0]: best=(s,xx,yy)
    return (best[1],best[2]) if best else (x,y)
S=[(x,y) if (x,y) in HBF and 0.2<(hbf.index((x,y))/len(hbf))<0.8 else snap(x,y) for x,y in P]
json.dump(S,open('hella-wp.json','w'))
img=Image.open('hella-map.png').convert('RGB'); d=ImageDraw.Draw(img)
d.line(S,fill=(255,0,90),width=2)
for x,y in S: d.ellipse((x-2,y-2,x+2,y+2),fill=(0,200,0))
img.resize((W*2,H*2)).save('hella-wp.png'); print(len(S))
