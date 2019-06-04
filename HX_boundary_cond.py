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


def fin_conditions(h,area,name):
    """Defining conditions for fin efficiency"""
    
    inputs = read_bc(name)
    
    num_fins = inputs["num_fins"]
    fin_thickness = inputs["fin_thickness"]
    fin_length = inputs["fin_length"]
    fin_width = inputs["fin_width"]
    wall_k = inputs["wall_k"]
    
    fin_area = []
    m = []
    eta_f = []
    eta_not = []
        
    if isinstance(fin_length, list):
        for k in range(len(fin_length)):
            if isinstance(fin_width, list):
                for l in range(len(fin_width)):
                    fin_area.append(fin_length[k]*fin_width[l])
            else:
                fin_area.append(fin_length[k]*fin_width)
    else:
        if isinstance(fin_width, list):
            for l in range(len(fin_width)):
                fin_area.append(fin_length*fin_width[l])
        else:
            fin_area = fin_length*fin_width
            
            
            
    if isinstance(fin_thickness, list):
        for j in range(len(fin_thickness)):
            if isinstance(fin_width, list):
                for l in range(len(fin_width)):
                    m.append(np.sqrt(h*(2*fin_thickness[j] + 2*fin_width[l])/(wall_k*fin_thickness[j]*fin_width[l])))
            else:
                m.append(np.sqrt(h*(2*fin_thickness[j] + 2*fin_width)/(wall_k*fin_thickness[j]*fin_width)))
    else:
        if isinstance(fin_width, list):
            for l in range(len(fin_width)):
                m.append(np.sqrt(h*(2*fin_thickness + 2*fin_width[l])/(wall_k*fin_thickness*fin_width[l])))
        else:
            m = np.sqrt(h*(2*fin_thickness + 2*fin_width/(wall_k*fin_thickness*fin_width)))
            
    
    
    if isinstance(m,list):
        for i in range(len(m)):    
            if isinstance(fin_length, list):
                for k in range(len(fin_length)):
                    eta_f.append(np.tanh(m[i]*(fin_length[k]/2))/(m[i]*fin_length[k]/2))
            else:
                eta_f.append(np.tanh(m[i]*(fin_length/2))/(m[i]*fin_length/2))
    else:    
        if isinstance(fin_length, list):
            for k in range(len(fin_length)):
                eta_f.append(np.tanh(m*(fin_length[k]/2))/(m*fin_length[k]/2))
        else:
            eta_f = np.tanh(m*(fin_length/2))/(m*fin_length/2)
    
    
    
    if isinstance(fin_area, list):
        for i in range(len(fin_area)):
            if isinstance(num_fins, list):
                for j in range(len(num_fins)):
                    if isinstance(eta_f, list):
                        for k in range(len(eta_f)):
                            eta_not.append(1-num_fins[j]*fin_area[i]*(1-eta_f[k])/area)
                    else:
                        eta_not.append(1-num_fins[j]*fin_area[i]*(1-eta_f)/area)
            else:
                if isinstance(eta_f, list):
                    for k in range(len(eta_f)):
                        eta_not.append(1-num_fins*fin_area[i]*(1-eta_f[k])/area)
                else:
                    eta_not.append(1-num_fins*fin_area[i]*(1-eta_f)/area)
                
    else:
        if isinstance(num_fins, list):
            for j in range(len(num_fins)):
                if isinstance(eta_f, list):
                    for k in range(len(eta_f)):
                        eta_not.append(1-num_fins[j]*fin_area*(1-eta_f[k])/area)
                else:
                    eta_not.append(1-num_fins[j]*fin_area*(1-eta_f)/area)
        else:
            if isinstance(eta_f, list):
                for k in range(len(eta_f)):
                    eta_not.append(1-num_fins*fin_area*(1-eta_f[k])/area)
            else:
                eta_not = 1-num_fins*fin_area*(1-eta_f)/area
    
    return eta_not
    
def main():

    pass


if __name__ == "__main__":
    main()
