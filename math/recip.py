# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 16:53:08 2017

@author: Administrator
"""

from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

def myrecip(z):
    return np.reciprocal(z)

z = np.linspace(0.01,300,100)
plt.plot(z, myrecip(z), 'b-')
plt.xlabel('$z$',fontsize=15)
plt.ylabel('$\sigma(z)$',fontsize=15)
plt.title('recip display')
plt.grid()
plt.show()