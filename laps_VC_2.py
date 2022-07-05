import numpy as np
import matplotlib.pyplot as plt
import csv
import my_function as myfunc
import os

#Parameter of cv_graph
# 諸パラメータ
folder 	= "220528_ad50um_611_cv"						### フォルダ名
subst 	= "ad50um"				               		### 基板名
FileNum = [1,2,3]
pH 	= [4,7,9]					                       	### pH
RepH = list(0 for i in range(len(pH)))
digit = 1
for i in range(len(pH)):
    RepH[i] = pH[i] / digit
N = 3

#LabVIEW Condition
#plus 
Vp_s = -0.2
Vp_f = 2.6
increment_p = 0.1
Vp = int((Vp_f - Vp_s) / increment_p)							  		### バイアス電圧のデータ点数
#minus
Vm_s = -2.7
Vm_f = 0.0
increment_m = 0.1
Vm = int((Vm_f - Vm_s) / increment_m)							  		### バイアス電圧のデータ点数

drift_Step = 0.2
drift = int(drift_Step / increment_m)

StepTime = Vp + Vm - drift*2

ary_s=-1.5
ary_f=1.0

#frq
frq_s = 1000
frq_f = 10000
frq_step = 1000
frq_N = int((frq_f - frq_s) / frq_step + 1)
frq = list(0 for i in range(frq_N))
for F in range(frq_N):
    frq[F] = frq_s + frq_step * F
#print(frq)


#plot graph
graph_plot = False

Ci_plot = True
Cd_plot = False
Z_plot = False

pH_change = True
Frq_change = True
Nernst_change = True



# 生データ参照先
dir_ref = r"C:\Users\kingg\Desktop\研究関連\Experiment\Measurementdata\C-V\{}".format(folder)
dir_Ref = dir_ref.strip("")
# csv/グラフファイル保存先
dir_save = r"C:\Users\kingg\Desktop\研究関連\Experiment\Measurementdata\C-V\{}".format(folder)
# _mと_pをマージしたcsvファイル名
name_csv="{0}.csv".format(subst)
# 保存するC-Vグラフ名
name_graph="CV_{0}_{1}".format(subst,pH)


#graph format settings
plt.rcParams['font.size'] = 12
plt.rcParams['font.family']= 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Serif CJK JP']
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.width'] = 1.2
plt.rcParams['ytick.major.width'] = 1.2
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['axes.grid']=True
plt.rcParams['grid.linestyle'] = ' '
plt.rcParams['grid.linewidth'] = 0.6
#plt.gca().ticklabel_format(style="sci", scilimits=(0,0), axis="y",useMathText=True)

#usage guide settings
plt.rcParams["legend.markerscale"] = 2
plt.rcParams["legend.fancybox"] = False
plt.rcParams["legend.framealpha"] = 1
plt.rcParams["legend.edgecolor"] = 'black'

#Define the parameter in main function​
markers = ["o", "v","*","D","s", "^", "<", ">", "1", "2", "3","d","x","h","H"]
colors = ["g","b","r","y","m","c","k","tab:blue","tab:orange","tab:purple","tab:brown","tab:gray","lime"]


#comfirm the directri of graph
import os 
os.chdir(dir_ref)

#print(os.getcwd())
#determination of array
#freq_m = np.zeros((Vm,N))
#freq_p = np.zeros((Vp,N))

cs_m = np.zeros((abs(Vm),N))
cs_p = np.zeros((Vp,N))
cs_raw = list([[[0 for i in range(StepTime)] for j in range(N)] for k in range(len(pH))] for l in range(frq_N))
cs_ave = list([[0 for i in range(StepTime)] for k in range(len(pH))] for l in range(frq_N))
cs_err = list([[0 for i in range(StepTime)] for k in range(len(pH))] for l in range(frq_N))
ci_raw = list([[[0 for i in range(StepTime)] for j in range(N)] for k in range(len(pH))] for l in range(frq_N))
ci_ave = list([[0 for i in range(StepTime)] for k in range(len(pH))] for l in range(frq_N))
ci_err = list([[0 for i in range(StepTime)] for k in range(len(pH))] for l in range(frq_N))
Z_raw = list([[[0 for i in range(StepTime)] for j in range(N)] for k in range(len(pH))] for l in range(frq_N))
Z_ave = list([[0 for i in range(StepTime)] for k in range(len(pH))] for l in range(frq_N))
Z_err = list([[0 for i in range(StepTime)] for k in range(len(pH))] for l in range(frq_N))
inf_V_ave = list([0 for i in range(len(pH))] for k in range(frq_N))
inf_V_err = list([0 for i in range(len(pH))] for k in range(frq_N))
bias_V = list(0 for i in range(StepTime))
res = list(0 for i in range(frq_N))
applxline = list(0 for i in range(frq_N))

