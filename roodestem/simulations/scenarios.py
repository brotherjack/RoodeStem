'''
Created on Jun 29, 2016

@author: Thomas Adriaan Hellinger
'''
from abc import ABCMeta, abstractmethod


class Scenario(object, metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass
    
    @property
    @abstractmethod
    def description(self):
        pass
    
    @property
    @abstractmethod
    def choices(self):
        pass
