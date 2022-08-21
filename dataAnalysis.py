import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import scipy.fftpack

PATH = "Data\Analogue comp"
data = {}


for entry in os.scandir(PATH):
    if entry.is_dir():
        gamma = {}
        for item in os.scandir(PATH + "\\" + entry.name):
            if item.is_dir():
                wave = {}
                for file in os.scandir(PATH + "\\" + entry.name + "\\" + item.name):
                    if file.name.endswith(".CSV"):
                        
                        df = pd.read_csv(file.path, names= ["Time", file.name[-6:-4]], skiprows=1)
                        wave[file.name[-6:-4]] = df
                if len(wave) != 0:
                    gamma[item.name] = wave
        if len(gamma) != 0:
            data[entry.name] = gamma
print("Initialisation Complete")

#%%

name_switch = {"RECTIFIED INVERTED DIFF G 2":"Rectified Inverted Differentiator, $\\gamma$ = 2",
               "INVERTED DIFF G 2":"Inverted Differentiator, $\\gamma$ = 2",
               "DIFF G 2":"Differentiator, $\\gamma$= 2",
               "DIFF G 10":"Differentiator, $\\gamma$ = 10",
               "G 2":"$\\gamma$ = 2",
               "G 10":"$\\gamma$ = 10"
               }
name_switch2 = {"N":"Sine",
                "S":"Square",
                "P":"Pulse",
                "T":"Triangle"
               }
        

i = 0
for item in data:
    if item != "EXTR":
        for waveform in data[item]:
            try:
                print(i)

                title = "Analogue Computer with " + name_switch[item] + " using a " + name_switch2[waveform[:1]] + " wave at frequency " + waveform[2:] + "Hz"
                
                
                
                C1 = data[item][waveform]["C1"]
    
                C2 = data[item][waveform]["C2"]
                
                print(C2.shape)
                
                
                fig, ax1 = plt.subplots()
                
                color = 'tab:red'
                ax1.title.set_text(title)
                ax1.set_title(title)
                ax1.set_ylabel('C1 (V)', color=color)
                ax1.plot(C1["Time"], C1["C1"], color=color)
                ax1.tick_params(axis='y', labelcolor=color)
                
                ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
                
                color = 'tab:blue'
                ax2.set_ylabel('C2 (V)', color=color)  # we already handled the x-label with ax1
                ax2.plot(C2["Time"], C2["C2"], color=color)
                ax2.tick_params(axis='y', labelcolor=color)
                
                fig.tight_layout()  # otherwise the right y-label is slightly clipped
                #fig.savefig(f"WavePlots/{item} {waveform}.png")
                plt.show()
                
                
                i += 1
            except:
                continue
#%%
name_switch = {"RECTIFIED INVERTED DIFF G 2":"Rectified Inverted Differentiator, $\\gamma$ = 2",
               "INVERTED DIFF G 2":"Inverted Differentiator, $\\gamma$ = 2",
               "DIFF G 2":"Differentiator, $\\gamma$= 2",
               "DIFF G 10":"Differentiator, $\\gamma$ = 10",
               "G 2":"$\\gamma$ = 2",
               "G 10":"$\\gamma$ = 10"
               }
name_switch2 = {"N":"Sine",
                "S":"Square",
                "P":"Pulse",
                "T":"Triangle"
               }

def calc_err(c2):
    #plt.plot(c2["Time"], c2["C2"])
    c2_av = {"Time":[], "C2 Av":[], "C2 err+":[], "C2 err-":[]}
    #plt.show()
    n = 200
    for i in range(int(c2.shape[0]/n)):
        c2_n = c2[i*n:(i+1)*(n)].reset_index()
        time_mid = c2_n["Time"][(int(len(c2_n)/2)-1)]
        v_err_pos = []
        v_err_neg = []
        v_av = []
        m = 100
        for j in range(int(c2_n.shape[0]/m)):
            c2_m = c2_n[j*m:(j+1)*(m)].reset_index()
            #print(c2_m.shape)
            
            mean = np.mean(c2_m["C2"])
            v_av.append(mean)
            v_max =np.max(c2_m["C2"])
            v_min =np.min(c2_m["C2"])
            
            v_err_pos.append(v_max)
            v_err_neg.append(v_min)
                        
        temp_dict = {"Time":time_mid, "C2 Av":np.mean(v_av), "C2 err+": np.mean(v_err_pos), "C2 err-": np.mean(v_err_neg)}
        
        #print(temp_dict)
        for column in c2_av:
            c2_av[column].append(temp_dict[column])
        #print(f"{time_mid},{v_av},  {v_max}, {v_min}")
    
    c2_av = pd.DataFrame(c2_av)
    return (c2_av)
