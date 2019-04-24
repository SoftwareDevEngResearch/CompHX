#!/usr/bin/env python3

import numpy as np
import pytest

def log_mean_temp_diff_counter(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    
    del_t_1 = temp_hot_in - temp_cold_out
    del_t_2 = temp_hot_out - temp_cold_in
    
    if del_t_1 == 0 or del_t_2 == 0:
        raise ValueError("Non-zero temperature difference required")
    if temp_hot_in < temp_hot_out or temp_cold_in > temp_cold_out:
        raise ValueError("Non-physical HX temperatures provided")
    
    return (del_t_1 - del_t_2)/np.log(del_t_1/del_t_2)
    

def log_mean_temp_diff_parallel(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    
    del_t_1 = temp_hot_in - temp_cold_in
    del_t_2 = temp_hot_out - temp_cold_out
    
    if del_t_1 == 0 or del_t_2 == 0:
        raise ValueError("Non-zero temperature difference required")
    if temp_hot_in < temp_hot_out or temp_cold_in > temp_cold_out:
        raise ValueError("Non-physical HX temperatures provided")
    
    return (del_t_1 - del_t_2)/np.log(del_t_1/del_t_2)

def test_lmtd_counter():
    assert log_mean_temp_diff_counter(100,85,30,55) == pytest.approx(49.83,.005)

def test_lmtd_counter2():
    with pytest.raises(ValueError):
        log_mean_temp_diff_counter(10,10,10,10)

def test_lmtd_counter3():
    with pytest.raises(ValueError):
        log_mean_temp_diff_counter(10,100,10,100)
        
def test_lmtd_counter4():
    with pytest.raises(ValueError):
        log_mean_temp_diff_counter(10,100,100,10)
            
def test_lmtd_parallel():
    assert log_mean_temp_diff_parallel(100,85,30,55) == pytest.approx(47.21,.005)

def test_lmtd_parallel2():
    with pytest.raises(ValueError):
        log_mean_temp_diff_parallel(10,10,10,10)
        
def test_lmtd_parallel3():
    with pytest.raises(ValueError):
        log_mean_temp_diff_parallel(10,100,100,10)
        
def test_lmtd_parallel4():
    with pytest.raises(ValueError):
        log_mean_temp_diff_parallel(100,10,100,10)

def q_lmtd_counter(U,area,temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    
    if min([U,area,temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out]) < 0:
        raise ValueError("Non-physical inputs have been provided for heat flux computation")
          
    return U*area*log_mean_temp_diff_counter(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out)

def q_lmtd_parallel(U,area,temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out):
    
    if min([U,area,temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out]) < 0:
        raise ValueError("Non-physical inputs have been provided for heat flux computation")
    
    return U*area*log_mean_temp_diff_parallel(temp_hot_in,temp_hot_out,temp_cold_in,temp_cold_out)

def test_q_lmtd_counter():
    assert q_lmtd_counter(1,1,100,85,30,55) == pytest.approx(49.83,.005)
    
def test_q_lmtd_counter2():
    with pytest.raises(ValueError):
        q_lmtd_counter(-11,1,100,-85,30,-55)
    
def test_q_lmtd_parallel():
    assert q_lmtd_parallel(1,1,100,85,30,55) == pytest.approx(47.21,.005)
    
def test_q_lmtd_parralel2():
    with pytest.raises(ValueError):
        q_lmtd_parallel(-11,1,100,-85,30,-55)

def c_min(mass_flow_rate_hot, spec_heat_hot, mass_flow_rate_cold, spec_heat_cold):
    
    c_hot = mass_flow_rate_hot*spec_heat_hot
    c_cold = mass_flow_rate_cold*spec_heat_cold
    
    if c_hot == 0 or c_cold == 0:
        raise ValueError("A non-zero c_min value should be specified")
    
    return min(c_hot,c_cold)

def test_c_min_cold():
    assert c_min(10,10,1,1) == 1
    
def test_c_min_hot():
    assert c_min(1,1,10,10) == 1
    
def test_c_min_equal():
    assert c_min(2,2,2,2) == 4
    
def test_c_min_zero():
    with pytest.raises(ValueError):
        c_min(0,1,0,2)




#if __name__ == '__main__':