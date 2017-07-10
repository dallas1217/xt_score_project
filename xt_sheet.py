#coding=utf-8

from enum import Enum
from openpyxl import Workbook
from openpyxl import load_workbook

wb=load_workbook('xt_score_template.xlsx')
ws=wb.get_sheet_by_name('Sheet1')

# 使用枚举方法定义常量，目前的BUG是相同值的位置会显示第一个成员位置，后续考虑位置单独性解决
class Position(Enum):
    FW=0
    FWR=2
    FWL=2
    AMR=2
    AML=2
    MR=2
    ML=2
    AMC=1
    CM=3
    DM=4
    DMR=5
    DML=5
    DR=5
    DL=5
    DC=6
    GK=7

# 模拟从json文件获取位置，生成位置模板，后续可以考虑保留该方法
pos_list=['GK','DR','DL','DC','DC','DM','DM','AMR','AML','AMC','FW']
# 打分表开始位置
start_line=33

for pos in pos_list:
    # 匹配枚举内的位置，生成表格
    if pos in Position.__members__.keys():
        pos_id=Position[pos].value    #获取位置IP，用于修改打分卡内位置和球员名称
        pos_name=Position[pos].name   #获取位置名称
        for i in range(4,28,3):
            default_pos=ws['A%d' %i].value
            if pos_id==default_pos:
                for row in ws.iter_rows(min_row=i,max_row=(i+2)):   #模板分为三行，这里i的值到i+2即为要使用的模板列
                    for cell in row:
                        new_cell=ws['%s%d' %(cell.column,start_line)]
                        new_cell.value=cell.value
                        new_cell.style=cell.style
                    #A列位置如何pos_id相等，修改球员名字和位置名字
                    if ws['A%d' %start_line].value==pos_id:
                        ws['A%d' %start_line].value='Player'
                        ws['B%d' %start_line].value=pos_name
                    start_line+=1
                    print(start_line)

                    
#保存表格
wb.save('xt_score_test.xlsx')



