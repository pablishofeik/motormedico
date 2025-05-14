import customtkinter as ctk
from typing import Callable, Optional
from image_file import find_image
from patient import PatientManager
from newuser import NewUser
from disease import DiseaseManager
from signs import SignManager
from symptoms import SymptomManager
from tests import TestManager
from inferenceengine import InferenceEngine

class MenuApp(ctk.CTkFrame):
    def __init__(self, master, on_logout: Callable, username: str = "Usuario"):
        """
        Inicializa el menú principal de la aplicación.
        
        Args:
            master: Widget padre
            on_logout: Función para manejar el cierre de sesión
            username: Nombre del usuario actual (por defecto "Usuario")
        """
        super().__init__(master)
        self.on_logout = on_logout
        self.username = username
        self.dropdown_visible = False
        
        # Configuración inicial
        self._setup_main_frame()
        self._setup_top_frame()
        self._setup_menu_screen()
        
        # Inicializar pantallas secundarias
        self._initialize_sub_screens()
        
        # Manejo de eventos
        self.bind("<Button-1>", self.close_dropdown)
        
    def _setup_main_frame(self) -> None:
        """Configura el frame principal."""
        self.main_frame = ctk.CTkFrame(
            self, 
            width=1024, 
            height=600, 
            corner_radius=0, 
            fg_color="#969696"
        )
        self.main_frame.pack(fill="both", expand=True)
        
    def _setup_top_frame(self) -> None:
        """Configura la barra superior con el nombre de usuario y menú desplegable."""
        self.top_frame = ctk.CTkFrame(
            self.main_frame, 
            width=1024, 
            height=50, 
            corner_radius=0, 
            fg_color="#FFFFFF"
        )
        self.top_frame.pack(fill="x")
        
        # Etiqueta de bienvenida
        welcome_text = f"Hola, {self.username}!"
        self.welcome_label = ctk.CTkLabel(
            self.top_frame, 
            text=welcome_text, 
            font=("Arial", 20, "bold"), 
            text_color="#000000"
        )
        self.welcome_label.pack(side="left", padx=20, pady=10)
        
        # Botón de usuario y menú desplegable
        self._setup_user_dropdown()
        
    def _setup_user_dropdown(self) -> None:
        """Configura el botón de usuario y el menú desplegable."""
        user_icon = find_image("images/login.png", 30)
        self.user_button = ctk.CTkButton(
            self.top_frame,
            text="",
            image=user_icon,
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#e0e0e0",
            command=self.toggle_dropdown
        )
        self.user_button.pack(side="right", padx=10, pady=10)
        
        # Frame del menú desplegable
        self.dropdown_frame = ctk.CTkFrame(
            self.main_frame, 
            width=150, 
            height=110, 
            corner_radius=5
        )
        
        # Opciones del menú
        options = [
            ("Crear usuario", self._handle_create_user),
            ("Cambiar de usuario", self._handle_change_user),
            ("Cerrar sesión", self._handle_logout)
        ]
        
        for text, command in options:
            btn = ctk.CTkButton(
                self.dropdown_frame,
                text=text,
                width=140,
                height=30,
                anchor="w",
                fg_color="transparent",
                hover_color="#e0e0e0",
                text_color="#000000",
                command=command
            )
            btn.pack(pady=2, fill="x", padx=5)
            
        # Asegurar que los clicks en el dropdown no lo cierren
        self.dropdown_frame.bind("<Button-1>", lambda e: e.stop_propagation())
        
    def _setup_menu_screen(self) -> None:
        """Configura la pantalla principal con los botones de opciones."""
        self.menu_screen = ctk.CTkFrame(
            self.main_frame, 
            width=1024, 
            height=550, 
            corner_radius=0, 
            fg_color="#969696"
        )
        self.menu_screen.pack(fill="both", expand=True)
        
        # Configuración de botones en una cuadrícula
        button_configs = [
            ("Pacientes", "images/patient.png", 50, self.Btn_patient, 0, 0),
            ("Enfermedades", "images/disease.png", 70, self.Btn_disease, 1, 0),
            ("Signos", "images/sign.png", 70, self.Btn_signs, 2, 0),
            ("Síntomas", "images/symptom.png", 70, self.Btn_symptoms, 0, 1),
            ("Pruebas", "images/test.png", 70, self.Btn_tests, 1, 1),
            ("Diagnóstico", "images/diagnostic.png", 70, self.Btn_diagnosis, 2, 1)
        ]
        
        # Posiciones en la cuadrícula
        grid_positions = [
            (100, 20), (400, 20), (700, 20),
            (100, 300), (400, 300), (700, 300)
        ]
        
        for (text, image_path, size, command, row, col), (x, y) in zip(button_configs, grid_positions):
            img = find_image(image_path, size)
            btn = ctk.CTkButton(
                self.menu_screen,
                text=text,
                image=img,
                compound="top",
                width=200,
                height=200,
                fg_color="#FFFFFF",
                text_color="#000000",
                command=command
            )
            btn.place(x=x, y=y)
            
    def _initialize_sub_screens(self) -> None:
        """Inicializa todas las pantallas secundarias."""
        self.sub_screens = {
            "patient": PatientManager(self, self.show_menu_screen),
            "user": NewUser(self, self.show_menu_screen),
            "disease": DiseaseManager(self, self.show_menu_screen),
            "sign": SignManager(self, self.show_menu_screen),
            "symptom": SymptomManager(self, self.show_menu_screen),
            "test": TestManager(self, self.show_menu_screen),
            "diagnosis": InferenceEngine(self, self.show_menu_screen)
        }
        
    def toggle_dropdown(self) -> None:
        """Alterna la visibilidad del menú desplegable."""
        if self.dropdown_visible:
            self.dropdown_frame.place_forget()
        else:
            # Posicionar el dropdown debajo del botón de usuario
            btn_x = self.user_button.winfo_rootx() - self.main_frame.winfo_rootx()
            btn_y = self.user_button.winfo_rooty() - self.main_frame.winfo_rooty()
            
            x = btn_x + self.user_button.winfo_width() - self.dropdown_frame.winfo_reqwidth()
            y = btn_y + self.user_button.winfo_height()
            
            self.dropdown_frame.place(x=x, y=y)
            self.dropdown_frame.lift()
            
        self.dropdown_visible = not self.dropdown_visible
        
    def close_dropdown(self, event=None) -> None:
        """Cierra el menú desplegable si está visible."""
        if self.dropdown_visible:
            # Verificar si el clic fue fuera del dropdown y del botón
            if (not self.dropdown_frame.winfo_contain(event.x_root, event.y_root) and
                not self.user_button.winfo_contain(event.x_root, event.y_root)):
                self.dropdown_frame.place_forget()
                self.dropdown_visible = False
                
    def _handle_create_user(self) -> None:
        """Maneja la creación de nuevo usuario."""
        self.show_sub_screen("user")
        self.close_dropdown()
        
    def _handle_change_user(self) -> None:
        """Maneja el cambio de usuario."""
        self.on_logout()
        self.close_dropdown()
        
    def _handle_logout(self) -> None:
        """Maneja el cierre de sesión."""
        self.master.destroy()
        self.close_dropdown()
        
    def show_menu_screen(self) -> None:
        """Muestra la pantalla principal del menú."""
        for screen in self.sub_screens.values():
            screen.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        
    def show_sub_screen(self, screen_name: str) -> None:
        """Muestra una pantalla secundaria específica.
        
        Args:
            screen_name: Nombre de la pantalla a mostrar
        """
        self.main_frame.pack_forget()
        self.sub_screens[screen_name].pack(fill="both", expand=True)
        
    # Métodos para mostrar cada pantalla secundaria
    def Btn_patient(self) -> None:
        self.show_sub_screen("patient")
        
    def Btn_disease(self) -> None:
        self.show_sub_screen("disease")
        
    def Btn_signs(self) -> None:
        self.show_sub_screen("sign")
        
    def Btn_symptoms(self) -> None:
        self.show_sub_screen("symptom")
        
    def Btn_tests(self) -> None:
        self.show_sub_screen("test")
        
    def Btn_diagnosis(self) -> None:
        self.show_sub_screen("diagnosis")
