#!/usr/local/python3.6/bin/python3.6

import json,xlsxwriter
from functools import reduce

### Initialize json stats and return name,position,stats list
def stats_info(field,info):
    stats_list=[]                                      #Return list to calculate,item in list is dictionary type
    for l in info[field]['players']:
        player_info={}
        if 'isFirstEleven' in l or 'subbedInExpandedMinute' in l:
            player_info['name']=l['name']              #Player name
            player_info['position']=l['position']      #Player position
            player_info['stats']=l['stats']            #Player stats in json file
            stats_list.append(player_info)
    return stats_list


def normal_stats(stats):
    stats_list=[]        #Return list that input into excel,item in list is dictionary type
    full_stats={}        #Full stats from json,items is in item_list
    xt_stats={}          #XT score stats,items is in stat_list and gk_list
    item_list=['aerialSuccess', 'aerialsTotal', 'aerialsWon', 'claimsHigh', 'clearances', 'collected', 'cornersAccurate', 'cornersTotal', 'defensiveAerials', 'dispossessed', 'dribbleSuccess', 'dribbledPast', 'dribblesAttempted', 'dribblesLost', 'dribblesWon', 'errors', 'foulsCommited', 'interceptions', 'offensiveAerials', 'offsidesCaught', 'parriedSafe', 'passSuccess', 'passesAccurate', 'passesKey', 'passesTotal', 'possession', 'ratings', 'shotsBlocked', 'shotsOffTarget', 'shotsOnTarget', 'shotsTotal', 'tackleSuccess', 'tackleSuccessful', 'tackleUnsuccesful', 'tacklesTotal', 'throwInAccuracy', 'throwInsAccurate', 'throwInsTotal', 'totalSaves', 'touches']
    stat_list=['aerialsWon','aerialsTotal','shotsOnTarget','shotsTotal','dribblesAttempted','dribblesWon','clearances','interceptions','tackleSuccessful','passesKey','errors','dribbledPast']
    gk_list=['totalSaves','claimsHigh','collected','parriedSafe','errors']
    ### Calculate single item in item list
    for line in stats:
        player_stats={}      #Total stats,includs name,position and XT score stats
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
            xt_stats['passSuccess']=reduce(percent_item,[full_stats['passesAccurate'],full_stats['passesTotal']])
            xt_stats['aerialSuccess']=reduce(percent_item,[full_stats['aerialsWon'],full_stats['aerialsTotal']])
            xt_stats['shotSuccess']=reduce(percent_item,[full_stats['shotsOnTarget'],full_stats['shotsTotal']])
            xt_stats['dribbleSuccess']=reduce(percent_item,[full_stats['dribblesWon'],full_stats['dribblesAttempted']])
        player_stats['stats']=xt_stats.copy()
        stats_list.append(player_stats)
    return stats_list

def single_item(item):
    count=0
    for i in item.values():
        count+=i
    return float('%.1f' %count)

def percent_item(success,total):
    if total==0.0:
        return 0.0
    if success<=total:
        return round((success/total*100))
    else:
        print("Total item must bigger than success item!")

if __name__=='__main__':
    f=open('json_1.txt','rb')
    for line in f.readlines():
        info=json.loads(line)
    f.close()
    away_stats=stats_info('away',info)
    print(normal_stats(away_stats))
