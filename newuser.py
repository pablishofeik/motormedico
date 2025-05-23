import customtkinter as ctk
from image_file import find_image
from tkinter import ttk, messagebox
from datetime import datetime  # Para manejar created_at
from conection import ConectionDB
from ErrorPopUp import Error

class NewUser(ctk.CTkFrame):
    def __init__(self, master, return_menu):
        super().__init__(master)
        self.return_menu = return_menu
        self.current_user = None
        
        # Configuración principal
        self.main_frame = ctk.CTkFrame(self, width=1024, height=600, corner_radius=0, fg_color="#969696")
        self.main_frame.pack(fill="both", expand=True)

        # Frame superior
        self.top_frame = ctk.CTkFrame(self.main_frame, width=1024, height=50, fg_color="#FFFFFF")
        self.top_frame.pack(fill="x", expand=False)

        # Frames para pantallas
        self.create_screens()
        
        # Botones de CRUD
        self.create_crud_buttons()
        
        # Frame inferior
        self.bottom_frame = ctk.CTkFrame(self.main_frame, width=1024, height=50, fg_color="#FFFFFF")
        self.bottom_frame.pack(side="bottom", fill="x")
        self.create_bottom_buttons()

        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                # Ajusta la consulta a tu tabla y campos
                query = "SELECT * FROM Users"
                cursor.execute(query)
                resultados = cursor.fetchall()

        except Exception as e:
            print(f"Error durante la consulta: {e}")
            Error(self, "Error al consultar la base de datos.")
        finally:
            connection.close()

        # Datos de ejemplo
        self.users = []
        self.load_user()

        # Configurar pantallas
        self.create_add_user_ui()
        self.create_edit_user_ui()
        self.create_delete_user_ui()
        self.create_view_users_ui()
        
        self.show_view_users()

    def create_screens(self):
        self.adduser_screen = ctk.CTkFrame(self.main_frame, fg_color="#969696")
        self.updateuser_screen = ctk.CTkFrame(self.main_frame, fg_color="#969696")
        self.deleteuser_screen = ctk.CTkFrame(self.main_frame, fg_color="#969696")
        self.viewuser_screen = ctk.CTkFrame(self.main_frame, fg_color="#969686")

    def create_crud_buttons(self):
        ctk.CTkButton(self.top_frame, text="Agregar Usuario", width=80, command=self.show_add_user).pack(side="left", padx=5)
        ctk.CTkButton(self.top_frame, text="Eliminar Usuario", width=80, command=self.show_delete_user).pack(side="left", padx=5)
        ctk.CTkButton(self.top_frame, text="Editar Usuario", width=80, command=self.show_update_user).pack(side="left", padx=5)
        ctk.CTkButton(self.top_frame, text="Ver Usuarios", width=80, command=self.show_view_users).pack(side="left", padx=5)

    def create_bottom_buttons(self):
        ctk.CTkButton(self.bottom_frame, text="Regresar al menu", width=80, command=self.return_menu).pack(side="left", padx=5)

    def create_add_user_ui(self):
        fields = [
            ("Nombre completo:", 80, 50),
            ("Username:", 80, 130),
            ("Contraseña:", 80, 210),
            ("Confirmar Contraseña:", 80, 290)
        ]

        self.add_entries = {}
        for text, x, y in fields:
            label = ctk.CTkLabel(self.adduser_screen, text=text, font=("Arial", 16), text_color="#000000")
            label.place(x=x, y=y)
            
            entry = ctk.CTkEntry(self.adduser_screen, width=300, height=40, fg_color="#FFFFFF")
            if "Contraseña" in text:
                entry.configure(show="*")
            entry.place(x=x, y=y+30)
            self.add_entries[text.replace(":", "").strip().lower()] = entry

        # Combobox para roles
        self.role_combobox = ctk.CTkComboBox(
            self.adduser_screen,
            values = ["Administrador", "Medico", "Patologo", "Forense"],
            width=300,
            height=40
        )
        self.role_combobox.place(x=410, y=130)

        ctk.CTkButton(
            self.adduser_screen,
            text="Guardar Usuario",
            command=self.save_user,
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).place(x=400, y=370)


    def load_user(self):
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                # Ajusta la consulta a tu tabla y campos
                query = "SELECT * FROM Users"
                cursor.execute(query)
                resultados = cursor.fetchall()

        except Exception as e:
            print(f"Error durante la consulta: {e}")
            Error(self, "Error al consultar la base de datos.")
        finally:
            connection.close()

        # Datos de ejemplo
        self.users = [
            {
                "id_user": row[0],
                "name": row[1],
                "username": row[2],
                "role": row[3],
                "created_at": row[4].strftime("%Y-%m-%d %H:%M:%S"),
                "password": row[5]
            }
            for row in resultados
        ]

    def save_user(self):
        # Obtener valores
        full_name = self.add_entries["nombre completo"].get().strip()
        username = self.add_entries["username"].get().strip()
        password = self.add_entries["contraseña"].get()
        confirm_password = self.add_entries["confirmar contraseña"].get()
        role = self.role_combobox.get()

        # Validar campos
        if error := self.validate_full_name(full_name):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_username(username):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_password(password):
            messagebox.showerror("Error", error)
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        if error := self.validate_role(role):
            messagebox.showerror("Error", error)
            return

        # Conexión a la base de datos
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                # Verificar si el username existe
                cursor.execute("SELECT 1 FROM Users WHERE username = %s", (username,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "El nombre de usuario ya existe")
                    return

                # Insertar nuevo usuario
                insert_query = """
                    INSERT INTO Users (name, username, password, role, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    full_name,
                    username,
                    password,  # Sin hashear (según requisito)
                    role,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))

                connection.commit()

                # Limpiar y actualizar interfaz
                self.clear_add_fields()
                messagebox.showinfo("Éxito", "Usuario creado correctamente")
                self.load_user()
                self.show_view_users()

        except Exception as e:
            print(f"Error al insertar usuario: {e}")
            Error(self, f"Error al guardar el usuario: {str(e)}")
        finally:
            connection.close()
        self.clear_add_fields()
        self.load_user()

    def clear_add_fields(self):
        for entry in self.add_entries.values():
            entry.delete(0, "end")
        self.role_combobox.set("")

    def create_edit_user_ui(self):
        fields = [
            ("Nombre completo:", 80, 50),
            ("Username:", 80, 130),
            ("Nueva Contraseña:", 80, 210),
            ("Confirmar Contraseña:", 80, 290)
        ]

        self.edit_entries = {}
        for text, x, y in fields:
            label = ctk.CTkLabel(self.updateuser_screen, text=text, font=("Arial", 16), text_color="#000000")
            label.place(x=x, y=y)
            
            entry = ctk.CTkEntry(self.updateuser_screen, width=300, height=40, fg_color="#FFFFFF")
            if "Contraseña" in text:
                entry.configure(show="*")
            entry.place(x=x, y=y+30)
            self.edit_entries[text.replace(":", "").strip().lower().replace("nueva ", "")] = entry

        self.edit_role_combobox = ctk.CTkComboBox(
            self.updateuser_screen,
            values=["Administrador", "Medico", "Patologo", "Forense"],
            width=300,
            height=40
        )
        self.edit_role_combobox.place(x=410, y=130)

        ctk.CTkButton(
            self.updateuser_screen,
            text="Actualizar Usuario",
            command=self.update_user,
            fg_color="#2196F3",
            hover_color="#1976D2"
        ).place(x=400, y=370)

    def update_user(self):
        # Obtener valores
        full_name = self.edit_entries["nombre completo"].get().strip()
        username = self.edit_entries["username"].get().strip()
        new_password = self.edit_entries["contraseña"].get()
        confirm_password = self.edit_entries["confirmar contraseña"].get()
        role = self.edit_role_combobox.get()

        # Validar campos básicos
        if error := self.validate_full_name(full_name):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_username(username):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_role(role):
            messagebox.showerror("Error", error)
            return

        # Validar contraseña (solo si se quiere cambiar)
        if new_password:
            if error := self.validate_password(new_password):
                messagebox.showerror("Error", error)
                return
            if new_password != confirm_password:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return

        # Conexión a la base de datos
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                # Verificar unicidad del username (excluyendo al usuario actual)
                cursor.execute(
                    "SELECT COUNT(*) FROM Users WHERE username = %s AND id_user != %s",
                    (username, self.current_user["id_user"])
                )
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Error", "El nombre de usuario ya existe")
                    return

                # Construir la consulta UPDATE dinámica
                update_fields = ["name = %s", "username = %s", "role = %s"]
                values = [full_name, username, role]

                if new_password:
                    update_fields.append("password = %s")
                    values.append(new_password)

                values.append(self.current_user["id_user"])  # ID para el WHERE

                # Ejecutar actualización
                update_query = f"UPDATE Users SET {', '.join(update_fields)} WHERE id_user = %s"
                cursor.execute(update_query, values)
                connection.commit()

                # Limpiar y actualizar interfaz
                self.clear_edit_fields()
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                self.load_user()  # Recargar datos actualizados
                self.show_view_users()

        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            Error(self, f"Error al actualizar el usuario: {str(e)}")
        finally:
            connection.close()

    def clear_edit_fields(self):
        for entry in self.edit_entries.values():
            entry.delete(0, "end")
        self.edit_role_combobox.set("")
        self.current_user = None

    def create_delete_user_ui(self):
        self.search_var = ctk.StringVar()
        ctk.CTkEntry(
            self.deleteuser_screen,
            textvariable=self.search_var,
            placeholder_text="Buscar usuario...",
            width=400
        ).pack(pady=10)
        
        columns = ("ID", "Nombre", "Username", "Rol", "Fecha Creación")
        self.delete_tree = ttk.Treeview(
            self.deleteuser_screen,
            columns=columns,
            show="headings",
            height=10,
            selectmode="extended"
        )
        
        for col in columns:
            self.delete_tree.heading(col, text=col)
            self.delete_tree.column(col, width=100)
            
        self.delete_tree.pack(fill="both", expand=True, padx=10)
        
        scrollbar = ttk.Scrollbar(self.deleteuser_screen, orient="vertical", command=self.delete_tree.yview)
        self.delete_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        ctk.CTkButton(
            self.deleteuser_screen,
            text="Eliminar Seleccionados",
            command=self.delete_selected_users,
            fg_color="#f44336",
            hover_color="#da190b"
        ).pack(pady=10)

    def delete_selected_users(self):
        selected_items = self.delete_tree.selection()
        if not selected_items:
            messagebox.showwarning("Advertencia", "Seleccione al menos un usuario")
            return

        user_ids = [self.delete_tree.item(item)["values"][0] for item in selected_items]

        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                # Usamos IN para eliminar múltiples usuarios
                format_strings = ','.join(['%s'] * len(user_ids))
                query = f"DELETE FROM Users WHERE id_user IN ({format_strings})"
                cursor.execute(query, tuple(user_ids))
            connection.commit()

            # Recargar lista de usuarios después de eliminar
            self.load_user()
            self.update_delete_list()
            messagebox.showinfo("Éxito", f"{len(user_ids)} usuarios eliminados")

        except Exception as e:
            print(f"Error al eliminar usuarios: {e}")
            Error(self, "Error al eliminar usuarios de la base de datos.")
        finally:
            connection.close()

    def update_delete_list(self):
        self.delete_tree.delete(*self.delete_tree.get_children())
        for user in self.users:
            self.delete_tree.insert("", "end", values=(
                user["id_user"],
                user["name"],
                user["username"],
                user["role"],
                user["created_at"]
            ))

    def create_view_users_ui(self):
        self.load_user()
        columns = ("ID", "Nombre", "Username", "Rol", "Fecha Creación")
        self.view_tree = ttk.Treeview(
            self.viewuser_screen,
            columns=columns,
            show="headings",
            height=15
        )
        
        col_widths = [50, 150, 100, 100, 150]
        for col, width in zip(columns, col_widths):
            self.view_tree.heading(col, text=col)
            self.view_tree.column(col, width=width, anchor="center")
            
        self.view_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.view_tree.bind("<Double-1>", self.load_user_for_edit)
        
        scrollbar = ttk.Scrollbar(self.viewuser_screen, orient="vertical", command=self.view_tree.yview)
        self.view_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def load_user_for_edit(self, event):
        selected = self.view_tree.selection()
        if selected:
            user_id = self.view_tree.item(selected[0])["values"][0]
            self.current_user = next((u for u in self.users if u["id_user"] == user_id), None)
            if self.current_user:
                self.edit_entries["nombre completo"].insert(0, self.current_user["name"])
                self.edit_entries["username"].insert(0, self.current_user["username"])
                self.edit_role_combobox.set(self.current_user["role"])
                self.show_update_user()

    def update_view_list(self):
        self.view_tree.delete(*self.view_tree.get_children())
        for user in self.users:
            self.view_tree.insert("", "end", values=(
                user["id_user"],
                user["name"],
                user["username"],
                user["role"],
                user["created_at"]
            ))

    def show_screen(self, screen):
        for s in [self.adduser_screen, self.updateuser_screen, 
                self.deleteuser_screen, self.viewuser_screen]:
            s.pack_forget()
        screen.pack(fill="both", expand=True)

    def show_add_user(self): 
        self.clear_add_fields()
        self.show_screen(self.adduser_screen)

    def show_update_user(self): 
        self.show_screen(self.updateuser_screen)

    def show_delete_user(self): 
        self.update_delete_list()
        self.show_screen(self.deleteuser_screen)

    def show_view_users(self): 
        self.update_view_list()
        self.show_screen(self.viewuser_screen)

    def search_users(self):
        query = self.search_var.get().lower()
        filtered = [
            u for u in self.users
            if query in str(u["id_user"]).lower() or
               query in u["name"].lower() or
               query in u["username"].lower() or
               query in u["role"].lower()
        ]
        self.update_delete_list(filtered)

    def validate_full_name(self, name):
        if not name.strip():
            return "El nombre no puede estar vacío"
        if len(name) > 100:
            return "El nombre no puede exceder 100 caracteres"
        if not all(c.isalpha() or c.isspace() for c in name):
            return "Solo se permiten letras y espacios"
        if len(name.split()) < 2:
            return "Debe ingresar al menos nombre y apellido"
        return None
    
    def validate_username(self, username):
        if not username.strip():
            return "El username no puede estar vacío"
        if len(username) < 4:
            return "El username debe tener al menos 4 caracteres"
        if len(username) > 50:
            return "El username no puede exceder 50 caracteres"
        if not username.isalnum():
            return "Solo se permiten caracteres alfanuméricos (a-z, 0-9)"
        return None
    
    def validate_password(self, password):
        if len(password) < 6:
            return "La contraseña debe tener al menos 6 caracteres"
        if not any(c.isupper() for c in password):
            return "La contraseña debe contener al menos una mayúscula"
        if not any(c.isdigit() for c in password):
            return "La contraseña debe contener al menos un número"
        return None
    
    def validate_role(self, role):
        valid_roles = ["Administrador", "Medico", "Patologo", "Forense"]
        if role not in valid_roles:
            return "Rol no válido"
        return None
       