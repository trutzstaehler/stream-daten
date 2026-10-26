import numpy as np
from PIL import Image, ImageFilter
m=np.load('alster-mask.npy')
m=np.array(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)))>127
H,W=m.shape
m=np.pad(m,1)
# Rand Kante für Kante ablaufen (gefüllte Fläche immer rechts)
ys,xs=np.nonzero(m); i=np.argmin(ys*100000+xs); r0,c0=int(ys[i]),int(xs[i])
D={'E':(0,1),'S':(1,0),'W':(0,-1),'N':(-1,0)}
L={'E':'N','N':'W','W':'S','S':'E'}; R={v:k for k,v in L.items()}
def la(y,x,d): return {'E':(y-1,x),'S':(y,x),'W':(y,x-1),'N':(y-1,x-1)}[d]
def ra(y,x,d): return {'E':(y,x),'S':(y,x-1),'W':(y-1,x-1),'N':(y-1,x)}[d]
f=lambda p: m[p]
y,x,d=r0,c0,'E'; pts=[]
for _ in range(200000):
    if f(la(y,x,d)): d=L[d]
    elif f(ra(y,x,d)): pass
    else: d=R[d]
    y,x=y+D[d][0],x+D[d][1]; pts.append((y,x))
    if (y,x)==(r0,c0) and len(pts)>4: break
P=np.array([(x-1,y-1) for y,x in pts],float); print('Randpunkte',len(P))
def rdp(p,eps):
    if len(p)<3: return p
    a,b=p[0],p[-1]; ab=b-a; n=np.hypot(*ab) or 1
    v=p-a; d=np.abs(ab[0]*v[:,1]-ab[1]*v[:,0])/n; i=np.argmax(d)
    if d[i]>eps: return np.vstack([rdp(p[:i+1],eps)[:-1],rdp(p[i:],eps)])
    return np.array([a,b])
k=np.argmax(np.hypot(*(P-P[0]).T)); S=np.vstack([rdp(P[:k+1],1.3)[:-1], rdp(np.vstack([P[k:],P[:1]]),1.3)[:-1]])
# Chaikin-Glättung
for _ in range(3):
    Q=[]
    for j in range(len(S)):
        p,q=S[j],S[(j+1)%len(S)]; Q+= [0.75*p+0.25*q, 0.25*p+0.75*q]
    S=np.array(Q)
# Start im Süden (unterster Punkt nahe der Mitte), Richtung: zuerst nach Westen
cx=S[:,0].mean(); j=np.argmax(S[:,1]-0.15*np.abs(S[:,0]-cx)); S=np.roll(S,-j,axis=0)
if S[5,0]>S[0,0]: S=np.vstack([S[:1],S[1:][::-1]])
# in viewBox 300x430 einpassen (Rand 18 oben, 40 unten für Beschriftung)
x0,y0=S.min(0); x1,y1=S.max(0); sc=min((300-36)/(x1-x0),(430-18-40)/(y1-y0))
T=(S-[x0,y0])*sc+[ (300-(x1-x0)*sc)/2, 18]
d='M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in T)+' Z'
print('Punkte',len(T),'Länge d',len(d),'bbox',T.min(0).round(1),T.max(0).round(1),'start',T[0].round(1))
open('alster-path.txt','w').write(d)
