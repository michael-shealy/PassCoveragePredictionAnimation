# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 10:36:44 2021

@author: CaleShealy
"""

from ipywidgets import interact, fixed
from matplotlib import animation
from matplotlib.animation import FFMpegWriter
import dateutil
from math import radians
from IPython.display import Video
#import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from create_football_field import create_football_field
import matplotlib.patches as patches
import ffmpeg

def animate_player_movement(weekNumber, playId, gameId,nflId,preds):
    weekData = pd.read_csv('data/week' + str(weekNumber) + '.csv')
    playData = pd.read_csv('data/plays.csv')
    
    playHome = weekData.query('gameId==' + str(gameId) + ' and playId==' + str(playId) + ' and team == "home"')
    playAway = weekData.query('gameId==' + str(gameId) + ' and playId==' + str(playId) + ' and team == "away"')
    playFootball = weekData.query('gameId==' + str(gameId) + ' and playId==' + str(playId) + ' and team == "football"')
    
    playHome['time'] = playHome['time'].apply(lambda x: dateutil.parser.parse(x).timestamp()).rank(method='dense')
    playAway['time'] = playAway['time'].apply(lambda x: dateutil.parser.parse(x).timestamp()).rank(method='dense')
    playFootball['time'] = playFootball['time'].apply(lambda x: dateutil.parser.parse(x).timestamp()).rank(method='dense')
    
    maxTime = int(playAway['time'].unique().max())
    print(maxTime)
    minTime = int(playAway['time'].unique().min())
    print(minTime)
    
    yardlineNumber = playData.query('gameId==' + str(gameId) + ' and playId==' + str(playId))['yardlineNumber'].item()
    yardsToGo = playData.query('gameId==' + str(gameId) + ' and playId==' + str(playId))['yardsToGo'].item()
    absoluteYardlineNumber = playData.query('gameId==' + str(gameId) + ' and playId==' + str(playId))['absoluteYardlineNumber'].item() - 10
    playDir = playHome.sample(1)['playDirection'].item()
    
    if (absoluteYardlineNumber > 50):
        yardlineNumber = 100 - yardlineNumber
    if (absoluteYardlineNumber <= 50):
        yardlineNumber = yardlineNumber
        
    if (playDir == 'left'):
        yardsToGo = -yardsToGo
    else:
        yardsToGo = yardsToGo
    
    fig, ax = create_football_field(highlight_line=True, highlight_line_number=yardlineNumber,figsize=(60,31.65))
    playDesc = playData.query('gameId==' + str(gameId) + ' and playId==' + str(playId))['playDescription'].item()
    plt.title(f'Game # {gameId} Play # {playId} \n {playDesc}',fontsize=40)
    
    def update_animation(time):
        patch = []
        
        homeX = playHome.query('time == ' + str(time))['x']
        homeY = playHome.query('time == ' + str(time))['y']
        homeNum = playHome.query('time == ' + str(time))['jerseyNumber']
        homeOrient = playHome.query('time == ' + str(time))['o']
        homeDir = playHome.query('time == ' + str(time))['dir']
        homeSpeed = playHome.query('time == ' + str(time))['s']
        patch.extend(plt.plot(homeX, homeY, 'o',c='gold', ms=75, mec='white'))
        
        # Home players' jersey number 
        for x, y, num in zip(homeX, homeY, homeNum):
            patch.append(plt.text(x, y, int(num), va='center', ha='center', color='black', fontsize=28))
            
        '''
        # Home players' orientation
        for x, y, orient in zip(homeX, homeY, homeOrient):
            dx, dy = calculate_dx_dy_arrow(x, y, orient, 1, 1)
            patch.append(plt.arrow(x, y, dx, dy, color='gold', width=0.5, shape='full'))
            
        # Home players' direction
        for x, y, direction, speed in zip(homeX, homeY, homeDir, homeSpeed):
            dx, dy = calculate_dx_dy_arrow(x, y, direction, speed, 1)
            patch.append(plt.arrow(x, y, dx, dy, color='black', width=0.25, shape='full'))
            
        '''
        
        # Home players' location
        awayX = playAway.query('time == ' + str(time))['x']
        awayY = playAway.query('time == ' + str(time))['y']
        awayNum = playAway.query('time == ' + str(time))['jerseyNumber']
        awayOrient = playAway.query('time == ' + str(time))['o']
        awayDir = playAway.query('time == ' + str(time))['dir']
        awaySpeed = playAway.query('time == ' + str(time))['s']
        patch.extend(plt.plot(awayX, awayY, 'o',c='orangered', ms=75, mec='white'))
        
        # Away players' jersey number 
        for x, y, num in zip(awayX, awayY, awayNum):
            patch.append(plt.text(x, y, int(num), va='center', ha='center', color='white', fontsize=28))
         
        '''
        # Away players' orientation
        for x, y, orient in zip(awayX, awayY, awayOrient):
            dx, dy = calculate_dx_dy_arrow(x, y, orient, 1, 1)
            patch.append(plt.arrow(x, y, dx, dy, color='orangered', width=0.5, shape='full'))
        
        # Away players' direction
        for x, y, direction, speed in zip(awayX, awayY, awayDir, awaySpeed):
            dx, dy = calculate_dx_dy_arrow(x, y, direction, speed, 1)
            patch.append(plt.arrow(x, y, dx, dy, color='black', width=0.25, shape='full'))
            
        '''
        
        # Away players' location
        footballX = playFootball.query('time == ' + str(time))['x']
        footballY = playFootball.query('time == ' + str(time))['y']
        patch.extend(plt.plot(footballX, footballY, 'o', c='black', ms=25, mec='white', data=playFootball.query('time == ' + str(time))['team']))
        
        for i in range(len(nflId)):
            player = weekData.query('gameId==' + str(gameId) + ' and playId==' + str(playId) + ' and nflId =='+str(nflId[i]) + ' and frameId==' + str(time))
            
            patch.append(ax.add_patch(plt.Rectangle(xy=(player.iloc[0,1]-20,player.iloc[0,2]-4.5),width=15,height=9,color='blue')))
            patch.append(plt.arrow(player.iloc[0,1]-5,player.iloc[0,2],5,0,color='black',width=0.25,shape='full'))
            #patch.extend(plt.plot(player.iloc[0,1]-3,player.iloc[0,2]+3,"s",color='green',ms=15))

            patch.append(plt.text(player.iloc[0,1]-12.5,player.iloc[0,2]+1.5,'P(man): {:.4f}'.format(round(preds[i][time-1,1],4)),va='center',color='white',fontsize=36,ha='center'))
            patch.append(plt.text(player.iloc[0,1]-12.5,player.iloc[0,2]-1.5,'P(zone): {:.4f}'.format(round(preds[i][time-1,0],4)),va='center',color='white',fontsize=36,ha='center'))
            #print(player)
        return patch
    
    ims = [[]]
    for time in np.arange(minTime, maxTime):
        patch = update_animation(time)
        ims.append(patch)
        
    anim = animation.ArtistAnimation(fig, ims, repeat=False)
    
    return anim