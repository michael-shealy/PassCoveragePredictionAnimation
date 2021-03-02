# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 17:54:59 2021

@author: CaleShealy
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import matplotlib.patches as patches
import statistics
import progressbar
from time import sleep
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, adjusted_rand_score
from ipywidgets import interact, fixed
from matplotlib import animation
from matplotlib.animation import FFMpegWriter
import dateutil
from math import radians
from IPython.display import Video
import warnings
from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.transform import dodge
from bokeh.io import curdoc
from bokeh.transform import dodge
from bokeh.layouts import column, layout, row
from bokeh.models import CustomJS, MultiChoice, RadioButtonGroup, Div, Select, FileInput, Panel, Tabs, Dropdown

gameinfo = pd.read_csv("data/games.csv")
playinfo = pd.read_csv("data/plays.csv")
week_menu = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17"]
week_dropdown = Select(title="What Week Was the Game?",value=week_menu[0],options=week_menu)
print(week_dropdown.value)

week_data = pd.read_csv("data/week"+week_dropdown.value+".csv")
unique_games = week_data["gameId"].unique()
print(unique_games)
print(len(unique_games))
game_menu = []
for game in unique_games:
    game_data = gameinfo.loc[gameinfo["gameId"]==game,:]
    print(game_data.shape)
    game_menu.append(game_data.iloc[0,3] + " vs. " + game_data.iloc[0,4])
    
print(game_menu)
game_dropdown = Select(title="What Game Was the Play?",value=game_menu[0],options=game_menu)
print(game_dropdown.value)
teams = game_dropdown.value.partition(' vs. ')
selected_game = gameinfo.loc[(gameinfo["homeTeamAbbr"]==teams[0]) & (gameinfo["visitorTeamAbbr"]==teams[2]),"gameId"].values[0]
print(selected_game)

plays_data = week_data.loc[week_data["gameId"]==selected_game,:]
unique_plays = plays_data["playId"].unique()
print(unique_plays)
print(len(unique_plays))

unique_plays = [str(unique_plays[i]) for i in range(len(unique_plays))]
print(unique_plays)
play_dropdown = Select(title="Select the Play to Analyze",value=unique_plays[0],options=unique_plays)
print(play_dropdown.value)





def my_input_handler():
    print(week_dropdown.value)
    
def function_to_call(attr,old,new):
    print(week_dropdown.value)


week_dropdown.on_change("value", function_to_call)


curdoc().add_root(week_dropdown)

