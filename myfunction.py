# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""

import random
#import math



#rateを入れれば、さいころを取得
#rateは0.0から3.0まで0.5刻み
def make_saikoro(rate):

    saikoro = [0]*6
    #1と6の目の数
    good_number_num = rate/0.5
    global idx
    for idx in range(int(good_number_num)):
        saikoro[idx] = random.choice([1,6])

    i = idx + 1

    for idx in range(i,6):
        saikoro[idx] = random.choice([2,3,4,5])
        
    #print(saikoro)
    return saikoro
    
def game_sa(x,y):
    return((x[0]-y[0])-(x[1]-y[1]))/2
    
def get_juni(t_idex,Junni):
    for i in range(6):
        if(Junni[i] == t_idex):
            return i + 1
        
#make_saikoro(2.9)