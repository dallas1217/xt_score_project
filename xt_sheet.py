#!/usr/bin/python
#coding=utf-8

import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook

wb=load_workbook('xt_score_template.xlsx')
ws=wb.get_sheet_by_name('Sheet1')

position='FWR'
for row in ws.iter_rows(min_row=4,max_row=6):
    for cell in row:
        new_cell=ws['%s%d' %(cell.column,(cell.row+30))]
        new_cell.style=cell.style
        new_cell.value=cell.value
        #ws['B%d' %(min_row+30)].value='Origi'

wb.save('xt_score_test.xlsx')

