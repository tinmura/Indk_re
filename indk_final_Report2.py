import numpy             as np
import matplotlib.pyplot as plt

from numpy.fft import fft, fftfreq, ifft


frq = 400       # サンプリングレート frq[Hz] (任意)
fin = 1         # 収録終了時刻 [s] (任意)
N   = frq * fin # サンプル数 [個]



def lowpassfilter(y, threshold): 
    xsfft = fftfreq(len(y), d=1/frq)
    tmp = fft(y)
    tmp[xsfft > threshold] = 0
    return ifft(tmp)


def highpassfilter(y, threshold): 
    xsfft = fftfreq(len(y), d=1/frq)
    tmp = fft(y)
    tmp[xsfft < threshold] = 0
    return ifft(tmp)


def amp(y):
    return 2 * abs(fft(y)) / len(y) 


def main(): 
    xs = np.linspace(0, fin, fin * frq)
    y  = np.sin(2 * np.pi * frq * xs)
    noise = np.random.randn(len(y))

    ynoise = y + noise 
    yave = np.convolve(ynoise, np.ones(5) / 5, mode='same')

    xsfft = fftfreq(len(ynoise), d=1/frq)
    crr   = amp(y)
    err   = amp(ynoise)
    ave   = amp(yave)

    plt.plot(y)  
    plt.plot(ynoise)  
    plt.plot(lowpassfilter(ynoise, 5))


    fig,ax = plt.subplots(3, 3, tight_layout = True)
    plt.subplots_adjust(wspace=0.5, hspace=0.5)


    ax[0,0].plot(xs, y)
    ax[0,1].plot(xs, ynoise)
    ax[0,2].plot(xs, yave)
    ax[1,1].plot(xs, yave - y)
    ax[1,2].plot(xs, ynoise - y)

    ax[2,0].plot(xsfft[1 : N//2], crr[1 : N//2])
    ax[2,1].plot(xsfft[1 : N//2], err[1 : N//2])
    ax[2,2].plot(xsfft[1 : N//2], ave[1 : N//2])

    plt.show()


main() 
