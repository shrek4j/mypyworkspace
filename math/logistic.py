# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 16:53:08 2017

@author: Administrator
"""

from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

def logistic(z):
    return 1 / (1 + np.exp(-z))

z = np.linspace(-10,10,100)
plt.plot(z, logistic(z), 'b-')
plt.xlabel('$z$',fontsize=15)
plt.ylabel('$\sigma(z)$',fontsize=15)
plt.title('logistic function')
plt.grid()
plt.show()