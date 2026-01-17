# Flash column that separates the liquid product B and the vapour fraction of the reactant A to feed back to the PFR 

#Importing Libraries 
import numpy as np 

#The Flash separator column 
def flash_separator(F_in,x,k):
    #unpacking constants F_in,x 
    #F_in = [F_A,F_B,F_i]
    #x = [F_A_v,F_A_l,F_B_v,F_B_l]

    K_A,K_B = k
    F_A,F_B,F_i = F_in
    F_A_v,F_A_l,F_B_v,F_B_l = x
    

    #Mass balances
    b1 = F_A_v + F_A_l - F_A  
    b2 = F_B_v + F_B_l - F_B 
 
    #Safety-Check prevents divide by zero 
    denom_v = max(1e-5, F_A_v + F_B_v + F_i)
    denom_l = max(1e-5, F_A_l + F_B_l)

    #Thermodynamic balances 

    t1 = (F_A_v/ denom_v) - K_A * (F_A_l / denom_l) 
    t2 = (F_B_v/ denom_v)  - K_B * (F_B_l/ denom_l)

    res1 = np.asarray([b1,b2,t1,t2])

    return res1