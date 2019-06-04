#!/usr/bin/env python3

import numpy as np
import yaml

def read_bc(name):

    with open(name, 'r') as f:
        inputs = yaml.safe_load(f)
    return inputs


def set_temp_boundary_conditions(name):
    """ Set the Boundary Condition values to be used in other computations"""
    
    inputs = read_bc(name)
    
    hot_temp_in = inputs["hot_temp_in"]
    hot_temp_out = inputs["hot_temp_out"]
    
    cold_temp_in = inputs["cold_temp_in"]
    cold_temp_out = inputs["cold_temp_out"]
    
    return hot_temp_in, hot_temp_out, cold_temp_in, cold_temp_out

def set_flow_boundary_conditions(name):
    """Defining the flow boundary conditions"""
    
    inputs = read_bc(name)
    
    h_cold = inputs["h_cold"]
    area_cold = inputs["area_cold"]
    
    h_hot = inputs["h_hot"]
    area_hot = inputs["area_hot"]
    
    return h_cold, area_cold, h_hot, area_hot
    
def main():

    pass


if __name__ == "__main__":
    main()
