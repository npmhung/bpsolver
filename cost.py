import numpy as np


#m = number of PM
#n = number of VMs
#returns total computational power begin utilized in the current assignment in X
def cost(n,m,Pbusy,Pidle,X,y,Rp,Rm,Tp,Tm):

    Pt = 0
    for j in range(0, m):
        Rpj=0
        Rmj=0
        for i in range(0, n):
            Rpj = Rpj + X[i, j]*Rp[i]
            Rmj = Rmj + X[i, j] * Rm[i]
        if y[j]==1:
            Pt = Pt + y[j] * (1) * ((Pbusy - Pidle) * (Rpj/100) + Pidle);
    return Pt

