import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import codecs




##################################################掃きだめ関数#####################################################
j = 0

def parser(list1D,s_val,e_val):
    return list1D[s_val:e_val]


def min_search2(list_data): #最小値の配列番号を出力
    Min =list_data[0]
    for i in range(len(list_data)):
        if(Min >= list_data[i]):
            Min = list_data[i]
            array_N = i
    return array_N

def error_val2(list_data, list_ave):  #1D配列の平均値と生データから標準偏差を出力
    dist = 0
    for i in range(len(list_data)):
        dist += np.power(list_data[i] - list_ave , 2) / len(list_data)
    return np.sqrt(dist)


def inf_p(list_I, list_V, list_size): #没関数　変曲点を微分の最大値から計算　if文で正しそうな変曲点にさせている
    diff = list(0 for i in range(list_size))
    for i in range(list_size - 1):
        diff[i+1] = (list_I[i+1] - list_I[i]) /(-list_V[i+1] + list_V[i])
        if (diff[i+1] >= max(diff)):
            if(20 < i and i < 110):
                inf_num = i
    print(inf_num)
    return inf_num

        
########################################グラフプロット関数#####################################################################
def IV_plot_pH(V_bias, Current, Err, pH, pH_degit ,graph_plot ,usecolor, usemarker,Save_Num):
    #print(pH)
    if(graph_plot == True):
        fig = plt.figure()
        Re_pH = list(0 for i in range(len(pH)))
        for i in range(len(pH)):
            Re_pH[i] = pH[i] / np.power(10, pH_degit)
        for i in range(len(pH)):
            plt.plot(V_bias[i]*(-1) , Current[i],
                    label = "pH = {0}".format(Re_pH[i]),
                    color = "{0}".format(usecolor[i]))
                    #marker = "{0}".format(usemarker[i]))
            plt.errorbar(V_bias[i] *(-1), Current[i], yerr= Err[i],capsize=5, fmt='o', markersize=2, ecolor='black', markeredgecolor = "black", color='w')
        #print(Re_pH)
        plt.xlabel("Bias Voltage [V]")
        plt.ylabel("Current[a.u.]")
        plt.xlim(min(V_bias[i] *(-1)) ,max(V_bias[i] *(-1)) - 0.1)
        plt.legend()
        fig.savefig("{0}_IV.png".format(Save_Num))
        
        
        
def IV_plot_frq(V_bias, Current, frq, frq_degit, graph_plot,  usecolor, usemarker):
    if(graph_plot == True):
        Re_frq = list(0 for i in range(len(frq)))
        for i in range(len(frq)):
            Re_frq[i] /= np.power(10, frq_degit)
        for i in range(len(frq)):
            plt.plot(V_bias[i], Current[i],
                    label = "f = {0}kHz".format(Re_frq[i]),
                    colors =usecolor[i],
                    marker = usemarker[i])



def Nernst_plot(V_bias,V_err, pH, pH_degit, graph_plot,  usecolor, usemarker,Save_Num):
    if(graph_plot == True):
        #print(pH)
        fig=plt.figure()
        Re__pH = list(0 for i in range(len(pH)))
        #print(pH)
        for i in range(len(pH)):
            Re__pH[i] = pH[i] / np.power(10, pH_degit)
        for i in range(len(pH)):
            plt.plot(Re__pH[i], V_bias[i] , 
                    label = "pH = {0}".format(Re__pH[i]),
                    color = "{0}".format(usecolor[i]),
                    marker = "{0}".format(usemarker[i]))
            plt.errorbar(Re__pH[i],V_bias[i] , yerr= V_err[i],
                capsize=5, fmt='o', markersize=2, ecolor='black', markeredgecolor = "black", color='w'
                )
            Co_eff = np.polyfit(Re__pH,V_bias,1)
            tmp = np.poly1d(Co_eff)
            V_plot = tmp(Re__pH)
            plt.plot(Re__pH,V_plot)
            plt.legend()
            plt.xlabel("pH []")
            plt.ylabel("Bias Voltage [V]")
            plt.xlim(min(Re__pH) - 0.1,max(Re__pH) + 0.1)
            plt.ylim(min(V_plot)-0.1,max(V_plot)+0.1)
        print("傾き：",Co_eff[0])
        print("切片：",Co_eff[1])    
        #print(Re__pH)
        fig.savefig("{0}Nernst.png".format(Save_Num))


