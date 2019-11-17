# -*- coding: utf-8 -*-
"""
Created on Tue May 14 16:40:26 2019

@author: Nobuaki
"""
from myfunction import make_saikoro,game_sa

import random
import numpy as np
#import decimal

#チーム
Team = ["広　　島","巨　　人","横　　浜","ヤクルト","阪　　神","中　　日"]
#対戦カード
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

#チームインデックス、勝ち数、負け数、引き分け、勝率,重み,前試合の結果
#omomiは0.0から3.0まで0.5刻み
Syohai = np.array([[0,0,0,0,0,1,0],#広島
                   [1,0,0,0,0,1,0],#巨人
                   [2,0,0,0,0,1.0,0],#横浜
                   [3,0,0,0,0,1.0,0],#ヤクルト
                   [4,0,0,0,0,1.0,0],#阪神
                   [5,0,0,0,0,1.0,0]])#中日
#順位表　勝率の高いチームから順に格納。チームインデックス、勝ち数、負け数、引き分け、ゲーム差、勝率、重み
Junihyo = np.array([[0,0,0,0,0.0,0,0],
                   [0,0,0,0,0.0,0,0],
                   [0,0,0,0,0.0,0,0],
                   [0,0,0,0,0.0,0,0],
                   [0,0,0,0,0.0,0,0],
                   [0,0,0,0,0.0,0,0]])

def Game(taisen):
    for x in range(taisen.shape[0]):
        ##チームのセット
        omote_idx = taisen[x,0]
        ura_idx   = taisen[x,1]
        #saikoro = [1,2,3,4,5,6]
        #重みで、目の確立を操作する。
        #print('{:.1f}'.format(round(Syohai[omote_idx,5],1)))
        omote_saikoro = make_saikoro(round(Syohai[omote_idx,5],1))
        #print(Syohai[omote_idx,5])
        ura_saikoro = make_saikoro(round(Syohai[ura_idx,5],1))
        Score_A = []
        Score_B = []
        sayonara = ""

#１，２だったら1点
        i = 1
        for i in range(12):
            
            point = 0
            while sayonara == "":
                saikoro_choice = np.random.choice(omote_saikoro)
                
                #print(saikoro_choice)
                if saikoro_choice == 1:
                    #print(Syohai[omote_idx,5])
                    point += 1
    
                elif saikoro_choice == 6:
                    point += 1
                    
                else:
                    point += 0
                    Score_A.append(int(point))
                    break
            

#裏の攻
            point = 0        
            sayonara == ""
            if i>=9 and (sum(Score_A) < sum(Score_B)):
                #Score_B.append(point)
                sayonara = "x"#裏の攻撃はやらない
                break
                
            else:    
                while sayonara == "": 
                    saikoro_choice = random.choice(ura_saikoro)
                    #print(saikoro_choice)

                    if saikoro_choice == 1:
                        #print(Syohai[omote_idx,5])
                        point += 1
                        #Score_B.append(point)
#さよなら判定
                        if i>=9 and (sum(Score_A) < sum(Score_B)+point):
                            sayonara = "x サヨナラ1点"
                            Score_B.append(point)
                            break
    
                    elif saikoro_choice == 6:
                        point += 1
    
#さよなら判定
                        if i>=9 and (sum(Score_A) < sum(Score_B)+point):
                            Score_B.append(point)
                            sayonara = "x サヨナラ1点"
                            break
                    
                    else:
                        point += 0
                        Score_B.append(point)
                        break
                    
#試合終了の判定
            if i>=9 and (sum(Score_A) != sum(Score_B)):
                break

