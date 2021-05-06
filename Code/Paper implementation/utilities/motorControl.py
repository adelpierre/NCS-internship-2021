import numpy as np
import math

def convertSpikesToAngle(spikes,a_max = math.pi, offset = 0):
    "Convert an array of spikes to a voltage value comprised between 0 and v_max"
    n = spikes.shape[0]
    a = a_max*spikes.sum()/n + offset
    return(a)
