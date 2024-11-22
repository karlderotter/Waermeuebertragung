# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 13:12:04 2023

@author: xk4236
"""

import numpy as np
import matplotlib.pyplot as plt
from IPython import get_ipython

from Parameter import *
from num_Parameter import *
from Initialisierung import *
'''
fig, axis = plt.subplots()

pcm = axis.pcolormesh(T_n, cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(pcm, ax=axis)
'''
#Ab hier



x, y = np.meshgrid(np.arange(xMax,xMin-dx,-dx),np.arange(yMax,yMin-dy,-dy))
#Numerische Fehler reduzieren indem 0 explizit zugeordnet wird
x[:,-1] = 0
y[-1,:] = 0


#Plot
#Damit Plot in einem seperaten Fenster angezeigt wird
#get_ipython().run_line_magic("matplotlib", "qt")

#eigentlicher Plot
figure, ax = plt.subplots()

extent = np.min(x), np.max(x), np.min(y), np.max(y)

picture = ax.imshow(T_n, cmap="jet", interpolation ="bilinear", extent=extent)
cbar = plt.colorbar(picture)
cbar.set_label("Temperatur / K")

ax.set_xlabel("x / m")
ax.set_ylabel("y / m")
ax.set_title("t = " + str(t0) + " s")
plt.show()
