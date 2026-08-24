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

def wls_side_quad(data, bw, donut=0.0):
    """Local-QUADRATIC one-side fit, triangular kernel, HC0 var of the intercept.
    Returns (alpha, var_alpha, n)."""
    pts=[(m,y) for m,y in data if donut<abs(m)<=bw]
    n=len(pts)
    if n<15: return None,None,n
    # normal equations for X=[1,m,m^2]
    S=[[0.0]*3 for _ in range(3)]; b=[0.0]*3
    for m,y in pts:
        w=1-abs(m)/bw; x=(1.0,m,m*m)
        for i in range(3):
            b[i]+=w*x[i]*y
            for j in range(3): S[i][j]+=w*x[i]*x[j]
    # solve S beta = b (3x3 gaussian elim) and invert S
    def solve3(A,rhs):
        M=[A[i][:]+[rhs[i]] for i in range(3)]
        for c in range(3):
            p=max(range(c,3),key=lambda r:abs(M[r][c]))
            if abs(M[p][c])<1e-12: return None
            M[c],M[p]=M[p],M[c]
            for r in range(3):
                if r!=c:
                    fk=M[r][c]/M[c][c]
                    for k in range(c,4): M[r][k]-=fk*M[c][k]
        return [M[i][3]/M[i][i] for i in range(3)]
    beta=solve3(S,b)
    if beta is None: return None,None,n
    inv0=solve3(S,[1.0,0.0,0.0])          # first row of S^{-1}
    if inv0 is None: return None,None,n
    # HC0: var(alpha) = e0' S^{-1} (sum w^2 e^2 x x') S^{-1} e0
    va=0.0
    for m,y in pts:
        w=1-abs(m)/bw; x=(1.0,m,m*m)
        e=y-sum(bb*xx for bb,xx in zip(beta,x))
        s=sum(inv0[i]*x[i] for i in range(3))
        va+=(w*e*s)**2
    return beta[0],va,n

def rd_rbc(pairs, bw, donut=0.0):
    """CCT robust bias-corrected RD with rho=b/h=1: the bias-corrected point
    estimate equals the local-QUADRATIC estimate at bandwidth bw, and the robust
    variance is the quadratic fit's HC0 variance (Calonico-Cattaneo-Titiunik
    2014, Remark 7 special case). Returns dict or None."""
    dl=[(m,y) for m,y in pairs if m<0 and y is not None]
    dr=[(m,y) for m,y in pairs if m>0 and y is not None]
    aL,vL,nL=wls_side_quad(dl,bw,donut); aR,vR,nR=wls_side_quad(dr,bw,donut)
    if aL is None or aR is None: return None
    tau=aR-aL; se=math.sqrt(vL+vR)
    return dict(tau=tau,se=se,z=(tau/se if se>0 else 0),nL=nL,nR=nR,aL=aL,aR=aR)
