import matplotlib.pyplot as plt
import numpy as np

def generar_segunda_grafica(x,y, generacion_actual):
    N = 500
    colors = np.random.rand(N)
    plt.clf()
    plt.title("Genethic Algorithms")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.scatter(x, y, s=500, c=colors, alpha=0.4)



