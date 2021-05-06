#%matplotlib inline
# import mpld3
# mpld3.enable_notebook()

import os
import time
import numpy as np
import matplotlib.pyplot as plt
from array2gif import write_gif
import sys
np.set_printoptions(threshold=sys.maxsize)
import pandas as pd
import csv

def print_gif(image, name='output'):
    "Print gif of the array of frame given as input"
    shape = image.shape
    gif = np.zeros((shape[0],3,shape[1],shape[2]))
    for i in range(shape[0]):
        gif[i,0,:,:] = 255*image[i,:,:]
        gif[i,1,:,:] = 255*image[i,:,:]
        gif[i,2,:,:] = 255*image[i,:,:]
    write_gif(gif, 'Output/' + name+'.gif', fps=shape[0])
    
def output_visualisation_both(input_spikes,o,v,o2,v2,a_m,sfn,dt,f=0,save=False):
    # Set figure size 
    nsll = 0.4  # neuron-spike line-length
    
    n = o.shape[0]
    ratios = [3,4,3,4,3,4]
        
    height = np.array(ratios).sum()+2
    width = 13

    fig, axs = plt.subplots(6, figsize=(width,height)) #, gridspec_kw={'height_ratios': ratios})
    fig.tight_layout(pad=5.0)
    fig.suptitle(sfn)
    
    n = input_spikes.shape[0]
    for i in range(n):
        i_indexes = np.array(np.where(input_spikes[i]>0))
        if i_indexes.shape[1] > 0:
            axs[0].eventplot(i_indexes.reshape(-1), lineoffsets=i+1)
        #axs.eventplot(i_indexes, orientation='horizontal', linewidths=2, colors='k', lineoffsets=i+1, linelengths=nsll)
    axs[0].set_title("Input spikes of the model")
    axs[0].set_xlabel("Time [ms]")
    axs[0].set_ylabel("Neuron index")
    axs[0].set_xlim((0,input_spikes.shape[1]))
    axs[0].set_xticks(np.arange(0, input_spikes.shape[1]+1, 1000))
    axs[0].set_ylim((0,input_spikes.shape[0]))
    axs[0].set_yticks(np.arange(0, input_spikes.shape[0]+1, 100))
    
    n = v.shape[0]
    axs[-5].plot(v[:], linewidth=2)
    axs[-5].set_title("Output of the model")
    axs[-5].set_xlabel("Time [ms]")
    axs[-5].set_ylabel("Voltage [mV]")
    axs[-5].set_xlim((0,n))

    o_indexes = np.where(o[:]>0)
    axs[-4].eventplot(o_indexes, linewidths=2, colors='k', linelengths=nsll) 
    axs[-4].set_xlabel("Time [ms]")
    axs[-4].set_ylabel("Spikes")
    axs[-4].set_xlim((0,n))
    axs[-4].set_xticks((0, n))

    n = v2.shape[0]
    axs[-3].plot(v2[:], linewidth=2)
    axs[-3].set_title("Output of the model")
    axs[-3].set_xlabel("Time [ms]")
    axs[-3].set_ylabel("Voltage [mV]")
    axs[-3].set_xlim((0,n))

    o2_indexes = np.where(o2[:]>0)
    axs[-2].eventplot(o2_indexes, linewidths=2, colors='k', linelengths=nsll) 
    axs[-2].set_xlabel("Time [ms]")
    axs[-2].set_ylabel("Spikes")
    axs[-2].set_xlim((0,n))
    axs[-2].set_xticks((0, n))

    if save == True:
        path = os.getcwd()
        path += "/Output/Run" + str(f)
        os.mkdir(path)
        plt.savefig(path + "/Plot.jpg")
        plt.close(fig)

