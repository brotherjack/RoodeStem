#!/usr/bin/env python
'''
Created on Jul 22, 2016

@author: Thomas Adriaan Hellinger
'''

from setuptools import setup

setup(name='RoodeStem',
      version='0.2.3',
      description='Voting simulator and ethereum group decision making engine.',
      author='Thomas Adriaan Hellinger',
      author_email='thellinger@acm.org',
      url='https://github.com/brotherjack/RoodeStem',
      packages=['.', 'simulations', 'voting_systems'],
        entry_points={
            'console_scripts': [
                'roodestem = app:App',
      ],
  },
)