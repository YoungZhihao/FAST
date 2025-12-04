'''
Author: Zhihao Young
Date: 2025-11-17 21:35:19
LastEditors: Zhihao Young
LastEditTime: 2025-11-25 22:09:34
FilePath: \multi-rate task\MakespanOptimizeFunc.py
Description: 
Only for Academic Uses
Copyright (c) 2025 by Zhihao Young, All Rights Reserved.
'''


from math import gcd
import time
from MakespanCalFunc import MakespanApproximation, PrecisionAnalysis
from StandardFunction import multimin
from numpy import mean
import portion as P


INF = 10**9



def SpaceCompression(task, Tasksch, OFT, Periods, Baselines, Executions, PckLengths, Distributions, Routes, R):
    flow = task
    INTR = {}
    hop_flow = {l:idx for idx, l in enumerate(Routes[flow])}
    
    for f in Tasksch:
        hop_f = {l:idx for idx, l in enumerate(Routes[f])}
        Intersec = set(Routes[f])&set(Routes[flow])
        if Intersec:
            intr, g = P.empty(), gcd(Periods[f], Periods[flow])
            subl1, subr1 = (Baselines[f]+Executions[f]+OFT[f]-Baselines[flow]-Executions[flow]-PckLengths[flow]/R)%g, \
                            (Baselines[f]+Executions[f]+OFT[f]-Baselines[flow]-Executions[flow]+PckLengths[f]/R)%g
            for link in Intersec:
                sub2 = hop_f[link]*PckLengths[f]/R-hop_flow[link]*PckLengths[flow]/R
                subl, subr = (subl1+sub2)%g, (subr1+sub2)%g
                if subl <= subr:
                    intr |= P.open(subl, subr)
                else:
                    intr |= P.closedopen(0, subr)|P.open(subl, g)
            if g in INTR:
                INTR[g] |= intr
            else:
                INTR[g] = intr
    
    for t in Tasksch:
        if Distributions[flow] == Distributions[t]:
            intr, g = P.empty(), gcd(Periods[t], Periods[flow])
            subl = Baselines[t]+OFT[t]-Baselines[flow]-Executions[flow]
            subr = Baselines[t]+OFT[t]-Baselines[flow]+Executions[t]
            if g in INTR:
                INTR[g] |= intr
            else:
                INTR[g] = intr

    return INTR



def OptMakespanSearch(task, TaskChain, OFT, INTR, Periods, Baselines, Executions, Deadlines, InfoFreshes, PckLengths, Routes, R):
    latency = (len(Routes[task])-1)*PckLengths[task]/R
    bound = multimin(Periods[task], Deadlines[task]-Executions[task], InfoFreshes[task]-latency)
    oft_opt, makespan_opt = 0, INF
    oft_fsb = 0
    cnt, finish = 0, len(INTR)    
    
    is_find = False
    while cnt < finish:
        for g, intr in INTR.items():
            omod = oft_fsb % g
            if omod in intr:
                for subintr in intr:
                    if omod < subintr.upper:
                        oft_fsb, cnt = subintr.upper-omod+oft_fsb, 1
                        if oft_fsb > bound:
                            if is_find:
                                return oft_opt
                            else:
                                return None
                        break
            else:
                cnt += 1
                if cnt == finish:
                    is_find = True
                    makespan_tmp = MakespanApproximation(TaskChain, task, oft_fsb, OFT, Periods, Baselines, 
                                                            Executions, PckLengths, Routes, R)
                    if makespan_tmp < makespan_opt:
                        makespan_opt = makespan_tmp
                        oft_opt = oft_fsb
    return oft_opt
