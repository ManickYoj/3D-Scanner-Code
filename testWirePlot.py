import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

ax1.plot(data['x'], data['y'], color='r', label='the data')
with open('box6.csv', 'rb') as csvfile:
     points = csv.reader(csvfile, delimiter=' ', quotechar='|')
     data = np.genfromtxt('e:\dir1\datafile.csv', delimiter=',', skip_header=10,skip_footer=10, names=['x', 'y', 'z'])
     fig=plt.figure()
     ax = fig.add_subplot(111, projection='3d')
     ax.plot_wireframe(ax, points[0], points[1], points[2])
 # C:\Users\cta\Documents\GitHub\3D-Scanner-Code\Exported Meshes\box6