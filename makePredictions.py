# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 10:29:17 2021

@author: CaleShealy
"""

import numpy as np
import pandas as pd
import pickle

gmm_bbt = pickle.load(open("gmm_bbt.sav","rb"))
gmm_abt = pickle.load(open("gmm_abt.sav","rb"))

def makePredictions(featuresbbt, featuresabt):
    bbt_pred = gmm_bbt.predict_proba(featuresbbt)
    abt_pred = gmm_abt.predict_proba(featuresabt)
    preds = np.concatenate([bbt_pred, abt_pred])
    return preds
    