#!/usr/bin/env python3

import numpy as np
import sympy as sp
from sympy.solvers import solve
from sympy import Symbol
import yaml


def log_mean_temp_diff_counter(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    """ Computes the Log-Mean-Temperatuer Difference (LMTD) for a counter-current HX. 
     
    Args:
        temp_hot_in (int, float): Hot side inlet temeprature.
        temp_hot_out (int, float): Hot side outelet temeprature.
        temp_cold_in (int, float): Cold side inlet temeprature.
        temp_cold_out (int, float): Cold side outelet temeprature.
        
    Returns:
        int, float: The value of the LMTD 
        
    """
    
    del_t_1 = temp_hot_in - temp_cold_out
    del_t_2 = temp_hot_out - temp_cold_in
    
    if del_t_1 == 0 or del_t_2 == 0:
        raise ValueError("Non-zero temperature difference required")
    if temp_hot_in < temp_hot_out or temp_cold_in > temp_cold_out:
        raise ValueError("Non-physical HX temperatures provided")
    
    return (del_t_1 - del_t_2)/np.log(del_t_1/del_t_2)  

def log_mean_temp_diff_parallel(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    """ Computes the Log-Mean-Temperatuer Difference (LMTD) for a parallel HX 
    
    Args:
        temp_hot_in (int, float): Hot side inlet temeprature.
        temp_hot_out (int, float): Hot side outelet temeprature.
        temp_cold_in (int, float): Cold side inlet temeprature.
        temp_cold_out (int, float): Cold side outelet temeprature.
        
    Returns:
        int, float: The value of the LMTD 
        
    """
    
    del_t_1 = temp_hot_in - temp_cold_in
    del_t_2 = temp_hot_out - temp_cold_out
    
    if del_t_1 == 0 or del_t_2 == 0:
        raise ValueError("Non-zero temperature difference required")
    if temp_hot_in < temp_hot_out or temp_cold_in > temp_cold_out:
        raise ValueError("Non-physical HX temperatures provided")
    
    return (del_t_1 - del_t_2)/np.log(del_t_1/del_t_2)


def q_lmtd_counter(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out, name):
    """ Computes the heat rate for a counter-current Heat Exchanger (HX) 
    
    This value of q is computed when no tubes or fins are used. 
    
    Args:
        temp_hot_in (int, float): Hot side inlet temeprature.
        temp_hot_out (int, float): Hot side outelet temeprature.
        temp_cold_in (int, float): Cold side inlet temeprature.
        temp_cold_out (int, float): Cold side outelet temeprature.
        name (str): This is the name of the input file
        
    Returns:
        int, float: The value of the heat removed be the HX 
    """
    
    with open(name, 'r') as f:
        inputs = yaml.safe_load(f)
    
    h_cold = inputs["h_cold"]
    area_cold = inputs["area_cold"]
    
    h_hot = inputs["h_hot"]
    area_hot = inputs["area_hot"]
    
    wall_k = inputs["wall_k"]
    wall_thickness = inputs["wall_thickness"]
    
    ua_inverted = (1/(h_cold*area_cold) + (wall_thickness/(wall_k*area_hot)) + 1/(h_hot*area_hot))
    ua = 1/ua_inverted
    

    if min([ua,temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out]) < 0:
        raise ValueError("Non-physical inputs have been provided for heat flux computation")
    else:
        q_lmtd_counter = ua*log_mean_temp_diff_counter(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out)
        return q_lmtd_counter


def q_lmtd_parallel(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out, name):
    """ Computes the heat rate LMTD for a parallel Heat Exchanger (HX) 
    
        
    This value of q is computed when no tubes or fins are used. 
    
    Args:
        temp_hot_in (int, float): Hot side inlet temeprature.
        temp_hot_out (int, float): Hot side outelet temeprature.
        temp_cold_in (int, float): Cold side inlet temeprature.
        temp_cold_out (int, float): Cold side outelet temeprature.
        name (str): This is the name of the input file
        
    Returns:
        int, float: The value of the heat removed be the HX 
    """
    
    with open(name, 'r') as f:
        inputs = yaml.safe_load(f)
    
    h_cold = inputs["h_cold"]
    area_cold = inputs["area_cold"]
    
    h_hot = inputs["h_hot"]
    area_hot = inputs["area_hot"]
    
    wall_k = inputs["wall_k"]
    wall_thickness = inputs["wall_thickness"]
    
    ua_inverted = (1/(h_cold*area_cold) + (wall_thickness/(wall_k*area_hot)) + 1/(h_hot*area_hot))
    ua = 1/ua_inverted
    

    if min([ua,temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out]) < 0:
        raise ValueError("Non-physical inputs have been provided for heat flux computation")
    else:
        q_lmtd_counter = ua*log_mean_temp_diff_parallel(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out)
        return q_lmtd_counter
    
def c_min(mass_flow_rate_hot, spec_heat_hot, mass_flow_rate_cold, spec_heat_cold):
    """Computes the minimum C value for NTU calculations
    
    Args:
        mass_flow_rate_hot (int, float): Hot side mass flow rate.
        spec_heat_hot (int, float): Hot side fluid specific heat.
        mass_flow_rate_cold (int, float): Cold side mass_flow_rate_cold.
        spec_heat_cold (int, float): Cold side fluid specific heat.
        
    Returns:
        int, float: The value of the minimum c value 
    """
    
    c_hot = mass_flow_rate_hot*spec_heat_hot
    c_cold = mass_flow_rate_cold*spec_heat_cold
    
    if c_hot == 0 or c_cold == 0:
        raise ValueError("A non-zero c_min value should be specified")
    
    return min(c_hot,c_cold)

def c_max(mass_flow_rate_hot, spec_heat_hot, mass_flow_rate_cold, spec_heat_cold):
    """Computes the maximum C value for NTU calculations
    
    Args:
        mass_flow_rate_hot (int, float): Hot side mass flow rate.
        spec_heat_hot (int, float): Hot side fluid specific heat.
        mass_flow_rate_cold (int, float): Cold side mass_flow_rate_cold.
        spec_heat_cold (int, float): Cold side fluid specific heat.
        
    Returns:
        int, float: The value of the maximum c value 
    """
    
    c_hot = mass_flow_rate_hot*spec_heat_hot
    c_cold = mass_flow_rate_cold*spec_heat_cold
    
    if c_hot == 0 or c_cold == 0:
        raise ValueError("A non-zero c_min value should be specified")
    
    return max(c_hot,c_cold)

def q_max_ntu(c_min, temp_hot_in, temp_cold_in):
    """Computes the maximum q value for the NTU method

    Args:
        c_min (int, float): minimum C value for NTU calculations.
        temp_hot_in (int, float): Hot side inlet temeprature.
        temp_cold_in (int, float): Cold side inlet temeprature.
        
    Returns:
        int, float: The value of the maximum q value for the NTU method    
    """
    
    return c_min*(temp_hot_in-temp_cold_in)

def epsilon_ntu(ntu, c_min, c_max, hx_type = 'parallel'):
    """Computes the effectiveness for different HX types for the NTU method. hx_type are parallel, counter, or shell.
    
    Args:
        ntu (int, float): number of transfer units.
        c_min (int, float): minimum C value for NTU calculations.
        c_max (int, float): maximum C value for NTU calculations.
        hx_type (str): the type of HX being analyzed. Options are parallel, counter, and shell. Other values yield an error

    Returns:
        int, float: The value of the effectivness for the different HX types.
    """
    
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
    else:
        raise ValueError("An invalid HX type was given.")

def q_ntu(epsilon, c_min, temp_hot_in, temp_cold_in):
    """Computes the q value for the NTU method
    
    Args:
        epsilon (int, float): The value of the effectivness for the HX.
        c_min (int, float): minimum C value for NTU calculations.
        temp_hot_in (int, float): Hot side inlet temeprature.
        temp_cold_in (int, float): Cold side inlet temeprature.

    Returns:
        int, float: The value of the removal from the NTU method.
    """
    
    return epsilon*c_min*(temp_hot_in-temp_cold_in)

def q_fin(temp_lmtd,name):
    """Computes the q value for a finned HX using the LMTD method
    
    Args:
        temp_lmtd (int, float): The value of the log mean temperature difference.
        name (str): name of the input file.

    Returns:
        int, float: The value of the removal for a finned HX.
    """
    
#    inputs = bcs.read_bc(name)
    with open(name, 'r') as f:
        inputs = yaml.safe_load(f)
    
    h_cold = inputs["h_cold"]
    area_cold = inputs["area_cold"]
    
    h_hot = inputs["h_hot"]
    area_hot = inputs["area_hot"]
    
    num_fins = inputs["num_fins"]
    fin_thickness = inputs["fin_thickness"]
    fin_length = inputs["fin_length"]
    fin_width = inputs["fin_width"]
    wall_k = inputs["wall_k"]
    wall_thickness = inputs["wall_thickness"]
    
    ua_inverted = []
    ua = []
    eta_not_cold = []
    eta_not_hot = []
    

    variables = []
    q = []
    
    counter = 0    
    for i in range(len(num_fins)):
        for j in range(len(fin_length)):
            for k in range(len(fin_width)):
                for l in range(len(fin_thickness)):
                    eta_not_cold.append(1-(num_fins[i]*fin_length[j]*fin_width[k]*(1-np.tanh(np.sqrt(h_cold*(2*fin_thickness[l] + 2*fin_width[k])/(wall_k*fin_thickness[l]*fin_width[k]))*(fin_length[j]/2))/(np.sqrt(h_cold*(2*fin_thickness[l] + 2*fin_width[k])/(wall_k*fin_thickness[l]*fin_width[k]))*fin_length[j]/2)))/area_cold)
                    eta_not_hot.append(1-(num_fins[i]*fin_length[j]*fin_width[k]*(1-np.tanh(np.sqrt(h_hot*(2*fin_thickness[l] + 2*fin_width[k])/(wall_k*fin_thickness[l]*fin_width[k]))*(fin_length[j]/2))/(np.sqrt(h_hot*(2*fin_thickness[l] + 2*fin_width[k])/(wall_k*fin_thickness[l]*fin_width[k]))*fin_length[j]/2)))/area_hot)
                    ua_inverted.append(1/(eta_not_cold[counter]*h_cold*(area_cold+num_fins[i]*fin_length[j]*fin_width[k])) + (wall_thickness/(wall_k*area_hot)) + 1/(eta_not_hot[counter]*h_hot*(area_hot+num_fins[i]*fin_length[j]*fin_width[k])))
                    ua.append(1/ua_inverted[counter])
                    q.append(ua[counter]*temp_lmtd)
                    variables.append([num_fins[i], fin_length[j], fin_width[k], fin_thickness[k]])
                    counter += 1


    return q, variables

def q_tube(temp_lmtd,name):
    """Computes the q value for a tubed HX using the LMTD method
    
    Args:
        temp_lmtd (int, float): The value of the log mean temperature difference.
        name (str): name of the input file.

    Returns:
        int, float: The value of the removal for a tubular HX.
    """
    
#    inputs = bcs.read_bc(name)
    with open(name, 'r') as f:
        inputs = yaml.safe_load(f)
    
    h_cold = inputs["h_cold"]
    area_cold = inputs["area_cold"]
    
    h_hot = inputs["h_hot"]
    area_hot = inputs["area_hot"]
    
    num_tubes = inputs["num_tubes"]
    tube_thickness = inputs["tube_thickness"]
    tube_length = inputs["tube_length"]
    tube_diameter = inputs["tube_outer_diameter"]
    wall_k = inputs["wall_k"]
    
    ua_inverted = []
    ua = []
    

    variables = []
    q = []
    
    counter = 0    
    for i in range(len(num_tubes)):
        for j in range(len(tube_length)):
            for k in range(len(tube_diameter)):
                for l in range(len(tube_thickness)):
                    ua_inverted.append(1/(h_cold*(area_cold+num_tubes[i]*tube_length[j]*(tube_diameter[k]-2*tube_thickness[l])*np.pi)) + ((np.log(tube_diameter[k]/(tube_diameter[k]-2*tube_thickness[l]))/(2*np.pi*wall_k*tube_length[j]))) + 1/(h_hot*(area_hot+num_tubes[i]*tube_length[j]*tube_diameter[k]*np.pi)))
                    ua.append(1/ua_inverted[counter])
                    q.append(ua[counter]*temp_lmtd)
                    variables.append([num_tubes[i], tube_length[j], tube_diameter[k], tube_thickness[k]])
                    counter += 1


    return q, variables

def temp_ntu_solver(q, epsilon, c_min, temp_hot_in = 0, temp_cold_in = 0, temp_type = 'cold'):
    """Computes the temp for the NTU method. temp_type options are hot or cold. This are for the inlet to the HX
    
    Args:
        q (int, float): The value of the heat removal for the NTU method 
        epsilon (int, float): The value of the effectivness for the HX.
        c_min (int, float): minimum C value for NTU calculations.
        temp_hot_in (int, float): Hot side inlet temeprature.
        temp_cold_in (int, float): Cold side inlet temeprature.
        temp_type(str): What temperature is to be solved for. Options are hot or cold. 

    Returns:
        int, float: The value of the temperature.
    """
    
    if temp_type == 'cold':
        temp_cold_in = Symbol('temp_cold_in')
        return solve(epsilon*c_min*(temp_hot_in-temp_cold_in) - q, temp_cold_in)[0]
    elif temp_type == 'hot':
        temp_hot_in = Symbol('temp_hot_in')
        return solve(epsilon*c_min*(temp_hot_in-temp_cold_in) - q, temp_hot_in)[0]
    else:
        raise ValueError("An incorrect input for the temp_type has been provided. Please select cold or hot.")
    
def lmtd_solver(q, U,area):
    """Computes the lmtd for a specified q value.
    
    Args:
        q (int, float): The value of the heat removal for the NTU method 
        U (int, float): The value of the resistance of the HX
        area (int, float): The surface area of the HX.

    Returns:
        int, float: The value of the LMTD.
    """
    
    lmtd = Symbol('lmtd')
    return solve(U*area*lmtd - q,lmtd)[0]

def temp_lmtd_solver_parallel(lmtd, temp_hot_in = 0 ,temp_hot_out = 0,temp_cold_in = 0,temp_cold_out = 0, temp_type = "hot_in"):
    """ Computes the temperature from a specified q value for a parallel HX using the LMTD method
    
    For the temperature of the unknown variable, input 0. 
    
    Args:
        lmtd (int, float): The value of the LMTD 
        temp_hot_in (int, float): Hot side inlet temeprature.
        temp_hot_out (int, float): Hot side outelet temeprature.
        temp_cold_in (int, float): Cold side inlet temeprature.
        temp_cold_out (int, float): Cold side outelet temeprature.
        temp_type(str): What temperature is to be solved for. Options are hot_in, hot_out, cold_in, or cold_out. 

    Returns:
        int, float: The value of the temperature.
    """
    
    if temp_type == "hot_in" or temp_type == "cold_in":
        del_t_2 = temp_hot_out - temp_cold_out
        del_t_1 =  Symbol('del_t_1')
        delta_t = float(solve((del_t_1 - del_t_2)/sp.log(del_t_1/del_t_2)-lmtd, del_t_1)[0])
        if temp_type == "hot_in":
            return delta_t + temp_cold_in
        else:
            return temp_hot_in - delta_t
        
    elif temp_type == "hot_out" or temp_type == "cold_out":
        del_t_1 = temp_hot_in - temp_cold_in
        del_t_2 =  Symbol('del_t_2')
        delta_t = float(solve((del_t_1 - del_t_2)/sp.log(del_t_1/del_t_2)-lmtd, del_t_2)[0])
        if temp_type == "hot_out":
            return delta_t + temp_cold_out
        else:
            return temp_hot_out - delta_t
        
    else:
        raise ValueError("An incorrect input for the temp_type has been provided. Please select cold_in, cold_out, hot_in, or hot_out.")

def temp_lmtd_solver_counter(lmtd, temp_hot_in = 0 ,temp_hot_out = 0,temp_cold_in = 0,temp_cold_out = 0, temp_type = "hot_in"):
    """ Computes the temperature from a specified q value for a counter-flow HX using the LMTD method
    
    For the temperature of the unknown variable, input 0. 
    
    Args:
        lmtd (int, float): The value of the LMTD 
        temp_hot_in (int, float): Hot side inlet temeprature.
        temp_hot_out (int, float): Hot side outelet temeprature.
        temp_cold_in (int, float): Cold side inlet temeprature.
        temp_cold_out (int, float): Cold side outelet temeprature.
        temp_type(str): What temperature is to be solved for. Options are hot_in, hot_out, cold_in, or cold_out. 

    Returns:
        int, float: The value of the temperature.
    """
    
    if temp_type == "hot_in" or temp_type == "cold_out":
        del_t_2 = temp_hot_out - temp_cold_in
        del_t_1 =  Symbol('del_t_1')
        delta_t = float(solve((del_t_1 - del_t_2)/sp.log(del_t_1/del_t_2)-lmtd, del_t_1)[0])
        if temp_type == "hot_in":
            return delta_t + temp_cold_out
        else:
            return temp_hot_in - delta_t
        
    elif temp_type == "hot_out" or temp_type == "cold_in":
        del_t_1 = temp_hot_in - temp_cold_out
        del_t_2 =  Symbol('del_t_2')
        delta_t = float(solve((del_t_1 - del_t_2)/sp.log(del_t_1/del_t_2)-lmtd, del_t_2)[0])
        if temp_type == "hot_out":
            return delta_t + temp_cold_in
        else:
            return temp_hot_out - delta_t
        
    else:
        raise ValueError("An incorrect input for the temp_type has been provided. Please select cold_in, cold_out, hot_in, or hot_out.")

def main():
    pass

if __name__ == "__main__":
    main()
