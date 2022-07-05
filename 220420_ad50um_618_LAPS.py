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
folder = "220420_ad50um_618_LAPS"

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
FileNum = [1,3,2,4,5,6,7,8]                      ###EAPS測定番号
#FileNum = [1,5,8]
frq = 400                                ###測定周波数(kHz)
pH = [692,649,612,576,546,461,419,400]                           ###測定pH
#pH = [692,546,400]
Meas_N = 3                               ###測定回数

#####################################EAPS設定####################################################################################

biasVoltage_S = 0.0                    ###バイアス電圧スタート                    
biasVoltage_F = 2.6                    ###バイアス電圧ラスト
increment = 0.01                        ###刻み値
StepTime = int( (biasVoltage_F - biasVoltage_S) / increment ) 

#####################################出力データ設定###############################################################################
RawData_graph = True
NormData_graph = True
Nernst_Diagram = True
pH_estimate = False

#####################################Nernst線図パラメータ####################################################################

##Select Measurement Mode##
Measurement_mode =1
#0...Use raw data
#1...Use normalized data

Inflection_mode =1
#0... Use one inflection
#1...Measure each inflection

if(Inflection_mode == 0):
    standard_pH = 642

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
###出力バイアス電圧###
plot_V = list(0 for i in range(StepTime))         

###1つのpH,1つの周波数に対する測定データ取り込み
biasVoltage_S *= (-1)
biasVoltage_F *= (-1)
#Meas_time = list(range(0,Meas_N,1))###ファイル末尾(測定回数)

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
    
    #Nernst計算
    if(Inflection_mode == 1):       #use each inflection
        if(Measurement_mode == 0):  #use raw data
            func.each_inf_search(Raw_I,Raw_V,Inf_V_ave, Inf_V_err, pH,Meas_N,StepTime)
        else:                       #use normalized data
            func.each_inf_search(Norm_I,Raw_V,Inf_V_ave, Inf_V_err, pH,Meas_N,StepTime)
    else:                           
        if(Measurement_mode == 0):
            func.std_inf_search(Raw_I,Raw_V,Inf_V_ave,standard_pH,  Inf_V_err, pH,Meas_N,StepTime)
        else:
            func.std_inf_search(Norm_I,Raw_V,Inf_V_ave,standard_pH,  Inf_V_err, pH,Meas_N,StepTime)

    
    #グラフプロット
    func.IV_plot_pH(plot_V, Raw_I_ave, Raw_I_err,
                    pH, pH_degit ,
                    RawData_graph ,colors, markers,0)
    
    func.IV_plot_pH(plot_V, Norm_I_ave, Norm_I_err,
                    pH, pH_degit ,
                    NormData_graph ,colors, markers,1)
    
    func.Nernst_plot(Inf_V_ave, Inf_V_err, pH,
                    pH_degit,
                    Nernst_Diagram,  colors, markers,2)

plt.show()






