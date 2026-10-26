import numpy as np
m=np.load('alster-mask.npy'); H,W=m.shape
m=np.pad(m,1)
# Moore-Nachbarschaft: Rand nachziehen
ys,xs=np.nonzero(m); i=np.argmin(ys*10000+xs); start=(ys[i],xs[i])
nb=[(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
cur=start; prev_dir=6; pts=[cur]
for _ in range(20000):
    for k in range(8):
        d=(prev_dir+6+k)%8   # links drehen
        ny,nx=cur[0]+nb[d][0],cur[1]+nb[d][1]
        if m[ny,nx]:
            cur=(ny,nx); prev_dir=d; break
    if cur==start: break
    pts.append(cur)
P=np.array([(x-1,y-1) for y,x in pts],float); print('Randpunkte',len(P))
def rdp(p,eps):
    if len(p)<3: return p
    a,b=p[0],p[-1]; ab=b-a; n=np.hypot(*ab) or 1
    v=p-a; d=np.abs(ab[0]*v[:,1]-ab[1]*v[:,0])/n; i=np.argmax(d)
    if d[i]>eps: return np.vstack([rdp(p[:i+1],eps)[:-1],rdp(p[i:],eps)])
    return np.array([a,b])
k=np.argmax(np.hypot(*(P-P[0]).T)); S=np.vstack([rdp(P[:k+1],1.7)[:-1], rdp(np.vstack([P[k:],P[:1]]),1.7)[:-1]])
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
