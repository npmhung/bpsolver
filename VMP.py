import numpy as np
from scipy.io import loadmat
from cost import *
from FFD import *

n = 15   #number of VMs
m = 10   #number of servers
Pbusy = 215 # average power(Watts) of server in busy state
Pidle = 162 # average power(Watts) of server in idle state
# --> assumption thresholds of each server is 100.

# threshold for cpu and memory.. assuming homogeneous system
#Tp = 90*np.ones(m) # threshold of processor usage
#Tm = 90*np.ones(m) # threshold of memory usage
Tp = (np.random.rand(m)*100).round()
Tm = (np.random.rand(m)*100).round()



# X = np.zeros((n,m)) # assignment matrix
# y = np.zeros( (1,m) ) # servers status (1,0) on/off



x = loadmat('Acomp_200.mat') # generated benchmark with different correlation and probabilities
input = x['CellTwentyFivePercent'] # using dataset with 25% average value
correlation = 0
input = np.array(input[correlation])  #correlation = 0 (negative), 1(weak negative), 2(zero), 3(weak positive), 4(positive)
Rp = input[0][:,0].round()
Rm = input[0][:,1].round()
X,y,power_ffd = ffd(n,m,Pbusy,Pidle,Rp,Rm,Tp,Tm)

print("RESULTS FOR FFD")
print("=================")
if X.sum()<n:
    print("Only %d vms can be assigned."%X.sum())
    print(X)
    print("Cannot find a suitable assignment")
else:
    print("assignment matrix: \n",X)
    print("Pt: ", power_ffd)
    print("server used: ", np.sum(y))


## SMT solver goes here

Rp = [int(u) for u in input[0][:, 0].round()]
Rm = [int(u) for u in input[0][:, 1].round()]
vms = list(zip(Rp, Rm))

cpu = [int(u) for u in Tp]
mem = [int(u) for u in Tm]
busy = [Pbusy]*m
idle = [Pidle]*m
pms = list(zip(cpu, mem, busy, idle))


from nonhomogeneous import M as stp_solver
power, assign = stp_solver(vms[:n], pms[:m])
print("========================")
print("========================")
print("")
print("RESULTS FOR STP SOLVER")
print("=======================")
if assign is None:
    print("Cannot find a suitable assignment")
else:
    print("assignment", assign)
    print("Pt: ", power)
    print("server used: ", len(assign))
