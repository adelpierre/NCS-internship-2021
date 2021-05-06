import numpy as np
import math

def set_params(x, y, dt):
    "Set the parameters of the simulation"
    if x!=y :
        nb_samples = int((max(x,y) - 1)/2)
    else:
        nb_samples = int(x//2)                     #Number of samples presented to the simulation
    nb_repetitions = int(1/(dt*nb_samples)) #Number of time one input will be repeated 
                                                   #during one step of the simulation
    return nb_samples, nb_repetitions

def input_generator(
    x,
    y,
    objects,
    nb_samples,
    dt,
    input_type="movement",
    mvt_type="up",
    initial_pos = None,
    add_negative_polarities = True,
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
                #Construction of the frame containing the object
                sim_input[i+1,pos_ini[0]-os[0]//2-i:pos_ini[0]+math.ceil(os[0]/2)-i,pos_ini[1]-math.ceil(os[1]//2):pos_ini[1]+math.ceil(os[1]/2)] += objects
                #Construction of the frame of difference
                if add_negative_polarities:
                    dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
                else:
                    dvs_output[i]=sim_input[i+1]-sim_input[i]
                    dvs_output[dvs_output<0] = 0

            elif mvt_type == "down":
                #Construction of the frame containing the object
                sim_input[i+1,pos_ini[0]-os[0]//2+i:pos_ini[0]+math.ceil(os[0]/2)+i,pos_ini[1]-math.ceil(os[1]//2):pos_ini[1]+math.ceil(os[1]/2)] += objects
                #Construction of the frame of difference
                if add_negative_polarities:
                    dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
                else:
                    dvs_output[i]=sim_input[i+1]-sim_input[i]
                    dvs_output[dvs_output<0] = 0
            elif mvt_type == "left":
                #Construction of the frame containing the object
                sim_input[i+1,pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-math.ceil(os[1]//2)-i:pos_ini[1]+math.ceil(os[1]/2)-i] += objects
                #Construction of the frame of difference
                if add_negative_polarities:
                    dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
                else:
                    dvs_output[i]=sim_input[i+1]-sim_input[i]
                    dvs_output[dvs_output<0] = 0
            elif mvt_type == "right":
                #Construction of the frame containing the object
                sim_input[i+1,pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-math.ceil(os[1]//2)+i:pos_ini[1]+math.ceil(os[1]/2)+i] += objects
                #Construction of the frame of difference
                if add_negative_polarities:
                    dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
                else:
                    dvs_output[i]=sim_input[i+1]-sim_input[i]
                    dvs_output[dvs_output<0] = 0
            else:
                raise Exception("Wrong movement type, please use up, down, left or right")
    elif input_type == "partial_movement":
        if t_2 > nb_samples:
            raise Warning("T2 > nb_samples, defaulting to nb_samples")
            t_2 = nb_samples
        for i in range(t_2):
            if mvt_type == "up":
                #Construction of the frame containing the object
                sim_input[i+1,pos_ini[0]-os[0]//2-i:pos_ini[0]+math.ceil(os[0]/2)-i,pos_ini[1]-math.ceil(os[1]//2):pos_ini[1]+math.ceil(os[1]/2)] += objects
                #Construction of the frame of difference
                dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
            elif mvt_type == "down":
                #Construction of the frame containing the object
                sim_input[i+1,pos_ini[0]-os[0]//2+i:pos_ini[0]+math.ceil(os[0]/2)+i,pos_ini[1]-math.ceil(os[1]//2):pos_ini[1]+math.ceil(os[1]/2)] += objects
                #Construction of the frame of difference
                dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
            elif mvt_type == "left":
                #Construction of the frame containing the object
                sim_input[i+1,pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-math.ceil(os[1]//2)-i:pos_ini[1]+math.ceil(os[1]/2)-i] += objects
                #Construction of the frame of difference
                dvs_output[i]=abs(sim_input[i+1]-sim_input[i])
            elif mvt_type == "right":
                #Construction of the frame containing the object
                sim_input[i+1,pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-math.ceil(os[1]//2)+i:pos_ini[1]+math.ceil(os[1]/2)+i] += objects
                #Construction of the frame of difference
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

def up_and_down(x,y,objects,nb_samples,dt):
    sim_input1, dvs_output1 = input_generator(x,y,objects,nb_samples,dt,add_negative_polarities=False)
    sim_input2, dvs_output2 = input_generator(x,y,objects,nb_samples,dt,input_type="movement",mvt_type="down",initial_pos=(2,y//2),add_negative_polarities=False)
    sim_input3, dvs_output3 = input_generator(x,y,objects,nb_samples,dt,input_type="movement",mvt_type="down",add_negative_polarities=False)
    sim_input4, dvs_output4 = input_generator(x,y,objects,nb_samples,dt,input_type="movement",initial_pos=(x-2,y//2),add_negative_polarities=False)
    sim_input = np.concatenate((sim_input1[1:], sim_input2[2:], sim_input3[3:], sim_input4[2:]))
    dvs_output = np.concatenate((dvs_output1, dvs_output2[1:], dvs_output3[2:], dvs_output4[2:]))
    return sim_input, dvs_output

def single_timestep(x,y,objects,previous_sim_frame,mvt_type="up",initial_pos = None,add_negative_polarities = True):
    sim_input = np.zeros((x,y))
    dvs_output = np.zeros((x,y))
    save_object = np.copy(objects)
    if initial_pos == None:
        pos_ini = (x//2, y//2)
    else:
        pos_ini = initial_pos
    os = objects.shape

    if mvt_type == "up":
        #Construction of the frame containing the object
        sim_input[pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-os[1]//2:pos_ini[1]+math.ceil(os[1]/2)] += objects
        #Construction of the frame of difference
        if add_negative_polarities:
            dvs_output=abs(sim_input-previous_sim_frame)
        else:
            dvs_output=sim_input-previous_sim_frame
            dvs_output[dvs_output<0] = 0

    elif mvt_type == "down":
        #Construction of the frame containing the object
        sim_input[pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-os[1]//2:pos_ini[1]+math.ceil(os[1]/2)] += objects
        #Construction of the frame of difference
        if add_negative_polarities:
            dvs_output=abs(sim_input-previous_sim_frame)
        else:
            dvs_output=sim_input-previous_sim_frame
            dvs_output[dvs_output<0] = 0

    elif mvt_type == "left":
        #Construction of the frame containing the object
        sim_input[pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-os[1]//2:pos_ini[1]+math.ceil(os[1]/2)] += objects
        #Construction of the frame of difference
        if add_negative_polarities:
            dvs_output=abs(sim_input-previous_sim_frame)
        else:
            dvs_output=sim_input-previous_sim_frame
            dvs_output[dvs_output<0] = 0

    elif mvt_type == "right":
        #Construction of the frame containing the object
        sim_input[pos_ini[0]-os[0]//2:pos_ini[0]+math.ceil(os[0]/2),pos_ini[1]-os[1]//2:pos_ini[1]+math.ceil(os[1]/2)] += objects
        #Construction of the frame of difference
        if add_negative_polarities:
            dvs_output=abs(sim_input-previous_sim_frame)
        else:
            dvs_output=sim_input-previous_sim_frame
            dvs_output[dvs_output<0] = 0

    else:
        raise Exception("Wrong movement type, please use up, down, left or right")
    
    return sim_input, dvs_output
