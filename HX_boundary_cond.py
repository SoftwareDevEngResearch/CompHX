#!/usr/bin/env python3

import numpy as np


def set_temp_boundary_conditions():
    """ Set the Boundary Condition values to be used in other computations"""
    hot_temp_in = 300
    hot_temp_out = 250
    
    cold_temp_in = 200
    cold_temp_out = 220
    
    return hot_temp_in, hot_temp_out, cold_temp_in, cold_temp_out

def set_flow_boundary_conditions():
    """Defining the flow boundary conditions"""
    
    
    h_cold = 10
    area_cold = .001
    
    h_hot = 150
    area_hot = 2.75   
    
    return h_cold, area_cold, h_hot, area_hot

def fin_conditions(h,area):
    """Defining conditions for fin efficiency"""
    
    # Fins are designed on the hot side of the HX for this application
    
#    _,_,h_hot,area_hot = set_flow_boundary_conditions()
    
    num_fins = 25
    fin_thickness = .001
    fin_length = .008
    fin_width = 1
    
    fin_area = fin_length*fin_width
    
    wall_k = 200
    
    m = np.sqrt(h*(2*fin_thickness + 2*fin_width)/(wall_k*fin_thickness*fin_width))
    eta_f = np.tanh(m*(fin_length/2))/(m*fin_length/2)
    eta_not = 1-num_fins*fin_area*(1-eta_f)/area
    
    return eta_not
    
def main():
#    print(fin_conditions())
    pass
#    print(set_temp_boundary_conditions())

if __name__ == "__main__":
    main()
