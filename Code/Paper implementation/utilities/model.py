import torch, torch.nn as nn
import norse.torch as norse

#Import of the Izhikevich module and functions from Norse
from norse.torch.module import izhikevich as izk
from norse.torch.functional.izhikevich import *

class Network(torch.nn.Module):
    def __init__(self, weight_matrix):
        super(Network, self).__init__()     
        self.LLBN = izk.IzhikevichRecurrentCell(1, 1, LLBN_behaviour, autapses=True, 
                                                input_weights=weights_matrix[2]*torch.ones(1),
                                                recurrent_weights=weights_matrix[3]*torch.ones(1), dt=dt)
        self.EBN = izk.IzhikevichCell(phasic_bursting, dt=dt)
        self.IFN = izk.IzhikevichCell(phasic_spiking, dt=dt)
        self.TN = izk.IzhikevichRecurrentCell(1, 1, tonic_bursting, autapses=True, 
                                              input_weights=weights_matrix[9]*torch.ones(1), 
                                              recurrent_weights=weights_matrix[10]*torch.ones(1), dt=dt)
        self.MN = izk.IzhikevichCell(phasic_spiking, dt=dt)
        self.LLBN2 = izk.IzhikevichRecurrentCell(1, 1, LLBN_behaviour, autapses=True, 
                                                input_weights=weights_matrix[14]*torch.ones(1),
                                                recurrent_weights=weights_matrix[15]*torch.ones(1), dt=dt)
        self.EBN2 = izk.IzhikevichCell(phasic_bursting, dt=dt)
        self.IFN2 = izk.IzhikevichCell(phasic_spiking, dt=dt)
        self.TN2 = izk.IzhikevichRecurrentCell(1, 1, tonic_bursting, autapses=True, 
                                              input_weights=weights_matrix[21]*torch.ones(1), 
                                              recurrent_weights=weights_matrix[22]*torch.ones(1), dt=dt)
        self.MN2 = izk.IzhikevichCell(phasic_spiking, dt=dt)
        self.s_2 = None
        self.s_3 = phasic_bursting.s
        self.s_4 = phasic_spiking.s
        self.s_5 = None
        self.s_6 = phasic_spiking.s
        self.s_22 = None
        self.s_32 = phasic_bursting.s
        self.s_42 = phasic_spiking.s
        self.s_52 = None
        self.s_62 = phasic_spiking.s
        
    def forward(self, input_mat, weights_matrix):        
        v = np.zeros((1,))
        v2 = np.zeros((1,))
        
        o_spikes = np.zeros((1,))
        o_spikes2 = np.zeros((1,))
        
        v_o = np.zeros((4,))
        v_o2 = np.zeros((4,))
        
        o_spikes_o = np.zeros((4,))
        o_spikes_o2 = np.zeros((4,))
        
        temp = torch.zeros((1,))
        temp2 = torch.zeros((1,))
        
        input_matrix = input_mat * weights_matrix[0]
        input_matrix2 = input_mat * weights_matrix[12]
        
        z_1 = np.reshape(input_matrix, (x*y,))
        z_12 = np.reshape(input_matrix2, (x*y,))
        
        z_plus = z_1.sum()
        z_plus2 = z_12.sum()
        
        z_2, self.s_2 = self.LLBN(torch.tensor(z_plus*weights_matrix[1]-temp.detach().numpy()).float(), self.s_2)
        z_22, self.s_22 = self.LLBN(torch.tensor(z_plus2*weights_matrix[13]-temp2.detach().numpy()).float(), 
                                    self.s_22)
        v_o[0] = self.s_2.v.detach().numpy()
        v_o2[0] = self.s_22.v.detach().numpy()
        o_spikes_o[0] = z_2.detach().numpy()
        o_spikes_o2[0] = z_22.detach().numpy()

        z_in = z_plus*weights_matrix[4] + z_2*weights_matrix[5]
        z_in2 = z_plus2*weights_matrix[16] + z_22*weights_matrix[17]
        z_3, self.s_3 = self.EBN(z_in, self.s_3)
        z_32, self.s_32 = self.EBN(z_in2, self.s_32)
        v_o[1] = self.s_3.v.detach().numpy()
        v_o2[1] = self.s_32.v.detach().numpy()
        o_spikes_o[1] = z_3.detach().numpy()
        o_spikes_o2[1] = z_32.detach().numpy()

        z_4, self.s_4 = self.IFN(z_3*weights_matrix[6], self.s_4)
        z_42, self.s_42 = self.IFN(z_32*weights_matrix[18], self.s_42)
        temp = z_4*weights_matrix[7]
        temp2 = z_42*weights_matrix[19]
        v_o[2] = self.s_4.v.detach().numpy()
        v_o2[2] = self.s_42.v.detach().numpy()
        o_spikes_o[2] = z_4.detach().numpy()
        o_spikes_o2[2] = z_42.detach().numpy()

        z_5, self.s_5 = self.TN(z_3.float()*weights_matrix[8], self.s_5)
        z_52, self.s_52 = self.TN(z_32.float()*weights_matrix[20], self.s_52)
        v_o[3] = self.s_5.v.detach().numpy()
        v_o2[3] = self.s_52.v.detach().numpy()
        o_spikes_o[3] = z_5.detach().numpy()
        o_spikes_o2[3] = z_52.detach().numpy()

        z_6, self.s_6 = self.MN(z_5*weights_matrix[11], self.s_6)
        z_62, self.s_62 = self.MN(z_52*weights_matrix[23], self.s_62)
        o_spikes = z_6.detach().numpy()
        o_spikes2 = z_62.detach().numpy()
        v = self.s_6.v.detach().numpy()
        v2 = self.s_62.v.detach().numpy()
        return o_spikes, v, o_spikes2, v2, o_spikes_o, v_o