###########################################
        print(Team[omote_idx] + ":", end= "")
        print(Score_A, end= "|") 
        print(sum(Score_A))

        print(Team[ura_idx] + ":", end= "") 
        print(Score_B, end= "|") 
        print(str(sum(Score_B)) + sayonara,end ="\n\n")

        if(Score_A > Score_B):
            Syohai[omote_idx,1] += 1
            Syohai[ura_idx,2]   += 1
           ###表が連勝したら⁺0.1、裏が連敗したら-0.1
            if(Syohai[omote_idx,6] == 1) and (Syohai[omote_idx,5] < 3.0):
                #print("連勝")
                Syohai[omote_idx,5] += 0.05
            if(Syohai[ura_idx,6] == -1) and (Syohai[ura_idx,5] > 0):
                Syohai[omote_idx,5] -= 0.05
                
            Syohai[omote_idx,6] = 1
            Syohai[ura_idx,6] = -1
            
        elif(Score_A < Score_B):
            Syohai[ura_idx,1]  += 1
            Syohai[omote_idx,2] += 1
            #表が連敗したら-0.1、裏が連勝したら+0.1
            if(Syohai[omote_idx,6] == -1) and (Syohai[omote_idx,5] > 0):
               Syohai[omote_idx,5] -= 0.05
            if(Syohai[ura_idx,6] == 1) and (Syohai[ura_idx,5] < 3.0):
               Syohai[omote_idx,5] += 0.05
            
            Syohai[omote_idx,6] = -1
            Syohai[ura_idx,6] = 1
            
        else:
            Syohai[omote_idx,3] += 1
            Syohai[ura_idx,3] += 1
                        
            Syohai[omote_idx,6] = 0
            Syohai[ura_idx,6] = 0
            
        #重みの制限
        #print(Syohai[omote_idx,5])
        #print(Syohai[ura_idx,5])
###############################################
    
for  kaisuu in range(15):
    #試合開始
    Game(Taisen_1)
    Game(Taisen_2)
    Game(Taisen_3)
    Game(Taisen_4)
    Game(Taisen_5)
    Game(Taisen_6)


#Syoritsu_to_Junni = []
Kachi_su_to_Junni = []

for idx in range(len(Team)):
    Kachi_su_to_Junni.append(Syohai[idx,1])
    
#順位表の計算
#Junni=np.argsort(Syoritsu_to_Junni)[::-1]
Junni=np.argsort(Kachi_su_to_Junni)[::-1]
#print(Junni)

Junni1=np.argsort(Syohai)[::-1]

#idx = 0
for idx in range(len(Junni)):
    Junihyo[idx,0] = int(Junni[idx])
    #print(Junihyo[idx,0])
    #順位表に試合結果を転記
    iidx = 1
    for iidx in range(4):
        Junihyo[idx,iidx] =Syohai[Junni[idx],iidx]
    
    Junihyo[idx,4] = Junihyo[idx,1]/(Junihyo[idx,1]+ Junihyo[idx,2] + Junihyo[idx,3])
    Junihyo[idx,6] = Syohai[idx,5] 

Junihyo[0,5] = 0
x=[0,0]
y=[0,0]

for idx in range(1,6):
    #print(idx)
    #print(Junihyo[idx-1,1])
    x[0] = Junihyo[idx-1,1]
    x[1] = Junihyo[idx-1,2]
    y[0] = Junihyo[idx,1]
    y[1] = Junihyo[idx,2]
    Junihyo[idx,5] = game_sa(x,y)
    
    
for idx in range(6):
    #iidx = int(Junihyo[idx,0])
    #print(str(iidx-1))
    #print(Team[iidx-1])
    print(Team[int(Junihyo[idx,0])], end= ":")
    #print(Syohai[int(Junihyo[idx,0]-1),])
    #勝ち数
    print(str(int(Junihyo[idx,1])) + "|" + str(int(Junihyo[idx,2])) + "|" + str(int(Junihyo[idx,3]))+ "|" + str(Junihyo[idx,5])+ "|" + str(round(Junihyo[idx,4],2))+ "|" + str(round(Junihyo[idx,6],2)))

#print(Syohai)
#print(get_juni(0,Junni))
print((kaisuu+1)*15)