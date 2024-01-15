import matplotlib.pyplot as plt
import os
import cv2

def generar_video(generacion):
    # Define la ruta completa de las carpetas
    img_folder_path = 'results/img'
    video_folder_path = 'results/video'

    if not os.path.exists(video_folder_path):
        os.makedirs(video_folder_path)

    # Lista para almacenar nombres de archivos de imágenes
    file_names = []

    # Loop para agregar nombres de archivos de imágenes a la lista
    for i in range(1, generacion):
        img_file_name = f'img_generacion_{i}.png'
        img_file_path = os.path.join(img_folder_path, img_file_name)
        file_names.append(img_file_path)

    # Utiliza OpenCV para crear un video en formato MP4
    video_path = os.path.join(video_folder_path, 'video.mp4')
    images = [cv2.imread(file) for file in file_names]
    height, width, layers = images[0].shape
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))

    for image in images:
        video.write(image)

    cv2.destroyAllWindows()
    video.release()
