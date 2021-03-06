﻿# -*- coding: utf-8 -*-
"""
Created on Tue May 14 16:40:26 2019

@author: Nobuaki
"""
from myfunction import game_sa,make_saikoro10,kougeki

#import random
import numpy as np
from scipy.stats import rankdata

import matplotlib.pyplot as plt


#import decimal

#チーム
Team = ["広　　島","巨　　人","横　　浜","ヤクルト","阪　　神","中　　日"]
#対戦カード


Taisen_0 = np.array([[0,1]])


Taisen_1 = np.array([[0,3],
                     [1,4],
                     [2,5]])

Taisen_2 = np.array([[0,5],
                     [1,3],
                     [2,4]])

Taisen_3 = np.array([[0,4],
                     [1,5],
                     [2,3]])

Taisen_4 = np.array([[0,1],
                     [3,4]])

Taisen_5 = np.array([[0,2],
                     [3,5]])

Taisen_6 = np.array([[1,2],
                     [4,5]])

#チームインデックス、勝ち数、負け数、引き分け、勝率,重み(ゲーム差),前試合の結果,順位,総打数,総安打

Syohai = np.array([[0,0,0,0,0,1.05,0,0,0,0],#広島
                   [1,0,0,0,0,1.05,0,0,0,0],#巨人
                   [2,0,0,0,0,1.04,0,0,0,0],#横浜
                   [3,0,0,0,0,1.03,0,0,0,0],#ヤクルト
                   [4,0,0,0,0,1.03,0,0,0,0],#阪神
                   [5,0,0,0,0,1.02,0,0,0,0]])#中日

#名前、打率、（ホームラン数）
TeamA = np.array([["sasaki", 0.33],#1
         ["sasaki", 0.33],#2
         ["sasaki", 0.33],#3
         ["sasaki", 0.33],#4
         ["sasaki", 0.33],#5
         ["sasaki", 0.33],#6
         ["sasaki", 0.33],#7
         ["sasaki", 0.33],#8
         ["sasaki", 0.33]])#9
         

game_loop = 1
Out = 3

Gh = np.zeros((7, (game_loop)))

def Game(taisen):
    for x in range(taisen.shape[0]):
        ##チームのセット
        omote_idx = taisen[x,0]
        ura_idx   = taisen[x,1]
        #saikoro = [1,2,3,4,5,6]
        omote_saikoro = make_saikoro10()
        ura_saikoro = make_saikoro10()
        
        Score_A = []
        Score_B = []
        Batt_and_Hit_A = [0,0]
        Batt_and_Hit_B = [0,0]
        sayonara = ""

#１，２だったら1点
        i = 0
        for i in range(12):
            #表の攻撃            
            print(Team[taisen[x,0]]+str(i+1) + "回の表" + str(sum(Score_A)) +"対"+ str(sum(Score_B)), end = "")
            #9回まで。outの数が閾値を超えない限り、攻撃を続ける。
            #Score_A.append(int(kougeki(omote_saikoro,Out,-1)))
            tmp = kougeki(omote_saikoro,Out,-1)
            Score_A.append(int(tmp[0]))
            Batt_and_Hit_A[0] += tmp[1]
            Batt_and_Hit_A[1] += tmp[2]

            #裏の攻撃
            #8回まで
            if i<8:
                print(Team[taisen[x,1]]+str(i+1) + "回の裏"+ str(sum(Score_A)) +"対"+ str(sum(Score_B)), end = "")
                #Score_B.append(int(kougeki(ura_saikoro,Out,-1)[0]))
                tmp = kougeki(ura_saikoro,Out,-1)
                Score_B.append(int(tmp[0]))
                Batt_and_Hit_B[0] += tmp[1]
                Batt_and_Hit_B[1] += tmp[2]

            #9回以降は攻撃するかの判断する。
            #勝っている場合は、攻撃しない
            elif i>=8:
                sayonara = ""
                if sum(Score_A) < sum(Score_B):
                    sayonara = "x"
                    Score_B.append(0)
                    break

                #引き分けもしくは負けている場合は、攻撃する。
                else:
                    #Score_B.append(int(kougeki(ura_saikoro, Out,sum(Score_A)-sum(Score_B)+1)[0]))
                    print(Team[taisen[x,1]]+str(i+1) + "回の裏"+ str(sum(Score_A)) +"対"+ str(sum(Score_B)), end = "")
                    tmp = kougeki(ura_saikoro,Out,sum(Score_A)-sum(Score_B)+1)
                    Score_B.append(int(tmp[0]))
                    Batt_and_Hit_B[0] += tmp[1]
                    Batt_and_Hit_B[1] += tmp[2]
                    #print("かったかも")
                    #攻撃終了後の確認
                    #裏がさよならのとき
                    if sum(Score_A) < sum(Score_B):
                        sayonara = "xさよなら"
                        break
                    #表が勝った時
                    elif sum(Score_A) > sum(Score_B):
                        break

