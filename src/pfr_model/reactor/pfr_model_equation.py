# PFR Modelling equations that are fed to the solver 

# Importing Libraries 
from pfr_model.kinetics.arrhenius import rate_constant 
from pfr_model.config.parameters import params,A,deltaH,Ua,Mbar,f,Ta,D,Cp,R

def pfr_odes(z,y,F_I,Ea):
    
    F_A,F_B,T,P = y                 # Unpacking Constants 
    F_tot = F_A + F_B + F_I         # Flowrates in mol/s 
    
    
    v_dot = (F_tot*R*T)/P           # Volumetric flow (Ideal gas) (m3/s)
    C_A = F_A/v_dot                 # Concentration (mol/m3)


    r = rate_constant(T,Ea)*C_A
    R_rate = r*A                         # Reaction Rate per unit volume (mol/(s*m))


    dFa_dz = -R_rate                     # Change in molar flow of A per meter (mol/(s*m))
    dFb_dz = R_rate                      # Change in molar flow of B per meter (mol/(s*m))


    Q_gen = (-deltaH * R_rate)                        # Heat generated per meter (J/s*m)  (W/m)
    Q_remove = Ua*A*(Ta-T)                       # Heat Removed per meter (J/s*m)    (W/m)
    dT_dz = (Q_gen+Q_remove)/(F_tot*Cp)          # Change in Temperature per meter (K/m)
 
    dPdz = -f*Mbar*F_tot**2*R*T/(2*D*A**2*P)     # Pressure drop per meter of the reactor (bar/m)
    

    return [dFa_dz, dFb_dz, dT_dz, dPdz]
