import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from image_file import find_image

class Product(ctk.CTkFrame):
    def __init__(self, master, return_menu):
        super().__init__(master)
        self.return_menu = return_menu
        self.current_patient = None

        # Configuración principal
        self.main_frame = ctk.CTkFrame(self, width=1024, height=600, corner_radius=0, fg_color="#969696")
        self.main_frame.pack(fill="both", expand=True)

        # Frame superior
        self.top_frame = ctk.CTkFrame(self.main_frame, width=1024, height=50, fg_color="#FFFFFF")
        self.top_frame.pack(fill="x", expand=False)

        # Frames para diferentes pantallas
        self.addpatient_screen = ctk.CTkFrame(self.main_frame, fg_color="#969696")
        self.deletepatient_screen = ctk.CTkFrame(self.main_frame, fg_color="#969696")
        self.updatepatient_screen = ctk.CTkFrame(self.main_frame, fg_color="#969696")
        self.viewpatient_screen = ctk.CTkFrame(self.main_frame, fg_color="#969696")

        # Botones de CRUD
        self.create_crud_buttons()
        self.create_bottom_buttons()

        # Datos de ejemplo
        self.patients = [
            {
                "id_patient": 1,
                "name": "Juan Pérez",
                "birth_date": "1990-05-15",
                "gender": "Masculino",
                "address": "Calle Falsa 123",
                "phone": "555-1234567"
            }
        ]

        # Configurar pantallas
        self.create_add_patient_ui()
        self.create_delete_patient_ui()
        self.create_update_patient_ui()
        self.create_view_patient_ui()

        self.show_view_patients()

    def create_crud_buttons(self):
        icons = [
            ("add.png", "Agregar Paciente", self.show_add_patient),
            ("delete.png", "Eliminar Paciente", self.show_delete_patient),
            ("update.png", "Editar Paciente", self.show_update_patient),
            ("view.png", "Ver Pacientes", self.show_view_patients)
        ]

        x_pos = 20
        for icon_name, tooltip, command in icons:
            img = find_image(f"images/{icon_name}", 30)
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
            self.main_frame,
            text="",
            image=return_img,
            width=30,
            height=20,
            fg_color="#FFFFFF",
            command=self.return_menu
        ).place(x=20, y=560)

    def create_add_patient_ui(self):
        fields = [
            ("Nombre Completo:", 80, 50),
            ("Fecha Nacimiento (AAAA-MM-DD):", 80, 130),
            ("Género:", 80, 210),
            ("Dirección:", 80, 290),
            ("Teléfono:", 80, 370)
        ]

        self.add_entries = {}
        for text, x, y in fields:
            label = ctk.CTkLabel(self.addpatient_screen, text=text, font=("Arial", 16), text_color="#000000")
            label.place(x=x, y=y)
            
            entry = ctk.CTkEntry(self.addpatient_screen, width=300, height=40, fg_color="#FFFFFF")
            entry.place(x=x, y=y+30)
            self.add_entries[text.split(":")[0].strip().lower()] = entry

        # Combobox para género
        self.gender_combobox = ctk.CTkComboBox(
            self.addpatient_screen,
            values=["Masculino", "Femenino", "Otro"],
            width=300,
            height=40
        )
        self.gender_combobox.place(x=80, y=250)

        ctk.CTkButton(
            self.addpatient_screen,
            text="Guardar Paciente",
            command=self.save_patient,
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).place(x=400, y=450)

    def save_patient(self):
        patient_data = {
            "name": self.add_entries["nombre completo"].get(),
            "birth_date": self.add_entries["fecha nacimiento (aaaa-mm-dd)"].get(),
            "gender": self.gender_combobox.get(),
            "address": self.add_entries["dirección"].get(),
            "phone": self.add_entries["teléfono"].get()
        }

        # Validaciones
        if not all(patient_data.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
            
        try:
            datetime.strptime(patient_data["birth_date"], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD")
            return

        # Generar ID
        patient_data["id_patient"] = max(p["id_patient"] for p in self.patients) + 1 if self.patients else 1
        
        self.patients.append(patient_data)
        messagebox.showinfo("Éxito", "Paciente registrado correctamente")
        self.show_view_patients()

    def create_delete_patient_ui(self):
        # Configuración de búsqueda
        self.search_var = ctk.StringVar()
        ctk.CTkEntry(
            self.deletepatient_screen,
            textvariable=self.search_var,
            placeholder_text="Buscar paciente...",
            width=400
        ).pack(pady=10)
        
        # Configuración de la tabla
        columns = ("ID", "Nombre", "Fecha Nacimiento", "Género", "Teléfono")
        self.tree = ttk.Treeview(self.deletepatient_screen, columns=columns, show="headings", height=10)
        
        col_widths = [50, 150, 120, 80, 120]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.deletepatient_screen, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Botón de eliminación
        ctk.CTkButton(
            self.deletepatient_screen,
            text="Eliminar Seleccionados",
            command=self.delete_selected_patients,
            fg_color="#f44336",
            hover_color="#da190b"
        ).pack(pady=10)

    def delete_selected_patients(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Advertencia", "Seleccione al menos un paciente")
            return
            
        patient_ids = [self.tree.item(item)["values"][0] for item in selected_items]
        self.patients = [p for p in self.patients if p["id_patient"] not in patient_ids]
        self.update_patient_list()
        messagebox.showinfo("Éxito", f"{len(patient_ids)} pacientes eliminados")

    def create_update_patient_ui(self):
        fields = [
            ("Nombre Completo:", 80, 50),
            ("Fecha Nacimiento (AAAA-MM-DD):", 80, 130),
            ("Género:", 80, 210),
            ("Dirección:", 80, 290),
            ("Teléfono:", 80, 370)
        ]

        self.update_entries = {}
        for text, x, y in fields:
            label = ctk.CTkLabel(self.updatepatient_screen, text=text, font=("Arial", 16), text_color="#000000")
            label.place(x=x, y=y)
            
            entry = ctk.CTkEntry(self.updatepatient_screen, width=300, height=40, fg_color="#FFFFFF")
            entry.place(x=x, y=y+30)
            self.update_entries[text.split(":")[0].strip().lower()] = entry

        self.update_gender_combobox = ctk.CTkComboBox(
            self.updatepatient_screen,
            values=["Masculino", "Femenino", "Otro"],
            width=300,
            height=40
        )
        self.update_gender_combobox.place(x=80, y=250)

        ctk.CTkButton(
            self.updatepatient_screen,
            text="Actualizar Paciente",
            command=self.update_patient,
            fg_color="#2196F3",
            hover_color="#1976D2"
        ).place(x=400, y=450)

    def update_patient(self):
        if not self.current_patient:
            messagebox.showerror("Error", "Seleccione un paciente primero")
            return
            
        updated_data = {
            "name": self.update_entries["nombre completo"].get(),
            "birth_date": self.update_entries["fecha nacimiento (aaaa-mm-dd)"].get(),
            "gender": self.update_gender_combobox.get(),
            "address": self.update_entries["dirección"].get(),
            "phone": self.update_entries["teléfono"].get()
        }

        # Validaciones
        if not all(updated_data.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
            
        try:
            datetime.strptime(updated_data["birth_date"], "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use AAAA-MM-DD")
            return

        # Actualizar paciente
        for patient in self.patients:
            if patient["id_patient"] == self.current_patient["id_patient"]:
                patient.update(updated_data)
                break
        
        messagebox.showinfo("Éxito", "Paciente actualizado correctamente")
        self.show_view_patients()

    def create_view_patient_ui(self):
        columns = ("ID", "Nombre", "Fecha Nacimiento", "Género", "Dirección", "Teléfono")
        self.view_tree = ttk.Treeview(self.viewpatient_screen, columns=columns, show="headings", height=15)
        
        col_widths = [50, 150, 120, 80, 200, 120]
        for col, width in zip(columns, col_widths):
            self.view_tree.heading(col, text=col)
            self.view_tree.column(col, width=width, anchor="w")
        
        self.view_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.view_tree.bind("<Double-1>", self.load_patient_for_edit)
        
        scrollbar = ttk.Scrollbar(self.viewpatient_screen, orient="vertical", command=self.view_tree.yview)
        self.view_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def load_patient_for_edit(self, event):
        selected = self.view_tree.selection()
        if selected:
            patient_id = self.view_tree.item(selected[0])["values"][0]
            self.current_patient = next((p for p in self.patients if p["id_patient"] == patient_id), None)
            if self.current_patient:
                self.update_entries["nombre completo"].insert(0, self.current_patient["name"])
                self.update_entries["fecha nacimiento (aaaa-mm-dd)"].insert(0, self.current_patient["birth_date"])
                self.update_gender_combobox.set(self.current_patient["gender"])
                self.update_entries["dirección"].insert(0, self.current_patient["address"])
                self.update_entries["teléfono"].insert(0, self.current_patient["phone"])
                self.show_update_patient()

    def update_patient_list(self):
        self.tree.delete(*self.tree.get_children())
        for patient in self.patients:
            self.tree.insert("", "end", values=(
                patient["id_patient"],
                patient["name"],
                patient["birth_date"],
                patient["gender"],
                patient["phone"]
            ))

    def update_view_list(self):
        self.view_tree.delete(*self.view_tree.get_children())
        for patient in self.patients:
            self.view_tree.insert("", "end", values=(
                patient["id_patient"],
                patient["name"],
                patient["birth_date"],
                patient["gender"],
                patient["address"],
                patient["phone"]
            ))

    def show_screen(self, screen):
        screens = [self.addpatient_screen, self.deletepatient_screen, 
                 self.updatepatient_screen, self.viewpatient_screen]
        for s in screens:
            s.pack_forget()
        screen.pack(fill="both", expand=True)

    def show_add_patient(self): self.show_screen(self.addpatient_screen)
    def show_delete_patient(self): 
        self.update_patient_list()
        self.show_screen(self.deletepatient_screen)
    def show_update_patient(self): self.show_screen(self.updatepatient_screen)
    def show_view_patients(self): 
        self.update_view_list()
        self.show_screen(self.viewpatient_screen)
        
