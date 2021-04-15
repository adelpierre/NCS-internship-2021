#%matplotlib inline
import os
import numpy as np
import matplotlib.pyplot as plt
from array2gif import write_gif

def print_gif(image, name='output'):
    "Print gif of the array of frame given as input"
    shape = image.shape
    gif = np.zeros((shape[0],3,shape[1],shape[2]))
    for i in range(shape[0]):
        gif[i,0,:,:] = 255*image[i,:,:]
        gif[i,1,:,:] = 255*image[i,:,:]
        gif[i,2,:,:] = 255*image[i,:,:]
    write_gif(gif, 'Output/' + name+'.gif', fps=shape[0])
    
def output_visualisation(input_spikes,o,v,v_m,sfn,dt,f=0,o_o=None,v_o=None,optional_plot=False,save=False):
    
    # Set figure size 
    nsll = 0.4  # neuron-spike line-length
    extra = 0
    
    n = o.shape[0]
    ratios = [10,3,4,4]
    
    if optional_plot:
        extra = o_o.shape[0]
        for i in range(extra):
            ratios += [3,4]
        
    height = np.array(ratios).sum()+2
    width = 15
        
    fig, axs = plt.subplots(4 + extra, figsize=(width,height)) #, gridspec_kw={'height_ratios': ratios})
    fig.tight_layout(pad=5.0)
    fig.suptitle(sfn)
    
    axs[0].imshow(input_spikes, cmap='Greys',aspect='auto') #Printing an image because eventplot is having issues displaying plots correctly
    # n = input_spikes.shape[0]
    # print(n)
    # for i in range(n):
    #     i_indexes = np.where(input_spikes[i]>0)
    #     i_indexes = np.flip(i_indexes)
    #     axs[0].eventplot(i_indexes, orientation='vertical', linewidths=2, colors='k', lineoffsets=i+1, linelengths=nsll)
    axs[0].set_title("Input spikes of the model for input of " + str(1000*dt) + "s duration")
    axs[0].set_xlabel("Time [ms]")
    axs[0].set_ylabel("Neuron index")
    axs[0].set_xlim((0,input_spikes.shape[1]))
    axs[0].set_xticks(np.arange(0, input_spikes.shape[1]+1, 100))
    axs[0].set_ylim((0,input_spikes.shape[0]))
    axs[0].set_yticks(np.arange(0, input_spikes.shape[0]+1, 100))
    
    for j in range(1,extra,2):
        n = v_o[j].shape[0]
        axs[j].plot(v_o[j,:], linewidth=2)
        axs[j].set_title("Output of the " + str(j) + "th layer")
        axs[j].set_xlabel("Time [ms]")
        axs[j].set_ylabel("Voltage [mV]")
        axs[j].set_xlim((0,n))

        o_indexes = np.where(o_o[j,:]>0)
        axs[j+1].eventplot(o_indexes, linewidths=2, colors='k', linelengths=nsll) 
        axs[j+1].set_xlabel("Time [ms]")
        axs[j+1].set_ylabel("Spikes")
        axs[j+1].set_xlim((0,n))
        axs[j+1].set_xticks((0, n))
    
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

    axs[-1].plot(v_m[:], linewidth=2)
    axs[-1].set_title("Voltage of the eye motor")
    axs[-1].set_xlabel("Time [ms]")
    axs[-1].set_ylabel("Voltage [V]")
    axs[-1].set_xlim((0,n))

    if save == True:
        path = os.getcwd()
        path += "/Output/Run" + str(f)
        os.mkdir(path)
        plt.savefig(path + "/Plot.jpg")
        plt.close(fig)
