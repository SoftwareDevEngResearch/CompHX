#!/usr/bin/env python3

#import numpy as np
import pytest
from . import HX_boundary_condition as bc

def test_temp_bc():
    assert bc.set_boundary_conditions() == (300, 250, 200, 220)