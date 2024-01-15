import matplotlib.pyplot as plt
import os
i = 0

def generar_segunda_grafica(x,y, generacion_actual):
    global i
    individuo_x = x
    individuo_y = y
    mejor_individuo = individuo_y.index(max(individuo_y))
    peor_individuo = individuo_y.index(min(individuo_y))
    i += 1
    colores = [(0.25, 0.65, 0.90) for _ in range(len(individuo_x))]
    colores[mejor_individuo] = (0.15, 0.68, 0.38)
    colores[peor_individuo] = (0.92, 0.23, 0.35) 
    
    
    plt.clf()
    plt.title("Genethic Algorithms " + str(generacion_actual))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    
    plt.axhline(0, color='black',linewidth=0.5)
    
    img_folder_path = 'results/second-graph/img'
    
    if not os.path.exists(img_folder_path):
        os.makedirs(img_folder_path)
    
    plt.scatter(individuo_x, individuo_y, s=500, c=colores, alpha=0.4)
    
    img_file_name = f'img_generacion_{i}.png'

    img_file_path = os.path.join(img_folder_path, img_file_name)
    plt.savefig(img_file_path)