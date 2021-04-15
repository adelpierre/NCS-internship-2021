from norse.torch.functional.izhikevich import *

def createIzhikevichSpikingBehaviour(
    a: float,
    b: float,
    c: float,
    d: float,
    v_rest: float,
    u_rest: float,
    tau_inv: float = 250,
    current: float = 1,
    print: bool = False,
    time_print : int = 250,
    timestep_print : float = 0.1
) -> IzhikevichSpikingBehaviour:
    """
    A function that allows for the creation of custom Izhikevich neurons models, as well as a visualization of their behaviour on a 250 ms time window
    """
    params = IzhikevichParameters(a=a, b=b, c=c, d=d, tau_inv=tau_inv)
    behaviour = IzhikevichSpikingBehaviour(
        p=params,
        s=IzhikevichState(
            v=torch.tensor(float(v_rest), requires_grad=True),
            u=torch.tensor(u_rest) * params.b,
        ),
    )
    if print:
        p, s = behaviour
        T1 = 20
        vs = []
        us = []
        cs = []
        time = []

        for t in np.arange(0, time_print, timestep_print):
            vs.append(s.v.item())
            us.append(s.u.item())
            time.append(t*timestep_print)

            if t > T1:
                input_current = current * torch.ones(1)
            else:
                input_current = 0 * torch.ones(1)
            _, s = izhikevich_step(input_current, s, p)
            cs.append(input_current)
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_ylabel('Membrane potential (mV)')
        ax1.set_xlabel('Time (ms)')
        ax1.plot(time, vs)
        ax2 = fig.add_subplot(212)
        ax2.set_ylabel('Input current (pA)')
        ax2.set_xlabel('Time (ms)')
        ax2.plot(time, cs)
    return behaviour