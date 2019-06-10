#!/usr/bin/env python3

#import numpy as np
import pytest
from . import HX_analyze as hx
#import HX_boundary_cond

def test_lmtd_counter():
    """Tests the LMTD for counter flow heat exchangers"""
    assert hx.log_mean_temp_diff_counter(100,85,30,55) == pytest.approx(49.83,.005)

def test_lmtd_counter2():
    """Tests the input parameters for the LMTD of counter flow heat exchangers"""
    with pytest.raises(ValueError):
        hx.log_mean_temp_diff_counter(10,10,10,10)

def test_lmtd_counter3():
    """Tests the input parameters for the LMTD of counter flow heat exchangers"""
    with pytest.raises(ValueError):
        hx.log_mean_temp_diff_counter(10,100,10,100)
        
def test_lmtd_counter4():
    """Tests the input parameters for the LMTD of counter flow heat exchangers"""
    with pytest.raises(ValueError):
        hx.log_mean_temp_diff_counter(10,100,100,10)
            
def test_lmtd_parallel():
    """Tests the LMTD for parallel flow heat exchangers"""
    assert hx.log_mean_temp_diff_parallel(100,85,30,55) == pytest.approx(47.21,.005)

def test_lmtd_parallel2():
    """Tests the input parameters for the LMTD of parallel flow heat exchangers"""
    with pytest.raises(ValueError):
        hx.log_mean_temp_diff_parallel(10,10,10,10)
        
def test_lmtd_parallel3():
    """Tests the input parameters for the LMTD of parallel flow heat exchangers"""
    with pytest.raises(ValueError):
        hx.log_mean_temp_diff_parallel(10,100,100,10)
        
def test_lmtd_parallel4():
    """Tests the input parameters for the LMTD of parallel flow heat exchangers"""
    with pytest.raises(ValueError):
        hx.log_mean_temp_diff_parallel(100,10,100,10)

def test_q_lmtd_counter():
    """Tests the LMTD q value for counter flow heat exchangers"""
    name = "input_lmtd.yaml"
    assert hx.q_lmtd_counter(100,85,30,55,name) == pytest.approx(49.83,.005)
    
def test_q_lmtd_counter2():
    """Tests the input parameters for the q value of the LMTD of counter flow heat exchangers"""
    name = "input_lmtd.yaml"
    with pytest.raises(ValueError):
        hx.q_lmtd_counter(100,-85,30,-55,name)
    
def test_q_lmtd_parallel():
    """Tests the LMTD q value for parallel flow heat exchangers"""
    name = "input_lmtd.yaml"
    assert hx.q_lmtd_parallel(100,85,30,55,name) == pytest.approx(47.21,.005)
    
def test_q_lmtd_parralel2():
    """Tests the input parameters for the q value of the LMTD of parallel flow heat exchangers"""
    name = "input_lmtd.yaml"
    with pytest.raises(ValueError):
        hx.q_lmtd_parallel(100,-85,30,-55,name)

def test_c_min_cold():
    """Tests the minimum c value computation for the cold side"""
    assert hx.c_min(10,10,1,1) == 1
    
def test_c_min_hot():
    """Tests the minimum c value computation for the hot side"""
    assert hx.c_min(1,1,10,10) == 1
    
def test_c_min_equal():
    """Tests the minimum c value computation when the c values are equal"""
    assert hx.c_min(2,2,2,2) == 4
    
def test_c_min_zero():
    """Tests the minimum c value computation when the c values are zero"""
    with pytest.raises(ValueError):
        hx.c_min(0,1,0,2)
        
def test_c_max_hot():
    """Tests the maximum c value computation for the hot side"""
    assert hx.c_max(1,1,10,10) == 100
    
def test_c_max_zero():
    """Tests the maximum c value computation for the hot side when the value is zero"""
    with pytest.raises(ValueError):
        hx.c_max(0,1,0,2)
        
def test_q_fin_single():
    """Tests the q value for a finned heat exchanger for a single value for all input parameters"""
    name = "input_single.yaml"
    
    test, _ = hx.q_fin(hx.log_mean_temp_diff_parallel(300,250,200,220),name)
    assert test == [103.96772491081622]
    
def test_q_max_ntu():
    """Tests the maximum q value for the NTU method"""
    assert hx.q_max_ntu(.1, 100, 10) == 9
    
def test_epsilon_ntu_parallel():
    """Tests the effectiveness value for the NTU method for a parallel HX"""
    assert hx.epsilon_ntu(10, .01, 1, 'parallel') == pytest.approx(0.99,.009)
    
def test_epsilon_ntu_counter():
    """Tests the effectiveness value for the NTU method for a counter HX"""
    assert hx.epsilon_ntu(10, .01, 1, 'counter') == pytest.approx(0.99995,.00005)
    
def test_epsilon_ntu_shell():
    """Tests the effectiveness value for the NTU method for a shell and tube HX"""
    assert hx.epsilon_ntu(10, .01, 1, 'counter') == pytest.approx(0.99495,.009)

