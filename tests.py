import customtkinter as ctk
from tkinter import ttk,messagebox
from datetime import datetime
from conection import ConectionDB
from ErrorPopUp import Error
import re

class TestManager(ctk.CTkFrame):
    def __init__(self, master, return_menu):
        super().__init__(master)
        self.return_menu = return_menu
        
        # Datos actuales
        self.current_patient = None
        self.current_consultation = None
        self.current_test_type = "Laboratorio"  # Valor por defecto
        self.patients = []
        
        # Estructura de datos para pruebas
        self.static_tests = {
            "Biometría Hemática": ["Glóbulos rojos", "Glóbulos blancos", "Hemoglobina", "Hematocrito", "Plaquetas"],
            "Química Sanguínea": ["Glucosa", "Urea", "Creatinina", "Colesterol", "Triglicéridos"],
            "Orina": ["Color", "Densidad", "pH", "Proteínas", "Glucosa en orina"],
            "Hepáticas": ["Bilirrubina", "AST", "ALT", "Fosfatasa alcalina"],
            "Tiroideas": ["T3", "T4", "TSH"]
        }
        
        # Mapeo de parámetros a IDs (debe coincidir con tu BD)
        self.parameter_ids = {
            "Glóbulos rojos": 1, "Glóbulos blancos": 2, "Hemoglobina": 3,
            "Hematocrito": 4, "Plaquetas": 5, "Glucosa": 6, "Urea": 7,
            "Creatinina": 8, "Colesterol": 9, "Triglicéridos": 10,
            "Color": 11, "Densidad": 12, "pH": 13, "Proteínas": 14,
            "Glucosa en orina": 15, "Bilirrubina": 16, "AST": 17,
            "ALT": 18, "Fosfatasa alcalina": 19, "T3": 20, "T4": 21, "TSH": 22
        }
        
        # Inicializar interfaces
        self.create_patient_selector()
        self.create_main_interface()
        self.create_edit_interface()
        
        # Mostrar pantalla inicial
        self.show_patient_selection_screen()
        self.load_patients()

    # --------------------------
    # Métodos de inicialización
    # --------------------------
    
    def create_patient_selector(self):
        """Crea la interfaz para selección de paciente"""
        self.patient_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        # Título
        ctk.CTkLabel(self.patient_frame, text="Seleccionar Paciente", 
                    font=("Arial", 20, "bold")).pack(pady=20)
        
        # Buscador
        search_frame = ctk.CTkFrame(self.patient_frame)
        search_frame.pack(pady=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, 
                                      placeholder_text="Buscar por nombre o ID", 
                                      width=300)
        self.search_entry.pack(side="left", padx=10)
        
        ctk.CTkButton(search_frame, text="Buscar", 
                     command=self.search_patient).pack(side="left")
        
        # Lista de pacientes
        self.patient_list = ctk.CTkScrollableFrame(self.patient_frame, 
                                                 width=400, height=200)
        self.patient_list.pack(pady=10)
        
        # Botón de regreso
        ctk.CTkButton(self.patient_frame, text="Regresar", 
                     command=self.return_menu).pack(pady=10)

    def create_main_interface(self):
        """Crea la pantalla principal con lista de exámenes"""
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        # Selector de consulta
        consultation_frame = ctk.CTkFrame(self.main_frame)
        consultation_frame.pack(pady=10)
        
        ctk.CTkLabel(consultation_frame, text="Consulta:").pack(side="left")
        self.consultation_selector = ctk.CTkOptionMenu(
            consultation_frame,
            command=self.select_consultation,
            values=[]
        )
        self.consultation_selector.pack(side="left", padx=10)
        
        # Selector de tipo de prueba
        type_frame = ctk.CTkFrame(self.main_frame)
        type_frame.pack(pady=10)
        
        ctk.CTkLabel(type_frame, text="Tipo de prueba:").pack(side="left")
        self.type_var = ctk.StringVar(value="Laboratorio")
        type_menu = ctk.CTkOptionMenu(type_frame, variable=self.type_var,
                                    values=["Laboratorio", "Post-mortem"],
                                    command=self.switch_test_type)
        type_menu.pack(side="left", padx=10)
        
        # Botones CRUD
        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="Nueva Prueba", 
                     command=self.new_test).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Editar", 
                     command=self.edit_test).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Eliminar", 
                     command=self.delete_test).pack(side="left", padx=5)
        
        # Listado de pruebas (Treeview)
        self.create_results_treeview()
        
        # Botón de regreso
        ctk.CTkButton(self.main_frame, text="Regresar", 
                     command=self.show_patient_selection_screen).pack(pady=10)

    def create_results_treeview(self):
        """Crea el Treeview para mostrar los resultados"""
        self.tree = ttk.Treeview(self.main_frame, 
                               columns=("Test", "Parámetros"), 
                               show="headings")
        self.tree.heading("Test", text="Tipo de Prueba")
        self.tree.heading("Parámetros", text="Resultados")
        self.tree.column("Test", width=200)
        self.tree.column("Parámetros", width=400)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def create_edit_interface(self):
        """Crea la pantalla de edición/creación de exámenes"""
        self.edit_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        # Cabecera con botones
        header = ctk.CTkFrame(self.edit_frame)
        header.pack(fill="x", pady=10)
        
        ctk.CTkButton(header, text="Guardar", 
                     command=self.save_test).pack(side="left", padx=5)
        ctk.CTkButton(header, text="Cancelar", 
                     command=self.show_main_screen).pack(side="left", padx=5)
        
        # Crear pestañas de pruebas
        self.create_test_tabs()

    def create_test_tabs(self):
        """Crea las pestañas para los diferentes tipos de pruebas"""
        self.tabview = ctk.CTkTabview(self.edit_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.entries = {}  # Diccionario para almacenar los campos de entrada
        
        # Crear una pestaña para cada tipo de prueba
        for test_name, parameters in self.static_tests.items():
            tab = self.tabview.add(test_name)
            
            # Crear campos para cada parámetro
            for i, param in enumerate(parameters):
                ctk.CTkLabel(tab, text=f"{param}:").grid(
                    row=i, column=0, padx=10, pady=5, sticky="w")
                
                entry = ctk.CTkEntry(tab)
                entry.grid(row=i, column=1, padx=10, pady=5)
                
                self.entries[param] = entry

    # --------------------------
    # Lógica de negocio
    # --------------------------
    
    def load_patients(self):
        """Carga la lista de pacientes desde la base de datos"""
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                query = "SELECT id_patient, name, birth_date FROM Patient"
                cursor.execute(query)
                self.patients = [
                    {"id_patient": row[0], "name": row[1], "birth_date": row[2]}
                    for row in cursor.fetchall()
                ]

        except Exception as e:
            print(f"Error durante la consulta: {e}")
            Error(self, "Error al consultar la base de datos.")
        finally:
            connection.close()

    def search_patient(self):
        """Filtra la lista de pacientes según el término de búsqueda"""
        query = self.search_entry.get().lower()
        for widget in self.patient_list.winfo_children():
            widget.destroy()

        for patient in self.patients:
            if (query in str(patient["id_patient"]) or 
                query in patient["name"].lower()):
                
                btn = ctk.CTkButton(
                    self.patient_list,
                    text=f"{patient['id_patient']} - {patient['name']}",
                    command=lambda p=patient: self.select_patient(p)
                )
                btn.pack(pady=2, fill="x")

    def select_patient(self, patient):
        """Establece el paciente actual y carga sus consultas"""
        self.current_patient = patient
        self.load_consultations()
        self.show_main_screen()

    def load_consultations(self):
        """Carga las consultas del paciente actual"""
        if not self.current_patient:
            return
            
        db = ConectionDB()
        connection = db.connect()
        if connection is None:
            Error(self, "Error de conexión a la base de datos")
            return
            
        try:
            with connection.cursor() as cursor:  
                query = """
                    SELECT id_consultation, consultation_date, notes 
                    FROM Consultation 
                    WHERE id_patient = %s
                    ORDER BY consultation_date DESC
                """
                cursor.execute(query, (self.current_patient['id_patient'],))
                self.consultations = cursor.fetchall()
                
                options = [f"{c[0]} - {c[1].strftime('%Y-%m-%d')}" 
                          for c in self.consultations]
                self.consultation_selector.configure(values=options)
                
                if options:
                    self.consultation_selector.set(options[0])
                    self.select_consultation(options[0])
                else:
                    self.consultation_selector.set("No hay consultas")
                    self.current_consultation = None
                    
        except Exception as e:
            print(f"Error cargando consultas: {e}")
            Error(self, "Error al cargar consultas")
        finally:
            connection.close()

    def select_consultation(self, selected_consultation):
        """Establece la consulta actual y actualiza la lista de exámenes"""
        if selected_consultation == "No hay consultas":
            self.current_consultation = None
            return
            
        consultation_id = int(selected_consultation.split(" - ")[0])
        
        for c in self.consultations:
            if c[0] == consultation_id:
                self.current_consultation = {
                    "id_consultation": c[0],
                    "consultation_date": c[1],
                    "notes": c[2]
                }
                break
        
        self.update_test_list()

    def switch_test_type(self, selected_type):
        """Cambia entre pruebas de laboratorio y post-mortem"""
        self.current_test_type = selected_type
        self.update_test_list()

    def update_test_list(self):
        """Actualiza la lista de exámenes según el tipo seleccionado"""
        self.tree.delete(*self.tree.get_children())
        
        if not self.current_consultation:
            return
            
        if self.current_test_type == "Laboratorio":
            self.load_lab_tests()
        else:
            self.load_postmortem_tests()

    def load_lab_tests(self):
        """Carga los exámenes de laboratorio para la consulta actual"""
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "Error de conexión a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        lt.test_name,
                        ltp.parameter_name,
                        cltr.result_value
                    FROM consultation_labtest_result cltr
                    JOIN LabTest_Parameter ltp ON cltr.id_parameter = ltp.id_parameter
                    JOIN LabTest lt ON ltp.id_lab_test = lt.id_lab_test
                    WHERE cltr.id_consultation = %s
                """
                cursor.execute(query, (self.current_consultation['id_consultation'],))
                resultados = cursor.fetchall()

                # Agrupar resultados por nombre de prueba
                grouped_results = {}
                for row in resultados:
                    test_name = row[0]
                    if test_name not in grouped_results:
                        grouped_results[test_name] = []
                    grouped_results[test_name].append(f"{row[1]}: {row[2]}")

                # Mostrar en el Treeview
                for test, params in grouped_results.items():
                    self.tree.insert("", "end", values=(test, ", ".join(params)))

        except Exception as e:
            print(f"Error cargando resultados: {e}")
            Error(self, "Error al cargar pruebas de laboratorio")
        finally:
            connection.close()

    def load_postmortem_tests(self):
        """Carga los exámenes post-mortem para la consulta actual"""
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "Error de conexión a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                        pt.test_name,
                        ptp.parameter_name,
                        cptr.result_value
                    FROM Consultation_PostMortemTest_Result cptr
                    JOIN PostMortemTest_Parameter ptp ON cptr.id_parameter = ptp.id_parameter
                    JOIN PostMortemTest pt ON ptp.id_postmortem_test = pt.id_postmortem_test
                    WHERE cptr.id_consultation = %s
                """
                cursor.execute(query, (self.current_consultation['id_consultation'],))
                resultados = cursor.fetchall()

                # Agrupar resultados por nombre de prueba
                grouped_results = {}
                for row in resultados:
                    test_name = row[0]
                    if test_name not in grouped_results:
                        grouped_results[test_name] = []
                    grouped_results[test_name].append(f"{row[1]}: {row[2]}")

                # Mostrar en el Treeview
                for test, params in grouped_results.items():
                    self.tree.insert("", "end", values=(test, ", ".join(params)))

        except Exception as e:
            print(f"Error cargando resultados post-mortem: {e}")
            Error(self, "Error al cargar resultados post-mortem")
        finally:
            connection.close()

    # --------------------------
    # Manejo de pantallas
    # --------------------------
    
    def show_patient_selection_screen(self):
        """Muestra la pantalla de selección de paciente"""
        self.current_patient = None
        self.current_consultation = None
        self.main_frame.pack_forget()
        self.edit_frame.pack_forget()
        self.patient_frame.pack(fill="both", expand=True)
        self.search_patient()

    def show_main_screen(self):
        """Muestra la pantalla principal con la lista de exámenes"""
        self.patient_frame.pack_forget()
        self.edit_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.update_test_list()

    def show_edit_screen(self, test_type=None, existing_values=None):
        """Muestra la pantalla de edición/creación"""
        self.main_frame.pack_forget()
        self.patient_frame.pack_forget()
        self.edit_frame.pack(fill="both", expand=True)
        
        # Limpiar todos los campos
        for entry in self.entries.values():
            entry.delete(0, 'end')
        
        # Establecer pestaña activa si se especificó un tipo
        if test_type:
            for tab_name in self.static_tests.keys():
                if test_type.lower() in tab_name.lower():
                    self.tabview.set(tab_name)
                    break
        
        # Cargar valores existentes si los hay
        if existing_values:
            self.load_existing_values(existing_values)

    def load_existing_values(self, existing_values):
        """Carga valores existentes en los campos del formulario"""
        for param_name, value in existing_values.items():
            if param_name in self.entries:
                self.entries[param_name].delete(0, 'end')
                self.entries[param_name].insert(0, value)

    # --------------------------
    # CRUD de exámenes
    # --------------------------
    
    def new_test(self):
        """Prepara la pantalla para crear un nuevo examen"""
        if not self.current_consultation:
            messagebox.showwarning("Error", "Seleccione una consulta primero")
            return
        
        self.show_edit_screen()

    def edit_test(self):
        """Prepara la pantalla para editar un examen existente"""
        if not self.current_consultation:
            messagebox.showwarning("Error", "Seleccione una consulta primero")
            return
            
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione una prueba a editar")
            return
        
        # Obtener nombre de la prueba seleccionada
        test_name = self.tree.item(selected[0])["values"][0]
        
        test_type = None
        for tab_name, params in self.static_tests.items():
                for param in params:
                    if re.search(r'\b' + re.escape(param) + r'\b', test_name):  # Coincide palabras completas
                        test_type = tab_name
                        break
                if test_type:
                    break
        
        # Cargar valores existentes
        db = ConectionDB()
        connection = db.connect()
        if connection is None:
            Error(self, "Error de conexión")
            return
        
        try:
            with connection.cursor() as cursor:
                # Obtener parámetros de esta prueba
                cursor.execute("""
                    SELECT ltp.parameter_name, cltr.result_value 
                    FROM consultation_labtest_result cltr
                    JOIN LabTest_Parameter ltp ON cltr.id_parameter = ltp.id_parameter
                    WHERE cltr.id_consultation = %s
                """, (self.current_consultation['id_consultation'],))
                
                existing_values = {row[0]: row[1] for row in cursor.fetchall()}
                
                # Mostrar pantalla de edición
                self.show_edit_screen(test_type=test_type, existing_values=existing_values)
                
        except Exception as e:
            print(f"Error cargando datos: {e}")
            Error(self, "Error al cargar prueba para edición")
        finally:
            connection.close()

    def delete_test(self):
        """Elimina el examen seleccionado"""
        selected = self.tree.selection()
        if not selected:
            return
            
        test_name = self.tree.item(selected[0])["values"][0]
        
        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la prueba {test_name}?"):
            return
        
        db = ConectionDB()
        connection = db.connect()
        if connection is None:
            Error(self, "Error de conexión")
            return
        
        try:
            with connection.cursor() as cursor:
                # Eliminar todos los parámetros de esta prueba
                cursor.execute("""
                    DELETE FROM consultation_labtest_result
                    WHERE id_consultation = %s
                    AND id_parameter IN (
                        SELECT id_parameter FROM LabTest_Parameter
                        WHERE parameter_name IN %s
                    )
                """, (self.current_consultation['id_consultation'], 
                     tuple(self.get_parameters_for_test(test_name))))
                
                connection.commit()
                messagebox.showinfo("Éxito", "Prueba eliminada correctamente")
                self.update_test_list()
                
        except Exception as e:
            print(f"Error eliminando prueba: {e}")
            connection.rollback()
            Error(self, "Error al eliminar la prueba")
        finally:
            connection.close()

    def get_parameters_for_test(self, test_name):
        """Obtiene los parámetros asociados a un tipo de prueba"""
        for tab_name, params in self.static_tests.items():
            if any(param in test_name for param in params):
                return params
        return []

    def save_test(self):
        """Guarda los resultados del examen (nuevo o editado)"""
        if not self.current_consultation:
            return
        
        # Obtener la pestaña activa (tipo de prueba)
        active_tab = self.tabview.get()
        
        if not active_tab:
            messagebox.showwarning("Error", "Seleccione un tipo de prueba")
            return
        
        # Validar que al menos un campo tenga valor
        has_data = any(
            entry.get().strip() 
            for param in self.static_tests[active_tab] 
            if (entry := self.entries.get(param))
        )
        
        if not has_data:
            messagebox.showwarning("Error", "Ingrese al menos un resultado")
            return
        
        db = ConectionDB()
        connection = db.connect()
        if not connection:
            return
        
        try:
            with connection.cursor() as cursor:
                # Eliminar resultados existentes de este tipo de prueba
                cursor.execute("""
                    DELETE FROM consultation_labtest_result
                    WHERE id_consultation = %s
                    AND id_parameter IN (
                        SELECT id_parameter FROM LabTest_Parameter
                        WHERE parameter_name IN %s
                    )
                """, (self.current_consultation['id_consultation'], 
                     tuple(self.static_tests[active_tab])))
                
                # Insertar nuevos resultados
                for param_name in self.static_tests[active_tab]:
                    entry = self.entries.get(param_name)
                    value = entry.get().strip() if entry else ""
                    
                    if value:  # Solo guardar si hay valor
                        cursor.execute("""
                            INSERT INTO consultation_labtest_result 
                            (id_consultation, id_parameter, result_value, date_recorded)
                            VALUES (%s, %s, %s, %s)
                        """, (
                            self.current_consultation['id_consultation'],
                            self.parameter_ids[param_name],
                            value,
                            datetime.now()
                        ))
                
                connection.commit()
                messagebox.showinfo("Éxito", "Resultados guardados correctamente")
                self.show_main_screen()
                
        except Exception as e:
            print(f"Error guardando resultados: {e}")
            connection.rollback()
            Error(self, f"Error al guardar los resultados: {str(e)}")
        finally:
            connection.close()