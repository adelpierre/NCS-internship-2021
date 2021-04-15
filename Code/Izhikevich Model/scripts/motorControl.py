import numpy as np

def convertSpikesToVoltage(spikes):
    n = spikes.shape[0]
    v = 5*spikes.sum()/n
    return(v)
