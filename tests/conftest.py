'''
Created on Jun 28, 2016

@author: Thomas Adriaan Hellinger
'''
import pytest


@pytest.fixture
def hook_into_path(): 
    import sys, os
    myPath = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, myPath + '/../')