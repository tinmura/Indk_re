import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os
import my_function as func
#comfirm the directri of graph
#prog_dir = r"C:\Users\satos\Documents\Python Scripts"
#os.chdir(prog_dir) ###ディレクトリを（）内に変更


SaveNum = 0                 ###グラフ保存番号
#####################################Parameter of iv_graph#####################################################################

###フォルダー名・パス設定###
folder = "220608_ad50um_PLLbefore"

# 生データ参照先
dir_ref = r"C:\Users\kingg\Desktop\研究関連\Experiment\Measurementdata\LAPS\{}".format(folder)
dir_Ref = dir_ref.strip("")  ###フォルダの場所取得
#csvデータ保存先
dir_save =r"C:\Users\kingg\Desktop\研究関連\Experiment\Measurementdata\LAPS\{}".format(folder)

#comfirm the directri of graph
os.chdir(dir_ref) ###ディレクトリを（）内に変更
#print(os.getcwd())



####################################測定ファイル名 : (FileNum)_(frq)_(pH)_(Meas_N)   ###########################################

Subs_type = 0                            ###半導体層：N型...0, P型...1
pH_degit = 2                             ###pHの有効数字 (cf pH = 7...0, pH = 7.0...1, pH = 7.00...2)
#FileNum = [1,2,4,5]                      ###EAPS測定番号
FileNum = [2,4,3,5,6,7]
frq = 500                                ###測定周波数(kHz)
#pH = [700,554,494,486]                           ###測定pH
pH = [700,554,536,494,486,400]
Meas_N = 3                               ###測定回数

#####################################EAPS設定####################################################################################

biasVoltage_S = 0.5                    ###バイアス電圧スタート                    
biasVoltage_F = 3.0                    ###バイアス電圧ラスト
increment = 0.02                        ###刻み値
StepTime = int( (biasVoltage_F - biasVoltage_S) / increment ) 
print(StepTime)
#####################################出力データ設定###############################################################################
RawData_graph = True
NormData_graph = True
Nernst_Diagram = True
pH_estimate = False

#####################################Nernst線図パラメータ####################################################################

##Select Measurement Mode##image.png
Measurement_mode =1
#0...Use raw data
#1...Use normalized data

Inflection_mode =2
#0... Use one inflection
#1...Measure each inflection
#2...Use 3D fitting

if(Inflection_mode == 0):
    standard_pH = 642
ary_s = -1.48
ary_f = -2.7
Re_Step = int((ary_s - ary_f) / increment)
s_val = int((biasVoltage_F + ary_f) / increment)
###################################pH変化量推定####################################################################

time = [0,1,2,3]
if(pH_estimate == True):
    #Nernst line  
    Co_slope = 0.0497
    Co_intercept = -1.5079
    #Base Current(Nernst_I[N])
    Base_Current = 508.1893333


##################################グラフ表示設定#####################################################################
#graph format settings
plt.rcParams['font.size'] = 20
plt.rcParams['legend.fontsize'] = 10
#plt.rcParams['font.family']= 'sans-serif'
#plt.rcParams['font.sans-serif'] = ['Noto Serif CJK JP']
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.width'] = 1.2
plt.rcParams['xtick.minor.visible'] = True
plt.rcParams['ytick.major.width'] = 1.2
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['axes.grid']=False
plt.rcParams['grid.linestyle'] = ' '
plt.rcParams['grid.linewidth'] = 0.6
#plt.gca().legendlabel.set_major_formatter(plt.FormatStrFormatter('%.3f'))
#plt.gca().ticklabel_format(style="sci", scilimits=(0,0), axis="y",useMathText=True)

#usage guide settings
plt.rcParams["figure.autolayout"] = True
plt.rcParams["legend.markerscale"] = 1
plt.rcParams["legend.fancybox"] = True
plt.rcParams["legend.framealpha"] = 1
plt.rcParams["legend.edgecolor"] = 'black'
plt.rcParams["legend.loc"] = "best"
plt.rcParams["legend.frameon"]
plt.rcParams["legend.facecolor"] = "white"

#Define the parameter in main function​
markers = ["o", "v","*","D","s", "^", "<", ">", "1", "2", "3","d","x","h","H"]
colors = ["g","b","r","y","m","c","k","tab:blue","tab:orange","tab:purple","tab:brown","tab:gray","lime"]



