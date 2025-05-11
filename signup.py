# signup.py
import customtkinter as ctk
from ErrorPopUp import Error
from conection import ConectionDB

class Signup(ctk.CTkFrame):
    def __init__(self, master, cambiar_a_login):
        super().__init__(master)
        self.cambiar_a_login = cambiar_a_login
        self.configure(fg_color="#969696")

        signup_frame = ctk.CTkFrame(self, width=485, height=671, corner_radius=0, fg_color="#969696")
        signup_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = ctk.CTkLabel(signup_frame, text="REGISTRO", font=("Arial", 24, "bold"), text_color="#FFFFFF")
        title_label.pack(pady=(20, 10))

        self.name_entry = self._create_entry(signup_frame, "Nombre completo")
        self.username_entry = self._create_entry(signup_frame, "Nombre de usuario")
        self.password_entry = self._create_entry(signup_frame, "Contraseña", show="*")

        signup_button = ctk.CTkButton(signup_frame, text="Crear cuenta", text_color="#000000",
                                      width=200, height=40, corner_radius=10, fg_color="#FFFFFF",
                                      command=self.register_user)
        signup_button.pack(pady=(10, 5))

        login_switch = ctk.CTkButton(signup_frame, text="¿Ya tienes cuenta? Inicia sesión", fg_color="transparent",
                                     text_color="#FFFFFF", hover=False, command=cambiar_a_login)
        login_switch.pack(pady=(5, 5))

    def _create_entry(self, parent, placeholder, show=""):
        label = ctk.CTkLabel(parent, text=placeholder, font=("Arial", 18), text_color="#FFFFFF")
        label.pack(pady=(10, 5))
        entry = ctk.CTkEntry(parent, width=300, height=40, corner_radius=10, fg_color="#FFFFFF",
                             text_color="#000000", show=show)
        entry.pack()
        return entry

    def register_user(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not name or not username or not password:
            Error(self, "Todos los campos son obligatorios.")
            return

        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
                if cursor.fetchone():
                    Error(self, "El nombre de usuario ya existe.")
                    return

                cursor.execute("INSERT INTO Users (name, username, password, role) VALUES (%s, %s, %s, %s)",
                               (name, username, password, "usuario"))
                connection.commit()
                self.cambiar_a_login()
        except Exception as e:
            print(f"Error durante el registro: {e}")
            Error(self, "Error al registrar el usuario.")
        finally:
            connection.close()
