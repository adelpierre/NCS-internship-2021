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

        # If parent wants a frame
        if camera_pipe.poll():
            buf_size = camera_pipe.recv()
            # Extract buffer of the right size
            send_buffer = ...

            camera_pipe.send(send_buffer)

      sleep(0.0001)


def model_worker(worker_pipe):
    while True:
        # Wait for input buffer and read it once its there
        input_buf = worker_pipe.recv()

        # Process input_buf

        # Send results
        worker_pipe.send(correction)


def main():

   # Camera configuratin
   n_cameras = 2
   cam_params = [
      { 
         "buffer_size": 50,
         "camera_id": name1,
      },
      { 
         "buffer_size": 50,
         "camera_id": name2,
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
   for i in range(n_cameras)
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
         if workers_params[i]["side"] == "left"
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