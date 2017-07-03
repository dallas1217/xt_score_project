#!/usr/local/python3.6/bin/python3.6

import json
from functools import reduce

def stats_info(field,info):
    names=[]
    stats=[]
    for l in info[field]['players']:
        if 'isFirstEleven' in l or 'subbedInExpandedMinute' in l:
            names.append(l['name'])
            stats.append(l['stats'])
    full_stats=dict(zip(names,stats))
    return full_stats

### Players statics about Non-GK players,return dictionary type
def normal_stats(stats):
    total_stat={}
    stat={}
    item_list=['aerialSuccess', 'aerialsTotal', 'aerialsWon', 'claimsHigh', 'clearances', 'collected', 'cornersAccurate', 'cornersTotal', 'defensiveAerials', 'dispossessed', 'dribbleSuccess', 'dribbledPast', 'dribblesAttempted', 'dribblesLost', 'dribblesWon', 'errors', 'foulsCommited', 'interceptions', 'offensiveAerials', 'offsidesCaught', 'parriedSafe', 'passSuccess', 'passesAccurate', 'passesKey', 'passesTotal', 'possession', 'ratings', 'shotsBlocked', 'shotsOffTarget', 'shotsOnTarget', 'shotsTotal', 'tackleSuccess', 'tackleSuccessful', 'tackleUnsuccesful', 'tacklesTotal', 'throwInAccuracy', 'throwInsAccurate', 'throwInsTotal', 'totalSaves', 'touches']

    stat_list=['aerialsWon','aerialsTotal','shotsOnTarget','shotsTotal','dribblesAttempted','dribblesWon','passesAccurate','passesTotal','clearances','interceptions','tackleSuccessful','passesKey','errors','dribbledPast']

    ### Calculate single item in item list
    for item in item_list:
        if item in stats:
            total_stat[item]=single_item(stats[item])
        else:
            total_stat[item]=0.0

    ### Add stat that need to show in worksheet to dictionary and return
    for item in item_list:
        if item in stat_list:
            stat[item]=total_stat[item]

    stat['passSuccess']=reduce(percent_item,[stat['passesAccurate'],stat['passesTotal']])
    stat['aerialSuccess']=reduce(percent_item,[stat['aerialsWon'],stat['aerialsTotal']])
    
        stat['shotSuccess']=reduce(percent_item,[stat['shotsOnTarget'],stat['shotsTotal']])
    stat['dribbleSuccess']=reduce(percent_item,[stat['dribblesWon'],stat['dribblesAttempted']])

    return stat

### Item calculate,including single calculate and percent calculate,return float type.Please noted that in percent calculate
def single_item(item):
    count=0
    for i in item.values():
        count+=i
    return float('%.1f' %count)

def percent_item(success,total):
    if total==0.0:
        return 0.0
    if success<=total:
        return float('%.1f' %(success/total*100))
    else:
        print("Total item must bigger than success item!")

if __name__=='__main__':
    f=open('json_1.txt','rb')
    for line in f.readlines():
        info=json.loads(line)
    f.close()
    away_stats=stats_info('away',info)
    home_stats=stats_info('home',info)
    for name,stat in home_stats.items():
        print(name,normal_stats(stat))
    for name,stat in away_stats.items():
        print(name,normal_stats(stat))
