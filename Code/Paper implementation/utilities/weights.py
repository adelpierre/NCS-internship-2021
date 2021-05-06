import numpy as np

def create_weights_fovea(x,y):
    weights_ini_up = np.zeros((x,y))
    weights_ini_down = np.zeros((x,y))
    for i in range(x):
        if i <= (x-1)/2 :
            weights_ini_up[i,:]+=(1-(2*i/(x-1)))
        else :
            weights_ini_down[i,:]+=(2*(i-(x-1)/2)/(x-1))
    return weights_ini_up,weights_ini_down

def create_weights(
    weight_fovea,
    weight_to_LLBN = 1,
    weight_LLBN_input = 1,
    weight_LLBN_recurrent = 1,
    weight_to_EBN = 1,
    weight_LLBN_EBN = 1,
    weight_EBN_IFN = 1,
    weight_IFN_LLBN = 1,
    weight_EBN_TN = 1,
    weight_TN_input = 1,
    weight_TN_recurrent = 1,
    weight_TN_MN = 1
):
    "Returns an array of weigths"
    weight_matrix = [weight_fovea, weight_to_LLBN, weight_LLBN_input, weight_LLBN_recurrent, weight_to_EBN, weight_LLBN_EBN, 
                     weight_EBN_IFN, weight_IFN_LLBN, weight_EBN_TN, weight_TN_input, weight_TN_recurrent, weight_TN_MN]
    return weight_matrix