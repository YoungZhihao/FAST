'''
Author: Zhihao Young
Date: 2025-11-25 19:58:41
LastEditors: Zhihao Young
LastEditTime: 2025-11-29 23:41:58
FilePath: \multi-rate task\StandardFunction.py
Description: 
Only for Academic Uses
Copyright (c) 2025 by Zhihao Young, All Rights Reserved.
'''

import math
import os
import xlrd, xlwt
from xlutils.copy import copy
from functools import reduce



def multimin(x, y, z):
    return min(min(x, y), z)



def LCM(List):
    if not List:
        return None
    return reduce(math.lcm, List)



def mod(x, y):
    modv = x % y
    return modv+y if modv < 0 else modv



def ExcelWrite(filepath, sheetname, timecost, Makespans, Precisions, TaskDelays): 
    sheetname = 'Sheet_{0}'.format(sheetname)
    
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        workbook = xlwt.Workbook()
        workbook.add_sheet(sheetname)
        workbook.save(filepath)
    workbook_r = xlrd.open_workbook(filepath)
    workbook_w = copy(workbook_r)
    
    names = workbook_r.sheet_names()
    if sheetname in names:
        idx = names.index(sheetname)
        worksheet = workbook_w.get_sheet(idx)
    else:
        worksheet = workbook_w.add_sheet(sheetname)
    
    title = ['Time Cost/s', 'Task Delay/μs', 'Makespan/μs', 'Precision/%']
    for i in range(len(title)):
        worksheet.write(0,i,title[i])
    
    worksheet.write(1, 0, timecost)
    for i in range(len(TaskDelays)):
        worksheet.write(i+1, 1, TaskDelays[i])
    for i in range(len(Makespans)):
        worksheet.write(i+1, 2, Makespans[i])
    for i in range(len(Precisions)):
        worksheet.write(i+1, 3, Precisions[i])

    workbook_w.save(filepath)



def ExcelReadResults(filepath, sheetname):
    sheetname = 'Sheet_{0}'.format(sheetname)
    
    TaskDelays = ReturnRowList(filepath, sheetname, 1)
    Makespans = ReturnRowList(filepath, sheetname, 2)
    Precisions = ReturnRowList(filepath, sheetname, 3)
    
    return TaskDelays, Makespans, Precisions



def ReturnRowList(filepath, sheetname, column):
    workbook = xlrd.open_workbook(filepath)
    sheet = workbook.sheet_by_name(sheetname)
    returnvalue = []
    
    for row in range(1, sheet.nrows):
        cell_value = sheet.cell_value(row, column)
        if cell_value != '':
            returnvalue.append(cell_value)
    
    return returnvalue