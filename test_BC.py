#!/usr/bin/env python3

#import numpy as np
import pytest
from . import HX_boundary_condition as hx

def test_temp_BC():
    assert hx.set_boundary_conditions() == (300, 250, 200, 220)