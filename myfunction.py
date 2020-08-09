# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""

import random
import math
import numpy as np


#rateを入れれば、さいころを取得
#rateは0.0から3.0まで0.5刻み
def make_saikoro(rate):

    saikoro = [0]*6
    #1と6の目の数
    good_number_num = rate//0.50
    #print(rate)
    #print(good_number_num)
    global idx
    for idx in range(int(good_number_num)):
        saikoro[idx] = random.choice([1,10])

    i = idx + 1

    for idx in range(i,6):
        saikoro[idx] = random.choice([2,3,4,5])
        
    #print(saikoro)
    return saikoro

#さいころの目は１から１０
def make_saikoro10():

    saikoro = [1,2,3,4,5,6,7,8,9,10]
    
    return saikoro

def make_saikoro100(daritsu):
    #1-3は安打
    #１から３の目を打率×１０の切り上げの個数
    hitNum = math.ceil(daritsu * 10)
    saikoro = [0] * 100
    #1から100までのさいころ
    for idx in range(1,101):
        
        saikoro[idx-1] = random.choice()
    print(saikoro)
    return saikoro

def game_sa(x,y):#チームインデックス同士のゲーム差プラスの時の順位はX>Y
    return((x[0]-y[0])-(x[1]-y[1]))/2
    
def get_juni(t_idex,Junni):
    for i in range(6):
        if(Junni[i] == t_idex):
            return i + 1

def get_runner(r):
    rui0 = 0b0000
    rui1 = 0b0001
    rui2 = 0b0010
    rui3 = 0b0100
    rui4 = 0b0111
    zyotai = "ランナー、"
    
    bin(r)
    
    if r==rui4:
        zyotai += "満塁"
    else:
        if (r & rui1) == rui1:
            zyotai += "1"
            
        if (r & rui2 == rui2):
            if(r & rui1 == rui1):
                zyotai += ",2"
            else:
                zyotai += "2"
                
        if (r & rui3 == rui3):
            if (r & rui1 == rui1) or (r & rui2 == rui2):
                zyotai += ",3"
            else:
                zyotai += "3"
                
        if(r != rui0):
            zyotai += "塁"
            
    if(r == rui0):
        zyotai += "なし"

    return zyotai

##
#print(runner(0b0101))
#print(get_runner(0b0101))

def point_check(run, hit):
    rui1 = 0b0001
    #rui2 = 0b0010
    #rui3 = 0b0100
    home = 0b1000
    clea = 0b0111
    point = 0
    tmp_runner = run

    #ヒットごとの進塁
    for i in range(1,hit+1):
        #print("進塁")
        #print(i)
        tmp_runner = (tmp_runner << 1)

        #打者１塁へ
        if(i==1):
            #print("1rui")
            tmp_runner = tmp_runner | rui1
        
        #print(bin(tmp_runner))

        #点が入ったか確認
        home_runner = tmp_runner & home

        if(home_runner == home):
            print("1点追加")
            point+=1
        #print("ホームランナー削除")
        home_runner = tmp_runner & clea
        #print(bin(home_runner))
        
    #print("このヒットで得点は、" + str(point) + "点")
        #print(point)
        
    return point,home_runner

#さいころ、攻撃できるアウトカウント、サヨナラが発生するために必要な得点
def kougeki(saikoro,out,score_dif):
    kai_point = [0,0,0] #得点、打数（打者の数）、安打数
    add_point = 0
    outcount = 0
    #回のはじめ
    runner = 0b0000
    

    #アウトの閾値まで攻撃
    while outcount < out:
        #print(str(outcount) + "アウト、" + runner(runner))
        #print(bin(runner))
        print(get_runner(runner))
        
        kai_point[1] += 1
        
        saikoro_choice = np.random.choice(saikoro)
        print("ピッチャー、なげました", end = " ")
        #print(saikoro_choice)
        
        #4-10は、アウト
        if saikoro_choice >=4 :
            outcount+=1
            print(str(outcount) + "out!")
        
        #1-3は安打
        else:
            #print("Hit!")  
            kai_point[2] += 1
            
            saikoro_choice = np.random.choice(saikoro)

            #print(saikoro_choice)
            #もう一回振って、1-7はシングル
            if 1 <= saikoro_choice <=7:
                print("シングルヒット")
                #print(bin(runner))
                add_point, runner = point_check(runner,1)
            #8-9は２ベース
            elif 7 <= saikoro_choice <=9:
                print("2塁打")
                add_point, runner = point_check(runner,2)
            #10は、、
            elif saikoro_choice ==10:
                saikoro_choice = np.random.choice(saikoro)
                print("入るか？",end = "")
                #print(saikoro_choice)
                ##1-6はスリーベース
                if 1 <= saikoro_choice <=3:
                    print("3塁打")
                    add_point, runner = point_check(runner,3)
                #7-10はホームラン
                elif 4 <= saikoro_choice <=10:
                    print("home run!!")
                    add_point, runner = point_check(runner,4)
            
            #print("ここで" + str(kai_point) + "点")
            kai_point[0] += add_point
            
            #サヨナラが発生する状態において、ヒットごとにサヨナラの確認をして、成立したら、攻撃中止。
            if 1 <= score_dif and kai_point[0] + add_point >= score_dif:
                break
    
    print("この回" + str(kai_point[0]) + "点")
    print("\n")
    return kai_point

   
    

#make_saikoro100(0.3)

        
    