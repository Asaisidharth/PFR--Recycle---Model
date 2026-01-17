from pfr_model.visualization.interactive_plots import slider_obj
from pfr_model.flowsheet.residuals import flowsheet_residual
from scipy.optimize import least_squares
from pfr_model.config.parameters import lb,ub,params,x0


def run_app(lb,ub,params,x0):

    T0 = 500.0
    P0 = 20e5

    res = least_squares(
        flowsheet_residual,
        x0,
        bounds = (lb,ub),
        args=(params,),
        verbose = 1
    )
    slider_obj(T0,P0,params,lb,ub,res)
if __name__ == "__main__":
    run_app(lb,ub,params,x0)



  