import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter
from ErrorPopUp import Error
from conection import ConectionDB
from menu import MenuApp
from login import Login
from menu import MenuApp

def mostrar_login():
    """Muestra el frame de Login y ajusta el tamaño de la ventana."""
    frame_menu.pack_forget()  # Ocultar el frame del menú
    frame_login.pack(fill="both", expand=True)  # Mostrar el frame de login
    root.geometry("400x600")  # Redimensionar la ventana para el login
    root.configure(fg_color="#969696")
    root.resizable(False, False)  # Desactivar redimensionamiento para login

def mostrar_menu():
    """Muestra el frame del menú y ajusta el tamaño de la ventana."""
    frame_login.pack_forget()  # Ocultar el frame de login
    frame_menu.pack(fill="both", expand=True)  # Mostrar el frame del menú
    root.title("Menu")
    root.geometry("1024x600")
    root.configure(fg_color="#969696")  # Fondo color #D6CDC6
    root.resizable(False, False)

root = ctk.CTk()
root.title("Login")

frame_login = Login(root, cambiar_a_menu=mostrar_menu)
frame_menu = MenuApp(root, mostrar_login)

mostrar_login()

root.mainloop()
