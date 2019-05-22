#!/usr/bin/env python3

import numpy as np
from . import HX_boundary_cond as bc
from sympy.solvers import solve
from sympy import Symbol
#import pytest

def log_mean_temp_diff_counter(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    """ Computes the LMTD for a counter-current HX """
    
    del_t_1 = temp_hot_in - temp_cold_out
    del_t_2 = temp_hot_out - temp_cold_in
    
    if del_t_1 == 0 or del_t_2 == 0:
        raise ValueError("Non-zero temperature difference required")
    if temp_hot_in < temp_hot_out or temp_cold_in > temp_cold_out:
        raise ValueError("Non-physical HX temperatures provided")
    
    return (del_t_1 - del_t_2)/np.log(del_t_1/del_t_2)  

def log_mean_temp_diff_parallel(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    """ Computes the LMTD for a parallel HX """
    
    del_t_1 = temp_hot_in - temp_cold_in
    del_t_2 = temp_hot_out - temp_cold_out
    
    if del_t_1 == 0 or del_t_2 == 0:
        raise ValueError("Non-zero temperature difference required")
    if temp_hot_in < temp_hot_out or temp_cold_in > temp_cold_out:
        raise ValueError("Non-physical HX temperatures provided")
    
    return (del_t_1 - del_t_2)/np.log(del_t_1/del_t_2)


def q_lmtd_counter(U,area,temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    """ Computes the heat rate for a counter-current HX """
    
    if min([U,area,temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out]) < 0:
        raise ValueError("Non-physical inputs have been provided for heat flux computation")
          
    return U*area*log_mean_temp_diff_counter(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out)

def q_lmtd_parallel(U,area,temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    """ Computes the heat rate LMTD for a parallel HX """
    
    if min([U,area,temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out]) < 0:
        raise ValueError("Non-physical inputs have been provided for heat flux computation")
    
    return U*area*log_mean_temp_diff_parallel(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out)

def c_min(mass_flow_rate_hot, spec_heat_hot, mass_flow_rate_cold, spec_heat_cold):
    """Computes the minimum C value for NTU calculations"""
    
    c_hot = mass_flow_rate_hot*spec_heat_hot
    c_cold = mass_flow_rate_cold*spec_heat_cold
    
    if c_hot == 0 or c_cold == 0:
        raise ValueError("A non-zero c_min value should be specified")
    
    return min(c_hot,c_cold)

def q_max_ntu(c_min, temp_hot_in, temp_cold_in):
    """Computes the maximum q value for the NTU method"""
    
    return c_min*(temp_hot_in-temp_cold_in)

def epsilon_ntu(ntu, c_min, c_max, hx_type = 'parallel', passes = 2):
    """Computes the effectiveness for different HX types for the NTU method. hx_type are parallel, counter, or shell. """
    
    c_r = c_min/c_max
    if hx_type == 'parallel':
        return (1-np.exp(-ntu*(1+c_r)))/(1+c_r)
    elif hx_type == 'counter':
        if c_r < 1:
            return (1-np.exp(-ntu*(1-c_r)))/(1-c_r*np.exp(-ntu*(1-c_r)))
        elif c_r == 1:
            return ntu/(1+ntu)
        else:
            raise ValueError("An invalid value of c_r was provided. Please provide a different value")
    elif hx_type == 'shell':
        return 2*(1+c_r+(1+c_r**2)**.5*((1+np.exp(-ntu*(1+c_r**2)**.5))/(1-np.exp(-ntu*(1+c_r**2)**.5))))**-1
            
def q_ntu(epsilon, c_min, temp_hot_in, temp_cold_in):
    """Computes the q value for the NTU method"""
    
    return epsilon*c_min*(temp_hot_in-temp_cold_in)

def q_fin(temp_lmtd):
    """Computes the q value for a finned HX using the LMTD method"""
    h_cold,area_cold,h_hot,area_hot = bc.set_flow_boundary_conditions()
    
    eta_not_hot = bc.fin_conditions(h_hot,area_hot)
    eta_not_cold = bc.fin_conditions(h_cold,area_cold)
    
    ua_inverted = 1/(eta_not_cold*h_cold*area_cold) + 1/(eta_not_hot*h_hot*area_hot)
    q_fin = (1/ua_inverted)*temp_lmtd
    
    return q_fin

def temp_ntu_solver(q, epsilon, c_min, temp_hot_in = 0, temp_cold_in = 0, temp_type = 'cold'):
    """Computes the temp for the NTU method. temp_type options are hot or cold. This are for the inlet to the HX"""
    
    if temp_type == 'cold':
        temp_cold_in = Symbol('temp_cold_in')
        return solve(epsilon*c_min*(temp_hot_in-temp_cold_in) - q, temp_cold_in)
    elif temp_type == 'hot':
        temp_hot_in = Symbol('temp_hot_in')
        return solve(epsilon*c_min*(temp_hot_in-temp_cold_in) - q, temp_hot_in)
    else:
        raise ValueError("An incorrect input for the temp_type has been provided. Please select cold or hot.")
    
def temp_lmtd_solver(q, U,area):
    """Computes the lmtd for a specified q value."""
    
    lmtd = Symbol('lmtd')
    return solve(U*area*lmtd - q,lmtd)

def temp_lmtd_solver_parallel(lmtd, temp_hot_in = 0 ,temp_hot_out = 0,temp_cold_in = 0,temp_cold_out = 0, temp_type = "hot_in"):
    """ Computes the temperature from a specified q value for a parallel HX using the LMTD method"""
    
    if temp_type == "hot_in" or temp_type == "cold_in":
        del_t_2 = temp_hot_out - temp_cold_out
        del_t_1 =  Symbol('del_t_1')
        delta_t = solve((del_t_1 - del_t_2)/np.log(del_t_1/del_t_2)-lmtd, del_t_1)
        if temp_type == "hot_in":
            return delta_t+ temp_cold_in
        else:
            return temp_hot_in - delta_t
        
    elif temp_type == "hot_out" or temp_type == "cold_out":
        del_t_1 = temp_hot_in - temp_cold_in
        del_t_2 =  Symbol('del_t_2')
        delta_t = solve((del_t_1 - del_t_2)/np.log(del_t_1/del_t_2)-lmtd, del_t_2)
        if temp_type == "hot_out":
            return delta_t+ temp_cold_out
        else:
            return temp_hot_out - delta_t
        
    else:
        raise ValueError("An incorrect input for the temp_type has been provided. Please select cold_in, cold_out, hot_in, or hot_out.")

def temp_lmtd_solver_counter(lmtd, temp_hot_in = 0 ,temp_hot_out = 0,temp_cold_in = 0,temp_cold_out = 0, temp_type = "hot_in"):
    """ Computes the temperature from a specified q value for a counter-flow HX using the LMTD method"""
    
    if temp_type == "hot_in" or temp_type == "cold_out":
        del_t_2 = temp_hot_out - temp_cold_in
        del_t_1 =  Symbol('del_t_1')
        delta_t = solve((del_t_1 - del_t_2)/np.log(del_t_1/del_t_2)-lmtd, del_t_1)
        if temp_type == "hot_in":
            return delta_t+ temp_cold_out
        else:
            return temp_hot_in - delta_t
        
    elif temp_type == "hot_out" or temp_type == "cold_in":
        del_t_1 = temp_hot_in - temp_cold_out
        del_t_2 =  Symbol('del_t_2')
        delta_t = solve((del_t_1 - del_t_2)/np.log(del_t_1/del_t_2)-lmtd, del_t_2)
        if temp_type == "hot_out":
            return delta_t+ temp_cold_in
        else:
            return temp_hot_out - delta_t
        
    else:
        raise ValueError("An incorrect input for the temp_type has been provided. Please select cold_in, cold_out, hot_in, or hot_out.")

def main():
    pass

if __name__ == "__main__":
    main()
