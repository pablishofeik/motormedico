import customtkinter as ctk
from tkinter import ttk, messagebox
from conection import ConectionDB
from ErrorPopUp import Error

class TestManager(ctk.CTkFrame):
    def __init__(self, master, return_menu):
        super().__init__(master)
        self.return_menu = return_menu
        
        # Datos de ejemplo
        self.patients = []
        
        # Pruebas asociadas a pacientes {patient_id: {lab: [], postmortem: []}}
        self.tests = {
            1: {
                "lab": [
                    {"id": 1, "type": "Biometría Hemática", "Glóbulos rojos": "4.5", "Glóbulos blancos": "6000"}
                ],
                "postmortem": []
            }
        }

        self.load_patients()
        
        self.current_patient = None
        self.current_test = None
        self.current_type = "Laboratorio"
        
        self.create_patient_selector()
        self.create_main_interface()
        self.create_edit_interface()
        
        
        self.show_patient_selection_screen()

    def load_patients(self):
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                # Ajusta la consulta a tu tabla y campos
                query = "SELECT * FROM Patient"
                cursor.execute(query)
                resultados = cursor.fetchall()

        except Exception as e:
            print(f"Error durante la consulta: {e}")
            Error(self, "Error al consultar la base de datos.")
        finally:
            connection.close()

        # Datos de ejemplo
        self.patients = [
            {
                "id_patient": row[0],
                "name": row[1],
                "birth_date": row[2].strftime("%Y-%m-%d %H:%M:%S"),
                "gender": row[3],
                "address": row[4],
                "phone": row[5]
            }
            for row in resultados
        ]
    
    def create_patient_selector(self):
        # Frame para selección de paciente
        self.patient_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        title = ctk.CTkLabel(self.patient_frame, text="Seleccionar Paciente", font=("Arial", 20, "bold"))
        title.pack(pady=20)
        
        # Buscador
        search_frame = ctk.CTkFrame(self.patient_frame)
        search_frame.pack(pady=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar por nombre o ID", width=300)
        self.search_entry.pack(side="left", padx=10)
        
        ctk.CTkButton(search_frame, text="Buscar", command=self.search_patient).pack(side="left")
        
        # Lista de pacientes
        self.patient_list = ctk.CTkScrollableFrame(self.patient_frame, width=400, height=200)
        self.patient_list.pack(pady=10)
        
        # Botón de regreso
        ctk.CTkButton(self.patient_frame, text="Regresar", command=self.return_menu).pack(pady=10)

    def search_patient(self):
        query = self.search_entry.get().lower()
        for widget in self.patient_list.winfo_children():
            widget.destroy()
            
        for patient in self.patients:
            if query in str(patient["id_patient"]) or query in patient["name"].lower():
                btn = ctk.CTkButton(
                    self.patient_list,
                    text=f"{patient['id_patient']} - {patient['name']}",
                    command=lambda p=patient: self.select_patient(p)
                )
                btn.pack(pady=2, fill="x")

    def select_patient(self, patient):
        self.current_patient = patient
        self.show_main_screen()

    def create_main_interface(self):
        # Frame principal de pruebas
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        # Selector de tipo de prueba
        type_frame = ctk.CTkFrame(self.main_frame)
        type_frame.pack(pady=10)
        
        ctk.CTkLabel(type_frame, text="Tipo de prueba:").pack(side="left")
        self.type_var = ctk.StringVar(value="Laboratorio")
        type_menu = ctk.CTkOptionMenu(type_frame, variable=self.type_var,
                                    values=["Laboratorio", "Post-mortem"],
                                    command=self.switch_type)
        type_menu.pack(side="left", padx=10)
        
        # Botones de CRUD
        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="Nueva Prueba", command=self.new_test).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Editar", command=self.edit_test).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar", command=self.delete_test).pack(side="left", padx=5)
        
        # Listado de pruebas
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Tipo", "Detalles"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Detalles", text="Detalles")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botón de regreso
        ctk.CTkButton(self.main_frame, text="Regresar a Pacientes", command=self.show_patient_selection_screen).pack(pady=10)

    def create_edit_interface(self):
        # Frame de edición
        self.edit_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        # Cabecera
        header = ctk.CTkFrame(self.edit_frame)
        header.pack(fill="x", pady=10)
        ctk.CTkButton(header, text="Guardar", command=self.save_test).pack(side="left", padx=5)
        ctk.CTkButton(header, text="Cancelar", command=self.show_main_screen).pack(side="left", padx=5)
        
        # Formulario
        self.form = ctk.CTkScrollableFrame(self.edit_frame, width=700, height=400)
        self.form.pack(fill="both", expand=True, padx=20, pady=10)
        self.entries = {}

    def switch_type(self, value):
        self.current_type = value
        self.update_list()

    def show_patient_selection_screen(self):
        self.current_patient = None
        self.main_frame.pack_forget()
        self.edit_frame.pack_forget()
        self.patient_frame.pack(fill="both", expand=True)
        self.search_patient()

    def show_main_screen(self):
        self.patient_frame.pack_forget()
        self.edit_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.update_list()

    def show_edit_screen(self):
        self.main_frame.pack_forget()
        self.edit_frame.pack(fill="both", expand=True)
        self.load_test_data()

    def update_list(self):
        self.tree.delete(*self.tree.get_children())
        if not self.current_patient:
            return
            
        tests = self.tests.get(self.current_patient["id"], {}).get("lab" if self.current_type == "Laboratorio" else "postmortem", [])
        
        for test in tests:
            details = ", ".join([f"{k}: {v}" for k, v in test.items() if k not in ["id", "type"]])
            self.tree.insert("", "end", values=(test["id"], test.get("type", ""), details))

    def new_test(self):
        if not self.current_patient:
            messagebox.showwarning("Error", "Seleccione un paciente primero")
            return
            
        self.current_test = None
        self.show_edit_screen()

    def edit_test(self):
        if not self.current_patient:
            messagebox.showwarning("Error", "Seleccione un paciente primero")
            return
            
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione una prueba")
            return
            
        test_id = self.tree.item(selected[0])["values"][0]
        tests = self.tests[self.current_patient["id"]]["lab" if self.current_type == "Laboratorio" else "postmortem"]
        self.current_test = next(t for t in tests if t["id"] == test_id)
        self.show_edit_screen()

    def delete_test(self):
        selected = self.tree.selection()
        if not selected:
            return
            
        test_id = self.tree.item(selected[0])["values"][0]
        tests = self.tests[self.current_patient["id"]]["lab" if self.current_type == "Laboratorio" else "postmortem"]
        self.tests[self.current_patient["id"]]["lab" if self.current_type == "Laboratorio" else "postmortem"] = [t for t in tests if t["id"] != test_id]
        self.update_list()

    def load_test_data(self):
        for widget in self.form.winfo_children():
            widget.destroy()
        self.entries.clear()
        
        if self.current_type == "Laboratorio":
            tabview = ctk.CTkTabview(self.form, width=600)
            tabview.pack(fill="both", expand=True)

            lab_tests = {
                "Biometría Hemática": ["Glóbulos rojos", "Glóbulos blancos", "Hemoglobina", "Hematocrito", "Plaquetas"],
                "Química Sanguínea": ["Glucosa", "Urea", "Creatinina", "Colesterol", "Triglicéridos"],
                "Orina": ["Color", "Densidad", "pH", "Proteínas", "Glucosa en orina"],
                "Hepáticas": ["Bilirrubina", "AST", "ALT", "Fosfatasa alcalina"],
                "Tiroideas": ["T3", "T4", "TSH"]
            }

            row_limit = 5
            for test_name, fields in lab_tests.items():
                tab = tabview.add(test_name)
                for i, field in enumerate(fields):
                    label = ctk.CTkLabel(tab, text=field + ":")
                    label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
                    entry = ctk.CTkEntry(tab, width=250)
                    entry.grid(row=i, column=1, padx=10, pady=5)
                    self.entries[field] = entry
        else:
            # Campos para post-mortem sin pestañas
            fields = [
                "Observaciones patológicas", "Estado de órganos", "Causa de muerte",
                "Hora estimada de muerte", "Signos de trauma"
            ]
            for i, field in enumerate(fields):
                label = ctk.CTkLabel(self.form, text=field + ":")
                label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
                entry = ctk.CTkEntry(self.form, width=500)
                entry.grid(row=i, column=1, padx=10, pady=5)
                self.entries[field] = entry
                    

    def save_test(self):
        if not self.current_patient:
            return
            
        test_data = {
            "id": self.current_test["id"] if self.current_test else self.get_next_id(),
            "type": self.current_type
        }
        
        for key, entry in self.entries.items():
            test_data[key] = entry.get()
            
        if self.current_patient["id"] not in self.tests:
            self.tests[self.current_patient["id"]] = {"lab": [], "postmortem": []}
            
        tests = self.tests[self.current_patient["id"]]["lab" if self.current_type == "Laboratorio" else "postmortem"]
        
        if self.current_test:
            index = next(i for i, t in enumerate(tests) if t["id"] == self.current_test["id"])
            tests[index] = test_data
        else:
            tests.append(test_data)
            
        self.show_main_screen()

    def get_next_id(self):
        tests = self.tests.get(self.current_patient["id"], {}).get("lab" if self.current_type == "Laboratorio" else "postmortem", [])
        return max((t["id"] for t in tests), default=0) + 1