import matplotlib.pyplot as plt
import os
i = 0

def generar_graficas(mejor_individuo, peor_individuo, promedio, generacion_actual):
    global i
    x = generacion_actual
    media = promedio
    mejor = mejor_individuo
    peor = peor_individuo
    print(f"Media = {media}, mejor = {mejor}, peor = {peor}, generacion_actual ={generacion_actual}")
    i += 1
    
    # Configura el gráfico fuera del bucle
    plt.clf()
    plt.title("Genethic Algorithms")
    plt.xlabel("Numero de generaciones")
    plt.ylabel("Eje Y")
    plt.grid(True)
    

    # Define la ruta completa de las carpetas
    img_folder_path = 'results/img'
    #video_folder_path = 'results/video'

    # Asegúrate de que las carpetas existan, si no, créalas
    if not os.path.exists(img_folder_path):
        os.makedirs(img_folder_path)

    #if not os.path.exists(video_folder_path):
    #    os.makedirs(video_folder_path)

    # Lista para almacenar nombres de archivos de imágenes
    #file_names = []

    plt.plot(x, media, label='Promedio', color='blue')  # Azul
    plt.plot(x, mejor, label='Mejor individuo', color='green')  # Verde
    plt.plot(x, peor, label='Peor individuo', color='red')  # Rojo
    
    # Mostrar la leyenda
    plt.legend()

    #Define el nombre del archivo con el índice actual
    img_file_name = f'img_generacion_{i}.png'

    # Guarda la imagen en la carpeta de imágenes especificada
    img_file_path = os.path.join(img_folder_path, img_file_name)
    plt.savefig(img_file_path)
    
    # Agrega el nombre del archivo de imagen a la lista
    #file_names.append(img_file_path)

    # Utiliza OpenCV para crear un video en formato MP4
    #video_path = os.path.join(video_folder_path, 'video.mp4')
    #images = [cv2.imread(file) for file in file_names]
    #height, width, layers = images[0].shape
    #video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))

    #for image in images:
    #    video.write(image)

    #cv2.destroyAllWindows()
    #video.release()


