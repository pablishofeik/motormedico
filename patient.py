import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from image_file import find_image
from conection import ConectionDB
from ErrorPopUp import Error
from datetime import datetime

class PatientManager(ctk.CTkFrame):
    def __init__(self, master, return_menu):
        super().__init__(master)
        self.return_menu = return_menu
        self.current_patient = None
        self.current_consultation = None
        
        # Datos de ejemplo
        self.patients = []
        self.consultations = []
        self.signs = [
            {"id": 1, "name": "Presión arterial", "unit": "mmHg"},
            {"id": 2, "name": "Frecuencia cardíaca", "unit": "lpm"}
        ]
        self.symptoms = [
            {"id": 1, "name": "Dolor de cabeza"},
            {"id": 2, "name": "Mareos"}
        ]
        
        # Configuración de la interfaz
        self.main_frame = ctk.CTkFrame(self, width=1024, height=600, fg_color="#ffffff")
        self.main_frame.pack(fill="both", expand=True)
        
        self.create_interfaces()
        self.load_patients()
        self.show_view_patients()

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

    def create_interfaces(self):
        # Frame superior con botones
        self.top_frame = ctk.CTkFrame(self.main_frame, height=50, fg_color="#f8f9fa")
        self.top_frame.pack(fill="x", pady=5, padx=10)
        
        # Botones principales
        self.create_crud_buttons()
        
        # Crear todas las pantallas
        self.create_add_patient_ui()
        self.create_delete_patient_ui()
        self.create_update_patient_ui()
        self.create_view_patient_ui()
        self.create_consultation_ui()
        
        # Botón de regreso
        self.create_bottom_buttons()

    def create_crud_buttons(self):
        ctk.CTkButton(self.top_frame, text="Nuevo", width=80, command=self.show_add_patient).pack(side="left", padx=5)
        ctk.CTkButton(self.top_frame, text="Editar", width=80, command=self.show_update_patient).pack(side="left", padx=5)
        ctk.CTkButton(self.top_frame, text="Eliminar", width=80, command=self.show_delete_patient).pack(side="left", padx=5)
        ctk.CTkButton(self.top_frame, text="Ver", width=80, command=self.show_view_patients).pack(side="left", padx=5)
        ctk.CTkButton(self.top_frame, text="Nueva Consulta", width=80, command=self.show_consultation).pack(side="left", padx=5)

    # Métodos para mostrar las diferentes pantallas
    def show_add_patient(self):
        self.show_screen(self.addpatient_screen)
        
    def show_delete_patient(self):
        self.show_screen(self.deletepatient_screen)
        self.load_patients_to_delete()
        
    def show_update_patient(self):
        self.show_screen(self.updatepatient_screen)
        self.load_patients_to_update()
        
    def show_view_patients(self):
        self.show_screen(self.viewpatient_screen)
        self.load_patients()
        self.load_patients_to_view()
        
    def show_consultation(self):
        selected = self.view_tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un paciente primero")
            return
            
        patient_id = self.view_tree.item(selected[0])["values"][0]
        self.current_patient = next(p for p in self.patients if p["id_patient"] == patient_id)
        
        # Limpiar campos anteriores
        for widget in self.signs_container.winfo_children():
            widget.destroy()
        for widget in self.symptoms_container.winfo_children():
            widget.destroy()
        
        self.show_screen(self.consultation_screen)

    def show_screen(self, screen):
        screens = [
            self.addpatient_screen, 
            self.deletepatient_screen,
            self.updatepatient_screen,
            self.viewpatient_screen,
            self.consultation_screen
        ]
        for s in screens:
            s.pack_forget()
        screen.pack(fill="both", expand=True)

    def create_add_patient_ui(self):
        self.addpatient_screen = ctk.CTkFrame(self.main_frame, fg_color="#ffffff")
        
        fields = [
            ("Nombre Completo:", 80, 50),
            ("Fecha Nacimiento (AAAA-MM-DD):", 80, 130),
            ("Dirección:", 80, 290),
            ("Teléfono:", 80, 370)
        ]

        self.add_entries = {}
        for text, x, y in fields:
            label = ctk.CTkLabel(self.addpatient_screen, text=text, font=("Arial", 16), text_color="#000000")
            label.place(x=x, y=y)
            
            entry = ctk.CTkEntry(self.addpatient_screen, width=300, height=40, fg_color="#FFFFFF")
            entry.place(x=x, y=y+30)
            
            # Usa el texto sin los espacios y los dos puntos para las claves
            field_key = text.split(":")[0].strip().lower()
            self.add_entries[field_key] = entry

        # ComboBox para el género
        label = ctk.CTkLabel(self.addpatient_screen, text="Género:", font=("Arial", 16), text_color="#000000")
        label.place(x=80, y=210)

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
        ).place(x=800, y=20)

    def save_patient(self):
        # Obtener valores
        full_name = self.add_entries["nombre completo"].get().strip()
        birth_date = self.add_entries["fecha nacimiento (aaaa-mm-dd)"].get().strip()
        gender = self.gender_combobox.get()
        address = self.add_entries["dirección"].get().strip()
        phone = self.add_entries["teléfono"].get().strip()

        # Validar campos
        if error := self.validate_full_name(full_name):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_birth_date(birth_date):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_gender(gender):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_address(address):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_phone(phone):
            messagebox.showerror("Error", error)
            return

        # Resto del código de save_patient...
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO Patient (name, birth_date, gender, address, phone)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    full_name,
                    datetime.strptime(birth_date, "%Y-%m-%d"),
                    gender,
                    address,
                    phone
                ))
                connection.commit()
            messagebox.showinfo("Éxito", "Paciente guardado correctamente")
            self.show_view_patients()

        except Exception as e:
            print(f"Error al insertar paciente: {e}")
            messagebox.showerror("Error", f"No se pudo guardar el paciente: {str(e)}")
        finally:
            connection.close()
        self.load_patients()

    def create_delete_patient_ui(self):
        # Crear la pantalla de eliminación de pacientes
        self.deletepatient_screen = ctk.CTkFrame(self.main_frame, fg_color="#969696")
        
        # Treeview para mostrar pacientes
        self.delete_tree = ttk.Treeview(self.deletepatient_screen, columns=("ID", "Nombre", "Género"), show="headings")
        self.delete_tree.heading("ID", text="ID")
        self.delete_tree.heading("Nombre", text="Nombre")
        self.delete_tree.heading("Género", text="Género")
        self.delete_tree.place(x=50, y=50, width=800, height=400)
        
        # Botón de eliminar
        ctk.CTkButton(
            self.deletepatient_screen,
            text="Eliminar Paciente Seleccionado",
            command=self.delete_selected_patient,
            fg_color="#FF5252",
            hover_color="#FF0000"
        ).place(x=300, y=470)
        
        # Llamar a la función para cargar pacientes
        self.load_patients_to_delete()

    def load_patients_to_delete(self):
        # Eliminar las filas anteriores del Treeview
        for item in self.delete_tree.get_children():
            self.delete_tree.delete(item)
        
        # Insertar los pacientes en el Treeview
        for patient in self.patients:
            self.delete_tree.insert("", "end", values=(
                patient["id_patient"],
                patient["name"],
                patient["gender"]
            ))

    def delete_selected_patient(self):
        # Obtener el paciente seleccionado en el Treeview
        selected = self.delete_tree.selection()
        
        if not selected:
            messagebox.showwarning("Error", "Seleccione un paciente para eliminar")
            return
        
        # Obtener el ID del paciente seleccionado
        patient_id = self.delete_tree.item(selected[0])["values"][0]
        
        # Confirmar la eliminación
        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar el paciente con ID {patient_id}?")
        if confirm:
            # Eliminar el paciente de la lista
            self.patients = [p for p in self.patients if p["id_patient"] != patient_id]
            
            # Eliminar el paciente de la base de datos utilizando la conexión existente
            try:
                self.delete_patient_from_db(patient_id)
            except Exception as e:
                print(f"Error al eliminar el paciente de la base de datos: {e}")
                messagebox.showerror("Error", "No se pudo eliminar el paciente de la base de datos.")
                return
            
            # Actualizar la vista
            self.load_patients_to_delete()
            
            messagebox.showinfo("Éxito", "Paciente eliminado correctamente")

    def delete_patient_from_db(self, patient_id):
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                query = "DELETE FROM Patient WHERE id_patient = %s"
                cursor.execute(query, (patient_id,))
                connection.commit()
            connection.close()
        except Exception as e:
            print(f"Error al eliminar el paciente: {e}")
            raise

    def create_update_patient_ui(self):
        self.updatepatient_screen = ctk.CTkFrame(self.main_frame, fg_color="#969696")
        
        # Treeview para seleccionar paciente
        self.update_tree = ttk.Treeview(self.updatepatient_screen, columns=("ID", "Nombre"), show="headings")
        self.update_tree.heading("ID", text="ID")
        self.update_tree.heading("Nombre", text="Nombre")
        self.update_tree.place(x=50, y=50, width=500, height=400)
        
        # Frame para los campos de edición
        self.update_fields_frame = ctk.CTkFrame(self.updatepatient_screen, width=400, height=400)
        self.update_fields_frame.place(x=600, y=50)
        
        # Campos de edición
        fields = [
            ("Nombre Completo:", 10, 10),
            ("Fecha Nacimiento:", 10, 90),
            ("Género:", 10, 170),
            ("Dirección:", 10, 250),
            ("Teléfono:", 10, 330)
        ]
        
        self.update_entries = {}
        for text, x, y in fields:
            label = ctk.CTkLabel(self.update_fields_frame, text=text)
            label.place(x=x, y=y)
            
            entry = ctk.CTkEntry(self.update_fields_frame, width=300)
            entry.place(x=x, y=y+30)
            self.update_entries[text.split(":")[0].strip().lower()] = entry

        self.update_gender = ctk.CTkComboBox(
            self.update_fields_frame,
            values=["Masculino", "Femenino", "Otro"]
        )
        self.update_gender.place(x=10, y=200)
        
        # Botón de actualizar
        ctk.CTkButton(
            self.updatepatient_screen,
            text="Actualizar Paciente",
            command=self.update_patient_data,
            fg_color="#4CAF50"
        ).place(x=400, y=470)

    def load_patients_to_update(self):
        for item in self.update_tree.get_children():
            self.update_tree.delete(item)
            
        for patient in self.patients:
            self.update_tree.insert("", "end", values=(
                patient["id_patient"],
                patient["name"]
            ))
            
        self.update_tree.bind("<<TreeviewSelect>>", self.load_patient_to_edit)

    def load_patient_to_edit(self, event):
        selected = self.update_tree.selection()
        if not selected:
            return
        
        patient_id = self.update_tree.item(selected[0])["values"][0]
        patient = next(p for p in self.patients if p["id_patient"] == patient_id)
        
        self.update_entries["nombre completo"].delete(0, "end")
        self.update_entries["nombre completo"].insert(0, patient["name"])
        
        self.update_entries["fecha nacimiento"].delete(0, "end")
        self.update_entries["fecha nacimiento"].insert(0, patient["birth_date"])
        
        self.update_gender.set(patient["gender"])
        
        self.update_entries["dirección"].delete(0, "end")
        self.update_entries["dirección"].insert(0, patient["address"])
        
        self.update_entries["teléfono"].delete(0, "end")
        self.update_entries["teléfono"].insert(0, patient["phone"])

    def update_patient_data(self):
        selected = self.update_tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un paciente para editar")
            return
        
        patient_id = self.update_tree.item(selected[0])["values"][0]
        
        # Obtener valores
        full_name = self.update_entries["nombre completo"].get().strip()
        birth_date = self.update_entries["fecha nacimiento"].get().strip()
        gender = self.update_gender.get()
        address = self.update_entries["dirección"].get().strip()
        phone = self.update_entries["teléfono"].get().strip()

        # Validar campos
        if error := self.validate_full_name(full_name):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_birth_date(birth_date):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_gender(gender):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_address(address):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_phone(phone):
            messagebox.showerror("Error", error)
            return

        # Resto del código de update_patient_data...
        try:
            self.update_patient_in_db(patient_id, {
                "name": full_name,
                "birth_date": birth_date,
                "gender": gender,
                "address": address,
                "phone": phone
            })
            messagebox.showinfo("Éxito", "Paciente actualizado correctamente")
            self.show_view_patients()
        except Exception as e:
            print(f"Error al actualizar paciente: {e}")
            messagebox.showerror("Error", f"No se pudo actualizar el paciente: {str(e)}")

    def update_patient_in_db(self, patient_id, patient):
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
        
                query = """
                    UPDATE Patient 
                    SET name = %s, birth_date = %s, gender = %s, address = %s, phone = %s
                    WHERE id_patient = %s
                """
                cursor.execute(query, (
                    patient["name"], 
                    patient["birth_date"], 
                    patient["gender"], 
                    patient["address"], 
                    patient["phone"], 
                    patient_id
                ))
                connection.commit()
            connection.close()
        except Exception as e:
            print(f"Error al actualizar el paciente: {e}")
            raise

    def create_view_patient_ui(self):
        self.load_patients()
          # Crear la pantalla de visualización de pacientes
        self.viewpatient_screen = ctk.CTkFrame(self.main_frame, fg_color="#ffffff")

        # Treeview para mostrar pacientes
        columns = ("ID", "Nombre", "Género", "Teléfono", "Dirección")
        self.view_tree = ttk.Treeview(self.viewpatient_screen, columns=columns, show="headings")

        # Configurar las columnas del Treeview
        for col in columns:
            self.view_tree.heading(col, text=col)
            self.view_tree.column(col, width=150)

        # Colocar el Treeview en la interfaz
        self.view_tree.place(x=50, y=50, width=900, height=400)

        # Llamar a la función que actualiza los pacientes de inmediato al crear la pantalla
        self.load_patients_to_view()

    def load_patients_to_view(self):
        # Eliminar las filas anteriores del Treeview
        for item in self.view_tree.get_children():
            self.view_tree.delete(item)

        # Insertar los nuevos datos de pacientes
        for patient in self.patients:
            self.view_tree.insert("", "end", values=(
                patient["id_patient"],
                patient["name"],
                patient["gender"],
                patient["phone"],
                patient["address"]
            ))

    def create_consultation_ui(self):
        self.consultation_screen = ctk.CTkFrame(self.main_frame, fg_color="#969696")
        
        # Cabecera
        header = ctk.CTkFrame(self.consultation_screen, height=40, fg_color="#FFFFFF")
        header.pack(fill="x", pady=5)
        ctk.CTkButton(header, text="Guardar Consulta", command=self.save_consultation).pack(side="left", padx=5)
        ctk.CTkButton(header, text="Cancelar", command=self.show_view_patients).pack(side="left", padx=5)
        
        # Formulario principal
        form = ctk.CTkScrollableFrame(self.consultation_screen, width=900, height=500)
        form.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sección de Signos Vitales
        signs_frame = ctk.CTkFrame(form)
        signs_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(signs_frame, text="Signos Clínicos", font=("Arial", 14, "bold")).pack(anchor="w")
        self.signs_container = ctk.CTkScrollableFrame(signs_frame, height=150)
        self.signs_container.pack(fill="x", pady=5)
        ctk.CTkButton(signs_frame, text="+ Agregar Signo", command=self.add_sign_row).pack(anchor="e")
        
        # Sección de Síntomas
        symptoms_frame = ctk.CTkFrame(form)
        symptoms_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(symptoms_frame, text="Síntomas Reportados", font=("Arial", 14, "bold")).pack(anchor="w")
        self.symptoms_container = ctk.CTkScrollableFrame(symptoms_frame, height=150)
        self.symptoms_container.pack(fill="x", pady=5)
        ctk.CTkButton(symptoms_frame, text="+ Agregar Síntoma", command=self.add_symptom_row).pack(anchor="e")

    def add_sign_row(self):
        frame = ctk.CTkFrame(self.signs_container)
        frame.pack(fill="x", pady=2)
        
        signo_cb = ctk.CTkComboBox(frame, values=[s['name'] for s in self.signs], width=200)
        signo_cb.pack(side="left", padx=5)
        
        ctk.CTkEntry(frame, placeholder_text="Valor", width=100).pack(side="left", padx=5)
        ctk.CTkComboBox(frame, values=["Leve", "Moderado", "Severo"], width=120).pack(side="left", padx=5)
        ctk.CTkButton(frame, text="X", width=30, command=lambda: frame.destroy()).pack(side="right")

    def add_symptom_row(self):
        frame = ctk.CTkFrame(self.symptoms_container)
        frame.pack(fill="x", pady=2)
        
        sintoma_cb = ctk.CTkComboBox(frame, values=[s['name'] for s in self.symptoms], width=200)
        sintoma_cb.pack(side="left", padx=5)
        
        ctk.CTkComboBox(frame, values=["Leve", "Moderado", "Intenso"], width=120).pack(side="left", padx=5)
        ctk.CTkEntry(frame, placeholder_text="Duración", width=100).pack(side="left", padx=5)
        ctk.CTkButton(frame, text="X", width=30, command=lambda: frame.destroy()).pack(side="right")

    def save_consultation(self):
        if not self.current_patient:
            messagebox.showerror("Error", "No hay paciente seleccionado")
            return
            
        consultation_data = {
            "patient_id": self.current_patient["id_patient"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "signs": [],
            "symptoms": []
        }
        
        # Recopilar signos
        for frame in self.signs_container.winfo_children():
            if isinstance(frame, ctk.CTkFrame):
                children = frame.winfo_children()
                sign_name = children[0].get()
                sign_data = {
                    "name": sign_name,
                    "value": children[1].get(),
                    "severity": children[2].get(),
                }
                consultation_data["signs"].append(sign_data)
        
        # Recopilar síntomas
        for frame in self.symptoms_container.winfo_children():
            if isinstance(frame, ctk.CTkFrame):
                children = frame.winfo_children()
                symptom_name = children[0].get()
                symptom_data = {
                    "name": symptom_name,
                    "intensity": children[1].get(),
                    "duration": children[2].get(),
                }
                consultation_data["symptoms"].append(symptom_data)
        
        # Validar consulta
        if error := self.validate_consultation_data(consultation_data):
            messagebox.showerror("Error", error)
            return
        
        # Guardar en base de datos
        try:
            db = ConectionDB()
            connection = db.connect()
            
            with connection.cursor() as cursor:
                # Insertar consulta
                cursor.execute(
                    "INSERT INTO Consultation (patient_id, date) VALUES (%s, %s)",
                    (consultation_data["patient_id"], consultation_data["date"])
                )
                consultation_id = cursor.lastrowid
                
                # Insertar signos
                for sign in consultation_data["signs"]:
                    cursor.execute(
                        """INSERT INTO ClinicalSigns (consultation_id, sign_id, value, severity)
                        VALUES (%s, %s, %s, %s)""",
                        (consultation_id, 
                         next(s["id"] for s in self.signs if s["name"] == sign["name"]),
                         sign["value"],
                         sign["severity"])
                    )
                
                # Insertar síntomas
                for symptom in consultation_data["symptoms"]:
                    cursor.execute(
                        """INSERT INTO Symptoms (consultation_id, symptom_id, intensity, duration)
                        VALUES (%s, %s, %s, %s)""",
                        (consultation_id,
                         next(s["id"] for s in self.symptoms if s["name"] == symptom["name"]),
                         symptom["intensity"],
                         symptom["duration"])
                    )
                
                connection.commit()
            
            messagebox.showinfo("Éxito", "Consulta guardada correctamente")
            self.show_view_patients()
            
        except Exception as e:
            print(f"Error al guardar consulta: {e}")
            messagebox.showerror("Error", f"No se pudo guardar la consulta: {str(e)}")
        finally:
            if 'connection' in locals():
                connection.close()

    def load_sample_data(self):
        self.patients = [{
            "id_patient": 1,
            "name": "Juan Pérez",
            "birth_date": "1990-05-15",
            "gender": "Masculino",
            "address": "Calle Falsa 123",
            "phone": "555-1234567"
        }]

    def create_bottom_buttons(self):
        bottom_frame = ctk.CTkFrame(self.main_frame, height=50, fg_color="#f8f9fa")
        bottom_frame.pack(side="bottom", fill="x", pady=5, padx=10)
        ctk.CTkButton(
            bottom_frame,
            text="Regresar al Menú",
            command=self.return_menu,
            ).pack(side="top", padx=5)
        
    def validate_full_name(self, name):
        if not name.strip():
            return "El nombre completo no puede estar vacío"
        if len(name) > 100:
            return "El nombre no puede exceder 100 caracteres"
        if not all(c.isalpha() or c.isspace() or c in "áéíóúñÁÉÍÓÚÑ" for c in name):
            return "Solo se permiten letras y espacios"
        if len(name.split()) < 2:
            return "Debe ingresar al menos nombre y apellido"
        return None

    def validate_birth_date(self, date_str):
        try:
            birth_date = datetime.strptime(date_str, "%Y-%m-%d")
            if birth_date > datetime.now():
                return "La fecha de nacimiento no puede ser futura"
            # Verificar edad mínima (ej. 0 años) y máxima (ej. 120 años)
            age = datetime.now().year - birth_date.year
            if age < 0 or age > 120:
                return "Edad no válida"
            return None
        except ValueError:
            return "Formato de fecha inválido (AAAA-MM-DD)"

    def validate_gender(self, gender):
        valid_genders = ["Masculino", "Femenino", "Otro"]
        if gender not in valid_genders:
            return "Género no válido"
        return None

    def validate_address(self, address):
        if not address.strip():
            return "La dirección no puede estar vacía"
        if len(address) > 200:
            return "La dirección no puede exceder 200 caracteres"
        return None

    def validate_phone(self, phone):
        if not phone.strip():
            return "El teléfono no puede estar vacío"
        # Validar formato básico (ajustar según requisitos)
        if len(phone) < 7 or len(phone) > 15:
            return "El teléfono debe tener entre 7 y 15 dígitos"
        if not phone.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            return "El teléfono solo puede contener números y caracteres especiales (+ -)"
        return None
    
    def validate_consultation_data(self, consultation_data):
        if not consultation_data["signs"]:
            return "Debe registrar al menos un signo clínico"
        if not consultation_data["symptoms"]:
            return "Debe registrar al menos un síntoma"
        
        # Validar cada signo
        for sign in consultation_data["signs"]:
            if not sign["value"]:
                return f"Valor faltante para {sign['name']}"
            try:
                float(sign["value"])  # Validar que sea numérico para signos vitales
            except ValueError:
                return f"Valor inválido para {sign['name']} (debe ser numérico)"
        
        return None
    