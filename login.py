import customtkinter as ctk
from PIL import Image, ImageTk
from typing import Callable, Optional, Tuple
from ErrorPopUp import Error
from conection import ConectionDB
from menu import MenuApp

class Login(ctk.CTkFrame):
    def __init__(self, master, on_login_success: Callable[[str], None],  # Añade este parámetro
        **kwargs):
   
        super().__init__(master)
        self.cambiar_a_menu = on_login_success
        
        # Configuración inicial
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """Configura todos los elementos de la interfaz de usuario."""
        self.configure(fg_color="#969696")
        
        # Frame principal del login
        self.login_frame = ctk.CTkFrame(
            self, 
            width=485, 
            height=671, 
            corner_radius=0, 
            fg_color="#969696"
        )
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo/Imagen
        self._add_login_image()
        
        # Título
        title_label = ctk.CTkLabel(
            self.login_frame, 
            text="INGRESO", 
            font=("Arial", 24, "bold"), 
            text_color="#FFFFFF"
        )
        title_label.pack(pady=(0, 20))
        
        # Campos de entrada
        self._setup_input_fields()
        
        # Botones
        self._setup_buttons()
        
    def _add_login_image(self) -> None:
        """Añade la imagen de login."""
        try:
            img = Image.open("images/login.png").resize((120, 120))
            self.login_img = ImageTk.PhotoImage(img)
            
            img_label = ctk.CTkLabel(
                self.login_frame, 
                image=self.login_img, 
                text=""
            )
            img_label.pack(pady=(10, 50))
        except FileNotFoundError:
            Error(self, "No se encontró la imagen de login")
        except Exception as e:
            Error(self, f"Error al cargar imagen: {str(e)}")
            
    def _setup_input_fields(self) -> None:
        """Configura los campos de usuario y contraseña."""
        # Campo de usuario
        username_label = ctk.CTkLabel(
            self.login_frame, 
            text="Usuario", 
            font=("Arial", 18), 
            text_color="#FFFFFF"
        )
        username_label.pack(pady=(0, 10))
        
        self.username_entry = ctk.CTkEntry(
            self.login_frame, 
            width=300, 
            height=40, 
            corner_radius=10, 
            fg_color="#FFFFFF", 
            text_color="#000000"
        )
        self.username_entry.pack(pady=(0, 20))
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # Campo de contraseña
        password_label = ctk.CTkLabel(
            self.login_frame, 
            text="Contraseña", 
            font=("Arial", 18), 
            text_color="#FFFFFF"
        )
        password_label.pack(pady=(0, 10))
        
        self.password_entry = ctk.CTkEntry(
            self.login_frame, 
            width=300, 
            height=40, 
            corner_radius=10, 
            fg_color="#FFFFFF", 
            show="*", 
            text_color="#000000"
        )
        self.password_entry.pack(pady=(0, 15))
        self.password_entry.bind("<Return>", lambda e: self.Btn_Login())
        
    def _setup_buttons(self) -> None:
        """Configura los botones de login y registro."""
        login_button = ctk.CTkButton(
            self.login_frame, 
            text="Ingresar", 
            text_color="#000000", 
            width=200, 
            height=40, 
            corner_radius=10, 
            fg_color="#FFFFFF", 
            command=self.Btn_Login
        )
        login_button.pack(pady=(0, 10))
        
    def Btn_Login(self) -> None:
        """Maneja el proceso de login."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            Error(self, "Usuario y contraseña son requeridos")
            return
            
        db = ConectionDB()
        connection = db.connect()
        
        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return
            
        try:
            with connection.cursor() as cursor:
                # Consulta mejorada para obtener también el nombre del usuario
                query = """
                SELECT username, name 
                FROM Users 
                WHERE username = %s AND password = %s
                """
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
                
                if result:
                    # Pasar el nombre de usuario al menú principal
                    self.cambiar_a_menu(result['name'] if 'name' in result else username)
                else:
                    Error(self, "Usuario o contraseña incorrectos")
        except Exception as e:
            print(f"Error durante el login: {e}")
            Error(self, "Error al verificar credenciales")
        finally:
            connection.close()
            
    def clear_fields(self) -> None:
        """Limpia los campos de entrada."""
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.username_entry.focus_set()