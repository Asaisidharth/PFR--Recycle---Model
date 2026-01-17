# Solver for the model 

# Importing Libraries 
import numpy as np 
from scipy.integrate import solve_ivp 
from pfr_model.config.parameters import L
from pfr_model.reactor.pfr_model_equation import pfr_odes 

#Solver for the PFR 
def solve_pfr(F_in,T_in,P0,Ea):
    
    F_I  = F_in[2] 
    T_in = max(T_in,200.0)          #Safety-Check to Ensure inputs are physical
    F_in = np.maximum(F_in, 0.0)
    y0   = [F_in[0],F_in[1],T_in,P0]

    sol = solve_ivp(
        pfr_odes,
        (0.0,L),
        y0,
        args=(F_I, Ea),
        method="BDF",
        rtol=1e-6,
        atol=1e-9
    )

    if not sol.success:
        raise RuntimeError("PFR Solver failed")
    return sol
