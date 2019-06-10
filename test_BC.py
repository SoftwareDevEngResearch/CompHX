#!/usr/bin/env python3

#import numpy as np
import pytest
from . import HX_boundary_cond as bc

def test_temp_bc():
    """Tests the input parameters for temperature"""
    name = "input_single.yaml"
    assert bc.set_temp_boundary_conditions(name) == (300, 250, 200, 220)
    
def test_flow_bc():
    """Tests the input parameters for flow conditions"""
    name = "input_single.yaml"
    assert bc.set_flow_boundary_conditions(name) == (10, .001, 150, 2.75)

def test_read():
    """Tests the input parameters for proper reading in of the file"""
    inputs = bc.read_bc("input_single.yaml")
    assert inputs["case"] == "example"
