#!/usr/bin/env python3

import numpy as np
import pytest

def log_mean_temp_diff_counter(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    
    del_t_1 = temp_hot_in - temp_cold_out
    del_t_2 = temp_hot_out - temp_cold_in
    
    return (del_t_1 - del_t_2)/np.log(del_t_1/del_t_2)
    

def log_mean_temp_diff_parallel(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    
    del_t_1 = temp_hot_in - temp_cold_in
    del_t_2 = temp_hot_out - temp_cold_out
    
    return (del_t_1 - del_t_2)/np.log(del_t_1/del_t_2)

def q_lmtd_counter(U,area,temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    
    return U*area*log_mean_temp_diff_counter(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out)

def q_lmtd_parallel(U,area,temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    
    return U*area*log_mean_temp_diff_parallel(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out)

def c_min(mass_flow_rate_hot, spec_heat_hot, mass_flow_rate_cold, spec_heat_cold):
    
    c_hot = mass_flow_rate_hot*spec_heat_hot
    c_cold = mass_flow_rate_cold*spec_heat_cold
    
    return min(c_hot,c_cold)




#if __name__ == '__main__':