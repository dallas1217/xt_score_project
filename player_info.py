#!/usr/local/python3.6/bin/python3.6

import json,xlsxwriter
from functools import reduce

### 初始化json内容，目前马龙提供的json文件有4行，先抽取带数据的一行进行测试（第一行），之后再优化爬虫脚本
### 返回字典类型，包含球员名，球员位置和球员所有数据
def stats_info(field,info):
    stats_list=[]                                      
    for l in info[field]['players']:
        player_info={}
        if 'isFirstEleven' in l or 'subbedInExpandedMinute' in l:
            player_info['name']=l['name']              #Player name
            player_info['position']=l['position']      #Player position
            player_info['stats']=l['stats']            #Player stats in json file
            stats_list.append(player_info)
    return stats_list

### 细化球员数据，筛选出符合xt_score的项并整合
def normal_stats(stats):
    stats_list=[]        #最终返回的符合xt_score的球员信息及数据，由xt_stats组合而成，列表类型
    full_stats={}        #全部数据，字典类型
    xt_stats={}          #返回的符合xt_score的单个球员数据
    ### 所有数据项
    item_list=['aerialSuccess', 'aerialsTotal', 'aerialsWon', 'claimsHigh', 'clearances', 'collected', 'cornersAccurate', 'cornersTotal', 'defensiveAerials', 'dispossessed', 'dribbleSuccess', 'dribbledPast', 'dribblesAttempted', 'dribblesLost', 'dribblesWon', 'errors', 'foulsCommited', 'interceptions', 'offensiveAerials', 'offsidesCaught', 'parriedSafe', 'passSuccess', 'passesAccurate', 'passesKey', 'passesTotal', 'possession', 'ratings', 'shotsBlocked', 'shotsOffTarget', 'shotsOnTarget', 'shotsTotal', 'tackleSuccess', 'tackleSuccessful', 'tackleUnsuccesful', 'tacklesTotal', 'throwInAccuracy', 'throwInsAccurate', 'throwInsTotal', 'totalSaves', 'touches']
    ### xt_score所需普通球员数据项
    stat_list=['aerialsWon','aerialsTotal','shotsOnTarget','shotsTotal','dribblesAttempted','dribblesWon','clearances','interceptions','tackleSuccessful','passesKey','errors','dribbledPast']
    ### xt_score所需门将数据项
    gk_list=['totalSaves','claimsHigh','collected','parriedSafe','errors']
    ### 根据位置计算和整合，分为普通球员和门将
    for line in stats:
        player_stats={}      
        player_stats['name']=line['name']
        player_stats['position']=line['position']
        for item in item_list:
            if item in line['stats']:
                full_stats[item]=single_item(line['stats'][item])
            else:
                full_stats[item]=0.0
        if 'GK' in line['position']:
            for item in item_list:
                            for item in item_list:
                if item in gk_list:
                    xt_stats[item]=full_stats[item]
            xt_stats['passSuccess']=reduce(percent_item,[full_stats['passesAccurate'],full_stats['passesTotal']])
        else:
            for item in item_list:
                if item in stat_list:
                    xt_stats[item]=full_stats[item]
            ### 一些百分比统计项，使用reduce函数加上percent_item函数进行计算
            xt_stats['passSuccess']=reduce(percent_item,[full_stats['passesAccurate'],full_stats['passesTotal']])
            xt_stats['aerialSuccess']=reduce(percent_item,[full_stats['aerialsWon'],full_stats['aerialsTotal']])
            xt_stats['shotSuccess']=reduce(percent_item,[full_stats['shotsOnTarget'],full_stats['shotsTotal']])
            xt_stats['dribbleSuccess']=reduce(percent_item,[full_stats['dribblesWon'],full_stats['dribblesAttempted']])
        player_stats['stats']=xt_stats.copy()
        stats_list.append(player_stats)
    return stats_list

### 单项数据总和
def single_item(item):
    count=0
    for i in item.values():
        count+=i
    return float('%.1f' %count)

### 百分比计算，返回浮点数，根据足球事实，total总大于等于success，假如total=0，返回0
def percent_item(success,total):
    if total==0.0:
        return 0.0
    if success<=total:
        return round((success/total*100))
    else:
        print("Total item must bigger than success item!")
        break

### 程序主题，输入json文件，后续会返回主客场状况、对阵球队名称等信息，目前测试场次为客场对阵西布朗的比赛
if __name__=='__main__':
    f=open('json_1.txt','rb')
    for line in f.readlines():
        info=json.loads(line)
    f.close()
    away_stats=stats_info('away',info)
    print(normal_stats(away_stats))
