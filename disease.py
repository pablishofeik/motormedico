import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

class DiseaseManager(ctk.CTkFrame):
    def __init__(self, master, return_menu):
        super().__init__(master)
        self.return_menu = return_menu
        
        # Configuración inicial
        self.current_disease = None
        self.diseases = []
        self.all_symptoms = []  # Deberían cargarse desde SymptomsManager
        self.all_signs = []     # Deberían cargarse desde SignsManager
        
        # Estilo
        ctk.set_appearance_mode("light")
        self.configure(fg_color="#ffffff")
        
        # Crear widgets
        self.create_main_interface()
        self.create_edit_interface()
        self.load_sample_data()
        
        # Mostrar pantalla principal
        self.show_main_screen()

    def create_main_interface(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        
        # Barra de herramientas
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="#f8f9fa", height=40)
        toolbar.pack(fill="x", pady=5, padx=10)
        
        ctk.CTkButton(toolbar, text="Nuevo", width=80, command=self.new_disease).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Editar", width=80, command=self.edit_disease).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Eliminar", width=80, command=self.delete_disease).pack(side="left", padx=5)
        
        # Búsqueda
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(toolbar, textvariable=self.search_var, placeholder_text="Buscar enfermedad...", width=250)
        search_entry.pack(side="right", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.update_list())
        
        # Listado
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Nombre", "Descripción"), show="headings", style="Custom.Treeview")
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
        # Frame de edición
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

    def load_sample_data(self):
        # Datos de ejemplo
        self.diseases = [
            {'id': 1, 'name': 'Diabetes', 'description': 'Enfermedad metabólica', 
             'symptoms': [1], 'signs': [1]},
            {'id': 2, 'name': 'Hipertensión', 'description': 'Presión arterial alta',
             'symptoms': [2], 'signs': [2]}
        ]
        self.all_symptoms = [
            {'id': 1, 'name': 'Sed excesiva'},
            {'id': 2, 'name': 'Dolor de cabeza'}
        ]
        self.all_signs = [
            {'id': 1, 'name': 'Glucosa elevada'},
            {'id': 2, 'name': 'Presión arterial alta'}
        ]

    def show_main_screen(self):
        self.edit_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.update_list()

    def show_edit_screen(self):
        self.main_frame.pack_forget()
        self.edit_frame.pack(fill="both", expand=True)

    def update_list(self):
        self.tree.delete(*self.tree.get_children())
        search_term = self.search_var.get().lower()
        
        for disease in self.diseases:
            if search_term in disease['name'].lower():
                self.tree.insert("", "end", values=(
                    disease['id'],
                    disease['name'],
                    disease['description'][:50] + "..." if len(disease['description']) > 50 else disease['description']
                ))

    def new_disease(self):
        self.current_disease = None
        self.name_entry.delete(0, 'end')
        self.desc_entry.delete('1.0', 'end')
        self.update_associations()
        self.show_edit_screen()

    def edit_disease(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione una enfermedad primero")
            return
            
        disease_id = self.tree.item(selected[0])['values'][0]
        self.current_disease = next(d for d in self.diseases if d['id'] == disease_id)
        self.load_disease_data()
        self.show_edit_screen()

    def load_disease_data(self):
        if self.current_disease:
            self.name_entry.delete(0, 'end')
            self.name_entry.insert(0, self.current_disease['name'])
            self.desc_entry.delete('1.0', 'end')
            self.desc_entry.insert('1.0', self.current_disease['description'])
            self.update_associations()

    def update_associations(self):
        # Limpiar listas
        for widget in self.symptoms_list.winfo_children():
            widget.destroy()
        for widget in self.signs_list.winfo_children():
            widget.destroy()
        
        if self.current_disease:
            # Síntomas
            for symptom_id in self.current_disease.get('symptoms', []):
                symptom = next(s for s in self.all_symptoms if s['id'] == symptom_id)
                self.create_association_item(self.symptoms_list, symptom['name'], 'symptom')
            
            # Signos
            for sign_id in self.current_disease.get('signs', []):
                sign = next(s for s in self.all_signs if s['id'] == sign_id)
                self.create_association_item(self.signs_list, sign['name'], 'sign')

    def create_association_item(self, parent, name, type_):
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
        if not self.current_disease:
            return
            
        if type_ == 'symptom':
            symptom_id = next(s['id'] for s in self.all_symptoms if s['name'] == name)
            self.current_disease['symptoms'].remove(symptom_id)
        else:
            sign_id = next(s['id'] for s in self.all_signs if s['name'] == name)
            self.current_disease['signs'].remove(sign_id)
        
        self.update_associations()

    def add_symptom(self):
        if not self.current_disease:
            return
        available = [s for s in self.all_symptoms if s['id'] not in self.current_disease['symptoms']]
        self.show_selector_popup(available, 'symptom')

    def add_sign(self):
        if not self.current_disease:
            return
        available = [s for s in self.all_signs if s['id'] not in self.current_disease['signs']]
        self.show_selector_popup(available, 'sign')
    
    def show_selector_popup(self, options, type_):
        if not options:
            messagebox.showinfo("Sin opciones", f"No hay {type_}s disponibles para agregar.")
            return
    
        popup = ctk.CTkToplevel(self)
        popup.title(f"Seleccionar {type_}")
        popup.geometry("400x300")
        
        label = ctk.CTkLabel(popup, text=f"Selecciona un {type_} para agregar")
        label.pack(pady=10)
        
        listbox = ctk.CTkScrollableFrame(popup)
        listbox.pack(fill="both", expand=True, padx=10, pady=5)

        for item in options:
            def add(item=item):  # Captura correcta del ítem en la lambda
                if type_ == 'symptom':
                    self.current_disease['symptoms'].append(item['id'])
                else:
                    self.current_disease['signs'].append(item['id'])
                self.update_associations()
                popup.destroy()
            
            row = ctk.CTkFrame(listbox)
            row.pack(fill="x", pady=2, padx=5)
        
        ctk.CTkLabel(row, text=item['name']).pack(side="left", padx=5)
        ctk.CTkButton(row, text="Agregar", command=add, width=80).pack(side="right", padx=5)

    def save_disease(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        
        if self.current_disease:
            # Actualizar existente
            self.current_disease['name'] = name
            self.current_disease['description'] = self.desc_entry.get('1.0', 'end-1c')
        else:
            # Crear nuevo
            new_id = max(d['id'] for d in self.diseases) + 1 if self.diseases else 1
            self.diseases.append({
                'id': new_id,
                'name': name,
                'description': self.desc_entry.get('1.0', 'end-1c'),
                'symptoms': [],
                'signs': []
            })
        
        self.show_main_screen()

    def delete_disease(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione una enfermedad primero")
            return
            
        if messagebox.askyesno("Confirmar", "¿Eliminar la enfermedad seleccionada?"):
            disease_id = self.tree.item(selected[0])['values'][0]
            self.diseases = [d for d in self.diseases if d['id'] != disease_id]
            self.update_list()