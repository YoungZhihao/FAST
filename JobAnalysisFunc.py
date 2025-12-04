'''
Author: Zhihao Young
Date: 2025-11-17 21:24:29
LastEditors: Zhihao Young
LastEditTime: 2025-11-21 11:47:24
FilePath: \multi-rate task\JobAnalysisFunc.py
Description: Functions related with job-level interaction analysis
Only for Academic Uses
Copyright (c) 2025 by Zhihao Young, All Rights Reserved.
'''

from math import ceil, gcd, floor


def SingleResponse(pretask, jobindex, Taskchain, OFT, Periods, Baselines, Executions, PckLengths, Routes, R):
    preindex = Taskchain.index(pretask)
    subtask = Taskchain[preindex+1]
    u = ceil(Baselines[pretask]+OFT[pretask]+Executions[pretask]+len(Routes[pretask])*PckLengths[pretask]/R- \
            Baselines[subtask]+OFT[subtask])/gcd(Periods[pretask],Periods[subtask])-1
    if Periods[pretask] >= Periods[subtask]:
        y = ceil((Periods[pretask]*(jobindex+1)+u*gcd(Periods[pretask],Periods[subtask]))/Periods[subtask])
    else:
        y = ceil((Periods[pretask]*jobindex+u*gcd(Periods[pretask],Periods[subtask]))/Periods[subtask])+1

    return y



def MultiResponse(pretask, goaltask, jobindex, Taskchain, OFT, Periods, Baselines, Executions, PckLengths, Routes, R):
    if len(Taskchain) == 1:
        return None
    jobindexlist = [jobindex]
    pretaskindex = Taskchain.index(pretask)
    subtask = Taskchain[pretaskindex+1]
    while subtask != goaltask:
        jobindex = SingleResponse(pretask, jobindex, Taskchain, OFT, Periods, Baselines, Executions, PckLengths, Routes, R)
        jobindexlist.append(jobindex)
        pretaskindex = Taskchain.index(subtask)
        pretask, subtask = subtask, Taskchain[pretaskindex+1]
    
    return jobindex, jobindexlist