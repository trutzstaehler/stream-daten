import numpy as np
from PIL import Image, ImageFilter
from collections import deque
im=np.array(Image.open('alster-map.png').convert('RGB')).astype(int)
H,W,_=im.shape
water=np.array([170,211,223])
d=np.abs(im-water).sum(2)
# Wasser + blaue Beschriftungen/Linien auf Wasser (bläuliche Töne)
blueish=(im[:,:,2]>im[:,:,0]+15)&(im[:,:,2]>150)
pin=np.zeros((H,W),bool); pin[215:290,150:205]=True
mask=((d<40)|blueish|(pin&(im[:,:,0]>150))).astype(np.uint8)*255
m=Image.fromarray(mask)
m=m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))   # Schließen: Schrift/Linien füllen
opened=m.filter(ImageFilter.MinFilter(int(__import__('sys').argv[1]) if len(__import__('sys').argv)>1 else 11)).filter(ImageFilter.MaxFilter(int(__import__('sys').argv[1]) if len(__import__('sys').argv)>1 else 11))  # Öffnen: Kanäle kappen
a=np.array(opened)>127
import sys
cut=int(sys.argv[2]) if len(sys.argv)>2 else 0
a[:cut,:]=False
a[150:218,200:]=False
a[:150,240:]=False
# größte zusammenhängende Fläche
lab=np.zeros(a.shape,int); best=(0,0); n=0
for y in range(H):
  for x in range(W):
    if a[y,x] and not lab[y,x]:
      n+=1; q=deque([(y,x)]); lab[y,x]=n; cnt=0
      while q:
        cy,cx=q.popleft(); cnt+=1
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
          ny,nx=cy+dy,cx+dx
          if 0<=ny<H and 0<=nx<W and a[ny,nx] and not lab[ny,nx]: lab[ny,nx]=n; q.append((ny,nx))
      if cnt>best[0]: best=(cnt,n)
comp=lab==best[1]
# Löcher füllen
out=~comp; reach=np.zeros_like(out); q=deque()
for y in range(H):
  for x in (0,W-1):
    if out[y,x]: reach[y,x]=1; q.append((y,x))
for x in range(W):
  for y in (0,H-1):
    if out[y,x] and not reach[y,x]: reach[y,x]=1; q.append((y,x))
while q:
  cy,cx=q.popleft()
  for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
    ny,nx=cy+dy,cx+dx
    if 0<=ny<H and 0<=nx<W and out[ny,nx] and not reach[ny,nx]: reach[ny,nx]=1; q.append((ny,nx))
filled=~reach.astype(bool)
np.save('alster-mask.npy',filled)
vis=np.array(Image.open('alster-map.png').convert('RGB'))
vis[filled]=(vis[filled]*0.3+np.array([255,0,80])*0.7).astype(np.uint8)
Image.fromarray(vis).save('alster-mask.png'); print('area',filled.sum())