###########################################
        print(Team[omote_idx] + ":", end= "")
        print(Score_A, end= "|") 
        print(sum(Score_A), end = " ")
        print("H" + str(Batt_and_Hit_A[1]), end = "\n")

        print(Team[ura_idx] + ":", end= "")
        #サヨナラの場合、Xとしたい。
        #Score_B[-1] = 'X'
        print(Score_B, end= "|") 
        print(str(sum(Score_B)) + sayonara,end =" ")
        print("H" + str(Batt_and_Hit_B[1]), end = "\n")

###########################################

        #print(ura_idx)
        if(sum(Score_A) > sum(Score_B)):
            Syohai[omote_idx,1] += 1
            Syohai[ura_idx,2]   += 1
           ###表が連勝したら⁺0.1、裏が連敗したら-0.1
            if(Syohai[omote_idx,6] == 1) and (Syohai[omote_idx,5] < 2.0):
                print("表 連勝①")
                Syohai[omote_idx,5] += 0.01

            if(Syohai[ura_idx,6] == -1) and (Syohai[ura_idx,5] > 0.5):
                print("裏 連敗②")
                Syohai[ura_idx,5] -= 0.01
                
            Syohai[omote_idx,6] = 1
            Syohai[ura_idx,6] = -1
            
        elif(sum(Score_A) < sum(Score_B)):
            Syohai[ura_idx,1]  += 1
            Syohai[omote_idx,2] += 1
            #表が連敗したら-0.1、裏が連勝したら+0.1
            if(Syohai[omote_idx,6] == -1) and (Syohai[omote_idx,5] > 0.5):
                print("表 連敗③")
                Syohai[omote_idx,5] -= 0.01
                
            if(Syohai[ura_idx,6] == 1) and (Syohai[ura_idx,5] < 2.0):
                print("裏 連勝④")
                Syohai[ura_idx,5] += 0.01
            
            Syohai[omote_idx,6] = -1
            Syohai[ura_idx,6] = 1
            
        else:
            Syohai[omote_idx,3] += 1
            Syohai[ura_idx,3] += 1
                        
            Syohai[omote_idx,6] = 0
            Syohai[ura_idx,6] = 0
        #print(Syohai[omote_idx,5])
        #print()
        print("\n")
        #勝率の計算(引分試合を除いた試合数のうち、勝った割合)
        Syohai[omote_idx,4] = Syohai[omote_idx,1]/(Syohai[omote_idx,1]+Syohai[omote_idx,2])
        Syohai[ura_idx,4] = Syohai[ura_idx,1]/(Syohai[ura_idx,1]+Syohai[ura_idx,2])
        
        #全打数の入力
        Syohai[omote_idx,8 ] += Batt_and_Hit_A[0]
        Syohai[ura_idx,8 ] += Batt_and_Hit_B[0]
        
        #前安打数
        Syohai[omote_idx,9 ] += Batt_and_Hit_A[1]
        Syohai[ura_idx,9 ] += Batt_and_Hit_B[1]
        
        #print(Syohai)


###############################################
    
