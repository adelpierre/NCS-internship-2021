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
from utilities.model import *
from multiprocessing import Process, Queue

# Import of the Izhikevich module and functions from Norse
from norse.torch.module import izhikevich as izk
from norse.torch.functional.izhikevich import *

# Initialization of the parameters of our simulation
x = 41 
y = 41         # Size of our input. For simplicity, we use a square image
dt = 0.001     # Timestep of our simulation
duration = 4   # Duration of the movement
n_motor = 0

x_p = 3                    # Size of the object moving within the frame
y_p = 3
point = np.ones((x_p,y_p))

nb_samples, nb_repetitions = set_params(x,y,dt)
print(nb_samples)
print(nb_repetitions)
mvt_full = np.zeros((int(duration/dt),x,y))
dvs_full = np.zeros((int(duration/dt),x,y))
sim_frame_ini = np.zeros((x,y))

n_motor = 20

dvs_buffer_size = 20
count = 0
i = 0
temp = 0
input_mat = [1,2]

def simulation(ini,to_processing,out):
    output = [[],[],[]]
    if ini == 'input generation':
        previous_sim_frame = np.zeros((x,y))
        dvs_buffer = np.zeros((dvs_buffer_size,x,y))
        mvt = np.zeros((dvs_buffer_size,x,y))
        relative_pos = 0
        print("Generating input...")
        for k in range(dvs_buffer_size):
            if i < 1:
                if count > nb_repetitions:
                    relative_pos -= 1
                sim_input, dvs_output = single_timestep(x,y,point,previous_sim_frame,mvt_type="up",initial_pos=((x//2+relative_pos,y//2)),add_negative_polarities=False)
            elif 1 < i < 3:
                if count > nb_repetitions:
                    relative_pos += 1
                sim_input, dvs_output = single_timestep(x,y,point,previous_sim_frame,mvt_type="down",initial_pos=((x//2+relative_pos,y//2)),add_negative_polarities=False)
            elif i > 3:
                if count > nb_repetitions:
                    relative_pos -= 1
                sim_input, dvs_output = single_timestep(x,y,point,previous_sim_frame,mvt_type="up",initial_pos=((x//2+relative_pos,y//2)),add_negative_polarities=False)
            previous_sim_frame = sim_input
            mvt[k] = sim_input
            dvs_buffer[k] = dvs_output
        output[0].append(mvt)
        output[1].append(dvs_buffer)
        to_processing.put(dvs_buffer)
        print("Input generated !")
    elif ini == 'processing':
        print("Processing data...")
        dvs_input = to_processing.get()
        
        # Defining weights
        weight_to_LLBN = 25
        weight_LLBN_input = 25
        weight_LLBN_recurrent = 25
        weight_to_EBN = 250
        weight_LLBN_EBN = 100
        weight_EBN_IFN = 100
        weight_IFN_LLBN = 100
        weight_EBN_TN = 100
        weight_TN_input = 25
        weight_TN_recurrent = 25
        weight_TN_MN = 100

        weights_ini_up,weights_ini_down = create_weights_fovea(x,y)

        weights_matrix1 = create_weights(
            weight_fovea = weights_ini_up,
            weight_to_LLBN = weight_to_LLBN,
            weight_LLBN_input = weight_LLBN_input,
            weight_LLBN_recurrent = weight_LLBN_recurrent,
            weight_to_EBN = weight_to_EBN,
            weight_LLBN_EBN = weight_LLBN_EBN,
            weight_EBN_IFN = weight_EBN_IFN,
            weight_IFN_LLBN = weight_IFN_LLBN,
            weight_EBN_TN = weight_EBN_TN,
            weight_TN_input = weight_TN_input,
            weight_TN_recurrent = weight_TN_recurrent,
            weight_TN_MN = weight_TN_MN
        )

        weights_matrix2 = create_weights(
            weight_fovea = weights_ini_down,
            weight_to_LLBN = weight_to_LLBN,
            weight_LLBN_input = weight_LLBN_input,
            weight_LLBN_recurrent = weight_LLBN_recurrent,
            weight_to_EBN = weight_to_EBN,
            weight_LLBN_EBN = weight_LLBN_EBN,
            weight_EBN_IFN = weight_EBN_IFN,
            weight_IFN_LLBN = weight_IFN_LLBN,
            weight_EBN_TN = weight_EBN_TN,
            weight_TN_input = weight_TN_input,
            weight_TN_recurrent = weight_TN_recurrent,
            weight_TN_MN = weight_TN_MN
        )

        weights_matrix = weights_matrix1 + weights_matrix2

        # Create model
        model = Network(weights_matrix)

        # Create output spikes and voltage variables
        o_tot = np.zeros((dvs_buffer_size,))
        o2_tot = np.zeros((dvs_buffer_size,))
        v_tot = np.zeros((dvs_buffer_size,))
        v2_tot = np.zeros((dvs_buffer_size,))
        o_o_tot = np.zeros((dvs_buffer_size,))
        o2_o_tot = np.zeros((dvs_buffer_size,))
        v_o_tot = np.zeros((dvs_buffer_size,))
        v2_o_tot = np.zeros((dvs_buffer_size,))
        i_tot = np.zeros((x*y,dvs_buffer_size))
        a_motor = np.zeros((dvs_buffer_size))
        buffer_model = np.zeros((0,))
        buffer_model2 = np.zeros((0,))

        # Run simulation
        for l in range(dvs_buffer_size):
            o, v, o2, v2, o_o, v_o, o_o2, v_o2 = model(dvs_input[l], weights_matrix)
            o, v, o2, v2, o_o, v_o, o_o2, v_o2 = model(dvs_input[l], weights_matrix)
            i_tot[l] += np.reshape(dvs_input[l],(x*y,))[::-1]
            o_tot[l] += o
            o2_tot[l] += o2
            v_tot[l] += v
            v2_tot[l] += v2
            o_o_tot[l] += o
            o2_o_tot[l] += o2
            v_o_tot[l] += v
            v2_o_tot[l] += v2
            buffer = np.append(buffer,o)
            buffer2 = np.append(buffer2,o2)
            if buffer.shape[0] > dvs_buffer_size:
                a_motor[l] = convertSpikesToAngle(buffer) - convertSpikesToAngle(buffer2)
                buffer_model = np.copy(buffer[1:])
                buffer_model2 = np.copy(buffer2[1:])
        output[2] = a_motor
        print("Data processed !")
    out.put(output)


if __name__ == "__main__":  # confirms that the code is under main function
    out = Queue()
    to_processing = Queue()
    names = ['input generation','processing']
    procs = []

    # instantiating process with arguments
    while i < duration:
        print(str(i) + "/" + str(duration))
        for name in names:
            proc = Process(target=simulation, args=(name,to_processing,out))
            procs.append(proc)
            temp = out.get()
            mvt_full = np.append(mvt_full,temp[0])
            dvs_full = np.append(dvs_full,temp[1])
        for p in procs:
            p.start()
        i+=dvs_buffer_size*dt
    print(mvt_full.shape)
    print(dvs_full.shape)

    # complete the processes
    for proc in procs:
        proc.join()