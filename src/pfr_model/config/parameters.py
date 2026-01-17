# Parameter storage script - Stores all the constants and Assumed values 

#Importing Libraries 

import numpy as np 

# Intial guess of the unkown vectors 

F_A0 = 1.0 # mol/s
F_B0 = 0.0 # mol/s 
F_i = 1.0  # mol/s
F_in = np.array([F_A0,F_B0,F_i])
T0 = 500 # k
P0 = 20e5 # 20 bar  
b = 0.3
k = np.array([0.1,0.2])
params = {
    "F_in" : F_in,
    "T_in" : T0,
    "b" : 0.3,
    "k" : k,
    "Ea" :48000.0 
}
Ea = 48000.0
x0 = np.array([
    0.05, 0.1,             # F_A_rec, F_B_rec (Guessing Recycle exists)
    0.3, 0.1,              # F_A_v, F_B_v (Vapor flow guess)
    1.1, 0.1,              # F_A_PFR_in, F_B_PFR_in (Inlet guess)
    0.2, 0.8,              # F_A_out, F_B_out (LOW A and HIGH B)
    600.0,                 # T_out (HOT to trigger ignition)
    0.1, 0.3               # F_A_l, F_B_l (Liquid flow guess)
])

lb = np.zeros(11) +1e-8    # Small epsilon > 0
ub = np.inf

#Gas constant and Kinetics 
R  = 8.314     # Universal gas constant (J/mol*K)
k0 = 5.0e3     # pre-exponential factor (1/s)


#Reactor Geometry 
L  = 2.5       # Lenght of the reactor in meters (m)
D  = 0.10      # Diameter of the reactor in meters (m)
A  = np.pi * D**2 / 4   # Area of the reactor (m2)

#Thermodynamic assumed constants 
Cp      = 100.0 
deltaH  = -80000.0

#Heat transfer constants
Ua      = 3000.0    # Overall Heat transfer coefficient (W/m2*K)
Ta      = 305.0     # Ambient Temperature in kelvin (K) 


#Pressure drop constants 
f       = 0.005     # Friction factor assumed 
Mbar    = 0.030     # Average molar mass (Kg/mol)

#Defaut Temperature and Pressure conditiosn 
P0      = 20e5      # Pressure in bar (bar)
T0      = 500.0     # Temperature in Kelvin (K)