def IV_plot_pH_Ecoli(V_bias, Current, Err, Time,graph_plot ,usecolor, usemarker,Save_Num):
    #print(pH)
    if(graph_plot == True):
        fig = plt.figure()
        Re_pH = list(0 for i in range(len(Time)))
        for i in range(len(Time)):
            plt.plot(V_bias[i]*(-1) , Current[i],
                    label = "Time = {0}h".format(Time[i]),
                    color = "{0}".format(usecolor[i]),
                    marker = "{0}".format(usemarker[i]))
            #plt.errorbar(V_bias[i] *(-1), Current[i], yerr= Err[i],capsize=5, fmt='o', markersize=2, ecolor='black', markeredgecolor = "black", color='w')
        plt.xlim(min(V_bias[i] *(-1)) ,max(V_bias[i] *(-1)) - 0.1)
        plt.legend()
        plt.xlabel("Bias Voltage [V]")
        plt.ylabel("Current [a.u.]")
        fig.savefig("{0}_IV.png".format(Save_Num))
        

def InfV_chg_plot(inf_V_ave,inf_V_err,Time,usecolor,usemarker,Save_Num):
    fig = plt.figure()
    for i in range(len(Time)):
        plt.plot(Time[i],inf_V_ave[i],
            label = "Time = {0}h".format(Time[i]),
            color = "{0}".format(usecolor[i]),
            marker = "{0}".format(usemarker[i]))
        plt.errorbar(Time[i], inf_V_ave[i], yerr= inf_V_err[i],
                    capsize=5, fmt='o', markersize=2, ecolor='black', markeredgecolor = "black", color='w')
        plt.xlim(min(Time)-0.2 ,max(Time)+ 0.2)
        plt.legend()
        plt.xlabel("Time[h]")
        plt.ylabel("Inflection Voltage [V]")
        fig.savefig("{0}_inf_V_chg.png".format(Save_Num))     
        

def pH_chg_plot(pHshift_ave,pHshift_err,Time,usecolor,usemarker,Save_Num):#pHの変化量をプロット
    fig = plt.figure()
    plt.plot(Time,pHshift_ave,color = "black",linestyle = "dashed")
    for i in range(len(Time)):
        plt.plot(Time[i],pHshift_ave[i],
            label = "Time = {0}h".format(Time[i]),
            color = "{0}".format(usecolor[i]),
            marker = "{0}".format(usemarker[i]))
        plt.errorbar(Time[i], pHshift_ave[i], yerr= pHshift_err[i],
                    capsize=5, fmt='o', markersize=2, ecolor='black', markeredgecolor = "black", color='w')
        plt.xlim(min(Time)-0.2 ,max(Time)+ 0.2)
        plt.xticks(Time)
        plt.legend()
        plt.xlabel("Time [h]")
        plt.ylabel("ΔpH[]")
        fig.savefig("{0}_pH_shift.png".format(Save_Num))   



######################################################メイン処理関数#########################################################

###平均値とエラーの計算　(三次元list[pH][FileNum][Step]　->　二次元list[pH][Step])　###
def Ave_errors_meas(Data_list, Data_ave, Data_error, pH, FileNum, Step): 
    dist = list([0 for i in range(Step)]
                for j in range(len(pH)))
    
    for i in range(len(pH)):
        for j in range(FileNum):
            for k in range(Step):
                Data_ave[i][k] += Data_list[i][j][k] / FileNum
        
        for k in range(Step):
            for j in range(FileNum):
                dist[i][k] += np.power(Data_list[i][j][k] - Data_ave[i][k], 2) / Step
            Data_error[i][k] = np.sqrt(dist[i][k]) 
    #print(type(Data_ave))


###データの正規化　三次元list : raw_data[pH][FileNum][Step]　-> 三次元list : norm_data[pH][FileNum][Step]
def Normalize(raw_data, norm_data, pH,FileNum,Step):
    Max_val = list([0 for i in range(FileNum)] for j in range(len(pH)))
    Min_val = list([0 for i in range(FileNum)] for j in range(len(pH)))
    for i in range(len(pH)):
        for j in range(FileNum):
            Max_val[i][j] = max(raw_data[i][j])
            Min_val[i][j] = min(raw_data[i][j])
            for k in range(Step):
                norm_data[i][j][k] = (raw_data[i][j][k] - Min_val[i][j]) / (Max_val[i][j] - Min_val[i][j])


###変曲点計算### 

