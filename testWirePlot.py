import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

with open('/Exported Meshes/box6.csv', 'rb') as csvfile:
     points = csv.reader(csvfile, delimiter=' ', quotechar='|')
     print(type(points))
     fig=plt.figure()
     ax = fig.add_subplot(111, projection='3d')
     Axes3D.plot_wireframe(points)
 # C:\Users\cta\Documents\GitHub\3D-Scanner-Code\Exported Meshes\box6