def output_visualisation_single(input_spikes,o,v,a_m,sfn,dt,f=0,save=False):
    # Set figure size 
    nsll = 0.4  # neuron-spike line-length
    
    n = o.shape[0]
    ratios = [3,4,3,4]
        
    height = np.array(ratios).sum()+2
    width = 13

    fig, axs = plt.subplots(4, figsize=(width,height)) #, gridspec_kw={'height_ratios': ratios})
    fig.tight_layout(pad=5.0)
    fig.suptitle(sfn)
    
    n = input_spikes.shape[0]
    for i in range(n):
        i_indexes = np.array(np.where(input_spikes[i]>0))
        if i_indexes.shape[1] > 0:
            axs[0].eventplot(i_indexes.reshape(-1), lineoffsets=i+1)
        #axs.eventplot(i_indexes, orientation='horizontal', linewidths=2, colors='k', lineoffsets=i+1, linelengths=nsll)
    axs[0].set_title("Input spikes of the model")
    axs[0].set_xlabel("Time [ms]")
    axs[0].set_ylabel("Neuron index")
    axs[0].set_xlim((0,input_spikes.shape[1]))
    axs[0].set_xticks(np.arange(0, input_spikes.shape[1]+1, 1000))
    axs[0].set_ylim((0,input_spikes.shape[0]))
    axs[0].set_yticks(np.arange(0, input_spikes.shape[0]+1, 100))
    
    n = v.shape[0]
    axs[-3].plot(v[:], linewidth=2)
    axs[-3].set_title("Output of the model")
    axs[-3].set_xlabel("Time [ms]")
    axs[-3].set_ylabel("Voltage [mV]")
    axs[-3].set_xlim((0,n))

    o_indexes = np.where(o[:]>0)
    axs[-2].eventplot(o_indexes, linewidths=2, colors='k', linelengths=nsll) 
    axs[-2].set_xlabel("Time [ms]")
    axs[-2].set_ylabel("Spikes")
    axs[-2].set_xlim((0,n))

    axs[-1].plot(a_m[:], linewidth=2)
    axs[-1].set_title("Angle of the eye motor")
    axs[-1].set_xlabel("Time [ms]")
    axs[-1].set_ylabel("Angle [rad]")
    axs[-1].set_xlim((0,n))

    if save == True:
        path = os.getcwd()
        path += "/Output/Run" + str(f)
        os.mkdir(path)
        plt.savefig(path + "/Plot.jpg")
        plt.close(fig)

def output_visualisation_single_tot(input_spikes,o,v,o_o,v_o,a_m,sfn,dt):
    # Set figure size 
    nsll = 0.4  # neuron-spike line-length

    n = o.shape[0]
    n_2 = o_o.shape[0]
    ratios = [3,4,3,4,4]
        
    height = np.array(ratios).sum()+2
    width = 13

    fig, axs = plt.subplots(4+2*n_2, figsize=(width,height)) #, gridspec_kw={'height_ratios': ratios})
    fig.tight_layout(pad=5.0)
    fig.suptitle(sfn)
    
    n = input_spikes.shape[0]
    print(n)
    for i in range(n):
        i_indexes = np.array(np.where(input_spikes[i]>0))
        if i_indexes.shape[1] > 0:
            axs[0].eventplot(i_indexes.reshape(-1), lineoffsets=i+1)
        #axs.eventplot(i_indexes, orientation='horizontal', linewidths=2, colors='k', lineoffsets=i+1, linelengths=nsll)
    axs[0].set_title("Input spikes of the model")
    axs[0].set_xlabel("Time [ms]")
    axs[0].set_ylabel("Neuron index")
    axs[0].set_xlim((0,input_spikes.shape[1]))
    axs[0].set_xticks(np.arange(0, input_spikes.shape[1]+1, 1000))
    axs[0].set_ylim((0,input_spikes.shape[0]))
    axs[0].set_yticks(np.arange(0, input_spikes.shape[0]+1, 100))
    
    for j in range(0,2*n_2,2):
        n = v_o[j].shape[0]
        axs[j+1].plot(v[int(j/2),:,:], linewidth=2)
        axs[j+1].set_title("Output of the model")
        axs[j+1].set_xlabel("Time [ms]")
        axs[j+1].set_ylabel("Voltage [mV]")
        axs[j+1].set_xlim((0,n))

        o_indexes = np.where(o_o[int(j/2),:,:]>0)
        axs[j+2].eventplot(o_indexes, linewidths=2, colors='k', linelengths=nsll) 
        axs[j+2].set_xlabel("Time [ms]")
        axs[j+2].set_ylabel("Spikes")
        axs[j+2].set_xlim((0,n))
        axs[j+2].set_xticks((0, n))
    
    n = v.shape[0]
    axs[-3].plot(v[:], linewidth=2)
    axs[-3].set_title("Output of the model")
    axs[-3].set_xlabel("Time [ms]")
    axs[-3].set_ylabel("Voltage [mV]")
    axs[-3].set_xlim((0,n))

    o_indexes = np.where(o[:]>0)
    axs[-2].eventplot(o_indexes, linewidths=2, colors='k', linelengths=nsll) 
    axs[-2].set_xlabel("Time [ms]")
    axs[-2].set_ylabel("Spikes")
    axs[-2].set_xlim((0,n))
    axs[-2].set_xticks((0, n))

    axs[-1].plot(a_m[:], linewidth=2)
    axs[-1].set_title("Angle of the eye motor")
    axs[-1].set_xlabel("Time [ms]")
    axs[-1].set_ylabel("Angle [rad]")
    axs[-1].set_xlim((0,n))

    if save == True:
        path = os.getcwd()
        path += "/Output/Run" + str(f)
        os.mkdir(path)
        plt.savefig(path + "/Plot.jpg")
        plt.close(fig)