###それぞれのpHでの変曲点計算
def each_inf_search(Raw_I,Raw_V,Inf_V_ave, Inf_V_err, pH,FileNum,Step):
    Inf_tmp = list([0 for i in range(FileNum)] for j in range(len(pH)))
    Inf_V_raw = list([0 for i in range(FileNum)] for j in range(len(pH)))
    Inf_I_raw = list([0 for i in range(FileNum)] for j in range(len(pH)))
    Inf_I_ave = list(0 for i in range(len(pH)))
    for i in range(len(pH)):
        for j in range(FileNum):
            Inf_tmp[i][j] = inf_p(Raw_I[i][j],Raw_V[i][j],Step)
            
            Inf_V_raw[i][j] = (Raw_V[i][j][Inf_tmp[i][j]] + Raw_V[i][j][Inf_tmp[i][j] - 1]) / 2
            Inf_I_raw[i][j] = (Raw_I[i][j][Inf_tmp[i][j]] + Raw_I[i][j][Inf_tmp[i][j] - 1]) / 2
            Inf_V_ave[i] += Inf_V_raw[i][j] / FileNum
            Inf_I_ave[i] += Inf_I_raw[i][j] / FileNum
        print(Inf_tmp[i])
        Inf_V_err[i] = error_val2(Inf_V_raw[i], Inf_V_ave[i])
        #print("変曲点")
        #print("pH :{0}".format(pH[i]))
        #print("Vbias : {0} \t Current : {1}\n".format(Inf_V_ave[i],Inf_I_ave[i]))
    
    
###基準pHでの変曲点計算
def std_inf_search(Raw_I,Raw_V,Inf_V_ave,std_pH, Inf_V_err, pH,FileNum,Step):
    Delta_I = list([[0 for i in range(Step)] for j in range(FileNum)] for k in range(len(pH)))
    Inf_p = list([0 for i in range(FileNum)] for j in range(len(pH)))
    Inf_V_raw = list([0 for i in range(FileNum)] for j in range(len(pH)))
    Inf_I_raw = list([0 for i in range(FileNum)] for j in range(len(pH)))
    Inf_I_ave = list(0 for i in range(len(pH)))
    for i in range(len(pH)):
        if(pH[i] == std_pH):
            for j in range(FileNum):
                Inf_p[i][j] = inf_p(Raw_I[i][j],Raw_V[i][j],Step)
                Inf_V_raw[i][j] = (Raw_V[i][j][Inf_p[i][j]] + Raw_V[i][j][Inf_p[i][j] - 1]) / 2
                Inf_I_raw[i][j] = (Raw_I[i][j][Inf_p[i][j]] + Raw_I[i][j][Inf_p[i][j] - 1]) / 2
                Inf_V_ave[i] += Inf_V_raw[i][j] / FileNum
                Inf_I_ave[i] += Inf_I_raw[i][j] / FileNum
        std_I = Inf_I_ave[std_pH]
        print(std_I)
    
    for i in range(len(pH)):
        for j in range(FileNum):
            for k in range(Step):
                Delta_I[i][j][k] = abs(Raw_I[i][j][k] - std_I)              
            Inf_p[i][j] = min_search2(Delta_I[i][j])
            #print(Inf_p[i][j])
            Inf_V_raw[i][j] = Raw_V[i][j][Inf_p[i][j]]
            Inf_V_ave[i] += Raw_V[i][j][Inf_p[i][j]] / FileNum
        Inf_V_err[i] = error_val2(Inf_V_raw[i], Inf_V_ave[i])
        #print("変曲点")
        #print("pH :{0}".format(pH[i]))
        #print("Vbias : {0} \t Current : {1}\n".format(Inf_V_ave[i],Inf_I_ave[i]))


def inf_meas(list_I_raw,list_V,inf_V_ave,inf_V_err, pH,FileNum,biasVoltage_f,ary_s,ary_f,increment):
    #3Dフィッティングして変曲点を計算
    
    Re_Step = int((ary_s - ary_f) / increment)
    Re_I = list([[0 for i in range(Re_Step)] for j in range(FileNum)] for k in range(len(pH)))
    Re_V = list([[0 for i in range(Re_Step)] for j in range(FileNum)] for k in range(len(pH)))
    inf_V = list([0 for i in range(FileNum)] for j in range(len(pH)))
    s_val = int((biasVoltage_f + ary_f) / increment)
    Co_eff = list([[0 for i in range(4)] for j in range(FileNum)] for k in range(len(pH)))
    
    
    for i in range(len(pH)):
        for j in range(FileNum):
            for k in range(Re_Step):
                Re_I[i][j][k] = list_I_raw[i][j][k + s_val]
                Re_V[i][j][k] = list_V[i][j][k + s_val]
            #print(list_V) 
            Co_eff[i][j] = np.polyfit(Re_V[i][j],Re_I[i][j],3)
            inf_V[i][j] = (-1) * Co_eff[i][j][1] / (3*Co_eff[i][j][0])
            inf_V_ave[i] += inf_V[i][j] / FileNum
        inf_V_err[i] = error_val2(inf_V[i],inf_V_ave[i])
    print(Re_V[0][0])
    print(inf_V)

