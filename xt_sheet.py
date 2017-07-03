#!/usr/local/python3.6/bin/python3.6
#coding=utf-8

import re
from openpyxl import Workbook
from openpyxl import load_workbook

wb=load_workbook('xt_score_template.xlsx')   #输入的xt_score excel模板
ws=wb.get_sheet_by_name('Sheet1')    #第一张表名

### 模拟player_info.py内的字典输出位置，之后便正式通过字典输出
pos_list=['GK','DR','DL','DC','DC','CM','CM','CM','FWR','FW','FWL']
l=[]
start_line=33    #从表格第33行开始输出结果

''' 4到28行为位置评分模板，按照以下位置设置成模板，详情请参考xt_scored_template.xlsx:
FW、AMC、FWR/FWL/AMR/AML/NR/ML、CM、DM、DR/DL/DMR/DML、DC、GK
目前已做到匹配模板位置项便黏贴，但出现FW匹配FW和FWR/FWL/AMR/AML/NR/ML问题，之后考虑通过正则表达式re匹配，做到更精确
至于模板内的色调，下一步考虑统一模板内用色，并进行测试
'''
for i in range(4,28,3):
    for position in pos_list:
        default_pos=ws['A%d' %i].value
        if position in default_pos:
            for row in ws.iter_rows(min_row=i,max_row=(i+2)):   #模板分为三行，这里i的值到i+2即为要使用的模板列
                for cell in row:
                        new_cell=ws['%s%d' %(cell.column,start_line)]
                        new_cell.value=cell.value
                        new_cell.style=cell.style
                start_line+=1
                print(start_line)
            ws['A%d' %start_line].value=position    #将模板原有的位置值替换成实际球员位置值
            print(ws['A%d' %start_line].value)
        else:
             ### 
             pass

### 保存excel
wb.save('xt_score_test.xlsx')
