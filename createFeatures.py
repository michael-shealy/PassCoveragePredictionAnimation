# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 10:02:17 2021

@author: CaleShealy
"""

import numpy as np
import pandas as pd
import math
import statistics

def createFeatures(playerData,playData):
    featuresbbt = pd.DataFrame(columns=["Var_X","Var_Y","Speed_Var","Off_Var","Def_Var","Off_Mean","Def_Mean","Off_Dir_Var","Off_Dir_Mean","Rat_Mean","Rat_Var","Los_Or_Mean","Percent_Same_Or"])
    featuresabt = pd.DataFrame(columns=["Var_X","Var_Y","Speed_Var","Off_Var","Def_Var","Off_Mean","Def_Mean","Off_Dir_Var","Off_Dir_Mean","Rat_Mean","Rat_Var","Los_Or_Mean","Percent_Same_Or"])
    
    ball_thrown = playerData.loc[playerData["event"]=="pass_forward",:].index[0]
    nflId = playerData.iloc[0,9]
    
    bbt = playerData.loc[playerData.index <= ball_thrown,:].copy()
    abt = playerData.loc[playerData.index > ball_thrown,:].copy()
    
    offensedata = playData.loc[playData["position"].isin(["QB", "RB","FB","WR","TE","HB"]),:].copy()
    defensedata = playData.loc[playData["position"].isin(["DE","DT","NT","OLB","MLB","CB","FS","SS","LB","ILB","DL","DB","S"]),:].copy()
    
    for i in range(bbt.shape[0]):
        frameId = bbt.iloc[i,13]
        data = bbt.iloc[0:(i+1),:]
        var_x = data["x"].var()
        var_y = data["y"].var()
        var_s = data["s"].var()
        if math.isnan(var_x):
            var_x = 0
            var_y = 0
            var_s = 0
            
        min_dists = []
        for i in range(data.shape[0]):
            frame_num = data.iloc[i,13]
            o_frame_players = offensedata.loc[offensedata["frameId"]==frame_num,:]
            dist_list = []
            for j in range(o_frame_players.shape[0]):
                dist = np.sqrt((data.iloc[i,2] - o_frame_players.iloc[j,2])**2 + (data.iloc[i,3]-o_frame_players.iloc[j,3])**2)
                dist_list.append(dist)
            min_dist = dist_list[np.where(dist_list==min(dist_list))[0][0]]
            min_dists.append(min_dist)
            
        
        off_mean = np.mean(min_dists)
        if len(min_dists)==1:
            off_var = 0
        else:
            off_var = statistics.variance(min_dists)
        
        min_dists = []
        defensedata.drop(defensedata.loc[defensedata["nflId"]==nflId,:].index,axis=0,inplace=True)
        for i in range(data.shape[0]):
            frame_num = data.iloc[i,13]
            d_frame_players = defensedata.loc[defensedata["frameId"]==frame_num,:]
            dist_list = []
            for j in range(d_frame_players.shape[0]):
                dist = np.sqrt((data.iloc[i,2] - d_frame_players.iloc[j,2])**2 + (data.iloc[i,3]-d_frame_players.iloc[j,3])**2)
                dist_list.append(dist)
            min_dist = dist_list[np.where(dist_list==min(dist_list))[0][0]]
            min_dists.append(min_dist)
            
        def_mean = np.mean(min_dists)
        if len(min_dists)==1:
            def_var = 0
        else:
            def_var = statistics.variance(min_dists)
            
        min_dirs = []
        for i in range(data.shape[0]):
            frame_num = data.iloc[i,13]
            o_frame_players = offensedata.loc[offensedata["frameId"]==frame_num,:]
            dist_list = []
            for j in range(o_frame_players.shape[0]):
                dist = np.sqrt((data.iloc[i,2] - o_frame_players.iloc[j,2])**2 + (data.iloc[i,3]-o_frame_players.iloc[j,3])**2)
                dist_list.append(dist)
            closest_o = np.where(dist_list==min(dist_list))[0][0]
            dir_d = data.iloc[i,7]
            dir_o = o_frame_players.iloc[closest_o,7]
            if np.abs(dir_d - dir_o) > 180:
                dir_diff = 360 - np.abs(dir_d - dir_o)
            else:
                dir_diff = np.abs(dir_d - dir_o)
            min_dirs.append(dir_diff)
    
        if len(min_dirs)==1:
            off_dir_var = 0
        else:
            off_dir_var = statistics.variance(min_dirs)
        off_dir_mean = np.mean(min_dirs)
        
        ratios = []
        for i in range(data.shape[0]):
            frame_num = data.iloc[i,13]
            o_frame_players = offensedata.loc[offensedata["frameId"]==frame_num,:]
            d_frame_players = defensedata.loc[defensedata["frameId"]==frame_num,:]
            o_dist_list = []
            d_dist_list = []
            for j in range(o_frame_players.shape[0]):
                dist = np.sqrt((data.iloc[i,2] - o_frame_players.iloc[j,2])**2 + (data.iloc[i,3]-o_frame_players.iloc[j,3])**2)
                o_dist_list.append(dist)
            for j in range(d_frame_players.shape[0]):
                dist = np.sqrt((data.iloc[i,2] - d_frame_players.iloc[j,2])**2 + (data.iloc[i,3]-d_frame_players.iloc[j,3])**2)
                d_dist_list.append(dist)
            closest_o = np.where(o_dist_list==min(o_dist_list))[0][0]
            closest_d = np.where(d_dist_list==min(d_dist_list))[0][0]
            o_min_dist = o_dist_list[closest_o]
            close_dist = np.sqrt((o_frame_players.iloc[closest_o,2]-d_frame_players.iloc[closest_d,2])**2+(o_frame_players.iloc[closest_o,3]-d_frame_players.iloc[closest_d,3])**2)
            ratio = o_min_dist / close_dist
            ratios.append(ratio)
    
        rat_mean = np.mean(ratios)
        if len(ratios)==1:
            rat_var=0
        else:
            rat_var = statistics.variance(ratios)
            
        direction = data.iloc[0,-2]
        or_diffs = []
        for i in range(data.shape[0]):
            orientation = data.iloc[i,6]
            if direction == "right":
                or_diff = np.abs(270-orientation)
                if or_diff > 180:
                    or_diff = 360 - np.abs(270-orientation)
            else:
                or_diff = np.abs(90-orientation)
                if or_diff > 180:
                    or_diff = 360 - np.abs(90-orientation)
    
            or_diffs.append(or_diff)
    
        los_or_mean = np.mean(or_diffs)
        
        is_same_way = []
        for i in range(data.shape[0]):
            orientation = data.iloc[i,6]
            frame_num = data.iloc[i,13]
            o_frame_players = offensedata.loc[offensedata["frameId"]==frame_num,:]
            o_dist_list = []
            for j in range(o_frame_players.shape[0]):
                dist = np.sqrt((data.iloc[i,2] - o_frame_players.iloc[j,2])**2 + (data.iloc[i,3]-o_frame_players.iloc[j,3])**2)
                o_dist_list.append(dist)
            closest_o = np.where(o_dist_list==min(o_dist_list))[0][0]
            off_orientation = o_frame_players.iloc[closest_o,6]
            if np.abs(orientation - off_orientation) <= 60:
                is_same_way.append(1)
            else:
                is_same_way.append(0)
    
        percent_same_or = np.mean(is_same_way)*100
        
        featuresbbt.loc[i,:] = [var_x, var_y, var_s, off_var, def_var, off_mean, def_mean, off_dir_var, off_dir_mean, rat_mean, rat_var, los_or_mean, percent_same_or]
        
    
        
    for i in range(abt.shape[0]):
        frameId = abt.iloc[i,13]
        data = abt.iloc[0:(i+1),:]
        var_x = data["x"].var()
        var_y = data["y"].var()
        var_s = data["s"].var()
        if math.isnan(var_x):
            var_x = 0
            var_y = 0
            var_s = 0
            
        min_dists = []
        for i in range(data.shape[0]):
            frame_num = data.iloc[i,13]
            o_frame_players = offensedata.loc[offensedata["frameId"]==frame_num,:]
            dist_list = []
            for j in range(o_frame_players.shape[0]):
                dist = np.sqrt((data.iloc[i,2] - o_frame_players.iloc[j,2])**2 + (data.iloc[i,3]-o_frame_players.iloc[j,3])**2)
                dist_list.append(dist)
            min_dist = dist_list[np.where(dist_list==min(dist_list))[0][0]]
            min_dists.append(min_dist)
            
        
        off_mean = np.mean(min_dists)
        if len(min_dists)==1:
            off_var = 0
        else:
            off_var = statistics.variance(min_dists)
        
        min_dists = []
        defensedata.drop(defensedata.loc[defensedata["nflId"]==nflId,:].index,axis=0,inplace=True)
        for i in range(data.shape[0]):
            frame_num = data.iloc[i,13]
            d_frame_players = defensedata.loc[defensedata["frameId"]==frame_num,:]
            dist_list = []
            for j in range(d_frame_players.shape[0]):
                dist = np.sqrt((data.iloc[i,2] - d_frame_players.iloc[j,2])**2 + (data.iloc[i,3]-d_frame_players.iloc[j,3])**2)
                dist_list.append(dist)
            min_dist = dist_list[np.where(dist_list==min(dist_list))[0][0]]
            min_dists.append(min_dist)
            
        def_mean = np.mean(min_dists)
        if len(min_dists)==1:
            def_var = 0
        else:
            def_var = statistics.variance(min_dists)
            
        min_dirs = []
        for i in range(data.shape[0]):
            frame_num = data.iloc[i,13]
            o_frame_players = offensedata.loc[offensedata["frameId"]==frame_num,:]
            dist_list = []
            for j in range(o_frame_players.shape[0]):
                dist = np.sqrt((data.iloc[i,2] - o_frame_players.iloc[j,2])**2 + (data.iloc[i,3]-o_frame_players.iloc[j,3])**2)
                dist_list.append(dist)
            closest_o = np.where(dist_list==min(dist_list))[0][0]
            dir_d = data.iloc[i,7]
            dir_o = o_frame_players.iloc[closest_o,7]
            if np.abs(dir_d - dir_o) > 180:
                dir_diff = 360 - np.abs(dir_d - dir_o)
            else:
                dir_diff = np.abs(dir_d - dir_o)
            min_dirs.append(dir_diff)
    
        if len(min_dirs)==1:
            off_dir_var = 0
        else:
            off_dir_var = statistics.variance(min_dirs)
        off_dir_mean = np.mean(min_dirs)
        
        ratios = []
        for i in range(data.shape[0]):
            frame_num = data.iloc[i,13]
            o_frame_players = offensedata.loc[offensedata["frameId"]==frame_num,:]
            d_frame_players = defensedata.loc[defensedata["frameId"]==frame_num,:]
            o_dist_list = []
            d_dist_list = []
            for j in range(o_frame_players.shape[0]):
                dist = np.sqrt((data.iloc[i,2] - o_frame_players.iloc[j,2])**2 + (data.iloc[i,3]-o_frame_players.iloc[j,3])**2)
                o_dist_list.append(dist)
            for j in range(d_frame_players.shape[0]):
                dist = np.sqrt((data.iloc[i,2] - d_frame_players.iloc[j,2])**2 + (data.iloc[i,3]-d_frame_players.iloc[j,3])**2)
                d_dist_list.append(dist)
            closest_o = np.where(o_dist_list==min(o_dist_list))[0][0]
            closest_d = np.where(d_dist_list==min(d_dist_list))[0][0]
            o_min_dist = o_dist_list[closest_o]
            close_dist = np.sqrt((o_frame_players.iloc[closest_o,2]-d_frame_players.iloc[closest_d,2])**2+(o_frame_players.iloc[closest_o,3]-d_frame_players.iloc[closest_d,3])**2)
            ratio = o_min_dist / close_dist
            ratios.append(ratio)
    
        rat_mean = np.mean(ratios)
        if len(ratios)==1:
            rat_var=0
        else:
            rat_var = statistics.variance(ratios)
            
        direction = data.iloc[0,-2]
        or_diffs = []
        for i in range(data.shape[0]):
            orientation = data.iloc[i,6]
            if direction == "right":
                or_diff = np.abs(270-orientation)
                if or_diff > 180:
                    or_diff = 360 - np.abs(270-orientation)
            else:
                or_diff = np.abs(90-orientation)
                if or_diff > 180:
                    or_diff = 360 - np.abs(90-orientation)
    
            or_diffs.append(or_diff)
    
        los_or_mean = np.mean(or_diffs)
        
        is_same_way = []
        for i in range(data.shape[0]):
            orientation = data.iloc[i,6]
            frame_num = data.iloc[i,13]
            o_frame_players = offensedata.loc[offensedata["frameId"]==frame_num,:]
            o_dist_list = []
            for j in range(o_frame_players.shape[0]):
                dist = np.sqrt((data.iloc[i,2] - o_frame_players.iloc[j,2])**2 + (data.iloc[i,3]-o_frame_players.iloc[j,3])**2)
                o_dist_list.append(dist)
            closest_o = np.where(o_dist_list==min(o_dist_list))[0][0]
            off_orientation = o_frame_players.iloc[closest_o,6]
            if np.abs(orientation - off_orientation) <= 60:
                is_same_way.append(1)
            else:
                is_same_way.append(0)
    
        percent_same_or = np.mean(is_same_way)*100
        
        featuresabt.loc[i,:] = [var_x, var_y, var_s, off_var, def_var, off_mean, def_mean, off_dir_var, off_dir_mean, rat_mean, rat_var, los_or_mean, percent_same_or]
        
    
    return featuresbbt, featuresabt