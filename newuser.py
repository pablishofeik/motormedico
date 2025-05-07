import customtkinter as ctk
from image_file import find_image
from tkinter import ttk, messagebox
from datetime import datetime  # Para manejar created_at

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

        # Datos de ejemplo
        self.users = [
            {
                "id_user": 1,
                "name": "Admin",
                "username": "admin",
                "role": "Administrador",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "password": "admin123"
            }
        ]
        
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
        icons = [
            ("add.png", "Agregar Usuario", self.show_add_user),
            ("delete.png", "Eliminar Usuario", self.show_delete_user),
            ("update.png", "Editar Usuario", self.show_update_user),
            ("view.png", "Ver Usuarios", self.show_view_users)
        ]

        x_pos = 20
        for icon, tooltip, command in icons:
            img = find_image(f"images/{icon}", 30)
            btn = ctk.CTkButton(
                self.top_frame,
                text="",
                image=img,
                width=30,
                height=30,
                fg_color="#FFFFFF",
                command=command
            )
            btn.place(x=x_pos, y=10)
            x_pos += 45

    def create_bottom_buttons(self):
        return_img = find_image("images/return.png", 30)
        ctk.CTkButton(
            self.bottom_frame,
            text="",
            image=return_img,
            width=30,
            height=20,
            fg_color="#FFFFFF",
            command=self.return_menu
        ).place(x=20, y=15)

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
            values=["Administrador", "Usuario", "Supervisor"],
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

    def save_user(self):
        password = self.add_entries["contraseña"].get()
        confirm_password = self.add_entries["confirmar contraseña"].get()
        
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
            
        user_data = {
            "name": self.add_entries["nombre completo"].get(),
            "username": self.add_entries["username"].get(),
            "password": password,  # Deberías hashear aquí
            "role": self.role_combobox.get(),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if not all(user_data.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
            
        if any(u["username"] == user_data["username"] for u in self.users):
            messagebox.showerror("Error", "El nombre de usuario ya existe")
            return
            
        user_data["id_user"] = max(u["id_user"] for u in self.users) + 1 if self.users else 1
        self.users.append(user_data)
        self.clear_add_fields()
        messagebox.showinfo("Éxito", "Usuario creado correctamente")
        self.show_view_users()

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
            values=["Administrador", "Usuario", "Supervisor"],
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
        if not self.current_user:
            messagebox.showerror("Error", "Seleccione un usuario primero")
            return
            
        new_password = self.edit_entries["contraseña"].get()
        confirm_password = self.edit_entries["confirmar contraseña"].get()
        
        if new_password and new_password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
            
        updated_data = {
            "name": self.edit_entries["nombre completo"].get(),
            "username": self.edit_entries["username"].get(),
            "role": self.edit_role_combobox.get()
        }
        
        if new_password:
            updated_data["password"] = new_password
            
        if not all([updated_data["name"], updated_data["username"], updated_data["role"]]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
            
        if updated_data["username"] != self.current_user["username"]:
            if any(u["username"] == updated_data["username"] for u in self.users):
                messagebox.showerror("Error", "El nombre de usuario ya existe")
                return

        for user in self.users:
            if user["id_user"] == self.current_user["id_user"]:
                user.update(updated_data)
                break
                
        self.clear_edit_fields()
        messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
        self.show_view_users()

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
        self.users = [u for u in self.users if u["id_user"] not in user_ids]
        self.update_delete_list()
        messagebox.showinfo("Éxito", f"{len(user_ids)} usuarios eliminados")

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