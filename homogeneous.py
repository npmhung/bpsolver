from math import log
import stp

class HSolver:
    def __init__(self, pm_cpu, pm_mem):
        # capacity for each physical machine
        self.pm_cpu = pm_cpu
        self.pm_mem = pm_mem

        # 
        self.vms = list()

        self.solver = None

    def add_vm(self, cpu, mem, **kwargs):
        #n = len(self.vms)
        self.vms.append({'cpu': cpu, 'mem': mem})

    def build(self, n_pm):
        """
        n_pm: number of physical machine
        """
        self.solver = stp.Solver()
        s = self.solver

        n_vm = len(self.vms)
        assign = {i: {} for i in range(n_vm)}
        for vid in range(n_vm):
            vm_total_assignment = 0
            for pid in range(n_pm):
                tmp = self.solver.bitvec('%d_%d'%(vid, pid), 32)
                
                vm_total_assignment += tmp

                s.add(tmp>=0)
                s.add(tmp<=1)

                assign[vid][pid] = tmp

            s.add(vm_total_assignment == 1)

        for pid in range(n_pm):
            cpu_util = 0
            mem_util = 0
            for vid in range(n_vm):
                cpu_util += self.vms[vid]['cpu']*assign[vid][pid]
                mem_util += self.vms[vid]['mem']*assign[vid][pid]
            s.add(cpu_util <= self.pm_cpu)
            s.add(mem_util <= self.pm_mem)
        

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


def M(vms, cpu_cap, mem_cap):
    """
    vms: [(cpu_i, mem_i), ...]
    cpu_cap: cpu capacity of each PM
    mem_cap: mem capacity of each PM
    """

    solver = HSolver(cpu_cap, mem_cap)
    for params in vms:
        solver.add_vm(*params)

    n = len(vms)
    bit_len = int(log(n)/log(2)+1)

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
    k, a = M([(10,30), (50,30), (1,1), (1,1), (10,1), (55, 70)], 55, 70)
    print(a)
