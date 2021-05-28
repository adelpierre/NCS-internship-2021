import numpy as np
import time
import matplotlib.pyplot as plt
import torch, torch.nn as nn
import norse
import sys
import norse.torch as norse
from time import perf_counter
from array2gif import write_gif
import utilities
from utilities.input_generation import *
from utilities.visualization import *
from utilities.cib import *
from utilities.weights import *

#Import of the Izhikevich module and functions from Norse
from norse.torch.module import izhikevich as izk
from norse.torch.functional.izhikevich import *

#Initialization of the parameters of our simulation
x = 127 
y = 127        #Size of our input. For simplicity, we use a square image
dt = 0.001     #Timestep of our simulation
duration = 1   #Duration of the movement
n_runs = 11000 #Nombre de runs
k = 0

x_p = 3                    #Size of the object moving within the frame
y_p = 3
point = np.ones((x_p,y_p))

nb_samples, nb_repetitions = set_params(x,y,duration,dt)

print(nb_samples)
print(nb_repetitions)

mvt, dvs_output = input_generator(x,y,point,nb_samples,nb_repetitions,dt)

#Creation of a weight matrix
weights_ini = np.zeros((x,y))
for i in range(x):
    if i <= (x-1)/2 :
        weights_ini[i,:]+=(1-(2*i/(x-1)))
    else :
        weights_ini[i,:]+=(2*(i-x//2)/(x-1))
        
#Definition of the parameters of the Izhikevich neuron models
LLBN_behaviour = createIzhikevichSpikingBehaviour(0.1,-0.075,-55,6,-60,-60,tau_inv=250)
behaviours = [LLBN_behaviour,phasic_bursting,phasic_spiking,tonic_spiking]

#Definition of the network
class Network(torch.nn.Module):
    def __init__(self, weight_matrix):
        super(Network, self).__init__()     
        self.LLBN = izk.IzhikevichRecurrentCell(1, 1, LLBN_behaviour, autapses=True, 
                                                input_weights=weights_matrix[2]*torch.ones(1),
                                                recurrent_weights=weights_matrix[3]*torch.ones(1), dt=dt)
        self.EBN = izk.IzhikevichCell(phasic_bursting, dt=dt)
        self.IFN = izk.IzhikevichCell(phasic_spiking, dt=dt)
        self.TN = izk.IzhikevichRecurrentCell(1, 1, tonic_spiking, autapses=True, 
                                              input_weights=weights_matrix[9]*torch.ones(1), 
                                              recurrent_weights=weights_matrix[10]*torch.ones(1), dt=dt)
        self.MN = izk.IzhikevichCell(phasic_spiking, dt=dt)
        
    def forward(self, input_mat, weight_matrix, nb_repetitions):        
        v = np.zeros((5, nb_repetitions))
        
        o_spikes = np.zeros((5,nb_repetitions))
        
        s_2 = None
        s_3 = phasic_bursting.s
        s_4 = phasic_spiking.s
        s_5 = None
        s_6 = phasic_spiking.s
        
        temp = torch.zeros((1,))
        
        input_matrix = input_mat * weights_matrix[0]
        z_1 = np.reshape(input_matrix, (x*y,))
        
        for ts in range(nb_repetitions):
            z_plus = z_1.sum()
            z_2, s_2 = self.LLBN(torch.tensor(z_plus*weights_matrix[1]-temp.detach().numpy()).float(), s_2)
            v[0,ts] = s_2.v.detach().numpy()
            o_spikes[0,ts] = z_2.detach().numpy()

            z_in = z_plus*weights_matrix[4] + z_2*weights_matrix[5]
            z_3, s_3 = self.EBN(z_in, s_3)
            v[1,ts] = s_3.v.detach().numpy()
            o_spikes[1,ts] = z_3.detach().numpy()
            
            z_4, s_4 = self.IFN(z_3*weights_matrix[6], s_4)
            temp = z_4*weights_matrix[7]
            v[2,ts] = s_4.v.detach().numpy()
            o_spikes[2,ts] = z_4.detach().numpy()
            
            z_5, s_5 = self.TN(z_3.float()*weights_matrix[8], s_5)
            v[3,ts] = s_5.v.detach().numpy()
            o_spikes[3,ts] = z_5.detach().numpy()
            
            z_6, s_6 = self.MN(z_5*weights_matrix[11], s_6)
            v[4,ts] = s_6.v.detach().numpy()
            o_spikes[4,ts] = z_6.detach().numpy()
        return o_spikes, v

for l1 in range(300):
    for l2 in range(4):
        for l3 in range(4):
            for l4 in range(100):
                for l5  in range(35):
                    for l6 in range(35):
                        for l7 in range(35):
                            for l8 in range(35):
                                for l9 in range(4):
                                    for l10 in range(4):
                                        for l11 in range(35):
                                            print("Computing run number " + str(k))
                                            #Create weight matrix
                                            weights_matrix = create_weights(
                                                weight_to_LLBN = 1+l11,
                                                weight_LLBN_input = 1+l10,
                                                weight_LLBN_recurrent = 1+l9,
                                                weight_to_EBN = 1+l8,
                                                weight_LLBN_EBN = 1+l7,
                                                weight_EBN_IFN = 1+l6,
                                                weight_IFN_LLBN = 1+l5,
                                                weight_EBN_TN = 1+l4,
                                                weight_TN_input = 1+l3,
                                                weight_TN_recurrent = 1+l2,
                                                weight_TN_MN = 1+l1
                                            )
                                            weights_matrix.insert(0,weights_ini)

                                            #Create model
                                            model = Network(weights_matrix)

                                            #Create output spikes and voltage variables
                                            o_tot = np.zeros((5,nb_repetitions*nb_samples))
                                            v_tot = np.zeros((5,nb_repetitions*nb_samples))
                                            i_tot = np.zeros((x*y*nb_samples,))

                                            #Run simulation
                                            for i in range(nb_samples):
                                                o, v = model(dvs_output[i], weights_matrix, nb_repetitions)
                                                i_tot[i*x*y:(i+1)*x*y] += np.reshape(dvs_output[i],(x*y,))
                                                o_tot[:,i*nb_repetitions:(i+1)*nb_repetitions] += o
                                                v_tot[:,i*nb_repetitions:(i+1)*nb_repetitions] += v

                                            output_visualisation(i_tot,o_tot,v_tot,"Test",nb_repetitions,dt,k,save = True)
                                            k += 1

                                            del o_tot, i_tot, v_tot
