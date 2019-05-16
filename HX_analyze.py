#!/usr/bin/env python3

import numpy as np
from . import HX_boundary_cond as bc
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
    
    c_hot = mass_flow_rate_hot*spec_heat_hot
    c_cold = mass_flow_rate_cold*spec_heat_cold
    
    if c_hot == 0 or c_cold == 0:
        raise ValueError("A non-zero c_min value should be specified")
    
    return min(c_hot,c_cold)

def q_max_ntu(c_min, temp_hot_in, temp_cold_in):
    return c_min*(temp_hot_in-temp_cold_in)

def epsilon_ntu(ntu, c_min, c_max, hx_type = 'parallel', passes = 2):
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
    return epsilon*c_min*(temp_hot_in-temp_cold_in)

def q_fin(temp_lmtd):
    
    h_cold,area_cold,h_hot,area_hot = bc.set_flow_boundary_conditions()
    
    eta_not_hot = bc.fin_conditions(h_hot,area_hot)
    eta_not_cold = bc.fin_conditions(h_cold,area_cold)
    
    ua_inverted = 1/(eta_not_cold*h_cold*area_cold) + 1/(eta_not_hot*h_hot*area_hot)
    q_fin = (1/ua_inverted)*temp_lmtd
    
    return q_fin

def main():
    pass

if __name__ == "__main__":
    main()
