#%matplotlib inline
import os
import numpy as np
import matplotlib.pyplot as plt
from array2gif import write_gif

def print_gif(image):
    shape = image.shape
    gif = np.zeros((shape[0],3,shape[1],shape[2]))
    for i in range(shape[0]):
        gif[i,0,:,:] = 255*image[i,:,:]
        gif[i,1,:,:] = 255*image[i,:,:]
        gif[i,2,:,:] = 255*image[i,:,:]
    write_gif(gif, 'output.gif', fps=shape[0])
    
def output_visualisation(input_spikes,o,v,v_m,  sfn,nb_repetition,dt,f=0,save=False):
    
    # Set figure size 
    nsll = 0.4  # neuron-spike line-length
    extra = 0
    
    # nb_neurons = o.shape[0]
    # n = o.shape[1]
    n = o.shape[0]
    ratios = [10,3,4,4]
    
    # rv = 3
    # for i in range(nb_neurons):
    #     ratios += [3,4]
        
    ratios.pop()
    height = np.array(ratios).sum()+2
    width = 15
        
    fig, axs = plt.subplots(2+2, figsize=(width,height)) #, gridspec_kw={'height_ratios': ratios})
    fig.tight_layout(pad=5.0)
    fig.suptitle(sfn)
    
    img = np.ones(input_spikes.shape)
    img = img - input_spikes
    axs[0].imshow(input_spikes, cmap='Greys',aspect='auto')
    # n = input_spikes.shape[0]
    # print(n)
    # for i in range(n):
    #     i_indexes = np.where(input_spikes[i]>0)
    #     i_indexes = np.flip(i_indexes)
    #     axs[0].eventplot(i_indexes, orientation='vertical', linewidths=2, colors='k', lineoffsets=i+1, linelengths=nsll)
    axs[0].set_xlabel("Input of the model for a timestep of " + str(1000*dt) + "ms")
    axs[0].set_ylabel("Spikes in IL")
    axs[0].set_xlim((0,input_spikes.shape[1]))
    axs[0].set_xticks(np.arange(0, input_spikes.shape[1]+1, 100))
    axs[0].set_ylim((0,input_spikes.shape[0]))
    axs[0].set_yticks(np.arange(0, input_spikes.shape[0]+1, 100))
    
    n = v.shape[0]
    for j in range(1,2,2):
        axs[j].plot(v[:], linewidth=2)
        axs[j].set_title("Output of the model")
        axs[j].set_xlabel("Time [ms]")
        axs[j].set_ylabel("Voltage [mV]")
        axs[j].set_xlim((0,n))

        o_indexes = np.where(o[:]>0)
        axs[j+1].eventplot(o_indexes, linewidths=2, colors='k', linelengths=nsll) 
        axs[j+1].set_xlabel("Time [ms]")
        axs[j+1].set_ylabel("Spikes")
        axs[j+1].set_xlim((0,nb_repetition))
        axs[j+1].set_xticks((0, n))

    axs[-1].plot(v_m[:], linewidth=2)
    axs[-1].set_title("Voltage of the eye motor")
    axs[-1].set_xlabel("Time [ms]")
    axs[-1].set_ylabel("Voltage [V]")
    axs[-1].set_xlim((0,n))

    if save == True:
        path = os.getcwd()
        path += "/Runs/Run" + str(f)
        os.mkdir(path)
        plt.savefig(path + "/Plot.jpg")
        plt.close(fig)
