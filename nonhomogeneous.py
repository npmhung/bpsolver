from math import log
import stp

class HSolver:
    def __init__(self):
        self.vms = list()
        self.pms = list()

        self.solver = None

    def add_vm(self, cpu, mem, **kwargs):
        #n = len(self.vms)
        self.vms.append({'cpu': cpu, 'mem': mem})

    def add_pm(self, cpu, mem, pbusy, pidle, **kwargs):
        self.pms.append({'cpu': cpu, 'mem': mem, 'pbusy': pbusy, 'pidle': pidle})

    def build(self, max_power, bit_len=32):
        """
        n_pm: number of physical machine
        bit_len: this should be polynomial size of the number of PMs and VMs
        """
        self.solver = stp.Solver()
        s = self.solver

        n_vm = len(self.vms)
        n_pm = len(self.pms)
        assign = {i: {} for i in range(n_vm)}
        for vid in range(n_vm):
            vm_total_assignment = 0
            for pid in range(n_pm):
                tmp = self.solver.bitvec('%d_%d'%(vid, pid), bit_len)
                
                vm_total_assignment += tmp

                s.add(tmp>=0)
                s.add(tmp<=1)

                assign[vid][pid] = tmp

            s.add(vm_total_assignment == 1)

        total_power_consumption = 0
        for pid in range(n_pm):
            cpu_util = 0
            mem_util = 0
            
            # I assume that each PM is always turned on, so it always consumes P_idle energy
            # power consumption of each physical machine
            cpu_utilization = 0
            for vid in range(n_vm):
                cpu_util += self.vms[vid]['cpu']*assign[vid][pid]
                mem_util += self.vms[vid]['mem']*assign[vid][pid]
                cpu_utilization += assign[vid][pid]*self.vms[vid]['cpu']

            s.add(cpu_util <= self.pms[pid]['cpu'])
            s.add(mem_util <= self.pms[pid]['mem'])

            diff = self.pms[pid]['pbusy'] - self.pms[pid]['pidle']
            total_power_consumption += self.pms[pid]['pidle'] + cpu_utilization*diff

        s.add(total_power_consumption <= max_power)

        

    def check(self):
        assert (self.solver is not None)
        return self.solver.check()

    def assign(self):
        assert (self.solver is not None)
        ret = {}
        a = self.solver.model()
        
        for _ in a:
            vid, pid = _.split('_')
            vid = int(vid)
            pid = int(pid)

            val = a[_]
            if val == 0:
                continue
            
            
            if ret.get(pid, None) is None:
                ret[pid] = [vid]
            else:
                ret[pid].append(vid)


        return ret



def parse_ans(asignment, n_pm):
    a = assignment

    ret 
    for u in a:
        vid, pid = u.split('_')
        val = a[u]
        if val == 1:
            ret += 'VM {} is assigned to PM {}'


def M(vms, pms):
    """
    vms: [(cpu_i, mem_i), ...]
    cpu_cap: cpu capacity of each PM
    mem_cap: mem capacity of each PM
    """

    solver = HSolver()
    for params in vms:
        solver.add_vm(*params)

    for params in pms:
        solver.add_pm(*params)

    max_power = 0
    for cpu, _, busy, idle in pms:
        max_power += cpu*(busy-idle)+idle

    bit_len = int(log(max_power)/log(2)+1)

    ret = list('1'*bit_len)
    for idx in range(len(ret)):
        ret[idx]='0'
        solver.build(int(''.join(ret),2))
        if solver.check():
            continue
        ret[idx]='1'

    # check again
    ret = int(''.join(ret), 2)
    solver.build(ret)
    if solver.check():
        return ret, solver.assign()

    return -1, None


if __name__=='__main__': 
    vms = [(10,30), (50,30), (1,1), (1,1), (10,1), (55, 70)]
    pms = [(20, 20, 2, 1), (1000, 1000, 3, 3), (10, 30, 2, 1), (50, 30, 3, 1), (55, 70, 4, 1)]
    k, a = M(vms, pms)
    print(k)
    print(a)
    print('========================')
    vms = [(10,30), (50,30), (1,1), (1,1), (10,1), (55, 70)]
    pms = [(20, 20, 2, 1), (1000, 1000, 33333, 3), (10, 30, 2, 1), (50, 30, 3, 1), (55, 70, 4, 1)]
    k, a = M(vms, pms)
    print(k)
    print(a)
