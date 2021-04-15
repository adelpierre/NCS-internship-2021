import numpy as np
import math

def set_params(x, y, duration, dt):
    if x!=y :
        nb_samples = int((max(x,y) - 1)/2)
    else:
        nb_samples = int(x//2)                     #Number of samples presented to the simulation
    nb_repetitions = int(duration/(dt*nb_samples)) #Number of time one input will be repeated 
                                                   #during one step of the simulation
    return nb_samples, nb_repetitions

def input_generator(
    x,
    y,
    objects,
    nb_samples,
    nb_repetitions,
    dt,
    input_type="movement",
    mvt_type="up",
    initial_pos = None,
    t_2 = 0,
    f_blink = 10
):
    sim_input = np.zeros((nb_samples+1,x,y))
    dvs_output = np.zeros((nb_samples,x,y))
    if initial_pos == None:
        pos_ini = (x//2, y//2)
    else:
        pos_ini = initial_pos
    os = objects.shape
    if input_type == "movement":
        for i in range(nb_samples):
            if mvt_type == "up":
                sim_input[i+1,pos_ini[0]-os[0]//2-i:pos_ini[0]+math.ceil(os[0]/2)-i,pos_ini[1]-math.ceil(os[1]//2):pos_ini[1]+math.ceil(os[1]/2)] += objects
                dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
            elif mvt_type == "down":
                sim_input[i+1,pos_ini[0]-os[0]//2+i:pos_ini[0]+math.ceil(os[0]/2)+i,pos_ini[1]-math.ceil(os[1]//2):pos_ini[1]+math.ceil(os[1]/2)] += objects
                dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
            elif mvt_type == "left":
                sim_input[i+1,pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-math.ceil(os[1]//2)-i:pos_ini[1]+math.ceil(os[1]/2)-i] += objects
                dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
            elif mvt_type == "right":
                sim_input[i+1,pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-math.ceil(os[1]//2)+i:pos_ini[1]+math.ceil(os[1]/2)+i] += objects
                dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
            else:
                raise Exception("Wrong movement type, please use up, down, left or right")
    elif input_type == "partial_movement":
        if t_2 > nb_samples:
            raise Warning("T2 > nb_samples, defaulting to nb_samples")
            t_2 = nb_samples
        for i in range(t_2):
            if mvt_type == "up":
                sim_input[i+1,pos_ini[0]-os[0]//2-i:pos_ini[0]+math.ceil(os[0]/2)-i,pos_ini[1]-math.ceil(os[1]//2):pos_ini[1]+math.ceil(os[1]/2)] += objects
                dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
            elif mvt_type == "down":
                sim_input[i+1,pos_ini[0]-os[0]//2+i:pos_ini[0]+math.ceil(os[0]/2)+i,pos_ini[1]-math.ceil(os[1]//2):pos_ini[1]+math.ceil(os[1]/2)] += objects
                dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
            elif mvt_type == "left":
                sim_input[i+1,pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-math.ceil(os[1]//2)-i:pos_ini[1]+math.ceil(os[1]/2)-i] += objects
                dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
            elif mvt_type == "right":
                sim_input[i+1,pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-math.ceil(os[1]//2)+i:pos_ini[1]+math.ceil(os[1]/2)+i] += objects
                dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
            else:
                raise Exception("Wrong movement type, please use up, down, left or right")
    elif input_type == "blinking":
        for i in range(0,nb_samples,2):
            sim_input[i+1,pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-math.ceil(os[1]//2):pos_ini[1]+math.ceil(os[1]/2)] += objects
            dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
        #raise Exception("WIP, please try again later")
    else:
        raise Exception("Wrong input type, please use movement or blinking")
    return sim_input, dvs_output
