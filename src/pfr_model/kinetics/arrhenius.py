# Arrhenius equation of the reaction in the reactor 

#Importing Libraries 
import numpy as np 
from pfr_model.config.parameters import R,k0 

def rate_constant(T,Ea):   
    T_safe = np.maximum(T,100.0)                #Cliping  T to avoid division by zero if solver tries T = 0
    return k0 * np.exp(-Ea / (R*T_safe))        
