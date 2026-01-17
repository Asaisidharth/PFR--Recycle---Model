#Import Libraries
import numpy as np 
from scipy.optimize import least_squares
from scipy.integrate import solve_ivp
from pfr_model.reactor.pfr_model_equation import pfr_odes
from pfr_model.flowsheet.residuals import flowsheet_residual
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider
import time 

#Create the slider object

def slider_obj(T0,P0,params,lb,ub,res):

    def init_state(res,params):
        return {
            "current_sol": res.x.copy(),
            "last_update_time": 0.0,
            "Ea": params["Ea"]
        }
    
    # Interactive Plots
    def solve_pfr_from_states(state,T_in,P0):  
        F_PFR_in =  [
                    state["current_sol"][4],
                     state["current_sol"][5],
                     1.0
                     ]
        current_Ea = state.get("Ea",48000.0)
        return    solve_ivp(
            pfr_odes,
            (0.0,2.5),
            [F_PFR_in[0], F_PFR_in[1], T0, P0],
            args=(1.0, current_Ea),
            method = "BDF"
        )
        
    def build_plots(sol):
        z = sol.t
        F_A, F_B, T, P = sol.y 


        # Add slider 
        #Define axis for slider: [left, bottom, width, height]
        fig= plt.figure(figsize=(12,8))
        gs = fig.add_gridspec(2,3, height_ratios=[3,1.2])
        plt.subplots_adjust(bottom=0.25)

        # Plotting Inital Lines (saving them as variables l1, l2, l3, so it gets updated later)
        ax1 = fig.add_subplot(gs[0,0])
        l1, = ax1.plot(z,F_A,'b-',linewidth=2,label='F_A')
        l2, = ax1.plot(z,F_B,'g-',linewidth=2,label='F_B')
        ax1.set_xlabel("Reactor Length (m)")
        ax1.set_ylabel("Molar flow (mol/s)")
        ax1.set_ylim(0, 1.5)
        ax1.set_xlim(0,2.5)
        ax1.grid(True,alpha=0.3)
        ax1.legend(loc = 'center right')

        ax2 = ax1.twinx()
        l3, = ax2.plot(z,T,'r--',linewidth=2, label = 'Temperature')
        ax2.set_ylabel('Temperature (k)')
        ax2.set_ylim(450,800)
        ax2.legend(loc='upper right')

        ax3 = fig.add_subplot(gs[0,2])
        l4, = ax3.plot(F_A,T,'k-',linewidth=2)
        ax3.set_xlabel("Molar flow (mol/s)")
        ax3.set_ylabel("Temperature (K)")
        ax3.set_title("Reaction Trajectory")
        ax3.grid(True,alpha=0.3)
        ax3.invert_xaxis()

        ax_text = fig.add_subplot(gs[1,:])
        ax_text.axis('off')

        kpi_text = ax_text.text(0.01,0.25, "", fontsize=12,
                                bbox = dict(boxstyle="round",facecolor = "wheat",alpha=0.5))
        return fig, (l1,l2,l3,l4), kpi_text
    
    def build_sliders(T0,Ea0):
        ax_temp = plt.axes([0.25, 0.1, 0.65, 0.03])
        ax_Ea = plt.axes([0.25,0.05,0.65,0.03])
        s_temp = Slider(
            ax_temp, 
            'Inlet Temp (K)', 
            400.0, 
            700.0, 
            valinit=T0
            )
        s_Ea = Slider(
            ax=ax_Ea,
            label='Activation Energy (Ea)',
            valmin=10000.0,
            valmax=70000.0,
            valinit=Ea0,
            valstep=100.0
        )
        return s_temp,s_Ea

    

    # The update function to make the calculation based on the slider position 

    def update(state, params, lb, ub, T0, P0, s_temp, s_Ea, lines, kpi_text, fig):
        
        update_delay = 0.1
        current_time = time.time()

        if current_time - state["last_update_time"] < update_delay:
            return
        
        #Read slider position 
        new_T = s_temp.val
        state["Ea"] = s_Ea.val
        params["T_in"] = new_T
        params["Ea"] = state["Ea"]

        guess = state["current_sol"].copy() # Biased Guess to keep the slider smooth 

        guess[8] = max(guess[8],600.0) # Forcing the hot solution first to keep the reactor ignited 
    
        try:
            new_res = least_squares(
                flowsheet_residual,
                state["current_sol"],
                bounds=(lb,ub),
                args=(params,),
                xtol=1e-4, 
                ftol=1e-4,
                verbose = 0
            )

            state["current_sol"] = new_res.x

            sol = solve_pfr_from_states(state,params["T_in"],P0)

            l1, l2, l3, l4 = lines
            l1.set_ydata(sol.y[0])
            l1.set_xdata(sol.t)

            l2.set_ydata(sol.y[1])
            l2.set_xdata(sol.t)

            l3.set_ydata(sol.y[2])
            l3.set_xdata(sol.t)

            l4.set_data(sol.y[0],sol.y[2])

            T_max = np.max(sol.y[2])
            F_A_inlet_total = sol.y[0][0]
            F_A_outlet = sol.y[0][-1]
            X_pass = (F_A_inlet_total-F_A_outlet)/F_A_inlet_total
            F_A_l_res = state["current_sol"][9]
            F_B_l_res = state["current_sol"][10]
            purity_B = F_B_l_res/(F_A_l_res + F_B_l_res + 1e-9)

            status_str = (
                f"Process Performance:\n"
                f"Per Pass Conversion : {X_pass*100:.2f}%\n"
                f"Reactor Hotspot: {T_max:.1f} K\n"
                f"Production B purity (Liquid):{purity_B*100:.1f}%\n"
                f"Liquid Production Rate:{F_B_l_res:.2f} mol/s"
                )
            kpi_text.set_text(status_str)
            
            fig.canvas.draw_idle()
            state["last_update_time"] = current_time

        except Exception as e:
            print(f"Solver failed at Ea={state['Ea']}")

    state = init_state(res,params)
    sol0 = solve_pfr_from_states(state,T0,P0)

    fig,lines,kpi_text = build_plots(sol0)
    s_temp,s_Ea        = build_sliders(T0,state["Ea"])

    if res.cost < 1e-4:
        print("Converged!")

    s_temp.on_changed(
        lambda v: update(state, params, lb, ub, T0, P0,
                         s_temp, s_Ea, lines, kpi_text, fig)
    )

    s_Ea.on_changed(
        lambda v: update(state, params, lb, ub, T0, P0,
                         s_temp, s_Ea, lines, kpi_text, fig)
    )

    plt.show()
    