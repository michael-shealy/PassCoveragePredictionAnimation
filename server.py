# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 13:13:02 2021

@author: CaleShealy
"""

from flask import Flask, render_template, request
import numpy as np
import CPHelpers

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
app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def index():
    weekNumber = ''
    game_vals = ''
    game_selected = ''
    plays = ''
    play_selected = ''
    players = ''
    selected_players = ''
    gif_made = ''
    if request.method=="POST" and "myDropdown" in request.form:
        weekNumber = request.form.get("myDropdown")
        print(weekNumber)
        game_vals = CPHelpers.getGames(int(weekNumber))
        print(game_vals)
        if "gameDropdown" not in request.form:
            return render_template('index.html',weekNumber=weekNumber, game_vals=game_vals)
    if request.method=="POST" and "gameDropdown" in request.form:
        game_selected = request.form.get("gameDropdown")
        print(game_selected)
        plays = CPHelpers.getPlays(game_selected)
        if "playDropdown" not in request.form:
            return render_template('index.html', weekNumber=weekNumber,game_vals=game_vals, game=game_selected, plays=plays)
    if request.method=="POST" and "playDropdown" in request.form:
        play_selected = request.form.get("playDropdown")
        weekNumber = request.form.get("myDropdown")
        game_selected = request.form.get("gameDropdown")
        players = CPHelpers.getPlayInfo(play_selected,weekNumber,game_selected)
        print(players)
        print(play_selected)
        if "players" not in request.form:
            return render_template('index.html',weekNumber=weekNumber, game_vals=game_vals, game=game_selected, plays=plays, play_selected=play_selected, players = players)
    if request.method=="POST" and "players" in request.form:
        selected_players = request.form.getlist("players")
        print(selected_players)
        CPHelpers.create_animation(selected_players,weekNumber,game_selected,play_selected)
        gif_made = 'true'
        return render_template('index.html',weekNumber=weekNumber, game_vals=game_vals, game=game_selected, plays=plays, play_selected=play_selected, players = players, gif_made = gif_made)
    return render_template('index.html')


if __name__ == '__main__':
  app.run(debug=True)