for  kaisuu in range(game_loop):
    #試合開始
    Game(Taisen_0)
    #Game(Taisen_1)
    #Game(Taisen_2)
    #Game(Taisen_3)
    #Game(Taisen_4)
    #Game(Taisen_5)
    #Game(Taisen_6)
    
    #順位の計算
    Saisyu_Jun = []
    #①勝率、②勝利数、③並んだ球団どうしの勝率を比較
    #勝率での順位
    #print(Syohai)
    Syoritsu_Jun = rankdata(-Syohai[:, 4],method='min') 
    #print(Syoritsu_Jun)
    Saisyu_Jun = Syoritsu_Jun
    #print(Syoritsu_Jun.shape)
    
    for juni in range(1,7):
        #print(np.count_nonzero(Syoritsu_Jun == juni, axis=0))
        if (np.count_nonzero(Syoritsu_Jun == juni, axis=0)) > 1:
            #print(juni)
            temp = np.full((6,8), 0.00)
            dabl = []
            for idx in range(0,6):         
                if Syoritsu_Jun[idx] == juni:
                    dabl.append(idx)
                    
                    temp[idx]= Syohai[idx,0:8]
                
            #print(dabl)
            Kachisu_Jun_temp = rankdata(-temp[:, 1],method='min') -1
            #print(Kachisu_Jun_temp)
            
            for ii in dabl:
                Saisyu_Jun[ii] = Syoritsu_Jun[ii] + Kachisu_Jun_temp[ii] 
                
    #print(Saisyu_Jun)
           
    
    for idx in range(0,6): 
        #順位の更新
        Syohai[idx,7] = Saisyu_Jun[idx]
        #グラフ情報への更新
        Gh[idx,kaisuu] = Saisyu_Jun[idx]
        #消化ゲーム数
        Gh[6,kaisuu] = (kaisuu + 1) * 5

#全試合終了

#順位順にソートしてコピー
Junihyo = Syohai[np.argsort(Syohai[:,7])][::1]

#５列目を初期化
Junihyo[0,5] = 0

for idx in range(1,6):
    #print(idx)
    #print(Junihyo[idx-1,1])
    x = [Junihyo[idx-1,1],Junihyo[idx-1,2]]
    y = [Junihyo[idx,1],Junihyo[idx,2]]
    #print(x)
    #print(y)
    #Junihyo の５列目にゲーム差を上書き
    Junihyo[idx,5] = game_sa(x,y)

    
#print(Junihyo)   

#順位表の表示
print("順位:チーム 勝 敗 分 率 差 チーム打率")
print("----------------------------")
for idx in range(6):
    #順位
    print(str(int(Junihyo[idx,7]))+"位", end= ":")
    #チーム名
    print(Team[int(Junihyo[idx,0])], end= ":")
    #print(Syohai[int(Junihyo[idx,0]-1),])
    #勝ち数,負け数、引き分け、勝率、ゲーム差、チーム打率
    print(str(int(Junihyo[idx,1])) + "|" + str(int(Junihyo[idx,2])) + "|" \
          + str(int(Junihyo[idx,3]))+ "|" + '{:.3f}'.format(Junihyo[idx,4])\
          + "|" + str(Junihyo[idx,5]) + "|"\
          + '{:.3f}'.format(Junihyo[idx,9]/Junihyo[idx,8])\
              
              )

#順位のグラフ
#グラフの定義
plt.ylim(0, 7)
plt.gca().invert_yaxis()

plt.xlabel("game num")
plt.ylabel("Rank")
plt.grid(True)

#広島、巨人、横浜、ヤクルト、阪神、中日
colorlist1 = ['#ff0000', '#F97709', '#094a8c', '#98c145', '#ffe201', '#1eb2e9']
colorlist2 = ['#ffffff', '#000000', '#ffffff', '#ffffff', '#000000', '#ffffff']

#横軸
left = Gh[6]

#縦軸
height0 = Gh[0]
height1 = Gh[1]
height2 = Gh[2]
height3 = Gh[3]
height4 = Gh[4]
height5 = Gh[5]


plt.plot(left, height0, color=colorlist1[0], marker="o", label="carp")
plt.plot(left, height1, color=colorlist1[1], marker="o", label="giants")
plt.plot(left, height2, color=colorlist1[2], marker="o", label="baystars")
plt.plot(left, height3, color=colorlist1[3], marker="o", label="swallows")
plt.plot(left, height4, color=colorlist1[4], marker="o", label="tigers")
plt.plot(left, height5, color=colorlist1[5], marker="o", label="doragons")

plt.legend(ncol = 3, bbox_to_anchor=(0.5, 1), loc='lower center', borderaxespad=0, fontsize=10)