"""
for i in range(len(pH)):###pHごとに拡張   
    for j in range(0,Meas_N,1):                         ###前列ファイル取り込み
        with open("{0:02}_{1}kHz_pH{2}_ {3}.txt".format(FileNum[i],frq,pH[i],j)) as data:
            sample_num = 0
            line = data.readlines()
            for k in range(0,StepTime,1):               ###小分けして配列に格納
                import_data[k] = line[k].rstrip('\n').split('\t')
                import_V[i][j][k] = float(import_data[k][0])
                import_I[i][j][k] = float(import_data[k][1])
                bias_V_ave[i][k] += float((-1) * import_V[i][j][k]) / len(Meas_time)
                photo_C_ave[i][k] += float(import_I[i][j][k]) / len(Meas_time)

                photo_C_tmp_raw[i][k][j] = import_I[i][j][k]
                sample_num += 1                
                if(import_I[i][j][k] > photo_C_max[i]):
                    photo_C_max[i] = import_I[i][j][k]
                if(import_I[i][j][k] < photo_C_min[i]):
                    photo_C_min[i] = import_I[i][j][k]
                
                data.close()               

    for j in range(0,Meas_N,1):         ######Normalize#########
        for k in range(0,StepTime,1):
            photo_C_sd[i][j][k] = (import_I[i][j][k] - photo_C_min[i]) / (photo_C_max[i] - photo_C_min[i])
            photo_C_tmp_sd[i][k][j] = photo_C_sd[i][j][k]
            photo_C_sd_ave[i][k] += photo_C_sd[i][j][k] / len(Meas_time)
    
    for j in range(0,StepTime,1):    ######Error Bar##########
        for k in range(0,Meas_N,1):
            tmp_raw[i][j] += np.power(photo_C_tmp_raw[i][j][k] - photo_C_ave[i][j] , 2)
            tmp_sd[i][j] += np.power(photo_C_tmp_sd[i][j][k] - photo_C_sd_ave[i][j] , 2)   
        Error_C_raw[i][j] = np.sqrt(tmp_raw[i][j] / Meas_N)
        Error_C_sd[i][j] = np.sqrt(tmp_sd[i][j] / Meas_N)
    Error_C_max_tmp[i] = max(Error_C_raw[i])             







RepH = list([0 for i in range(len(pH))])
for i in range(0,len(pH),1):
    RepH[i] = pH[i] 
    if(RepH[i] - standard_pH == 0):
        N = i

if(Nernst_Diagram == True):
    for j in range(0,Meas_N,1):
        for k in range(0,StepTime,1):
            if(k > 0):
                Delta_I[N][j][k] = import_I[N][j][k] - import_I[N][j][k-1]
                if(max_Delta_I[N][j] < Delta_I[N][j][k]):
                    max_Delta_I[N][j] = Delta_I[N][j][k]
                    Nernst_V_tmp[N][j] = import_V[N][j][k]
                    tmp = k
        #print(tmp)
        Nernst_V[N] += ((Nernst_V_tmp[N][j] + import_V[N][j][tmp - 1]))/ 6
        Nernst_I[N] += ((import_I[N][j][tmp] / 3) + (import_I[N][j][tmp - 1] / 3)) / 2
    Base_Current = Nernst_I[N]
    #print(Nernst_I[N])
    for i in range(0,len(pH),1):
        if(i != N):
            #print(i)
            for j in range(Meas_N):
                for k in range(StepTime):
                    Delta_I_Nernst_tmp[k] = import_I[i][j][k] - Nernst_I[N]
                    if(k > 0):
                        if(Delta_I_Nernst_tmp[k] * Delta_I_Nernst_tmp[k-1] < 0):
                            Nernst_V_tmp[i][j] = (Nernst_I[N] - import_I[i][j][k-1])*(import_V[i][j][k] - import_V[i][j][k-1]) / (import_I[i][j][k] - import_I[i][j][k-1]) + import_V[i][j][k-1]
                
                Nernst_V[i] += float(Nernst_V_tmp[i][j]) / 3
        #print(Nernst_V_tmp[i])
        for j in range(0,Meas_N,1):
            tmp_Nernst_V[i][j] += np.power((Nernst_V_tmp[i][j] * (-1)) - Nernst_V[i],2) 
        Nernst_V_error[i] = np.sqrt(tmp_Nernst_V[i][j] / Meas_N)
        Nernst_V[i] *= (-1)
        
#print(Nernst_V)
#print(Base_Current)
if(pH_estimate == True):
    for i in range(0,len(pH),1):
        
        for j in range(Meas_N):
            for k in range(StepTime):
                Delta_I_Nernst_tmp[k] = import_I[i][j][k] - Base_Current
                if(k > 0):
                    if(Delta_I_Nernst_tmp[k] * Delta_I_Nernst_tmp[k-1] < 0):
                        Nernst_V_tmp[i][j] = (Base_Current - import_I[i][j][k-1])*(import_V[i][j][k] - import_V[i][j][k-1]) / (import_I[i][j][k] - import_I[i][j][k-1]) + import_V[i][j][k-1]
                
            Nernst_V[i] += float(Nernst_V_tmp[i][j]) / (-3)
        
        RepH[i] =  (Nernst_V[i] - Co_intercept) / Co_slope 
        #print(Nernst_V_tmp[i])
        for j in range(0,Meas_N,1):
            tmp_Nernst_V[i][j] += np.power((Nernst_V_tmp[i][j] * (-1)) - Nernst_V[i],2) 
        Nernst_V_error[i] = np.sqrt(tmp_Nernst_V[i][j] / Meas_N)
        #Nernst_V[i] *= (-1)
#print(Nernst_V)
#print(Nernst_V_error)                    
#print(RepH) 




###個別でグラフ作成し保存する###
save_fig_raw = plt.figure()
if(pH_estimate == False):
    for i in range(0,len(pH),1):
        #RepH[i] = pH[i] 
        plt.plot(bias_V_ave[i],photo_C_ave[i], label = "pH{0:.2f}".format(RepH[i]) ,color = "{0}".format(colors[i]),marker = "{0}".format(markers[i]),markersize = '8',lw = 2)
        plt.errorbar(bias_V_ave[i], photo_C_ave[i], yerr = Error_C_raw[i],capsize = 5, markersize = 6, ecolor = 'black',linestyle = "None")
else:
    for i in range(0,len(pH),1):
        plt.plot(bias_V_ave[i],photo_C_ave[i], label = "{0}h".format(i) ,color = "{0}".format(colors[i]),marker = "{0}".format(markers[i]),markersize = '8',lw = 2)
        plt.errorbar(bias_V_ave[i], photo_C_ave[i], yerr = Error_C_raw[i],capsize = 5, markersize = 6, ecolor = 'black',linestyle = "None")
#plt.title("Raw I-V characteristics")
plt.grid(True)
plt.xlabel("Bias Voltage [V]",fontsize = 30)
plt.ylabel("Current [nA]",fontsize = 30)
plt.xlim(biasVoltage_F - 0.05,biasVoltage_S + 0.05)
photo_C_max = max(photo_C_ave) 
photo_C_max += max(Error_C_max_tmp)
plt.ylim(0,max(photo_C_max))
plt.xticks([-2.0,-1.5,-1.0,-0.5,0.0])
plt.tick_params(labelsize = 20)
plt.tight_layout()
plt.legend()
plt.savefig('{0:02}_IVcurve_{1}kHz_raw_graph.png'.format(SaveNum,frq),dpi = 300,orientation = 'portrait' , transparent = False , pad_inches = 0.0)



fig_Norm = plt.figure(figsize = (5,5))
if(pH_estimate == False):
    for i in range(0,len(pH),1):
        plt.plot(bias_V_ave[i],photo_C_sd_ave[i], label = "pH{0:.2f}".format(RepH[i]) ,color = "{0}".format(colors[i]),marker = "{0}".format(markers[i]),markersize = '8',lw = 2)
        plt.errorbar(bias_V_ave[i], photo_C_sd_ave[i], yerr = Error_C_sd[i],capsize = 5,ecolor = 'black',linestyle = "None")
else:
        for i in range(0,len(pH),1):
            plt.plot(bias_V_ave[i],photo_C_sd_ave[i], label = "{0}h".format(i) ,color = "{0}".format(colors[i]),marker = "{0}".format(markers[i]),markersize = '8',lw = 2)
            plt.errorbar(bias_V_ave[i], photo_C_sd_ave[i], yerr = Error_C_sd[i],capsize = 5,ecolor = 'black',linestyle = "None")

#plt.title("Normalized I-V characteristics")
plt.grid(True)
plt.xlabel("Bias Voltage [V]",fontsize = 30)
plt.ylabel("Current [a.u.]",fontsize = 30)
plt.xlim(biasVoltage_F - 0.05,biasVoltage_S + 0.05)
plt.ylim(0,1.2)
plt.yticks([0,0.2,0.4,0.6,0.8,1.0])
plt.xticks([-2.0,-1.5,-1.0,-0.5,0.0])
plt.tick_params(labelsize = 20,width = 3, length = 10)
plt.tight_layout()
plt.legend()
plt.savefig('{0:02}_IVcurve{1}kHz_normalized_graph.png'.format(SaveNum,frq),dpi = 300,orientation = 'portrait' , transparent = False , pad_inches = 0.0)
#plt.show()

if(Nernst_Diagram == True):
    fig_Nernst = plt.figure(figsize = (5,5))
    a = np.polyfit(RepH,Nernst_V,1)
    #print(a)
    Approx = np.poly1d(a)(RepH)
    for i in range(0,len(pH),1):    
        plt.plot( RepH[i],Nernst_V[i],label = "pH{0:.2f}".format(RepH[i]), color = "{0}".format(colors[i]),marker = "{0}".format(markers[i]),markersize = '8',lw = 2)
        #plt.errorbar( RepH[i],Nernst_V[i], yerr = Nernst_V_error[i],capsize = 5,ecolor = 'black',linestyle = "None")
    plt.plot(RepH,Approx,label = "y = {0:.4f}x + {1:.4f}".format(a[0],a[1]))
    plt.grid(True)
    plt.ylabel("Bias Voltage [V]",fontsize = 30)
    plt.xlabel("pH [-]",fontsize = 30)
    plt.ylim(min(Nernst_V) - 0.1 ,max(Nernst_V) + 0.1)
    plt.xlim(0,max(RepH) + 1)
    #plt.yticks([0.00,2.00,4.00,6.00,8.00])
    #plt.xticks([-2.0,-1.5,-1.0,-0.5,0.0])
    plt.tick_params(labelsize = 20,width = 3, length = 10)
    #plt.tight_layout()
    #plt.legend()
    plt.savefig('{0:02}_IVcurve{1}kHz_nernst_graph.png'.format(SaveNum,frq),dpi = 300,orientation = 'portrait' , transparent = False , pad_inches = 0.0)



if(pH_estimate == True):
    fig_Estimate = plt.figure(figsize = (5,5))
    
    plt.plot(time,RepH, label = "LB medium with E.coli" ,marker = "{0}".format(markers[i]),markersize = '8',lw = 2)
    plt.grid(True)
    plt.xlabel("Time [h]",fontsize = 30)
    plt.ylabel("Estimated pH [-]",fontsize = 30)
    plt.ylim(min(RepH)-0.1,max(RepH)+0.1)
    plt.xlim(min(time)-0.5,max(time) + 0.5)
    #plt.yticks([0.00,2.00,4.00,6.00,8.00])
    #plt.xticks([-2.0,-1.5,-1.0,-0.5,0.0])
    plt.tick_params(labelsize = 20,width = 3, length = 10)
    #plt.tight_layout()
    #plt.legend()


plt.show()    

for line in range(len(pH)):      #上書き方式でファイル出力
    with open("{0}".format(name_csv),'a', newline = "") as SaveFile:
        writer=csv.writer(SaveFile,delimiter = ",")
        if(line ==  0):
            writer.writerow(np.round(bias_V_ave[line],3))
        writer.writerow(np.round(photo_C_ave[line],3))




for line in range(len(pH)):    #新規書き込み方式でファイル出力
    print(line)
    with open("{0}".format(name_csv),'w', newline = "") as SaveFile:
        writer=csv.writer(SaveFile,delimiter = ",")
        #print(np.round(bias_V_ave,2))
        if(line ==  1):
            writer.writerow(np.round(bias_V_ave[line],3))
        writer.writerow(np.round(photo_C_ave[line],3))

"""
    
### 以下エラー表示は生成するcsvマージﾌｧｲﾙが現在開いてしまっているために起きるエラー ###
#Traceback (most recent call last):
#  File "C:\Users\chono\Desktop\python_cmd\CV\00_cv_multi.py", line 57, in <module>
#    with open(name_csv,'a',newline='')as f1:
#PermissionError: [Errno 13] Permission denied: 'silson1.csv'