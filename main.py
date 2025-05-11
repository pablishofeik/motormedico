import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter
from ErrorPopUp import Error
from conection import ConectionDB
from menu import MenuApp
from login import Login
from menu import MenuApp
from signup import Signup

def mostrar_login():
    frame_signup.pack_forget()
    frame_menu.pack_forget()
    frame_login.pack(fill="both", expand=True)
    root.geometry("400x600")
    root.configure(fg_color="#969696")

def mostrar_signup():
    frame_login.pack_forget()
    frame_menu.pack_forget()
    frame_signup.pack(fill="both", expand=True)
    root.geometry("400x600")
    root.configure(fg_color="#969696")

def mostrar_menu():
    frame_login.pack_forget()
    frame_signup.pack_forget()
    frame_menu.pack(fill="both", expand=True)
    root.title("Menu")
    root.geometry("1024x600")
    root.configure(fg_color="#969696")

root = ctk.CTk()
root.title("Login")

frame_login = Login(root, cambiar_a_menu=mostrar_menu, cambiar_a_signup=mostrar_signup)
frame_signup = Signup(root, cambiar_a_login=mostrar_login)
frame_menu = MenuApp(root, mostrar_login)

mostrar_login()

root.mainloop()