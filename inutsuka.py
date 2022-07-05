import numpy as np
import matplotlib.pyplot as plt
import pandas
import random
from pykalman import KalmanFilter

"""
f_s = 44100 # サンプリングレート f_s[Hz] (任意)
t_fin = 1 # 収録終了時刻 [s] (任意)
dt = 1/f_s # サンプリング周期 dt[s]
N = int(f_s * t_fin) # サンプル数 [個]
"""

#ノイズ含んだ波形生成プログラム
def waveFunc(t, frq): #->return 1D array
    return np.sin(2*np.pi*frq * t)
def noiseFunc(N):
    return np.random.randn(N)


#ディジタルフィルタ関数
def med_fil(med_N,x):
    med_arr = np.zeros(1,int(len(x)-(med_N-1)/2))

def ave_Fil(ave_N,x): #x -> 1D list   #ave_N -> 2m-1
    return np.convolve(x, np.ones(ave_N)/ave_N, mode='same')

def err(raw_sig, correct_sig):
    return np.subtract(raw_sig,correct_sig)

def filtered_kalman(values):
    kf = KalmanFilter(transition_matrices=np.array([[1, 1], [0, 1]]),
                      transition_covariance=0.0001 * np.eye(2)) # np.eyeは単位行列
    smoothed = kf.em(values).smooth(values)[0]
    filtered = kf.em(values).filter(values)[0]
    return smoothed, filtered

###FFT function###
###Caution###
#if N = x power of 2 -> FFT
#else -> DFT
def fft_amp(y):
    N = len(y)
    y_fft = np.fft.fft(y) # 離散フーリエ変換
    return abs(y_fft/(N/2)) # 音の大きさ（振幅の大きさ）

def fft_frq(N,dt):
    return np.fft.fftfreq(N, d=dt) # 周波数を割り当てる（※後述）
