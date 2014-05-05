import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

with open('box6.csv', 'rb') as csvfile:
     points = csv.reader(csvfile, delimiter=' ', quotechar='|')
     print(type(points))
     fig=plt.figure()
     ax = fig.add_subplot(111, projection='3d')
     Axes3D.plot_wireframe(ax, points[0], points[1], points[2])
 # C:\Users\cta\Documents\GitHub\3D-Scanner-Code\Exported Meshes\box6