#File import
for i in range(len(pH)):
    for j in range(N):
        with open("{0:02}_pH{1}_m_{2}".format(FileNum[i],pH[i],j+1)) as f_m:
            lst=list(csv.reader(f_m))
            #print(lst)
            for k in range(1+drift,Vm+1,1):
                bias_V[k-1-drift] = float(lst[k][0])
                for F in range(0,frq_N,1):
                    cs_raw[F][i][j][k-1-drift] = float(lst[F*(abs(Vm)+1)+ k][2])
                    ci_raw[F][i][j][k-1-drift] = float(lst[F*(abs(Vm)+1)+ k][1])
                    Z_raw[F][i][j][k-1-drift] = float(lst[F*(abs(Vm)+1)+ k][3])
                    
        with open("{0:02}_pH{1}_p_{2}".format(FileNum[i],pH[i],j+1)) as f_p:
            lst=list(csv.reader(f_p))
            for k in range(Vm+1+drift,StepTime+1+drift*2,1):
                bias_V[k-1-drift*2] = float(lst[k-Vm][0])
                for F in range(0,frq_N,1):
                    #cs_p[F] = lst[(F-1)*(abs(Vm+1))+ (k-Vm)][2]
                    cs_raw[F][i][j][k-1-drift*2] = float(lst[F*(Vp+1)+ (k-Vm)][2])
                    ci_raw[F][i][j][k-1-drift*2] = float(lst[F*(Vp+1)+ (k-Vm)][1])
                    Z_raw[F][i][j][k-1-drift*2] = float(lst[F*(Vp+1)+ (k-Vm)][3])


for F in range(frq_N):
    myfunc.Ave_errors_meas(cs_raw[F], cs_ave[F], cs_err[F], pH, N, StepTime)
    if(Cd_plot == True):
        myfunc.inf_meas_ForCV(cs_raw[F],bias_V,inf_V_ave[F],inf_V_err[F], pH,N,StepTime)
        myfunc.Ave_errors_meas(cs_raw[F], cs_ave[F], cs_err[F], pH, N, StepTime)
    elif(Ci_plot == True):
        myfunc.inf_meas_ForCV(ci_raw[F],bias_V,inf_V_ave[F],inf_V_err[F], pH,N,StepTime)
        myfunc.Ave_errors_meas(ci_raw[F], ci_ave[F], ci_err[F], pH, N, StepTime)
    elif(Z_plot == True):
        myfunc.inf_meas_ForCV(Z_raw[F],bias_V,inf_V_ave[F],inf_V_err[F], pH,N,StepTime)
        myfunc.Ave_errors_meas(Z_raw[F], Z_ave[F], Z_err[F], pH, N, StepTime)

#print(inf_V_ave)

