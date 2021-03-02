# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 09:41:08 2021

@author: CaleShealy
"""

import numpy as np
import pandas as pd

def RemovePassRushers(playData):
    defense_data = playData.loc[playData["position"].isin(["DE","DT","NT","OLB","MLB","CB","FS","SS","LB","ILB","DL","DB","S"]),:]
    defense_start = defense_data.loc[defense_data["event"]=="ball_snap",:]
    
    max_dist_list = []
    for i in range(defense_start.shape[0]):
        player_data = defense_data.loc[(defense_data["nflId"]==defense_start.iloc[i,9]) & (defense_data["gameId"]==defense_start.iloc[i,-4]) & (defense_data["playId"]==defense_start.iloc[i,-3]),:]
        pass_forward = player_data.loc[player_data["event"]=="pass_forward",:].index
        
        if len(pass_forward)==0:
            pass_forward = player_data.loc[player_data["event"]=="qb_sack"].index
        if len(pass_forward)==0:
            pass_forward = player_data.loc[player_data["event"]=="tackle"].index
        if len(pass_forward)==0:
            pass_forward = player_data.loc[player_data["event"]=="qb_spike"].index
        if len(pass_forward)==0:
            pass_forward = player_data.loc[player_data["event"]=="pass_shovel"].index
        if len(pass_forward)==0:
            pass_forward = player_data.loc[player_data["event"]=="qb_strip_sack"].index
        if len(pass_forward)==0:
            pass_forward = player_data.loc[player_data["event"]=="pass_tipped"].index
        player_data = player_data.loc[(player_data.index > defense_start.index[i]) & (player_data.index <= pass_forward[0]),:]
        dist_list = []
        for j in range(player_data.shape[0]):
            dist = player_data.iloc[j,1] - player_data.iloc[0,1]
            dist_list.append(dist)
        if defense_start.iloc[i,-2]=="left":
            max_dist_list.append(np.max(dist_list))
        else:
            max_dist_list.append(np.min(dist_list))
        
    
    rush_ind = np.where(np.array(max_dist_list) < -1)
    rushId = defense_start.loc[defense_start.index[rush_ind],["nflId","gameId","playId"]]
    coverage_players = defense_data.copy()
    for i in range(rushId.shape[0]):
        dropped_player = defense_data.loc[(defense_data["nflId"]==rushId.iloc[i,0]) & (defense_data["gameId"]==rushId.iloc[i,1]) & (defense_data["playId"]==rushId.iloc[i,2]),:].index
        coverage_players.drop(dropped_player,axis=0,inplace=True)
        
    return coverage_players