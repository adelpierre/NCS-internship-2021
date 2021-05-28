import numpy as np
import time
import matplotlib.pyplot as plt
import torch, torch.nn as nn
import norse
import sys
import norse.torch as norse
import utilities
from utilities.input_generation import *
from utilities.visualization import *
from utilities.cib import *
from utilities.weights import *
from utilities.model import *
from multiprocessing import Process, Pipe

#Import of the Izhikevich module and functions from Norse
from norse.torch.module import izhikevich as izk
from norse.torch.functional.izhikevich import *

#Initialization of the parameters of our simulation
x = 41 
y = 41         #Size of our input. For simplicity, we use a square image
dt = 0.001     #Timestep of our simulation
duration = 4   #Duration of the movement
n_motor = 0

x_p = 3                    #Size of the object moving within the frame
y_p = 3
point = np.ones((x_p,y_p))

nb_samples, nb_repetitions = set_params(x,y,dt)
mvt_full = np.zeros((int(duration/dt),x,y))
dvs_full = np.zeros((int(duration/dt),x,y))
sim_frame_ini = np.zeros((x,y))

n_motor = 20

dvs_buffer_size = 20
count = 0
i = 0
temp = 0
buffer = []

def simulated_camera_worker(camera_pipe,i,params):
   while True:
      # Build simulated frame
      send_buffer = []
      buf_size = camera_pipe.recv()
      previous_sim_frame = np.zeros((x,y))
      dvs_buffer = np.zeros((buf_size,x,y))
      mvt = np.zeros((buf_size,x,y))
      relative_pos = 0
      print("Generating input...")
      for k in range(buf_size):
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

      # If parent wants a frame
      if camera_pipe.poll():
         buf_size = camera_pipe.recv()
         # Extract buffer of the right size
         send_buffer = [previous_sim_frame, mvt, dvs_buffer]
         
         camera_pipe.send(send_buffer)

      #sleep(0.0001)


def model_worker(worker_pipe):
   print("Processing data...")
   while True:
      # Wait for input buffer and read it once its there
      dvs_input = worker_pipe.recv()
      
      # Process input_buf
      
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
      print("Data processed !")
      # Send results
      worker_pipe.send(a_motor)


def main():
   # Camera configuratin
   n_cameras = 2
   cam_params = [
      { 
         "buffer_size": dvs_buffer_size,
         "camera_id": left_cam,
      },
      { 
         "buffer_size": dvs_buffer_size,
         "camera_id": right_cam,
      },
   ]

   # Workers conf
   n_workers = 3
   workers_params = [
      { 
         "side": "left"
      },
      { 
         "side": "left"
      },
      { 
         "side": "right"
      },
   ]

   # -----------------------------------------------------------------
   #   Pipes and subprocesses initialisation
   # -----------------------------------------------------------------

   # Create communication pipes
   parent_camera_pipes, child_camera_pipes = [], []
   for i in range(n_cameras):
      parent, child = Pipe()
      parent_camera_pipes.append(parent)
      child_camera_pipes.append(child)

   parent_worker_pipes, child_worker_pipes = [], []
   for i in range(n_workers):
      parent, child = Pipe()
      parent_workers_pipes.append(parent)
      child_workers_pipes.append(child)

   # Create processes
   camera_procs = []
   for i in range(n_cameras):
      proc = Process(target=camera_worker, args=(child_camera_pipes[i], cam_params[i]))
      camera_procs.append(proc)

   for p in camera_procs:
      p.start()

   # Idem for workers processes.

   # -----------------------------------------------------------------
   #   Boucle temporelle
   # -----------------------------------------------------------------

   for i in steps:
      # Input camera
      buf_sizes = [20, 20]
      input_buffers = []
      for i in range(n_cameras):
         parent_camera_pipes.send(buf_sizes[i])
         tmp = parent_camera_pipes.recv()
         input_buffers.append(tmp)

      # Send data to workers
      for i in range(n_workers):
         if workers_params[i]["side"] == "left":
            parent_workers_pipes[i].send(input_buffers[0])
         else:
            parent_workers_pipes[i].send(input_buffers[1])

      # Read data from workers
      corrections = []
      for i in range(n_workers):
         tmp = parent_workers_pipes[i].recv()
         corrections.append(recv)

      # Apply corrections

   # Rebelote