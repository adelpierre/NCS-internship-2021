import numpy as np

def convertSpikesToVoltage(spikes,v_max = 5, offset = 0):
    "Convert an array of spikes to a voltage value comprised between 0 and v_max"
    n = spikes.shape[0]
    v = v_max*spikes.sum()/n + offset
    return(v)