#Data plot
if(graph_plot==True):
    
    if(pH_change == True):
        if(Cd_plot == True):
            for F in range(frq_N):
                fig = plt.figure()
                for i in range(len(pH)):
                    plt.plot(bias_V,cs_ave[F][i],label = "pH = {0}".format(RepH[i]),color = "{0}".format(colors[i]),marker = "{0}".format(markers[i]))
                    plt.errorbar(bias_V,cs_ave[F][i],yerr=cs_err[F][i],capsize=5, fmt='o', markersize=2, ecolor='black', markeredgecolor = "black", color='w')
                plt.legend()
                plt.title("Frq = {}".format(frq[F]))
                plt.xlim(-2.0,2.0)
                plt.ylim(min(cs_ave[F][0])*0.7,max(cs_ave[F][0])*1.3)
                #fig.savefig(subst+"_"+)
        if(Ci_plot == True):
            for F in range(frq_N):
                fig = plt.figure()
                for i in range(len(pH)):
                    plt.plot(bias_V,ci_ave[F][i],label = "pH = {0}".format(RepH[i]),color = "{0}".format(colors[i]),marker = "{0}".format(markers[i]))
                    plt.errorbar(bias_V,ci_ave[F][i],yerr=ci_err[F][i],capsize=5, fmt='o', markersize=2, ecolor='black', markeredgecolor = "black", color='w')
                plt.legend()
                plt.title("Frq = {}".format(frq[F]))
                plt.xlim(-2.0,2.0)
                plt.ylim(min(ci_ave[F][0]),max(ci_ave[F][0]))
                #fig.savefig(subst+"_"+)
        if(Z_plot == True):
            for F in range(frq_N):
                fig = plt.figure()
                for i in range(len(pH)):
                    plt.plot(bias_V,Z_ave[F][i],label = "pH = {0}".format(RepH[i]),color = "{0}".format(colors[i]),marker = "{0}".format(markers[i]))
                    plt.errorbar(bias_V,Z_ave[F][i],yerr=Z_err[F][i],capsize=5, fmt='o', markersize=2, ecolor='black', markeredgecolor = "black", color='w')
                plt.legend()
                plt.title("Frq = {}".format(frq[F]))
                plt.xlim(-2.0,2.0)
                #plt.ylim(min(Z_ave[F][0])*0.7,max(Z_ave[F][0])*1.3)
                #fig.savefig(subst+"_"+)


    if(Frq_change == True):
        if(Cd_plot == True):
            for i in range(len(pH)):
                fig = plt.figure()
                for F in range(frq_N):
                    plt.plot(bias_V,cs_ave[F][i],label = "frq = {0}".format(frq[F]),color = "{0}".format(colors[F]),marker = "{0}".format(markers[i]))
                    plt.errorbar(bias_V,cs_ave[F][i],yerr=cs_err[F][i],capsize=5, fmt='o', markersize=2, ecolor='black', markeredgecolor = "black", color='w')
                plt.legend()
                plt.title("pH={}".format(RepH[i]))
                plt.xlim(Vm_s,Vp_f)
                plt.ylim(min(cs_ave[0][0])*0.7,max(cs_ave[0][0])*1.3)
                #fig.savefig(subst+"_"+freq_m".jpg")            
        if(Ci_plot == True):
            for i in range(len(pH)):
                fig = plt.figure()
                for F in range(frq_N):
                    plt.plot(bias_V,ci_ave[F][i],label = "frq = {0}".format(frq[F]),color = "{0}".format(colors[F]),marker = "{0}".format(markers[i]))
                    plt.errorbar(bias_V,ci_ave[F][i],yerr=ci_err[F][i],capsize=5, fmt='o', markersize=2, ecolor='black', markeredgecolor = "black", color='w')
                plt.legend()
                plt.title("pH={}".format(RepH[i]))
                plt.xlim(Vm_s,Vp_f)
                #plt.ylim(min(ci_ave[0][0])*0.7,max(ci_ave[0][0])*1.3)
                #fig.savefig(subst+"_"+freq_m".jpg")   
        if(Z_plot == True):
            for i in range(len(pH)):
                fig = plt.figure()
                for F in range(frq_N):
                    plt.plot(bias_V,Z_ave[F][i],label = "frq = {0}".format(frq[F]),color = "{0}".format(colors[F]),marker = "{0}".format(markers[i]))
                    plt.errorbar(bias_V,Z_ave[F][i],yerr=cs_err[F][i],capsize=5, fmt='o', markersize=2, ecolor='black', markeredgecolor = "black", color='w')
                plt.legend()
                plt.title("pH={}".format(RepH[i]))
                plt.xlim(Vm_s,Vp_f)
                #plt.ylim(min(Z_ave[0][0])*0.7,max(Z_ave[0][0])*1.3)
                #fig.savefig(subst+"_"+freq_m".jpg")   

    if(Nernst_change == True):
        for F in range(frq_N):
            fig = plt.figure()
            res[F] = np.polyfit(RepH,inf_V_ave[F],1)
            applxline[F] = np.poly1d(res[F])(RepH)
            for i in range(len(pH)):
                plt.plot(RepH[i],inf_V_ave[F][i],color = "{0}".format(colors[F]),marker = "{0}".format(markers[i]))
                plt.errorbar(RepH[i],inf_V_ave[F][i],yerr=inf_V_err[F][i],capsize=5, fmt='o', markersize=2, ecolor='black', markeredgecolor = "black", color='w')
                plt.plot(RepH,applxline[F],linestyle = "dashed")
            plt.title("frq={}".format(frq[F]))
            plt.xlim(min(RepH)-0.5,max(RepH)+0.5)
            plt.text(6,min(inf_V_ave[F]),"y={0:.3f}x + {1:.3f}".format(res[F][0],res[F][1]),fontsize = 15)
            
            #fig.savefig(subst+"_"+freq_m".jpg")       
    plt.show()
#npArray = np.loadtxt(name_csv,delimiter = ",")

"""
# 軸ラベルの設定
xtitle2 = "bias voltage [V]"
ytitle2 = "capasitance [F]"

# x,y値の設定
x = npArray[:,0]
y = np.zeros((1,N))
for N in range(1,N+1,1):
    y[N] = npArray[:,N]
    plt.plot(x, y[N])


plt.title(name_graph)
plt.xlabel(xtitle2)
plt.ylabel(ytitle2)
##plt.savefig(subst+"_"+freq1+"_"+ph+".jpg")
plt.show()
"""






### 以下エラー表示は生成するcsvマージﾌｧｲﾙが現在開いてしまっているために起きるエラー ###
#Traceback (most recent call last):
#  File "C:\Users\chono\Desktop\python_cmd\CV\00_cv_multi.py", line 57, in <module>
#    with open(name_csv,'a',newline='')as f1:
#PermissionError: [Errno 13] Permission denied: 'silson1.csv'
