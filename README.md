# Closed-loop learning for visuo-motor coordination using neuromorphic hardware.

## Context:

Computational models of the brain have so far tended to focus either on biological realism or on task performance, but have rarely combined both aspects in a unified framework. A variety of models is available, each covering different parts of the brain, but models integrating multiple brain regions are generally lacking. Visuo-motor tasks are a prime example of complex tasks requiring the coordination of multiple brain regions, which moreover lend themselves to neurorobotics applications. It is unknown how the brain manages to perform visuo-motor coordination at its extremely low power consumption, but spike-based communication may hold an important key to its high energy efficiency.

## Brief description of the project:

This project aims at bringing together biologically plausible models of different brain regions (cerebellum, motor cortex, visual cortex) into a unified/simplified whole performing a visuo-motor task. In particular, a robotic head (see Illustrations 1. and 2.) with two event cameras for eyes and six servomotors allowing yaw and pitch of both eyes and neck will be used to generate saccades and produce vestibulo-ocular reflexes to detect and follow salient objects in the scene.

<img src="Documentation/Images/DiagramSenActCPU.png" width="1000">
Illustration 1. Robotic head: block diagram with sensors, actuators and computing unit

The robotic head will be controlled by spiking neural networks (SNNs) running on SpiNNaker, a neuromorphic computing platform. The SNNs will integrate sensory information (visual, proprioceptive, vestibular) and will produce motor output as a response in order to perform ‘hard-coded’ pre-defined tasks. Cognitive behavior will be tackled on a second stage if time allows it. Validation of the spiking models will be done in simulation prior to be implemented on the physical setup. For that, the neurorobotics platform (NRP) will be used.

<img src="Documentation/Images/RoboticHead.png" width="1000">
Illustration 2. Robotic Head: Physical Setup


### More information:
- https://www.humanbrainproject.eu/en/
- https://github.com/norse/norse
- http://spinnakermanchester.github.io/spynnaker/5.0.0/PyNNOnSpinnakerInstall.html
- https://spinnaker8manchester.readthedocs.io/en/master/spynnaker8/modules.html
- http://neuralensemble.org/docs/PyNN/index.html
- https://neurorobotics.net/local_install.html


### The internship work includes:
- Literature review (cerebellum, motor cortex, visual cortex) 	
- Design/simplification of SNNs for visuo-motor function 	
- Simulation of embodied agent on the NRP 	
- Implementation of spiking models on SpiNNaker 	
- Hardware setup (event cameras + motors + IMUs).

### Student name:
Adrien Delpierre (ajmde@kth.se)

### Supervisor:
Jörg Conradt (jconradt@kth.se)

### Co-supervisors:
- Juan P. Romero B. (jprb@kth.se)
- Jens E. Pedersen (jeped@kth.se)

## References:

* A. Morales-Gregorio et al., “Towards a neuronal network model of macaque visuomotor cortices,” p. 1.

* S. Tolu, M. C. Capolei, L. Vannucci, C. Laschi, E. Falotico, and M. Vanegas, “A Cerebellum-Inspired Learning Approach for Adaptive and Anticipatory Control,” International Journal of Neural Systems, vol. 30, Sep. 2019, doi: 10.1142/S012906571950028X.

* H. T. Kalidindi, L. Vannucci, C. Laschi, and E. Falotico, “Cerebellar adaptive mechanisms explain the optimal control of saccadic eye movements,” Bioinspir. Biomim., vol. 16, no. 1, p. 016004, Nov. 2020, doi: 10.1088/1748-3190/abae7f.

* I. Abadía, F. Naveros, J. A. Garrido, E. Ros, and N. R. Luque, “On Robot Compliance: A Cerebellar Control Approach,” IEEE Transactions on Cybernetics, pp. 1–14, 2019, doi: 10.1109/TCYB.2019.2945498.

* O. Rhodes et al., “Real-time cortical simulation on neuromorphic hardware,” Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences, vol. 378, no. 2164, p. 20190160, Feb. 2020, doi: 10.1098/rsta.2019.0160.

* S. B. Furber, F. Galluppi, S. Temple, and L. A. Plana, “The SpiNNaker Project,” Proceedings of the IEEE, vol. 102, no. 5, pp. 652–665, May 2014, doi: 10.1109/JPROC.2014.2304638.

* X. Jin, M. Lujan, L. A. Plana, S. Davies, S. Temple, and S. B. Furber, “Modeling Spiking Neural Networks on SpiNNaker,” Computing in Science Engineering, vol. 12, no. 5, pp. 91–97, Sep. 2010, doi: 10.1109/MCSE.2010.112.

* S. B. Furber et al., “Overview of the SpiNNaker System Architecture,” IEEE Transactions on Computers, vol. 62, no. 12, pp. 2454–2467, Dec. 2013, doi: 10.1109/TC.2012.142.
