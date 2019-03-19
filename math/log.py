# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 16:53:08 2017

@author: Administrator
"""

from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt


z =  np.linspace(-10, 10, 2000)
plt.plot(z, np.arcsinh(z))
plt.xlabel('Angle [rad]')
plt.ylabel('sin(x)')
plt.axis('tight')
plt.grid()
plt.show()