def test_epsilon_ntu_counter_cr1():
    """Tests the effectiveness value for the NTU method for a counter HX"""
    assert hx.epsilon_ntu(10, 1, 1, 'counter') == pytest.approx(0.909,.01)    
    
def test_q_ntu():
    """Tests the q value for the NTU method"""
    assert hx.q_ntu(10, 1, 100, 10) == 900
    
def test_temp_ntu_solver1():
    """Tests the temperature solver value for the NTU method for the cold side"""
    assert hx.temp_ntu_solver(900, 10, 1, 100, 0, 'cold') == pytest.approx(10,.1)
    
def test_temp_ntu_solver2():
    """Tests the temperature solver value for the NTU method for the hot side"""
    assert hx.temp_ntu_solver(900, 10, 1, 0, 10, 'hot') == pytest.approx(100,.1)
    
def test_temp_ntu_solver3():
    """Tests the temperature solver value for the NTU method for incorrect input"""
    with pytest.raises(ValueError):
        hx.temp_ntu_solver(900, 10, 1, 0, 10, 'hout')
        
def test_lmtd_solver():
    """Tests the lmtd solver"""
    assert hx.lmtd_solver(100, 1, 1) == 100

def test_temp_lmtd_solver_parallel1():
    """Tests the temperature lmtd solver for parallel flow for the hot side inlet"""
    assert hx.temp_lmtd_solver_parallel(10, 0, 100, 10, 60, temp_type = "hot_in") == pytest.approx(211, 1)
    
def test_temp_lmtd_solver_parallel2():
    """Tests the temperature lmtd solver for parallel flow for the cold side inlet"""
    assert hx.temp_lmtd_solver_parallel(100, 211.879, 100, 10, 60, temp_type = "cold_in") == pytest.approx(10, 1)
    
def test_temp_lmtd_solver_parallel3():
    """Tests the temperature lmtd solver for parallel flow for the hot side outlet"""
    assert hx.temp_lmtd_solver_parallel(100, 210, 0, 10, 60, temp_type = "hot_out") == pytest.approx(72, 1)
    
def test_temp_lmtd_solver_parallel4():
    """Tests the temperature lmtd solver for parallel flow for the cold side outlet"""
    assert hx.temp_lmtd_solver_parallel(100, 210, 100, 10, 60, temp_type = "cold_out") == pytest.approx(100, 1)
    
def test_temp_lmtd_solver_parallel5():
    """Tests the temperature lmtd solver for parallel flow for incorrect input"""
    with pytest.raises(ValueError):
        hx.temp_lmtd_solver_parallel(100, 211.879, 100, 10, 60, temp_type = "cold12_out")
        
def test_temp_lmtd_solver_counter1():
    """Tests the temperature lmtd solver for counter flow for the hot side inlet"""
    assert hx.temp_lmtd_solver_counter(100, 0, 100, 10, 60, temp_type = "hot_in") == pytest.approx(170, 1)
    
def test_temp_lmtd_solver_counter2():
    """Tests the temperature lmtd solver for counter flow for the cold side inlet"""
    assert hx.temp_lmtd_solver_counter(100, 210, 100, 10, 60, temp_type = "cold_in") == pytest.approx(38, 1)
    
def test_temp_lmtd_solver_counter3():
    """Tests the temperature lmtd solver for counter flow for the hot side outlet"""
    assert hx.temp_lmtd_solver_counter(100, 210, 0, 10, 60, temp_type = "hot_out") == pytest.approx(72, 1)
    
def test_temp_lmtd_solver_counter4():
    """Tests the temperature lmtd solver for counter flow for the cold side outlet"""
    assert hx.temp_lmtd_solver_counter(100, 210, 100, 10, 60, temp_type = "cold_out") == pytest.approx(170, 1)
    
def test_temp_lmtd_solver_counter5():
    """Tests the temperature lmtd solver for counter flow for incorrect input"""
    with pytest.raises(ValueError):
        hx.temp_lmtd_solver_counter(100, 211.879, 100, 10, 60, temp_type = "cold12_out")
        
    
def test_fin_conditions_parallel():
    """Tests the q value for a finned, parallel heat exchanger for multiple values pf input parameters"""
    name = "input_test.yaml"
    
    test, _ = hx.q_fin(hx.log_mean_temp_diff_parallel(300,250,200,220),name)
    
    assert test == pytest.approx((103.96772491081622,103.96772491081622,103.96772491081622,103.96772491081622,
                            103.96772491081622,103.96772491081622,103.96772491081622,103.96772491081622))

def test_fin_conditions_counter():
    """Tests the q value for a finned, counter heat exchanger for multiple values pf input parameters"""
    name = "input_test.yaml"
    
    test, _ = hx.q_fin(hx.log_mean_temp_diff_counter(300,250,200,220),name)
    
    assert test == pytest.approx((114.13982986,114.13982986,114.13982986,114.13982986,
                            114.13982986,114.13982986,114.13982986,114.13982986))