import matplotlib.pyplot as plt
import os
import random
i = 0

def generar_segunda_grafica(x,y, generacion_actual):
    global i
    individuo_x = x
    individuo_y = y
    i += 1
    colors = [
        (0.25, 0.65, 0.90),  # Azul claro
        (0.95, 0.15, 0.15),  # Rojo oscuro
        (0.50, 0.75, 0.25),  # Verde claro
        (0.80, 0.50, 0.20),  # Naranja oscuro
        (0.60, 0.30, 0.70)   # Morado
        # Puedes añadir más colores según tus preferencias
    ]
    selected_color = random.choice(colors)
    
    plt.clf()
    plt.title("Genethic Algorithms" + str(generacion_actual))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    
    plt.axhline(0, color='black',linewidth=0.5)
    
    img_folder_path = 'results/second-graph/img'
    
    if not os.path.exists(img_folder_path):
        os.makedirs(img_folder_path)
    
    plt.scatter(individuo_x, individuo_y, s=500, c=[selected_color], alpha=0.4)
    
    img_file_name = f'img_generacion_{i}.png'

    img_file_path = os.path.join(img_folder_path, img_file_name)
    plt.savefig(img_file_path)