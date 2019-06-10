import numpy as np

from cost import *
# UNTITLED2     Summary    of    this    function    goes    here    % Detailed    explanation    goes    here    X = zeros(n, m); % assignment    matrix    y = zeros(1, m); % servers    status(1, 0)    on / off
# return X,y,Costmin, Power

def ffd(n, m, Pbusy, Pidle, Rp, Rm, Tp, Tm):
    X = np.zeros((n, m))  # assignment matrix
    y = np.zeros(( m))  # servers status (1,0) on/off
    for k in range (0,n):

        for j in range (0,m):

            Rpj = 0
            Rmj = 0

            if ((y[j] == 0) and (Rp[k] <= Tp[j])):
                if (Rm[k] <= Tm[j]):
                    #print("PM turned on")
                    y[j] = 1
                    X[k, j] = 1
                break

            elif(y[j] == 1):

                for i in range(0,n):
                    Rpj = Rpj + X[i, j] * Rp[i]
                    Rmj = Rmj + X[i, j] * Rm[i]

                if ((Rpj + Rp[k]) <= Tp[j]) and ((Rmj + Rm[k]) <= Tm[j]):
                    X[k, j] = 1
                    break

    power_use = cost(n, m, Pbusy, Pidle, X, y, Rp, Rm, Tp, Tm)
    return X,y,power_use
