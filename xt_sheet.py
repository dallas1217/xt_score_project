#!/usr/bin/python
#coding=utf-8

import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook

wb=load_workbook('xt_score_template.xlsx')
ws=wb.get_sheet_by_name('Sheet1')

pos_list=['FWR']
l=[]

for i in range(4,28,3):
    default_pos=ws['A%s' %i].value
    for position in pos_list:
        if position in default_pos:
            for row in ws.iter_rows(min_row=i,max_row=(i+2)):
                for cell in row:
                    if isinstance(ws['%s%d' %(cell.column,(cell.row+30))].value,'NoneType'):
                        print('OK')
                    #    new_cell=ws['%s%d' %(cell.column,(cell.row+30))]
                    #    new_cell.style=cell.style
                    #    new_cell.value=cell.value
                    else:
                        print('Not OK')
                    #    new_cell=ws['%s%d' %(cell.column,(cell.row+33))]
                    #    new_cell.style=cell.style
                    #    new_cell.value=cell.value

        else:
             pass



wb.save('xt_score_test.xlsx')
