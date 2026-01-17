# Flowsheet of the whole system as a function 

#Importing Libraries

import numpy as np 
from pfr_model.reactor.pfr_solver import solve_pfr 
from pfr_model.separation.flash import flash_separator 
from pfr_model.config.parameters import P0
#The Flowsheet

def flowsheet_residual(x_fr,params):
    #x_fr = [F_A_rec, F_B_rec,F_A_v,F_B_v,F_A_PFR_in,F_B_PFR_in,F_A_out,F_B_out,T_out,F_A_l,F_B_l]
    #params = [b,F_in,T,k]
    #b = [] separation values 
    # F_in = F_A,F_B,F_i

    b = params["b"]
    F_in = params["F_in"]
    T_in = params["T_in"]
    k = params["k"]
    #Ea = params["Ea"]
    Ea = params.get("Ea",48000.0)


    F_A_rec = x_fr[0]
    F_B_rec = x_fr[1]
    F_A_v   = x_fr[2]
    F_B_v   = x_fr[3]
    F_A_PFR_in = x_fr[4]
    F_B_PFR_in =  x_fr[5]
    F_A_out = x_fr[6] 
    F_B_out = x_fr[7]
    T_out = x_fr[8]
    F_A_l = x_fr[9]
    F_B_l = x_fr[10]
    F_A = F_in[0]
    F_B = F_in[1]
    F_i = F_in[2]
    X_flash = [F_A_v,F_A_l,F_B_v,F_B_l]
    F_PFR_in = [F_A_PFR_in,F_B_PFR_in,F_i]

    # Recycle residual equations 

    R_rec_A = F_A_rec - b * F_A_v
    R_rec_B = F_B_rec - b * F_B_v

    # PFR inlet residuals

    R_mix_A = F_A_PFR_in - (F_A + F_A_rec)
    R_mix_B = F_B_PFR_in - (F_B + F_B_rec)

    F_PFR_in = [F_A_PFR_in, F_B_PFR_in, F_i]

    sol = solve_pfr(F_PFR_in, T_in, Ea,P0)
    F_A_pred, F_B_pred, T_pred,P_pred = sol.y[:, -1]
   
    R_PFR_A = F_A_out - F_A_pred
    R_PFR_B = F_B_out - F_B_pred
    R_PFR_T = (T_out- T_pred) / 100.0

    

    F_flash_in = [F_A_out,F_B_out,F_i]
    res3 = flash_separator(F_flash_in,X_flash,k)

    res2 = np.asarray([R_rec_A,R_rec_B,R_mix_A,R_mix_B,R_PFR_A,R_PFR_B,R_PFR_T])
    residual_final = np.concatenate((res2,res3))

    return residual_final / np.maximum(1.0,np.abs(x_fr))