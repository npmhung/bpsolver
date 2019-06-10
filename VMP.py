import numpy as np
from scipy.io import loadmat
from cost import *
from FFD import *

n = 200   #number of VMs
m = 200     #number of servers
Pbusy = 215 # average power(Watts) of server in busy state
Pidle = 162 # average power(Watts) of server in idle state
# --> assumption thresholds of each server is 100.

# threshold for cpu and memory.. assuming homogeneous system
Tp = 0.9*np.ones(m) # threshold of processor usage
Tm = 0.9*np.ones(m) # threshold of memory usage



# X = np.zeros((n,m)) # assignment matrix
# y = np.zeros( (1,m) ) # servers status (1,0) on/off



x = loadmat('Acomp_200.mat') # generated benchmark with different correlation and probabilities
input = x['CellTwentyFivePercent'] # using dataset with 25% average value
correlation = 0
input = np.array(input[correlation])  #correlation = 0 (negative), 1(weak negative), 2(zero), 3(weak positive), 4(positive)
Rp = input[0][:,0]/100
Rm = input[0][:,1]/100
X,y,power_ffd = ffd(n,m,Pbusy,Pidle,Rp,Rm,Tp,Tm)

print("RESULTS FOR FFD")
print("=================")
print("assignment matrix: \n",X)
print("Pt: ", power_ffd)
print("server used: ", np.sum(y))


## SMT solver goes here 