#%%
print("Noise Analysis of P 100 plot with Gamma 10 with Differentiator")
data_range = (20000, 70000)
#plt.plot(data["DIFF G 10"]["P_100"]["C1"][data_range[0]:data_range[1]]["Time"], data["DIFF G 10"]["P_100"]["C1"][data_range[0]:data_range[1]]["C1"])
#calc_err(data["DIFF G 10"]["P_100"]["C2"][data_range[0]:data_range[1]])
calc_err(data["DIFF G 10"]["P_100"]["C2"])

letters = "abcdefghijklmnopqrstuvwxyz"

for item in data:
    if item != "EXTR":
        i = 0
        for waveform in data[item]:
            try:
                title = letters[i]+") Analogue Computer with " + name_switch[item] + " using a " + name_switch2[waveform[:1]] + " wave at frequency " + waveform[2:] + "mHz"
                
     
                
                C1 = data[item][waveform]["C1"]
    
                C2 = calc_err(data[item][waveform]["C2"])
                
                
                
                fig, (ax1, axf) = plt.subplots(ncols = 2, figsize = (10, 5))
                
                color = "#665BC2"
                fig.suptitle(title)
                ax1.set_xlabel("Time (s)")
                ax1.set_title("Input + Output")
                ax1.set_ylabel('C1 (V)', color=color)
                p1 = ax1.plot(C1["Time"], C1["C1"], color=color)
                ax1.tick_params(axis='y', labelcolor=color)
                ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
                
                color = "#F50000"
                ax2.set_ylabel('C2 (V)', color=color)  # we already handled the x-label with ax1
                p2 = ax2.plot(C2["Time"], C2["C2 Av"], color=color )
                p3 = ax2.fill_between(C2["Time"], C2["C2 err-"],C2["C2 err+"],alpha=0.5, edgecolor='#D63230', facecolor='#F39237')
                ax2.tick_params(axis='y', labelcolor=color)
                
                
                axf.set_title("Fourier Analysis")
                
                N = C2["C2 Av"].shape[0]
                
                sp    = np.fft.fft(C2["C2 Av"])/(10*(N**0.5))
                freq = np.fft.fftfreq(len(C2["C2 Av"]), np.abs(C2["Time"][1] - C2["Time"][0]))
                
                            
                axf.set_ylabel('Amplitude')
                axf.set_xlabel('Frequency (Hz)')
                axf.plot(freq, np.abs(sp),"k", color=color)
                #axf.plot(freq, sp.imag)
                axf.tick_params(axis='y')
                axf.set_xlim((0, 10))
                
                fig.tight_layout()  # otherwise the right y-label is slightly clipped
                #PATH =f"WavePlots/Fourier/{item}"
                PATH = "imgs"
                #if not os.path.isdir(PATH):
                #    os.mkdir(PATH)
                fig.savefig(f"{PATH}/{item} {waveform}.png")
                
                plt.show()#
                i += 1
                
            except:
                continue
#%%

plot = calc_err(data["INVERTED DIFF G 2"]["S_2000"]["C2"])
plt.plot(plot["Time"], plot["C2 Av"])
plt.show()
N = plot["C2 Av"].shape[0]
sp    = np.fft.fft(plot["C2 Av"])[5:15]/(10*(N**0.5))
freq = np.fft.fftfreq(len(plot["C2 Av"]), np.abs(plot["Time"][1] - plot["Time"][0]))[5:15]
plt.plot(freq, np.abs(sp), "k")
plt.ylabel('Amplitude')
plt.xlabel('Frequency (Hz)')
#axf.plot(freq, sp.imag)
plt.tick_params(axis='y')
plt.xlim((0, 10))

maximum = 0
frequency = 0
for i in range(int(sp.shape[0]/2)):
    if sp[i] > maximum:
        maximum = sp[i]
        frequency = freq[i]
print(frequency)
print(np.abs(maximum))

#%%