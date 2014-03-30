'''
Created on 26 Feb, 2014

@author: yzhang28
'''
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import Bbox

fig1 = plt.figure()
ax = fig1.add_subplot(111, projection='3d')

# y | x  0     1     2     3     4
#------------------------------------
# 0 |    1     1     0     0     0    
# 1 |    1     1     0     0     0    
# 2 |    1     1     0     0     0    
# 3 |    1     1     0     0     0    
# 4 |    1     0     0     0     0    
# 5 |    0     0     0     0     0   

xa1pos = [0,1, 0,1, 0,1, 0,1, 0]
ya1pos = [0,0, 1,1, 2,2, 3,3, 4]
za1pos = [0,0, 0,0, 0,0, 0,0, 0]
dxa1 = np.ones(len(xa1pos))*0.7
dya1 = np.ones(len(ya1pos))*0.7
dza1 = np.ones(len(za1pos))

xa0pos = [2,3,4, 2,3,4, 2,3,4, 2,3,4, 1,2,3,4, 0,1,2,3,4]
ya0pos = [0,0,0, 1,1,1, 2,2,2, 3,3,3, 4,4,4,4, 5,5,5,5,5]
za0pos = [0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0,0, 0,0,0,0,0]
dxa0 = np.ones(len(xa0pos))*0.7
dya0 = np.ones(len(ya0pos))*0.7
dza0 = np.zeros(len(za0pos))+0.005

ax.bar3d(xa0pos, ya0pos, za0pos, dxa0, dya0, dza0, color='white',alpha=0.15)
blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="grey", alpha=0.45)
ax.bar3d(xa1pos, ya1pos, za1pos, dxa1, dya1, dza1, color='red',alpha=0.75)
red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
ax.legend([blue_proxy,red_proxy],['Not charging','Charging'], loc='best', fontsize=12)
# xlim([0.01,5.99])
# ylim([-0.99,8.99])
xlabel('Location state $\mathcal{L}$',fontsize=16)
ylabel('Energy state $\mathcal{E}$', fontsize=16)
ax.set_zlabel('Action (Charging/not charging)', fontsize=16)
ax.set_zticks([0,1])



fig2 = plt.figure()
ax = fig2.add_subplot(111, projection='3d')

# y | x  0     1     2     3     4
#------------------------------------
# 0 |    1     1     1     0     0    
# 1 |    1     1     1     0     0    
# 2 |    1     1     1     0     0    
# 3 |    1     1     1     0     0    
# 4 |    0     0     0     0     0    
# 5 |    0     0     0     0     0   

xb1pos = [0,1,2, 0,1,2, 0,1,2, 0,1,2]
yb1pos = [0,0,0, 1,1,1, 2,2,2, 3,3,3]
zb1pos = [0,0,0, 0,0,0, 0,0,0, 0,0,0]
dxb1 = np.ones(len(xb1pos))*0.7
dyb1 = np.ones(len(yb1pos))*0.7
dzb1 = np.ones(len(zb1pos))

xb0pos = [3,4, 3,4, 3,4, 3,4, 0,1,2,3,4, 0,1,2,3,4]
yb0pos = [0,0, 1,1, 2,2, 3,3, 4,4,4,4,4, 5,5,5,5,5]
zb0pos = [0,0, 0,0, 0,0, 0,0, 0,0,0,0,0, 0,0,0,0,0]
dxb0 = np.ones(len(xb0pos))*0.7
dyb0 = np.ones(len(yb0pos))*0.7
dzb0 = np.zeros(len(zb0pos))+0.005

ax.bar3d(xb0pos, yb0pos, zb0pos, dxb0, dyb0, dzb0, color='white',alpha=0.15)
blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="grey", alpha=0.45)
ax.bar3d(xb1pos, yb1pos, zb1pos, dxb1, dyb1, dzb1, color='red',alpha=0.75)
red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
ax.legend([blue_proxy,red_proxy],['Not charging','Charging'], loc='best', fontsize=12)
# xlim([0.01,5.99])
# ylim([-0.99,8.99])
xlabel('Location state $\mathcal{L}$',fontsize=16)
ylabel('Energy state $\mathcal{E}$', fontsize=16)
ax.set_zlabel('Action (Charging/not charging)', fontsize=16)
ax.set_zticks([0,1])