def pH_shift_meas(list_I_raw,list_V,pHshift_ave,pHshift_err, Time,Nernst_slope,FileNum,biasVoltage_f,ary_s,ary_f,increment):
    #3Dフィッティングして変曲点を計算してpH変化量を計算
    
    Re_Step = int((ary_s - ary_f) / increment)
    Re_I = list([[0 for i in range(Re_Step)] for j in range(FileNum)] for k in range(len(Time)))
    Re_V = list([[0 for i in range(Re_Step)] for j in range(FileNum)] for k in range(len(Time)))
    inf_V = list([0 for i in range(FileNum)] for j in range(len(Time)))
    inf_V_ave = list(0 for i in range(len(Time)))
    pH_shift = list([0 for i in range(FileNum)] for j in range(len(Time)))
    s_val = int((biasVoltage_f + ary_f) / increment)
    Co_eff = list([[0 for i in range(4)] for j in range(FileNum)] for k in range(len(Time)))
    
    
    for i in range(len(Time)):
        for j in range(FileNum):
            for k in range(Re_Step):
                Re_I[i][j][k] = list_I_raw[i][j][k + s_val]
                Re_V[i][j][k] = list_V[i][j][k + s_val]
            #print(list_V)    
            Co_eff[i][j] = np.polyfit(Re_V[i][j],Re_I[i][j],3)
            inf_V[i][j] = (-1) * Co_eff[i][j][1] / (3*Co_eff[i][j][0])
            inf_V_ave[i] += inf_V[i][j] / FileNum
    for j in range(FileNum):
        for i in range(len(Time)):
            pH_shift[i][j] = (inf_V[i][j] - inf_V_ave[0]) / Nernst_slope
            pHshift_ave[i] += pH_shift[i][j] / FileNum
    for i in range(len(Time)):
        pHshift_err[i] = error_val2(pH_shift[i] , pHshift_ave[i])
    print(pHshift_ave)
    #print(Re_V)
    #print(Nernst_slope)


def inf_meas_ForCV(list_C_raw,list_V,inf_V_ave,inf_V_err, pH,FileNum,Step):#3DフィッティングCV測定用
    #Re_Step = int((ary_s - ary_f) / increment)
    Re_C = list([[0 for i in range(Step)] for j in range(FileNum)] for k in range(len(pH)))
    Re_V = list([[0 for i in range(Step)] for j in range(FileNum)] for k in range(len(pH)))
    inf_V = list([0 for i in range(FileNum)] for j in range(len(pH)))
    Co_eff = list([[0 for i in range(4)] for j in range(FileNum)] for k in range(len(pH)))
    for i in range(len(pH)):
        for j in range(FileNum):
            for k in range(Step):
                Re_C[i][j][k] = list_C_raw[i][j][k]
                Re_V[i][j][k] = list_V[k] 
            Co_eff[i][j] = np.polyfit(Re_V[i][j],Re_C[i][j],3)
            inf_V[i][j] = (-1) * Co_eff[i][j][1] / (3*Co_eff[i][j][0])
            inf_V_ave[i] += inf_V[i][j] / FileNum
        inf_V_err[i] = error_val2(inf_V[i],inf_V_ave[i])


###データ読み込みに失敗したとき用###
def pro_read_csv(path, encoding='utf-8', usecols=None):
    """
    pd.read_csv()で読めないcsvファイルを読み込む。

    Args:
        path: str
            読み込むファイルのパス。

        encoding: str, optional(default='utf-8)
            エンコード。

        usecols: list of str, optional(default=None)
            指定したカラムのみを読み込む場合に使用。

    Returns:
        df: DataFrame
            読み込んだDataFrame。
    """
    if usecols is None:
        print('usecols: all columns')
        with codecs.open(path, 'r', encoding, 'ignore') as file:
            df = pd.read_table(file, delimiter=',')
    else:
        # 指定したカラムのみ読み込む場合
        print('usecols:', usecols)
        with codecs.open(path, 'r', encoding, 'ignore') as file:
            df = pd.read_table(file, delimiter=',', usecols=usecols)

    return df