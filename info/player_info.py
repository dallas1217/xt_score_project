#coding = utf-8

import json,sys
from functools import reduce

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

### 细化球员数据，筛选出符合xt_score的项并整合，返回xt_list。whoscored按照时间点返回数据，需要函数求和以及计算总共的百分比
def normal_stats(line):
    full_stats={}   #全部数据，字典类型
    xt_list=[]      #最终返回的符合xt_score的球员信息及数据，列表类型

    # whosored在Match Center所有项目
    item_list=['aerialSuccess', 'aerialsTotal', 'aerialsWon', 'claimsHigh', 'clearances', 'collected', 'cornersAccurate', 'cornersTotal', 'defensiveAerials', 'dispossessed', 'dribbleSuccess', 'dribbledPast', 'dribblesAttempted', 'dribblesLost', 'dribblesWon', 'errors', 'foulsCommited', 'interceptions', 'offensiveAerials', 'offsidesCaught', 'parriedSafe', 'passSuccess', 'passesAccurate', 'passesKey', 'passesTotal', 'possession', 'ratings', 'shotsBlocked', 'shotsOffTarget', 'shotsOnTarget', 'shotsTotal', 'tackleSuccess', 'tackleSuccessful', 'tackleUnsuccesful', 'tacklesTotal', 'throwInAccuracy', 'throwInsAccurate', 'throwInsTotal', 'totalSaves', 'touches']
    # xt_score普通球员项目
    outfield_list=['dribbledPast','dribblesWon','passesKey','errors']
    # xt_score门将项目
    #gk_list=['totalSaves','claimsHigh','collected','parriedSafe','errors']
    gk_list=['totalSaves','collected','errors']

    ### 根据位置计算和整合，分为普通球员和门将
    for l in line:
        xt_stats={}
        xt_stats['name'] = l['name']
        xt_stats['position'] = l['position']
        xt_stats['stats']={}
        
        for item in item_list:
            if item in l['stats']:
                full_stats[item]=single_item(l['stats'][item])
            else:
                full_stats[item]=0.0
                
        if 'GK' in l['position']:
            for key in full_stats.keys():
                if key in gk_list:
                    xt_stats['stats'][key] = full_stats[key]
            ### 门将位置值需要统计传球成功率，使用reduce函数加上percent_item函数进行计算
            xt_stats['stats']['passSuccess']=reduce(percent_item,[full_stats['passesAccurate'],full_stats['passesTotal']])

        else:
            ### 普通球员需要统计传球成功率，射门成功率，对抗成功率和盘带成功率
            for key in full_stats.keys():
                if key in outfield_list:
                    xt_stats['stats'][key] = full_stats[key]
            xt_stats['stats']['passSuccess']=reduce(percent_item,[full_stats['passesAccurate'],full_stats['passesTotal']])
            xt_stats['stats']['aerialSuccess']=reduce(percent_item,[full_stats['aerialsWon'],full_stats['aerialsTotal']])
            xt_stats['stats']['shotSuccess']=reduce(percent_item,[full_stats['shotsOnTarget'],full_stats['shotsTotal']])
            #xt_stats['stats']['dribbleSuccess']=reduce(percent_item,[full_stats['dribblesWon'],full_stats['dribblesAttempted']])
            xt_stats['stats']['defenceStats']=full_stats['clearances']+full_stats['interceptions']+full_stats['tackleSuccessful']
                
        xt_list.append(xt_stats)
    return xt_list

### 单项数据求和
def single_item(item):
    count=0
    for i in item.values():
        count+=i
    return float('%.1f' %count)

### 百分比数据求值
def percent_item(success,total):
    if total==0.0:
        return 0.0
    if success<=total:
        return float('%.1f' %(success/total*100))
    else:
        print("Total item must bigger than success item!")
        sys.exit(1)

### 返回计算结果，列表类型
def main():
    f=open('json_1.txt','rb')
    for line in f.readlines():
        info=json.loads(line)
    f.close()
    liver_stats=normal_stats(stats_info('away',info))
    return liver_stats

if __name__=='__main__':
    main()
