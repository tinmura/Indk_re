import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import inutsuka as func

####Condition of signal####
f_s = 1024 # サンプリングレート f_s[Hz] (任意)
t_fin = 1 # 収録終了時刻 [s] (任意)
dt = 1/f_s # サンプリング周期 dt[s]
N = int(f_s * t_fin) # サンプル数 [個]
fs=10

t = np.linspace(0,t_fin,N)
#NoiseSig = func.combFunc(func.waveFunc(t,f_s),func.noiseFunc(N),N)
CorrectSig = func.waveFunc(t,f_s)
NoiseSig = CorrectSig + func.noiseFunc(N)

####Filtering####
Ave_Sig = func.ave_Fil(5,NoiseSig)
print("Kalman_s")
smoothed, filtered = func.filtered_kalman(NoiseSig)
print("Kalman_f")

####Evaluation####
print("fft_s")
Plot_frq =func.fft_frq(N,dt)
Crr_amp =func.fft_amp(CorrectSig)
Err_amp =func.fft_amp(NoiseSig)
Ave_amp =func.fft_amp(Ave_Sig)

#Kf_amp = func.fft_amp(smoothed[:,0])
#plt.figure(figsize=(10,3))
print("fft_f")
fig,ax = plt.subplots(3,4,tight_layout = True)
plt.subplots_adjust(wspace=0.5,hspace=0.5)

ax[2,2].plot(Plot_frq[1:N//2],Ave_amp[1:N//2])
Ave_amp[(Plot_frq > fs)] = 0
LowPass = np.fft.ifft(Ave_amp)
ax[2,3].plot(t,LowPass)

ax[0,0].plot(t,CorrectSig)
ax[0,1].plot(t,NoiseSig)
ax[0,2].plot(t,Ave_Sig)
ax[1,1].plot(t,func.err(Ave_Sig,CorrectSig))
ax[1,2].plot(t,func.err(NoiseSig,CorrectSig))
ax[1,3].plot(t,func.err(smoothed[:,0],CorrectSig))
ax[2,0].plot(Plot_frq[1:N//2],Crr_amp[1:N//2])
ax[2,1].plot(Plot_frq[1:N//2],Err_amp[1:N//2])
#ax[2,2].plot(Plot_frq[1:N//2],Ave_amp[1:N//2])
#ax[0,3].plot(t, smoothed[:, 0])
#ax[2,3].plot(Plot_frq[1:N//2],Kf_amp[1:N//2])
'''
'''
plt.show()