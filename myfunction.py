# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""

import random
import math

#rateを入れれば、さいころを取得
#rateは0.5から2.0まで
def make_saikoro(rate):
    #rate1 = rate * 10
 
    rate1 = math.ceil(rate*10) 
    #print("a"+ str(rate1))
    saikoro = [0]*60
    saikoro_idx = random.sample(range(60),k=60)
    
    for idx in range(int(rate1)+1):
        saikoro[saikoro_idx[idx]] = 1
    i = idx
    for idx in range(i,i+6):
        saikoro[saikoro_idx[idx]] = 2
    i = idx
    for idx in range(i,60):
        saikoro[saikoro_idx[idx]] = random.choice([3,4,5,6])
        
    #print(saikoro)
    return saikoro

#print(make_saikoro(1.3))
    
def game_sa(x,y):
    return((x[0]-y[0])-(x[1]-y[1]))/2