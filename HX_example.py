#!/usr/bin/env python3

#import numpy as np
#from . import HX_boundary_cond as bc
#import sympy as sp
#from sympy.solvers import solve
#from sympy import Symbol
#import scipy.special as sc
#import pytest

import HX_analyze as hx
import HX_boundary_cond as bc
import sys
import matplotlib.pyplot as plt

# This script works as an example of how to use the modules developed to solve a HX problem with provided boundary conditions

def main():
    
    name = sys.argv[1]
    
    
    hot_temp_in, hot_temp_out, cold_temp_in, cold_temp_out = bc.set_temp_boundary_conditions(name)
    
    h_cold, area_cold, h_hot, area_hot = bc.set_flow_boundary_conditions(name)
    
    eta_not_hot = bc.fin_conditions(h_hot,area_hot,name)
    print(eta_not_hot)
    
    eta_not_cold = bc.fin_conditions(h_cold,area_cold,name)
    print(eta_not_cold)
#    lmtd_parallel = hx.log_mean_temp_diff_parallel(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out)
#    lmtd_counter = hx.log_mean_temp_diff_counter(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out)
    
#    U =  hx.u_resistance(eta_not_cold, h_cold, area_cold, eta_not_hot, h_hot, area_hot)
    
    q_lmtd_counter = hx.q_fin(eta_not_hot, eta_not_cold, h_cold, area_cold, h_hot, area_hot, hx.log_mean_temp_diff_counter(hot_temp_in, hot_temp_out, cold_temp_in, cold_temp_out))
    q_lmtd_parallel = hx.q_fin(eta_not_hot, eta_not_cold, h_cold, area_cold, h_hot, area_hot, hx.log_mean_temp_diff_parallel(hot_temp_in, hot_temp_out, cold_temp_in, cold_temp_out))
#    q_lmtd_counter = hx.q_lmtd_counter(U,hot_temp_in, hot_temp_out, cold_temp_in, cold_temp_out)
#    q_lmtd_parallel = hx.q_lmtd_parallel(U,hot_temp_in, hot_temp_out, cold_temp_in, cold_temp_out)
#    
#    print(q_lmtd_counter, q_lmtd_parallel)
#    print(len(q_lmtd_counter), len(q_lmtd_parallel))
#    print(max(q_lmtd_counter))
#    print(max(q_lmtd_parallel))
    
    plt.plot(q_lmtd_counter)
    plt.plot(q_lmtd_counter)
#    plt.grid()
#    plt.title('Turbulent Kinetic Energy Spectrum for a Pipe')
#    plt.xlim(right=1000.)
#    plt.ylim(top=1.)
#    plt.xlabel('Frequency')
#    plt.ylabel('TKE')
    plt.legend()
    plt.savefig("test.png")
    plt.show()
    plt.close()
    
    

if __name__ == "__main__":
    main()