# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 09:03:08 2021

@author: CaleShealy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import math
import matplotlib.patches as patches
import statistics
#import progressbar
#from time import sleep
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, adjusted_rand_score

from ipywidgets import interact, fixed
from matplotlib import animation
from matplotlib.animation import FFMpegWriter
import dateutil
from math import radians
from IPython.display import Video
import warnings
from RemovePassRushers import RemovePassRushers
from createFeatures import createFeatures
from makePredictions import makePredictions
from animate_player_movement import animate_player_movement
import ffmpeg

games = pd.read_csv("data/games.csv")
plays = pd.read_csv("data/plays.csv")
weekId = 1

def getGames(weekId):
    global week 
    week = weekId
    gamedata = games.loc[games["week"]==weekId,:]
    game_vals = []
    for i in range(gamedata.shape[0]):
        game_vals.append(gamedata.iloc[i,4] + " vs. " + gamedata.iloc[i,3])
        
    game_vals = np.array(game_vals)
    game_vals.shape = (game_vals.shape[0],1)
    d = dict(enumerate(game_vals,1))
    for key in d:
        d[key] = d[key][0]
    return d

#gameVals = getGames(weekId)
#print(gameVals)
game = "ATL vs. PHI"

def getPlays(game):
    teams = game.partition(" vs. ")
    away_team = teams[0]
    home_team = teams[2]
    global gameId 
    gameId = games.loc[(games["visitorTeamAbbr"]==away_team) & (games["homeTeamAbbr"]==home_team),"gameId"].values[0]
    playIDs = plays.loc[plays["gameId"]==gameId,"playId"].unique()
    d = dict(enumerate(playIDs,1))
    return d

#playVals = getPlays(game)
#print(playVals)
play = 320
    
def getPlayInfo(play,week,game):
    teams = game.partition(" vs. ")
    away_team = teams[0]
    home_team = teams[2]
    global gameId 
    gameId = games.loc[(games["visitorTeamAbbr"]==away_team) & (games["homeTeamAbbr"]==home_team),"gameId"].values[0]
    weekData = pd.read_csv("data/week"+str(week)+".csv")
    global playData
    playData = weekData.loc[(weekData["gameId"]==gameId) & (weekData["playId"]==int(play)),:]
    global coveragePlayers
    coveragePlayers = RemovePassRushers(playData)
    uniques = coveragePlayers["displayName"].unique()
    d = dict(enumerate(uniques,1))
    return d
    
#players = getPlayInfo(play)
#print(players)
players = ["Desmond Trufant","Robert Alford","Ricardo Allen"]

def create_animation(players,week,game,play):
    teams = game.partition(" vs. ")
    away_team = teams[0]
    home_team = teams[2]
    global gameId 
    gameId = games.loc[(games["visitorTeamAbbr"]==away_team) & (games["homeTeamAbbr"]==home_team),"gameId"].values[0]
    nflIds = []
    preds = []
    for player in players:
        playerData = coveragePlayers.loc[coveragePlayers["displayName"]==player,:]
        nflIds.append(playerData.iloc[0,9])
        featuresbbt, featuresabt = createFeatures(playerData,playData)
        player_preds = makePredictions(featuresbbt,featuresabt)
        preds.append(player_preds)
    anim = animate_player_movement(week,play,gameId,nflIds,preds)
    print(anim)
    anim.save(filename="static/testanimation.gif", writer="ffmpeg")
    
    
#create_animation(players)
