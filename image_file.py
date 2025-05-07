import os
from PIL import Image, ImageTk

def find_image (file_name, size):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, file_name)
        choseen_img = Image.open(image_path).resize((size, size))
        choseen_tk = ImageTk.PhotoImage(choseen_img)
        return choseen_tk
    except FileNotFoundError:
        print(f"Error: No se encontró la imagen {file_name} en {image_path}")
        choosen_tk = None