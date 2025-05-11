import customtkinter as ctk
from tkinter import ttk, messagebox
from image_file import find_image

class DiagnosisManagement(ctk.CTkFrame):
    def __init__(self, master, return_menu):
        super().__init__(master)
        self.return_menu = return_menu

        ctk.set_appearance_mode("light")
        self.configure(fg_color="#ffffff")

        self.create_main_interface()
        self.create_edit_interface()
        # Mostrar pantalla principal
        #self.show_main_screen()

        
    def create_main_interface(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        # Barra de herramientas
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="#000000", height=40)
        toolbar.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkButton(toolbar, text="Nuevo", width=80, command=self.new_diagnosis).pack(side="left", padx=5)
   
        
        # Botón de regreso
        ctk.CTkButton(self.main_frame, text="Regresar al Menú", command=self.return_menu).pack(pady=10)
 
    def new_diagnosis(self):
        print("")

    def create_edit_interface(self):
        # Frame de edición
        self.edit_frame = ctk.CTkFrame(self, fg_color="#ffffff")

    
       
        

    
    