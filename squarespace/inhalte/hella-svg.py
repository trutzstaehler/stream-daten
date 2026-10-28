import numpy as np, json
from PIL import Image, ImageFilter
from collections import deque
im=np.array(Image.open('hella-map.png').convert('RGB')).astype(int); H,W,_=im.shape
S=np.array(json.load(open('hella-wp.json')),float)
# Strecke verdichten
dense=[S[0]]
for a,b in zip(S,S[1:]):
    n=max(1,int(np.hypot(*(b-a))/2))
    for t in np.linspace(0,1,n+1)[1:]: dense.append(a+(b-a)*t)
R=np.array(dense)
seg=np.r_[0,np.cumsum(np.hypot(*np.diff(R,axis=0).T))]; total=seg[-1]
MK=[(0,326,383),(1,228,378),(2,150,391),(3,56,386),(4,100,424),(5,192,425),(6,285,432),(7,372,437),(8,458,441),(9,541,392),(10,552,346),(11,515,287),(12,582,281),(13,648,220),(14,603,151),(15,596,72),(16,540,10),(17,520,80),(18,527,139),(19,515,198),(20,487,284),(21,430,300),(21.0975,434,286)]
fr=[];last=0
for km,x,y in MK:
    # nächster Streckenpunkt NACH dem vorigen (Reihenfolge erzwingen)
    d=np.hypot(R[last:,0]-x,R[last:,1]-y); i=last+int(np.argmin(d[:max(5,len(d))]))
    if km==0: i=0
    if km==21.0975: i=len(R)-1
    fr.append(round(seg[i]/total,4)); last=i
# Wasser
wat=(np.abs(im-np.array([208,235,244])).sum(2)<28)
wat=np.array(Image.fromarray((wat*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(3)))>127
lab=np.zeros((H,W),int); comps=[]; n=0
for y in range(H):
  for x in range(W):
    if wat[y,x] and not lab[y,x]:
      n+=1; q=deque([(y,x)]); lab[y,x]=n; c=0
      while q:
        cy,cx=q.popleft(); c+=1
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
          ny,nx=cy+dy,cx+dx
          if 0<=ny<H and 0<=nx<W and wat[ny,nx] and not lab[ny,nx]: lab[ny,nx]=n; q.append((ny,nx))
      comps.append((c,n))
comps=sorted(comps,reverse=True)[:4]
def trace(mask):
    ys,xs=np.nonzero(mask); i=np.argmin(ys*100000+xs); r0,c0=int(ys[i]),int(xs[i])
    D={'E':(0,1),'S':(1,0),'W':(0,-1),'N':(-1,0)}; L={'E':'N','N':'W','W':'S','S':'E'}; Rr={v:k for k,v in L.items()}
    la=lambda y,x,d:{'E':(y-1,x),'S':(y,x),'W':(y,x-1),'N':(y-1,x-1)}[d]
    ra=lambda y,x,d:{'E':(y,x),'S':(y,x-1),'W':(y-1,x-1),'N':(y-1,x)}[d]
    f=lambda p: 0<=p[0]<H and 0<=p[1]<W and mask[p]
    y,x,d=r0,c0,'E'; pts=[]
    for _ in range(400000):
        if f(la(y,x,d)): d=L[d]
        elif f(ra(y,x,d)): pass
        else: d=Rr[d]
        y,x=y+D[d][0],x+D[d][1]; pts.append((x,y))
        if (y,x)==(r0,c0) and len(pts)>4: break
    return np.array(pts,float)
def rdp(p,eps):
    if len(p)<3: return p
    a,b=p[0],p[-1]; ab=b-a; nn=np.hypot(*ab) or 1; v=p-a; dd=np.abs(ab[0]*v[:,1]-ab[1]*v[:,0])/nn; i=np.argmax(dd)
    if dd[i]>eps: return np.vstack([rdp(p[:i+1],eps)[:-1],rdp(p[i:],eps)])
    return np.array([a,b])
def chaikin(P,it,closed):
    for _ in range(it):
        Q=[] if closed else [P[0]]
        rng=range(len(P)) if closed else range(len(P)-1)
        for j in rng:
            p,q=P[j],P[(j+1)%len(P)]; Q+=[0.75*p+0.25*q,0.25*p+0.75*q]
        if not closed: Q.append(P[-1])
        P=np.array(Q)
    return P
waters=[]
for c,nid in comps:
    P=trace(lab==nid); k=len(P)//2
    Q=np.vstack([rdp(P[:k+1],2.2)[:-1],rdp(P[k:],2.2)[:-1]]); waters.append(chaikin(Q,3,True))
# Ausschnitt: Strecke + Rand
x0,y0=R.min(0)-14; x1,y1=R.max(0)+14
sc=1000/(x1-x0)
tr=lambda P:(np.array(P)-[x0,y0])*sc
fmt=lambda P:'M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in tr(P))
Rs=chaikin(rdp(R,0.6),2,False)
out={'vb':f'0 0 1000 {(y1-y0)*sc:.0f}','route':fmt(Rs),'water':[fmt(Q)+' Z' for Q in waters],'fr':fr,
     'start':tr([R[0]])[0].round(1).tolist(),'ziel':tr([R[-1]])[0].round(1).tolist()}
json.dump(out,open('hella-svg.json','w'))
print(out['vb'], len(out['route']), [len(w) for w in out['water']], out['fr'][:6], out['fr'][-4:])
