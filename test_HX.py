#!/usr/bin/env python3

#import numpy as np
import pytest
from . import HX_analyze as hx

def test_lmtd_counter():
    assert hx.log_mean_temp_diff_counter(100,85,30,55) == pytest.approx(49.83,.005)

def test_lmtd_counter2():
    with pytest.raises(ValueError):
        hx.log_mean_temp_diff_counter(10,10,10,10)

def test_lmtd_counter3():
    with pytest.raises(ValueError):
        hx.log_mean_temp_diff_counter(10,100,10,100)
        
def test_lmtd_counter4():
    with pytest.raises(ValueError):
        hx.log_mean_temp_diff_counter(10,100,100,10)
            
def test_lmtd_parallel():
    assert hx.log_mean_temp_diff_parallel(100,85,30,55) == pytest.approx(47.21,.005)

def test_lmtd_parallel2():
    with pytest.raises(ValueError):
        hx.log_mean_temp_diff_parallel(10,10,10,10)
        
def test_lmtd_parallel3():
    with pytest.raises(ValueError):
        hx.log_mean_temp_diff_parallel(10,100,100,10)
        
def test_lmtd_parallel4():
    with pytest.raises(ValueError):
        hx.log_mean_temp_diff_parallel(100,10,100,10)

def test_q_lmtd_counter():
    assert hx.q_lmtd_counter(1,1,100,85,30,55) == pytest.approx(49.83,.005)
    
def test_q_lmtd_counter2():
    with pytest.raises(ValueError):
        hx.q_lmtd_counter(-11,1,100,-85,30,-55)
    
def test_q_lmtd_parallel():
    assert hx.q_lmtd_parallel(1,1,100,85,30,55) == pytest.approx(47.21,.005)
    
def test_q_lmtd_parralel2():
    with pytest.raises(ValueError):
        hx.q_lmtd_parallel(-11,1,100,-85,30,-55)

def test_c_min_cold():
    assert hx.c_min(10,10,1,1) == 1
    
def test_c_min_hot():
    assert hx.c_min(1,1,10,10) == 1
    
def test_c_min_equal():
    assert hx.c_min(2,2,2,2) == 4
    
def test_c_min_zero():
    with pytest.raises(ValueError):
        hx.c_min(0,1,0,2)
        
def test_q_fin():
    assert hx.q_fin(2,2,1,1,1,1,hx.log_mean_temp_diff_parallel(100,85,30,55)) == pytest.approx(47.21,.005)
    
def test_q_max_ntu():
    assert hx.q_max_ntu(.1, 100, 10) == 9
    
def test_epsilon_ntu_parallel():
    assert hx.epsilon_ntu(10, .01, 1, 'parallel') == pytest.approx(0.99,.009)
    
def test_epsilon_ntu_counter():
    assert hx.epsilon_ntu(10, .01, 1, 'counter') == pytest.approx(0.99995,.00005)
    
def test_epsilon_ntu_shell():
    assert hx.epsilon_ntu(10, .01, 1, 'counter') == pytest.approx(0.99495,.009)

def test_epsilon_ntu_counter_cr1():
    assert hx.epsilon_ntu(10, 1, 1, 'counter') == pytest.approx(0.909,.01)    
    
def test_q_ntu():
    assert hx.q_ntu(10, 1, 100, 10) == 900
    
def test_temp_ntu_solver1():
    assert hx.temp_ntu_solver(900, 10, 1, 100, 0, 'cold') == pytest.approx(10,.1)
    
def test_temp_ntu_solver2():
    assert hx.temp_ntu_solver(900, 10, 1, 0, 10, 'hot') == pytest.approx(100,.1)
    
def test_temp_ntu_solver3():
    with pytest.raises(ValueError):
        hx.temp_ntu_solver(900, 10, 1, 0, 10, 'hout')
        
def test_lmtd_solver():
    assert hx.lmtd_solver(100, 1, 1) == 100

def test_temp_lmtd_solver_parallel1():
    assert hx.temp_lmtd_solver_parallel(10, 0, 100, 10, 60, temp_type = "hot_in") == pytest.approx(211, 1)
    
def test_temp_lmtd_solver_parallel2():
    assert hx.temp_lmtd_solver_parallel(100, 211.879, 100, 10, 60, temp_type = "cold_in") == pytest.approx(10, 1)
    
def test_temp_lmtd_solver_parallel3():
    assert hx.temp_lmtd_solver_parallel(100, 210, 0, 10, 60, temp_type = "hot_out") == pytest.approx(72, 1)
    
def test_temp_lmtd_solver_parallel4():
    assert hx.temp_lmtd_solver_parallel(100, 210, 100, 10, 60, temp_type = "cold_out") == pytest.approx(100, 1)
    
def test_temp_lmtd_solver_parallel5():
    with pytest.raises(ValueError):
        hx.temp_lmtd_solver_parallel(100, 211.879, 100, 10, 60, temp_type = "cold12_out")
        
def test_temp_lmtd_solver_counter1():
    assert hx.temp_lmtd_solver_counter(100, 0, 100, 10, 60, temp_type = "hot_in") == pytest.approx(170, 1)
    
def test_temp_lmtd_solver_counter2():
    assert hx.temp_lmtd_solver_counter(100, 210, 100, 10, 60, temp_type = "cold_in") == pytest.approx(38, 1)
    
def test_temp_lmtd_solver_counter3():
    assert hx.temp_lmtd_solver_counter(100, 210, 0, 10, 60, temp_type = "hot_out") == pytest.approx(72, 1)
    
def test_temp_lmtd_solver_counter4():
    assert hx.temp_lmtd_solver_counter(100, 210, 100, 10, 60, temp_type = "cold_out") == pytest.approx(170, 1)
    
def test_temp_lmtd_solver_counter5():
    with pytest.raises(ValueError):
        hx.temp_lmtd_solver_counter(100, 211.879, 100, 10, 60, temp_type = "cold12_out")
        
def test_u_resistance():
    assert hx.u_resistance(1,1,2,1,1,2) == 1
