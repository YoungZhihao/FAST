'''
Author: Zhihao Young
Date: 2025-11-19 20:33:10
LastEditors: Zhihao Young
LastEditTime: 2025-11-30 22:54:29
FilePath: \multi-rate task\main.py
Description: The main file of the Makespan Optimization Problem
Only for Academic Uses
Copyright (c) 2025 by Zhihao Young, All Rights Reserved.
'''


from math import gcd, lcm, floor, ceil
from MakespanOptimizeFunc import SpaceCompression, OptMakespanSearch
from MakespanCalFunc import PrecisionAnalysis, Makespan
from StandardFunction import ExcelWrite
import time
import xlrd, xlwt


# R = 1000 # 1000Mbps, 1000bits/μs
R = 10000 # 1Gbps, 10000bits/μs


def MakespanOptimization(Tasks, TaskChains, Periods, Baselines, Executions, Deadlines, InfoFreshes, PckLengths, Distributions, Routes, R):
    OFT = {i: None for i in Tasks}
    TaskSch = []
    
    starttime = time.perf_counter()
    
    for taskchain in TaskChains:
        for task in taskchain:
            InfeasibleInterval = SpaceCompression(task, TaskSch, OFT, 
                                    Periods, Baselines, Executions, PckLengths, Distributions, Routes, R)
            if not InfeasibleInterval:
                OFT[task] = 0
                TaskSch.append(task)
                continue
            optimized_offset = OptMakespanSearch(task, taskchain, OFT, InfeasibleInterval, Periods, 
                                                 Baselines, Executions, Deadlines, InfoFreshes, PckLengths, Routes, R)
            OFT[task] = optimized_offset
            TaskSch.append(task)
    
    endtime = time.perf_counter()
    timecost = endtime - starttime

    return 0
    

