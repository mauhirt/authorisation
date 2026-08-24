"""Shared local-linear RD machinery (triangular kernel, HC0 SEs). Pure stdlib."""
import math

def wls_side(data, bw, donut=0.0):
    """data: [(margin, y)] one side; returns (alpha, var_alpha, n)."""
    pts=[(m,y) for m,y in data if donut<abs(m)<=bw]
    n=len(pts)
    if n<10: return None,None,n
    S0=S1=S2=Sy=Smy=0.0
    for m,y in pts:
        w=1-abs(m)/bw
        S0+=w; S1+=w*m; S2+=w*m*m; Sy+=w*y; Smy+=w*m*y
    det=S0*S2-S1*S1
    if det<=0: return None,None,n
    a=(S2*Sy-S1*Smy)/det; b=(S0*Smy-S1*Sy)/det
    inv00,inv01=S2/det,-S1/det
    B00=B01=B11=0.0
    for m,y in pts:
        w=1-abs(m)/bw; e=y-a-b*m; we2=(w*e)**2
        B00+=we2; B01+=we2*m; B11+=we2*m*m
    va=inv00*inv00*B00+2*inv00*inv01*B01+inv01*inv01*B11
    return a,va,n

def rd(pairs, bw, donut=0.0):
    """pairs: [(margin, y)] both sides; returns dict or None."""
    dl=[(m,y) for m,y in pairs if m<0 and y is not None]
    dr=[(m,y) for m,y in pairs if m>0 and y is not None]
    aL,vL,nL=wls_side(dl,bw,donut); aR,vR,nR=wls_side(dr,bw,donut)
    if aL is None or aR is None: return None
    tau=aR-aL; se=math.sqrt(vL+vR)
    return dict(tau=tau,se=se,z=(tau/se if se>0 else 0),nL=nL,nR=nR,aL=aL,aR=aR)
