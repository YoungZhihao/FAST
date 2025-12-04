'''
Author: Zhihao Young
Date: 2025-09-16 22:44:25
LastEditors: Zhihao Young
LastEditTime: 2025-11-25 22:02:27
FilePath: \multi-rate task\MakespanCalFunc.py
Description: Functions concerning makespan calculation
Only for Academic Uses
Copyright (c) 2025 by Zhihao Young, All Rights Reserved.
'''

from math import gcd, lcm, ceil, floor
from JobAnalysisFunc import SingleResponse, MultiResponse
from StandardFunction import LCM, mod



def FastScaler(TaskChain, Periods):
    elements = [(0,Periods[TaskChain[i+1]]//gcd(Periods[TaskChain[i]],Periods[TaskChain[i+1]])-1)
                for i in range(len(TaskChain)-1)]
    weights = [gcd(Periods[TaskChain[i]],Periods[TaskChain[i+1]]) for i in range(len(TaskChain)-1)]
    possible = {0}
    for (min_val, max_val), w in zip(elements, weights):
        possible = {s+w*k for s in possible for k in range(min_val,max_val+1)}
    return possible
    


def MakespanApproximation(TaskChain, task, offset, OFT, Periods, Baselines, Executions, PckLengths, Routes, R):
    taskindex = TaskChain.index(task)
    taskchain = TaskChain[:taskindex+1]
    
    if taskindex == 0:
        return Executions[task]+offset
    
    Z1_g = 0
    pN = Periods[taskchain[-1]]
    
    for i in range(taskindex):
        u = ceil((Baselines[taskchain[i]]+OFT[taskchain[i]]+Executions[taskchain[i]]+len(Routes[taskchain[i]])*PckLengths[taskchain[i]]/R
                  -Baselines[taskchain[i+1]]-offset)/gcd(Periods[taskchain[i]],Periods[taskchain[i+1]]))-1
        if Periods[taskchain[i]] >= Periods[taskchain[i+1]]:
            g = Periods[taskchain[i]] + u*gcd(Periods[taskchain[i]],Periods[taskchain[i+1]])
        else:
            g = Periods[taskchain[i+1]] + u*gcd(Periods[taskchain[i]],Periods[taskchain[i+1]])
        Z1_g += g % gcd(Periods[taskchain[i]],pN)
    
    Z2 = FastScaler(TaskChain, Periods)
    k = 0
    while Z1_g+k*gcd(Periods[TaskChain[0]],pN) not in Z2:
        k += 1
    
    return Z1_g+k*gcd(Periods[TaskChain[0]],pN)



def Makespan(TaskChain, OFT, Periods, Baselines, Executions, PckLengths, Routes, R):
    HyperPeriod = LCM(Periods)
    makespan = 0
    
    if len(TaskChain) == 1:
        task = TaskChain[0]
        return OFT[task]+Executions[task]
    
    for i in range(0, HyperPeriod//Periods[TaskChain[0]]):
        starttask, goaltask = TaskChain[0], TaskChain[-1]
        lastindex, _ = MultiResponse(starttask, goaltask, i, TaskChain, OFT, Periods, Baselines, Executions, PckLengths, Routes, R)
        makespan_tmp = Baselines[goaltask]+lastindex*Periods[goaltask]+OFT[goaltask]+Executions[goaltask]-\
                        Baselines[starttask]-i*Periods[starttask]
        makespan = max(makespan, makespan_tmp)
    
    return makespan_tmp



def PrecisionAnalysis(TaskChain, OFT, Periods, Baselines, Executions, PckLengths, Routes, R):
    error = 0
    
    for i in range(len(TaskChain)-1):
        u = ceil((Baselines[TaskChain[i]]+OFT[TaskChain[i]]+Executions[TaskChain[i]]+len(Routes[TaskChain[i]])*PckLengths[TaskChain[i]]/R
                  -Baselines[TaskChain[i+1]]-OFT[TaskChain[i+1]])/gcd(Periods[TaskChain[i]],Periods[TaskChain[i+1]]))-1
        y = SingleResponse(TaskChain[i], 1, TaskChain, OFT, Periods, Baselines, Executions, PckLengths, Routes, R)
        if Periods[TaskChain[i]]*y+u*gcd(Periods[TaskChain[i]],Periods[TaskChain[i+1]]) == 0:
            continue
        else:
            error += (Periods[TaskChain[i+1]]-gcd(Periods[TaskChain[i]],Periods[TaskChain[i+1]]))/\
                    (Periods[TaskChain[i]]*y+u*gcd(Periods[TaskChain[i]],Periods[TaskChain[i+1]]))
    error -= 1
    
    return error
        
        