fig3 = plt.figure()
ax = fig3.add_subplot(111, projection='3d')

# y | x  0     1     2
#---------------------
# 0 |    1     1     1    
# 1 |    1     1     1    
# 2 |    1     1     1    
# 3 |    1     1     1    
# 4 |    0     0     0    
# 5 |    0     0     0

xc1pos = [0,1,2, 0,1,2, 0,1,2, 0,1,2]
yc1pos = [0,0,0, 1,1,1, 2,2,2, 3,3,3]
zc1pos = [0,0,0, 0,0,0, 0,0,0, 0,0,0]
dxc1 = np.ones(len(xc1pos))*0.7
dyc1 = np.ones(len(yc1pos))*0.7
dzc1 = np.ones(len(zc1pos))

xc0pos = [0,1,2, 0,1,2]
yc0pos = [4,4,4, 5,5,5]
zc0pos = [0,0,0, 0,0,0]
dxc0 = np.ones(len(xc0pos))*0.7
dyc0 = np.ones(len(yc0pos))*0.7
dzc0 = np.zeros(len(zc0pos))+0.005

ax.bar3d(xc0pos, yc0pos, zc0pos, dxc0, dyc0, dzc0, color='white',alpha=0.15)
blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="grey", alpha=0.45)
ax.bar3d(xc1pos, yc1pos, zc1pos, dxc1, dyc1, dzc1, color='red',alpha=0.75)
red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
ax.legend([blue_proxy,red_proxy],['Not charging','Charging'], loc='best', fontsize=12)
xlim([0.0,3.0], auto=False)
ylim([0.0,6.0])
xlabel('Traffic generation state $\mathcal{W}$',fontsize=16)
ylabel('Energy state $\mathcal{E}$', fontsize=16)
ax.set_zlabel('Action (Charging/not charging)', fontsize=16)
ax.set_zticks([0,1])




fig4 = plt.figure()
ax = fig4.add_subplot(111, projection='3d')

# y | x  0     1     2
#---------------------
# 0 |    1     1     1    
# 1 |    1     1     1    
# 2 |    1     1     1    
# 3 |    1     1     1    
# 4 |    1     1     1    
# 5 |    0     0     0

xe1pos = [0,1,2, 0,1,2, 0,1,2, 0,1,2, 0,1,2]
ye1pos = [0,0,0, 1,1,1, 2,2,2, 3,3,3, 4,4,4]
ze1pos = [0,0,0, 0,0,0, 0,0,0, 0,0,0, 0,0,0]
dxe1 = np.ones(len(xe1pos))*0.7
dye1 = np.ones(len(ye1pos))*0.7
dze1 = np.ones(len(ze1pos))

xe0pos = [0,1,2]
ye0pos = [5,5,5]
ze0pos = [0,0,0]
dxe0 = np.ones(len(xe0pos))*0.7
dye0 = np.ones(len(ye0pos))*0.7
dze0 = np.zeros(len(ze0pos))+0.005

ax.bar3d(xe0pos, ye0pos, ze0pos, dxe0, dye0, dze0, color='white',alpha=0.15)
blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="grey", alpha=0.45)
ax.bar3d(xe1pos, ye1pos, ze1pos, dxe1, dye1, dze1, color='red',alpha=0.75)
red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
ax.legend([blue_proxy,red_proxy],['Not charging','Charging'], loc='best', fontsize=12)
xlim([0.0,3.0], auto=False)
ylim([0.0,6.0])
xlabel('Traffic generation state $\mathcal{W}$',fontsize=16)
ylabel('Energy state $\mathcal{E}$', fontsize=16)
ax.set_zlabel('Action (Charging/not charging)', fontsize=16)
ax.set_zticks([0,1])




plt.show()