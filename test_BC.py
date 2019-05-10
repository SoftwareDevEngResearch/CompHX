#!/usr/bin/env python3

#import numpy as np
import pytest
from . import HX_boundary_cond as bc

def test_temp_bc():
    assert bc.set_temp_boundary_conditions() == (300, 250, 200, 220)
    
def test_fin_efficiency():
    assert bc.fin_conditions(150,2.75) == pytest.approx(.994,.0005)