###読み込みデータ###
import_data = list([0 for i in range(StepTime)]) 
###生データ###
Raw_V = list([[0 for i in range(StepTime)] for j in range(Meas_N)] for k in range(len(pH)))  
Raw_I = list([[0 for i in range(StepTime)] for j in range(Meas_N)] for k in range(len(pH)))  
Raw_I_ave = list([0 for i in range(StepTime)] for j in range(len(pH)))
Raw_I_err = list([0 for i in range(StepTime)] for j in range(len(pH)))
###正規化データ###
Norm_I = list([[0 for i in range(StepTime)] for j in range(Meas_N)] for k in range(len(pH)))
Norm_I_ave = list([0 for i in range(StepTime)] for j in range(len(pH)))
Norm_I_err = list([0 for i in range(StepTime)] for j in range(len(pH)))
###変曲点###
Inf_V_ave = list(0 for i in range(len(pH)))
Inf_V_err = list(0 for i in range(len(pH)))
###変曲点
Re_V = list([[0 for i in range(Re_Step)] for j in range(Meas_N)] for k in range(len(pH)))  
Re_I = list([[0 for i in range(Re_Step)] for j in range(Meas_N)] for k in range(len(pH)))  
###出力バイアス電圧###
plot_V = list(0 for i in range(StepTime))         

## i...pH
## j...FileNumber
## k...biasVoltage 

if __name__== "__main__":
    
    ###ファイルインポート###
    for i in range(len(pH)):   
        for j in range(0,Meas_N,1):      
            import_data = pd.read_csv(
                "{0:02}_pH{2}_{1}Hz_ {3}.txt".format(FileNum[i],frq,pH[i],j),
                sep = '\t',
                header = None)
            Raw_I[i][j] = import_data[1]
            Raw_V[i][j] = import_data[0] * (-1)
            plot_V[i] = import_data[0]
    

    ###データ処理###
    func.Ave_errors_meas(Raw_I, Raw_I_ave, Raw_I_err, pH, Meas_N, StepTime)    #生データの平均値, エラー計算
    func.Normalize(Raw_I, Norm_I, pH, Meas_N, StepTime)                         #生データの正規化
    func.Ave_errors_meas(Norm_I, Norm_I_ave, Norm_I_err, pH, Meas_N, StepTime) #正規化データの平均値, エラー計算
    

    
    #グラフプロット
    if(RawData_graph == True):
        func.IV_plot_pH(plot_V, Raw_I_ave, Raw_I_err,
                        pH, pH_degit ,
                        RawData_graph ,colors, markers, 0)
    if(NormData_graph == True):
        func.IV_plot_pH(plot_V, Norm_I_ave, Norm_I_err,
                        pH, pH_degit ,
                        NormData_graph ,colors, markers,1)

    #Nernst計算
    if(Nernst_Diagram == True):
        if(Inflection_mode == 1):       #use each inflection
            if(Measurement_mode == 0):  #use raw data
                func.each_inf_search(Raw_I, Raw_V, Inf_V_ave, Inf_V_err,
                                    pH, Meas_N, StepTime)
            else:                       #use normalized data
                func.each_inf_search(Norm_I, Raw_V, Inf_V_ave, Inf_V_err,
                                    pH, Meas_N, StepTime)
                
        elif(Inflection_mode == 2):
            if(Measurement_mode == 0):
                for i in pH:
                    for j in range(Meas_N):
                        Re_I[i][j] = func.parser(Raw_I[i][j])
                        Re_V[i][j] = func.parser(Raw_V[i][j])
                func.inf_meas(Raw_I,Raw_V,Inf_V_ave,Inf_V_err,pH,Meas_N,biasVoltage_F,ary_s,ary_f,increment)
            else:
                
                func.inf_meas(Norm_I,Raw_V,Inf_V_ave,Inf_V_err,pH,Meas_N,biasVoltage_F,ary_s,ary_f,increment)
                #inf_meas(list_I_raw,list_V,inf_V_ave,inf_V_err, pH,FileNum,ary_s,ary_f,increment)
                
        else:                           
            if(Measurement_mode == 0):
                func.std_inf_search(Raw_I, Raw_V, Inf_V_ave, standard_pH, Inf_V_err,
                                    pH, Meas_N, StepTime)
            else:
                func.std_inf_search(Norm_I, Raw_V, Inf_V_ave, standard_pH, Inf_V_err,
                                    pH, Meas_N, StepTime)
                
        func.Nernst_plot(Inf_V_ave, Inf_V_err, pH,
                        pH_degit, Nernst_Diagram, colors, markers, 2)
                    
plt.show()

    
### 以下エラー表示は生成するcsvマージﾌｧｲﾙが現在開いてしまっているために起きるエラー ###
#Traceback (most recent call last):
#  File "C:\Users\chono\Desktop\python_cmd\CV\00_cv_multi.py", line 57, in <module>
#    with open(name_csv,'a',newline='')as f1:
#PermissionError: [Errno 13] Permission denied: 'silson1.csv'