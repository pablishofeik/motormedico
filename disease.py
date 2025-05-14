import customtkinter as ctk
from tkinter import ttk, messagebox
from conection import ConectionDB
from ErrorPopUp import Error

class DiseaseManager(ctk.CTkFrame):
    def __init__(self, master, return_menu):
        super().__init__(master)
        self.return_menu = return_menu
        
        # Configuración inicial
        self.current_disease = None
        self.diseases = []
        self.all_symptoms = []  
        self.all_signs = []     
        
        # Estilo
        ctk.set_appearance_mode("light")
        self.configure(fg_color="#ffffff")
        
        # Crear interfaces
        self.create_main_interface()
        self.create_edit_interface()
        
        # Cargar datos iniciales
        self.load_initial_data()
        
        # Mostrar pantalla principal
        self.show_main_screen()

    def create_main_interface(self):
        """Crea la interfaz principal de listado de enfermedades"""
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        # Barra de herramientas
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="#f8f9fa", height=40)
        toolbar.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkButton(toolbar, text="Nuevo", width=80, command=self.new_disease).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Editar", width=80, command=self.edit_disease).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Eliminar", width=80, command=self.delete_disease).pack(side="left", padx=5)
        
        # Búsqueda
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(toolbar, textvariable=self.search_var, 
                                   placeholder_text="Buscar enfermedad...", width=250)
        search_entry.pack(side="right", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.update_list())
        
        # Listado
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Nombre", "Descripción"), 
                                show="headings", style="Custom.Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=200)
        self.tree.column("Descripción", width=400)
        self.tree.bind("<Double-1>", lambda e: self.edit_disease())
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Botón de regreso
        ctk.CTkButton(self.main_frame, text="Regresar al Menú", command=self.return_menu).pack(pady=10)

    def create_edit_interface(self):
        """Crea la interfaz de edición/creación de enfermedades"""
        self.edit_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        # Cabecera
        header = ctk.CTkFrame(self.edit_frame, fg_color="#f8f9fa", height=40)
        header.pack(fill="x", pady=5, padx=10)
        ctk.CTkButton(header, text="Guardar", width=80, command=self.save_disease).pack(side="left", padx=5)
        ctk.CTkButton(header, text="Cancelar", width=80, command=self.show_main_screen).pack(side="left", padx=5)
        
        # Formulario
        form_frame = ctk.CTkFrame(self.edit_frame, fg_color="#ffffff")
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Campos de datos
        ctk.CTkLabel(form_frame, text="Nombre de la enfermedad:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ctk.CTkEntry(form_frame, width=400)
        self.name_entry.grid(row=0, column=1, pady=5)
        
        ctk.CTkLabel(form_frame, text="Descripción:").grid(row=1, column=0, sticky="nw", pady=5)
        self.desc_entry = ctk.CTkTextbox(form_frame, width=400, height=100)
        self.desc_entry.grid(row=1, column=1, pady=5)
        
        # Asociaciones
        associations_frame = ctk.CTkFrame(form_frame)
        associations_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        
        # Síntomas
        symptoms_frame = ctk.CTkFrame(associations_frame)
        symptoms_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(symptoms_frame, text="Síntomas asociados").pack()
        self.symptoms_list = ctk.CTkScrollableFrame(symptoms_frame, height=150)
        self.symptoms_list.pack(fill="both", expand=True)
        ctk.CTkButton(symptoms_frame, text="+ Agregar síntoma", command=self.add_symptom).pack(pady=5)
        
        # Signos
        signs_frame = ctk.CTkFrame(associations_frame)
        signs_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(signs_frame, text="Signos asociados").pack()
        self.signs_list = ctk.CTkScrollableFrame(signs_frame, height=150)
        self.signs_list.pack(fill="both", expand=True)
        ctk.CTkButton(signs_frame, text="+ Agregar signo", command=self.add_sign).pack(pady=5)

    def load_initial_data(self):
        """Carga todos los datos necesarios al iniciar"""
        self.load_diseases()
        self.load_all_symptoms()
        self.load_all_signs()

    def load_diseases(self):
        """Carga todas las enfermedades desde la base de datos"""
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                # Consulta para obtener las enfermedades
                query = """
                    SELECT d.id_disease, d.name, d.description,
                           GROUP_CONCAT(DISTINCT ds.id_symptom) AS symptoms,
                           GROUP_CONCAT(DISTINCT dsign.id_sign) AS signs
                    FROM Disease d
                    LEFT JOIN Disease_Symptom ds ON d.id_disease = ds.id_disease
                    LEFT JOIN Disease_Sign dsign ON d.id_disease = dsign.id_disease
                    GROUP BY d.id_disease
                """
                cursor.execute(query)
                enfermedades = cursor.fetchall()

                # Formatear los datos
                self.diseases = []
                for enfermedad in enfermedades:
                    symptom_ids = [int(id) for id in enfermedad[3].split(',')] if enfermedad[3] else []
                    sign_ids = [int(id) for id in enfermedad[4].split(',')] if enfermedad[4] else []
                    
                    self.diseases.append({
                        "id_disease": enfermedad[0],
                        "name": enfermedad[1],
                        "description": enfermedad[2],
                        "symptoms": symptom_ids,
                        "signs": sign_ids
                    })

        except Exception as e:
            print(f"Error durante la consulta de enfermedades: {e}")
            Error(self, "Error al consultar las enfermedades.")
        finally:
            connection.close()

        self.update_list()

    def load_all_symptoms(self):
        """Carga todos los síntomas disponibles"""
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_symptom, symptom_name FROM Symptom")
                self.all_symptoms = [
                    {'id': row[0], 'name': row[1]} 
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            print(f"Error cargando síntomas: {e}")
            Error(self, "Error al cargar síntomas")
        finally:
            connection.close()

    def load_all_signs(self):
        """Carga todos los signos disponibles"""
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_sign, sign_name FROM Sign")
                self.all_signs = [
                    {'id': row[0], 'name': row[1]} 
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            print(f"Error cargando signos: {e}")
            Error(self, "Error al cargar signos")
        finally:
            connection.close()

    def show_main_screen(self):
        """Muestra la pantalla principal"""
        self.edit_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.update_list()

    def show_edit_screen(self):
        """Muestra la pantalla de edición"""
        self.main_frame.pack_forget()
        self.edit_frame.pack(fill="both", expand=True)

    def update_list(self):
        """Actualiza la lista de enfermedades"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filtrar según búsqueda
        search_term = self.search_var.get().lower()
        
        # Insertar registros
        for disease in self.diseases:
            if search_term in disease['name'].lower():
                self.tree.insert("", "end", values=(
                    disease['id_disease'],
                    disease['name'],
                    disease['description'][:50] + "..." if len(disease['description']) > 50 else disease['description']
                ))

    def new_disease(self):
        """Prepara la interfaz para crear una nueva enfermedad"""
        self.current_disease = {
            "id_disease": None,
            "name": "",
            "description": "",
            "symptoms": [],
            "signs": []
        }
        
        # Limpiar campos
        self.name_entry.delete(0, 'end')
        self.desc_entry.delete('1.0', 'end')
        
        # Actualizar listas de asociaciones
        self.update_associations()
        
        # Mostrar pantalla de edición
        self.show_edit_screen()

    def edit_disease(self):
        """Prepara la interfaz para editar una enfermedad existente"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione una enfermedad primero")
            return
            
        disease_id = self.tree.item(selected[0])['values'][0]
        self.current_disease = next(d for d in self.diseases if d['id_disease'] == disease_id)
        
        # Cargar datos en los campos
        self.load_disease_data()
        
        # Mostrar pantalla de edición
        self.show_edit_screen()

    def load_disease_data(self):
        """Carga los datos de la enfermedad actual en los campos de edición"""
        if self.current_disease:
            self.name_entry.delete(0, 'end')
            self.name_entry.insert(0, self.current_disease['name'])
            
            self.desc_entry.delete('1.0', 'end')
            self.desc_entry.insert('1.0', self.current_disease['description'])
            
            self.update_associations()

    def update_associations(self):
        """Actualiza las listas de síntomas y signos asociados"""
        # Limpiar listas existentes
        for widget in self.symptoms_list.winfo_children():
            widget.destroy()
            
        for widget in self.signs_list.winfo_children():
            widget.destroy()
        
        if not self.current_disease:
            return
            
        # Mostrar síntomas asociados
        for symptom_id in self.current_disease.get('symptoms', []):
            symptom = next((s for s in self.all_symptoms if s['id'] == symptom_id), None)
            if symptom:
                self.create_association_item(self.symptoms_list, symptom['name'], 'symptom')
        
        # Mostrar signos asociados
        for sign_id in self.current_disease.get('signs', []):
            sign = next((s for s in self.all_signs if s['id'] == sign_id), None)
            if sign:
                self.create_association_item(self.signs_list, sign['name'], 'sign')
        
    def create_association_item(self, parent, name, type_):
        """Crea un elemento de asociación en la lista"""
        frame = ctk.CTkFrame(parent, fg_color="#f8f9fa", corner_radius=5)
        frame.pack(fill="x", pady=2)
        
        ctk.CTkLabel(frame, text=name).pack(side="left", padx=5)
        
        ctk.CTkButton(
            frame, 
            text="X", 
            width=30,
            fg_color="#dc3545",
            hover_color="#bb2d3b",
            command=lambda: self.remove_association(name, type_)
        ).pack(side="right")

    def remove_association(self, name, type_):
        """Elimina una asociación de la enfermedad actual"""
        if not self.current_disease:
            return
            
        if type_ == 'symptom':
            # Buscar el ID del síntoma por su nombre
            symptom = next((s for s in self.all_symptoms if s['name'] == name), None)
            if symptom and symptom['id'] in self.current_disease['symptoms']:
                self.current_disease['symptoms'].remove(symptom['id'])
        else:
            # Buscar el ID del signo por su nombre
            sign = next((s for s in self.all_signs if s['name'] == name), None)
            if sign and sign['id'] in self.current_disease['signs']:
                self.current_disease['signs'].remove(sign['id'])
        
        self.update_associations()

    def add_symptom(self):
        """Muestra el diálogo para agregar un síntoma"""
        if not self.current_disease:
            return
            
        # Obtener síntomas no asociados
        available = [
            s for s in self.all_symptoms 
            if s['id'] not in self.current_disease.get('symptoms', [])
        ]
        
        self.show_selector_popup(available, 'symptom')

    def add_sign(self):
        """Muestra el diálogo para agregar un signo"""
        if not self.current_disease:
            return
            
        # Obtener signos no asociados
        available = [
            s for s in self.all_signs 
            if s['id'] not in self.current_disease.get('signs', [])
        ]
        
        self.show_selector_popup(available, 'sign')

    def show_selector_popup(self, options, type_):
        """Muestra un popup para seleccionar síntomas o signos a agregar"""
        if not options:
            messagebox.showinfo("Sin opciones", f"No hay {type_}s disponibles para agregar.")
            return
    
        popup = ctk.CTkToplevel(self)
        popup.title(f"Seleccionar {type_}")
        popup.geometry("400x300")
        popup.grab_set()  # Hace el popup modal
        
        label = ctk.CTkLabel(popup, text=f"Selecciona un {type_} para agregar")
        label.pack(pady=10)
        
        listbox = ctk.CTkScrollableFrame(popup)
        listbox.pack(fill="both", expand=True, padx=10, pady=5)

        for item in options:
            row = ctk.CTkFrame(listbox)
            row.pack(fill="x", pady=2, padx=5)
            
            ctk.CTkLabel(row, text=item['name']).pack(side="left", padx=5)
            
            ctk.CTkButton(
                row, 
                text="Agregar", 
                command=lambda i=item: self.add_association(i, type_, popup),
                width=80
            ).pack(side="right", padx=5)

    def add_association(self, item, type_, popup):
        """Agrega una asociación a la enfermedad actual"""
        if not self.current_disease:
            return
            
        if type_ == 'symptom':
            if item['id'] not in self.current_disease['symptoms']:
                self.current_disease['symptoms'].append(item['id'])
        else:
            if item['id'] not in self.current_disease['signs']:
                self.current_disease['signs'].append(item['id'])
        
        self.update_associations()
        popup.destroy()

    def save_disease(self):
        """Guarda la enfermedad en la base de datos"""
        name = self.name_entry.get().strip()
        description = self.desc_entry.get("1.0", "end-1c").strip()

        if not name:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                if self.current_disease and self.current_disease['id_disease']:
                    # Actualizar enfermedad existente
                    query = "UPDATE Disease SET name=%s, description=%s WHERE id_disease=%s"
                    cursor.execute(query, (name, description, self.current_disease['id_disease']))
                    disease_id = self.current_disease['id_disease']
                else:
                    # Insertar nueva enfermedad
                    query = "INSERT INTO Disease (name, description) VALUES (%s, %s)"
                    cursor.execute(query, (name, description))
                    disease_id = cursor.lastrowid
                
                # Guardar asociaciones de síntomas
                cursor.execute("DELETE FROM Disease_Symptom WHERE id_disease=%s", (disease_id,))
                for symptom_id in self.current_disease.get('symptoms', []):
                    cursor.execute(
                        "INSERT INTO Disease_Symptom (id_disease, id_symptom) VALUES (%s, %s)",
                        (disease_id, symptom_id)
                    )
                
                # Guardar asociaciones de signos
                cursor.execute("DELETE FROM Disease_Sign WHERE id_disease=%s", (disease_id,))
                for sign_id in self.current_disease.get('signs', []):
                    cursor.execute(
                        "INSERT INTO Disease_Sign (id_disease, id_sign) VALUES (%s, %s)",
                        (disease_id, sign_id)
                    )
                
                connection.commit()
                messagebox.showinfo("Éxito", "Enfermedad guardada correctamente")
                
                # Actualizar datos locales
                self.load_diseases()
                self.show_main_screen()

        except Exception as e:
            print(f"Error al guardar enfermedad: {e}")
            Error(self, "No se pudo guardar la enfermedad.")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()

    def delete_disease(self):
        """Elimina la enfermedad seleccionada"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione una enfermedad primero")
            return
        
        disease_id = self.tree.item(selected[0])['values'][0]
        
        if not messagebox.askyesno("Confirmar", "¿Eliminar la enfermedad seleccionada?"):
            return
            
        db = ConectionDB()
        connection = db.connect()
        
        try:
            with connection.cursor() as cursor:
                # Eliminar asociaciones primero
                cursor.execute("DELETE FROM Disease_Symptom WHERE id_disease = %s", (disease_id,))
                cursor.execute("DELETE FROM Disease_Sign WHERE id_disease = %s", (disease_id,))
                
                # Eliminar enfermedad
                cursor.execute("DELETE FROM Disease WHERE id_disease = %s", (disease_id,))
                
                connection.commit()
                messagebox.showinfo("Éxito", "Enfermedad eliminada")
                
                # Actualizar lista
                self.load_diseases()
                
        except Exception as e:
            print(f"Error al eliminar: {e}")
            Error(self, "No se pudo eliminar. ¿Tiene asociaciones?")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()