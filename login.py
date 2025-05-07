import customtkinter as ctk
from PIL import Image, ImageTk
from ErrorPopUp import Error
from conection import ConectionDB
from menu import MenuApp

class Login (ctk.CTkFrame):
    def __init__(self, master, cambiar_a_menu):
        super().__init__(master)
        
        # Configuración de la ventana principal
        cambiar = cambiar_a_menu
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Crear el rectángulo central
        login_frame = ctk.CTkFrame(self, width=485, height=671, corner_radius=0, fg_color="#969696")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        login_frame.configure(fg_color="#969696")
        self.configure(fg_color="#969696")
        # Agregar contenido al rectángulo
        #logo_label = ctk.CTkLabel(login_frame, text="LOGO", font=("Arial", 32, "bold"), text_color="#FFFFFF")
        #logo_label.pack(pady=(30, 20))  # Espaciado superior
        self.add_image("images/login.png", screen_width/2-60, screen_height/2-300)  # Ajusta la posición según sea necesario

        title_label = ctk.CTkLabel(login_frame, text="INGRESO", font=("Arial", 24, "bold"), text_color="#FFFFFF")
        title_label.pack(pady=(0, 0))  # Espaciado entre elementos

        # Campo de usuario
        username_label = ctk.CTkLabel(login_frame, text="Usuario", font=("Arial", 18), text_color="#FFFFFF")
        username_label.pack(pady=(0, 10))  # Espaciado superior

        self.username_entry = ctk.CTkEntry(login_frame, width=300, height=40, corner_radius=10, fg_color="#FFFFFF", text_color="#000000")
        self.username_entry.pack(pady=(0, 20))  # Espaciado entre elementos
        
        # Campo de contraseña
        password_label = ctk.CTkLabel(login_frame, text="Contraseña", font=("Arial", 18), text_color="#FFFFFF")
        password_label.pack(pady=(0, 10))

        self.password_entry = ctk.CTkEntry(login_frame, width=300, height=40, corner_radius=10, fg_color="#FFFFFF", show="*", text_color="#000000")
        self.password_entry.pack(pady=(0, 15))

        # Botón de ingreso
        login_button = ctk.CTkButton(login_frame, text="Ingresar", text_color= "#000000", width=200, height=40, corner_radius=10, fg_color="#FFFFFF", 
                                     command=cambiar)
        login_button.pack(pady=(0, 0))

    def add_image(self, image_path, x, y):
        try:
            # Cargar la imagen, aplicar el blur, y ajustarla al tamaño deseado
            img = Image.open(image_path).resize((120, 120))
            img_tk = ImageTk.PhotoImage(img)

            # Crear etiqueta para mostrar la imagen
            circle_label = ctk.CTkLabel(self, image=img_tk, text="")
            circle_label.pack(pady=(10, 50))
        except FileNotFoundError:
            Error(self, "No se encontró la imagen en {image_path}")

    def Btn_Login(self):
        db = ConectionDB()
        conection = db.connect()
        user = self.username_entry.get()
        password = self.password_entry.get()
        """
        if conection is None:
            Error(self, "No se pudo conectar a la Base de datos")
            return 
        try:
            with conection.cursor() as cursor:
                # Consulta SQL para verificar usuario y contraseña
                query = "SELECT * FROM Usuario WHERE contacto = %s AND contacto = %s"
                cursor.execute(query, (user, password))
                resultado = cursor.fetchone()

                if resultado:
                    self.open_menu(conection)
                else:
                    Error(self, "Usuario o contraseña incorrectos.")
        except Exception as e:
            print(f"Error durante la consulta: {e}")
            return False
        finally:
            conection.close()
            
        """
        self.open_menu()


    def open_menu(self):
        self.destroy()  # Cierra la ventana actual
        menu_app = MenuApp()  # Pasa la conexión al menú
        menu_app.mainloop()