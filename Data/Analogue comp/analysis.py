# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 09:58:36 2021

@author: vamsi
"""

import pandas as pd
import matplotlib.pyplot as plt

c1 = pd.read_csv("Gamma - 2\P_100\P_100_C1.CSV", names=["time","C1"], skiprows=(1))
c2 = pd.read_csv("Gamma - 2\P_100\P_100_C2.CSV", names=["time","C2"], skiprows=(1))
plt.plot(c2["time"],c2["C2"])