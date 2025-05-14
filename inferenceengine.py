import customtkinter as ctk
from tkinter import ttk, messagebox
from conection import ConectionDB
from ErrorPopUp import Error
import math
from datetime import datetime

class InferenceEngine(ctk.CTkFrame):
    def __init__(self, master, return_menu):
        super().__init__(master)
        self.return_menu = return_menu
        
        # Configuración inicial
        self.current_patient = None
        self.current_consultation = None
        self.patients = []
        self.consultations = []
        self.diseases = []
        self.analysis_results = []

        self.symptom_dict = {}
        self.sign_dict = {}
        
        # Estilo
        ctk.set_appearance_mode("light")
        self.configure(fg_color="#ffffff")
        
        # Crear interfaces
        self.create_patient_selection()
        self.create_consultation_selection()
        self.create_analysis_display()
        
        # Cargar datos iniciales
        self.load_patients()
        self.load_diseases()
        self.load_data()

        # Mostrar pantalla inicial
        self.show_patient_selection()

    def create_patient_selection(self):
        """Interfaz para selección de paciente"""
        self.patient_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        # Barra de herramientas
        toolbar = ctk.CTkFrame(self.patient_frame, fg_color="#f8f9fa", height=40)
        toolbar.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkButton(toolbar, text="Regresar", width=80, command=self.return_menu).pack(side="left", padx=5)
        
        # Búsqueda
        self.search_patient_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(toolbar, textvariable=self.search_patient_var, 
                                   placeholder_text="Buscar paciente...", width=250)
        search_entry.pack(side="right", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.update_patient_list())
        
        # Listado de pacientes
        self.patient_tree = ttk.Treeview(self.patient_frame, columns=("ID", "Nombre", "Edad", "Género", "Teléfono"), 
                                       show="headings", style="Custom.Treeview")
        self.patient_tree.heading("ID", text="ID")
        self.patient_tree.heading("Nombre", text="Nombre")
        self.patient_tree.heading("Edad", text="Edad")
        self.patient_tree.heading("Género", text="Género")
        self.patient_tree.heading("Teléfono", text="Teléfono")
        self.patient_tree.column("ID", width=50, anchor="center")
        self.patient_tree.column("Nombre", width=200)
        self.patient_tree.column("Edad", width=80, anchor="center")
        self.patient_tree.column("Género", width=100, anchor="center")
        self.patient_tree.column("Teléfono", width=120, anchor="center")
        self.patient_tree.bind("<Double-1>", lambda e: self.select_patient())
        self.patient_tree.pack(fill="both", expand=True, padx=10, pady=5)

    def create_consultation_selection(self):
        """Interfaz para selección de consulta"""
        self.consultation_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        # Barra de herramientas
        toolbar = ctk.CTkFrame(self.consultation_frame, fg_color="#f8f9fa", height=40)
        toolbar.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkButton(toolbar, text="Regresar", width=80, command=self.show_patient_selection).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Analizar", width=80, command=self.show_analysis).pack(side="left", padx=5)
        
        # Info paciente
        self.patient_info_label = ctk.CTkLabel(toolbar, text="", anchor="w")
        self.patient_info_label.pack(side="left", padx=10, fill="x", expand=True)
        
        # Listado de consultas
        self.consultation_tree = ttk.Treeview(self.consultation_frame, 
                                            columns=("ID", "Fecha", "Notas", "Síntomas", "Signos", "Análisis"), 
                                            show="headings", style="Custom.Treeview")
        self.consultation_tree.heading("ID", text="ID")
        self.consultation_tree.heading("Fecha", text="Fecha")
        self.consultation_tree.heading("Notas", text="Notas")
        self.consultation_tree.heading("Síntomas", text="Síntomas")
        self.consultation_tree.heading("Signos", text="Signos")
        self.consultation_tree.heading("Análisis", text="Análisis")
        self.consultation_tree.column("ID", width=50, anchor="center")
        self.consultation_tree.column("Fecha", width=100, anchor="center")
        self.consultation_tree.column("Notas", width=200)
        self.consultation_tree.column("Síntomas", width=150)
        self.consultation_tree.column("Signos", width=150)
        self.consultation_tree.column("Análisis", width=100, anchor="center")
        self.consultation_tree.bind("<Double-1>", lambda e: self.show_analysis())
        self.consultation_tree.pack(fill="both", expand=True, padx=10, pady=5)

    def create_analysis_display(self):
        """Interfaz para mostrar resultados de análisis"""
        self.analysis_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        # Barra de herramientas
        toolbar = ctk.CTkFrame(self.analysis_frame, fg_color="#f8f9fa", height=40)
        toolbar.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkButton(toolbar, text="Regresar", width=80, command=self.show_consultation_selection).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Guardar", width=80, command=self.save_analysis).pack(side="left", padx=5)
        
        # Info consulta
        self.consultation_info_label = ctk.CTkLabel(toolbar, text="", anchor="w")
        self.consultation_info_label.pack(side="left", padx=10, fill="x", expand=True)
        
        # Contenedor principal
        main_container = ctk.CTkFrame(self.analysis_frame, fg_color="#ffffff")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sección de síntomas y signos
        data_frame = ctk.CTkFrame(main_container)
        data_frame.pack(fill="x", pady=5)
        
        # Síntomas
        symptoms_frame = ctk.CTkFrame(data_frame)
        symptoms_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(symptoms_frame, text="Síntomas reportados", font=("Arial", 12, "bold")).pack()
        self.symptoms_text = ctk.CTkTextbox(symptoms_frame, height=150, wrap="word")
        self.symptoms_text.pack(fill="both", expand=True)
        
        # Signos
        signs_frame = ctk.CTkFrame(data_frame)
        signs_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(signs_frame, text="Signos encontrados", font=("Arial", 12, "bold")).pack()
        self.signs_text = ctk.CTkTextbox(signs_frame, height=150, wrap="word")
        self.signs_text.pack(fill="both", expand=True)
        
        # Resultados de análisis
        results_frame = ctk.CTkFrame(main_container)
        results_frame.pack(fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(results_frame, text="Resultados del Análisis", font=("Arial", 14, "bold")).pack()
        
        self.results_container = ctk.CTkScrollableFrame(results_frame, height=200)
        self.results_container.pack(fill="both", expand=True)
        
        # Advertencia si no hay coincidencias
        self.warning_label = ctk.CTkLabel(results_frame, text="", text_color="red")
        self.warning_label.pack()

    def load_patients(self):
        """Carga la lista de pacientes desde la base de datos, calculando la edad a partir de birth_date"""
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_patient, name, birth_date, gender, phone 
                    FROM Patient 
                    ORDER BY name
                """)
                self.patients = []
                for row in cursor.fetchall():
                    id_patient, name, birth_date, gender, phone = row
                    
                    # Calcular edad si hay fecha de nacimiento
                    age = self.calculate_age(birth_date) if birth_date else "N/A"
                    
                    self.patients.append({
                        "id": id_patient,
                        "name": name,
                        "birth_date": birth_date,
                        "age": age,
                        "gender": gender,
                        "phone": phone
                    })
        except Exception as e:
            print(f"Error cargando pacientes: {e}")
            Error(self, "Error al cargar pacientes")
        finally:
            connection.close()

        self.update_patient_list()

    def calculate_age(self, birth_date):
        """Calcula la edad basándose en la fecha de nacimiento"""
        today = datetime.now()
        
        # Manejar diferentes formatos de fecha
        if isinstance(birth_date, str):
            try:
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return "N/A"
        elif isinstance(birth_date, datetime):
            pass
        else:
            return "N/A"
            
        age = today.year - birth_date.year
        
        # Ajustar si aún no ha pasado el cumpleaños este año
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        return age

    def load_consultations(self, patient_id):
        """Carga las consultas de un paciente con información de síntomas, signos y resultados de laboratorio"""
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                # Consulta principal para obtener información básica de consultas
                query = """
                    SELECT 
                        c.id_consultation, 
                        DATE_FORMAT(c.consultation_date, '%%d/%%m/%%Y') as formatted_date,
                        c.notes,
                        GROUP_CONCAT(DISTINCT s.symptom_name SEPARATOR ', ') AS symptoms,
                        GROUP_CONCAT(DISTINCT sg.sign_name SEPARATOR ', ') AS signs,
                        CASE 
                            WHEN EXISTS (
                                SELECT 1 FROM Consultation_LabTest_Result 
                                WHERE id_consultation = c.id_consultation
                            ) THEN 'Con resultados'
                            ELSE 'Sin resultados'
                        END AS lab_status
                    FROM Consultation c
                    LEFT JOIN Consultation_Symptom cs ON c.id_consultation = cs.id_consultation
                    LEFT JOIN Symptom s ON cs.id_symptom = s.id_symptom
                    LEFT JOIN Consultation_Sign csg ON c.id_consultation = csg.id_consultation
                    LEFT JOIN Sign sg ON csg.id_sign = sg.id_sign
                    WHERE c.id_patient = %s
                    GROUP BY c.id_consultation
                    ORDER BY c.consultation_date DESC
                """
                cursor.execute(query, (patient_id,))
                
                self.consultations = [
                    {
                        "id": row[0],
                        "date": row[1],
                        "notes": row[2] if row[2] else "Sin notas",
                        "symptoms": row[3] if row[3] else "Ninguno",
                        "signs": row[4] if row[4] else "Ninguno",
                        "analysis": row[5]  # Usamos el estado de laboratorio como "análisis"
                    }
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            print(f"Error cargando consultas: {e}")
            Error(self, "Error al cargar consultas")
        finally:
            connection.close()

        self.update_consultation_list()

    def load_diseases(self):
        """Carga las enfermedades con sus síntomas y signos asociados"""
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                # Consulta optimizada para obtener enfermedades con síntomas y signos
                query = """
                    SELECT 
                        d.id_disease, 
                        d.name, 
                        d.description,
                        GROUP_CONCAT(DISTINCT s.id_symptom) AS symptom_ids,
                        GROUP_CONCAT(DISTINCT s.symptom_name) AS symptom_names,
                        GROUP_CONCAT(DISTINCT sg.id_sign) AS sign_ids,
                        GROUP_CONCAT(DISTINCT sg.sign_name) AS sign_names
                    FROM Disease d
                    LEFT JOIN Disease_Symptom ds ON d.id_disease = ds.id_disease
                    LEFT JOIN Symptom s ON ds.id_symptom = s.id_symptom
                    LEFT JOIN Disease_Sign dsg ON d.id_disease = dsg.id_disease
                    LEFT JOIN Sign sg ON dsg.id_sign = sg.id_sign
                    GROUP BY d.id_disease
                    ORDER BY d.name
                """
                cursor.execute(query)
                self.diseases = [
                    {
                        "id": row[0],
                        "name": row[1],
                        "description": row[2],
                        "symptom_ids": [int(id) for id in row[3].split(',')] if row[3] else [],
                        "symptom_names": row[4].split(',') if row[4] else [],
                        "sign_ids": [int(id) for id in row[5].split(',')] if row[5] else [],
                        "sign_names": row[6].split(',') if row[6] else []
                    }
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            print(f"Error cargando enfermedades: {e}")
            Error(self, "Error al cargar enfermedades")
        finally:
            connection.close()

    def load_consultation_details(self, consultation_id):
        """Carga los detalles completos de una consulta incluyendo resultados de laboratorio"""
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return None

        try:
            with connection.cursor() as cursor:
                # Obtener síntomas
                cursor.execute("""
                    SELECT s.id_symptom, s.symptom_name, cs.intensity, cs.duration
                    FROM Consultation_Symptom cs
                    JOIN Symptom s ON cs.id_symptom = s.id_symptom
                    WHERE cs.id_consultation = %s
                """, (consultation_id,))
                symptoms = [{
                    "id": row[0], 
                    "name": row[1],
                    "intensity": row[2],
                    "duration": row[3]
                } for row in cursor.fetchall()]
                
                # Obtener signos
                cursor.execute("""
                    SELECT s.id_sign, s.sign_name, cs.value, cs.severity
                    FROM Consultation_Sign cs
                    JOIN Sign s ON cs.id_sign = s.id_sign
                    WHERE cs.id_consultation = %s
                """, (consultation_id,))
                signs = [{
                    "id": row[0], 
                    "name": row[1],
                    "value": row[2],
                    "severity": row[3]
                } for row in cursor.fetchall()]
                
                # Obtener resultados de laboratorio
                cursor.execute("""
                    SELECT ltr.id_parameter, lp.parameter_name, ltr.result_value, lp.unit
                    FROM Consultation_LabTest_Result ltr
                    JOIN LabTest_Parameter lp ON ltr.id_parameter = lp.id_parameter
                    WHERE ltr.id_consultation = %s
                """, (consultation_id,))
                lab_results = [{
                    "parameter": row[1],
                    "value": row[2],
                    "unit": row[3]
                } for row in cursor.fetchall()]
                
                return {
                    "symptoms": symptoms,
                    "signs": signs,
                    "lab_results": lab_results
                }
        except Exception as e:
            print(f"Error cargando detalles de consulta: {e}")
            return None
        finally:
            connection.close()


    def update_patient_list(self):
        """Actualiza la lista de pacientes mostrada"""
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
        
        search_term = self.search_patient_var.get().lower()
        
        for patient in self.patients:
            if search_term in patient['name'].lower():
                self.patient_tree.insert("", "end", values=(
                    patient['id'],
                    patient['name'],
                    patient['age'],
                    patient['gender'],
                    patient['phone']
                ))

    def update_consultation_list(self):
        """Actualiza la lista de consultas mostrada"""
        for item in self.consultation_tree.get_children():
            self.consultation_tree.delete(item)
        
        for consultation in self.consultations:
            self.consultation_tree.insert("", "end", values=(
                consultation['id'],
                consultation['date'],
                consultation['notes'],
                consultation['symptoms'],
                consultation['signs']
            ))

    def show_patient_selection(self):
        """Muestra la pantalla de selección de paciente"""
        self.consultation_frame.pack_forget()
        self.analysis_frame.pack_forget()
        self.patient_frame.pack(fill="both", expand=True)
        self.update_patient_list()

    def show_consultation_selection(self):
        """Muestra la pantalla de selección de consulta"""
        self.patient_frame.pack_forget()
        self.analysis_frame.pack_forget()
        self.consultation_frame.pack(fill="both", expand=True)
        
        if self.current_patient:
            patient = next(p for p in self.patients if p['id'] == self.current_patient)
            self.patient_info_label.configure(
                text=f"Paciente: {patient['name']} | Edad: {patient['age']} | Género: {patient['gender']}"
            )
        
        self.update_consultation_list()

    def show_analysis(self):
        """Muestra la pantalla de análisis"""
        selected = self.consultation_tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione una consulta primero")
            return
            
        self.current_consultation = self.consultation_tree.item(selected[0])['values'][0]
        consultation_details = self.load_consultation_details(self.current_consultation)
        
        if not consultation_details:
            Error(self, "Error al cargar detalles de la consulta")
            return
        
        # Mostrar pantalla de análisis
        self.patient_frame.pack_forget()
        self.consultation_frame.pack_forget()
        self.analysis_frame.pack(fill="both", expand=True)
        
        # Actualizar información de la consulta
        consultation = next(c for c in self.consultations if c['id'] == self.current_consultation)
        patient = next(p for p in self.patients if p['id'] == self.current_patient)
        self.consultation_info_label.configure(
            text=f"Consulta del {consultation['date']} - Paciente: {patient['name']}"
        )
        
        # Mostrar síntomas y signos
        self.symptoms_text.delete("1.0", "end")
        self.symptoms_text.insert("1.0", "\n".join([s['name'] for s in consultation_details['symptoms']]))
        
        self.signs_text.delete("1.0", "end")
        self.signs_text.insert("1.0", "\n".join([s['name'] for s in consultation_details['signs']]))
        
        # Realizar inferencia
        self.perform_inference(consultation_details)

    def perform_inference(self, consultation_details):
        """Realiza el análisis de inferencia considerando síntomas, signos y resultados de laboratorio"""
        # Limpiar resultados anteriores
        for widget in self.results_container.winfo_children():
            widget.destroy()

        self.warning_label.configure(text="")

        # Obtener datos de la consulta
        consultation_symptoms = {s['id'] for s in consultation_details['symptoms']}
        consultation_signs = {s['id'] for s in consultation_details['signs']}
        lab_results = consultation_details.get('lab_results', [])

        # Variables para resultados
        disease_matches = []

        for disease in self.diseases:
            disease_symptoms = set(disease['symptom_ids'])
            disease_signs = set(disease['sign_ids'])

            # Coincidencias
            symptom_intersection = consultation_symptoms.intersection(disease_symptoms)
            sign_intersection = consultation_signs.intersection(disease_signs)

            # Cálculo de scores
            symptom_score = len(symptom_intersection) / len(disease_symptoms) if disease_symptoms else 0
            sign_score = len(sign_intersection) / len(disease_signs) if disease_signs else 0
            lab_score = self.calculate_lab_match_score(disease['id'], lab_results)

            total_score = 0.7 * symptom_score + 0.2 * sign_score + 0.1 * lab_score

            if total_score > 0:
                matched_symptoms = [self.symptom_dict[sid] for sid in symptom_intersection]
                matched_signs = [self.sign_dict[sid] for sid in sign_intersection]

                disease_matches.append({
                    "id": disease['id'],
                    "name": disease['name'],
                    "description": disease['description'],
                    "score": total_score,
                    "matched_symptoms": matched_symptoms,
                    "matched_signs": matched_signs
                })

        # Ordenar por puntaje
        disease_matches.sort(key=lambda x: x['score'], reverse=True)

        # Top 3 con al menos 95%
        top_diseases = [d for d in disease_matches if d['score'] >= 0.95][:3]

        if not top_diseases:
            self.warning_label.configure(
                text="Advertencia: No se encontraron enfermedades con probabilidad ≥95%. Se recomienda análisis adicional."
            )
            top_diseases = disease_matches[:3]

        # Mostrar resultados
        for i, disease in enumerate(top_diseases, 1):
            frame = ctk.CTkFrame(self.results_container, fg_color="#f8f9fa", corner_radius=5)
            frame.pack(fill="x", pady=5, padx=5)

            header = ctk.CTkFrame(frame, fg_color="transparent")
            header.pack(fill="x")

            ctk.CTkLabel(header, text=f"{i}. {disease['name']}", font=("Arial", 12, "bold")).pack(side="left")

            progress_frame = ctk.CTkFrame(header, fg_color="transparent")
            progress_frame.pack(side="right", padx=10)

            ctk.CTkLabel(progress_frame, text=f"{disease['score']*100:.1f}%").pack(side="left", padx=5)
            progress = ctk.CTkProgressBar(progress_frame, width=100)
            progress.pack(side="left")
            progress.set(disease['score'])

            desc_frame = ctk.CTkFrame(frame, fg_color="transparent")
            desc_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(desc_frame, text=disease['description'], wraplength=600, justify="left").pack(anchor="w")

            data_frame = ctk.CTkFrame(frame, fg_color="transparent")
            data_frame.pack(fill="x", pady=5)

            symptoms_frame = ctk.CTkFrame(data_frame)
            symptoms_frame.pack(side="left", fill="x", expand=True, padx=5)
            ctk.CTkLabel(symptoms_frame, text="Síntomas coincidentes:").pack(anchor="w")
            for symptom in disease['matched_symptoms']:
                ctk.CTkLabel(symptoms_frame, text=f"- {symptom}", justify="left").pack(anchor="w")

            signs_frame = ctk.CTkFrame(data_frame)
            signs_frame.pack(side="left", fill="x", expand=True, padx=5)
            ctk.CTkLabel(signs_frame, text="Signos coincidentes:").pack(anchor="w")
            for sign in disease['matched_signs']:
                ctk.CTkLabel(signs_frame, text=f"- {sign}", justify="left").pack(anchor="w")

    def select_patient(self):
        """Selecciona un paciente para ver sus consultas"""
        selected = self.patient_tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un paciente primero")
            return
            
        self.current_patient = self.patient_tree.item(selected[0])['values'][0]
        self.load_consultations(self.current_patient)
        self.show_consultation_selection()

    def save_analysis(self):
        
        """Guarda el análisis realizado en la base de datos"""
        if not self.current_consultation:
            messagebox.showwarning("Error", "No hay consulta seleccionada")
            return
        
        # Obtener el mejor diagnóstico (primero en la lista)
        results = self.results_container.winfo_children()
        if not results:
            messagebox.showwarning("Error", "No hay resultados para guardar")
            return
        
        # El primer frame contiene el mejor diagnóstico
        best_match_frame = results[0]
        widgets = best_match_frame.winfo_children()
        
        # El primer widget es el header que contiene el nombre
        header = widgets[0]
        disease_name = header.winfo_children()[0].cget("text").split(". ")[1]
        
        # El segundo widget es el progress_frame que contiene el porcentaje
        progress_frame = widgets[1]
        percentage = float(progress_frame.winfo_children()[0].cget("text").replace("%", ""))
        
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                # Verificar si ya existe un análisis para esta consulta
                cursor.execute("SELECT id_analysis FROM Analysis WHERE id_consultation = %s", (self.current_consultation,))
                existing = cursor.fetchone()
                
                if existing:
                    # Actualizar análisis existente
                    query = """
                        UPDATE Analysis 
                        SET diagnosis = %s, probability = %s, analysis_date = CURRENT_DATE
                        WHERE id_consultation = %s
                    """
                    cursor.execute(query, (disease_name, percentage/100, self.current_consultation))
                else:
                    # Insertar nuevo análisis
                    query = """
                        INSERT INTO Analysis (id_consultation, diagnosis, probability, analysis_date)
                        VALUES (%s, %s, %s, CURRENT_DATE)
                    """
                    cursor.execute(query, (self.current_consultation, disease_name, percentage/100))
                
                connection.commit()
                messagebox.showinfo("Éxito", "Análisis guardado correctamente")
                
                # Actualizar lista de consultas
                self.load_consultations(self.current_patient)
                
        except Exception as e:
            print(f"Error al guardar análisis: {e}")
            Error(self, "No se pudo guardar el análisis")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()

    def load_data(self):
        """Carga todos los síntomas y signos desde la base de datos"""
        db = ConectionDB()
        connection = db.connect()

        all_symptoms = []
        all_signs = []

        try:
            with connection.cursor() as cursor:
                # Cargar síntomas
                cursor.execute("SELECT id_symptom, symptom_name FROM Symptom")
                symptoms = cursor.fetchall()
                all_symptoms = [{"id": row[0], "name": row[1]} for row in symptoms]

                # Cargar signos
                cursor.execute("SELECT id_sign, sign_name FROM Sign")
                signs = cursor.fetchall()
                all_signs = [{"id": row[0], "name": row[1]} for row in signs]

        except Exception as e:
            print("Error al cargar síntomas y signos:", e)
        finally:
            connection.close()

        # Guardar en diccionarios para acceso rápido
        self.symptom_dict = {s['id']: s['name'] for s in all_symptoms}
        self.sign_dict = {s['id']: s['name'] for s in all_signs}

    def calculate_lab_match_score(self, disease_id, lab_results):
        """Calcula el porcentaje de coincidencia con patrones de laboratorio esperados"""
        if not lab_results:
            return 0
        
        db = ConectionDB()
        connection = db.connect()
        
        try:
            with connection.cursor() as cursor:
                # Obtener los patrones esperados para esta enfermedad
                cursor.execute("""
                    SELECT lp.id_parameter, dlp.expected_pattern
                    FROM Disease_LabParameter dlp
                    JOIN LabTest_Parameter lp ON dlp.id_parameter = lp.id_parameter
                    WHERE dlp.id_disease = %s
                """, (disease_id,))
                expected_patterns = {row[0]: row[1] for row in cursor.fetchall()}
                
                if not expected_patterns:
                    return 0
                    
                # Comparar con los resultados reales
                matches = 0
                for result in lab_results:
                    param_id = result['id_parameter']
                    if param_id in expected_patterns:
                        # Aquí deberías implementar una lógica más sofisticada para comparar
                        # los valores reales con los patrones esperados
                        matches += 1
                
                return matches / len(expected_patterns)
                
        except Exception as e:
            print(f"Error calculando coincidencia de laboratorio: {e}")
            return 0
        finally:
            connection.close()