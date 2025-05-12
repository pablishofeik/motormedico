import customtkinter as ctk
from tkinter import ttk, messagebox
from conection import ConectionDB
from ErrorPopUp import Error

class SignManager(ctk.CTkFrame):
    def __init__(self, master, return_menu):
        super().__init__(master)
        self.return_menu = return_menu

        self.signs = []
        self.current_sign = None

        ctk.set_appearance_mode("light")
        self.configure(fg_color="#ffffff")

        self.create_main_interface()
        self.create_edit_interface()
        self.load_sample_data()

        self.show_main_screen()

    def create_main_interface(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff")

        toolbar = ctk.CTkFrame(self.main_frame, fg_color="#f8f9fa", height=40)
        toolbar.pack(fill="x", pady=5, padx=10)

        ctk.CTkButton(toolbar, text="Nuevo", width=80, command=self.new_sign).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Editar", width=80, command=self.edit_sign).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Eliminar", width=80, command=self.delete_sign).pack(side="left", padx=5)

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(toolbar, textvariable=self.search_var, placeholder_text="Buscar signo...", width=250)
        search_entry.pack(side="right", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.update_list())

        self.tree = ttk.Treeview(
            self.main_frame, 
            columns=("ID", "Nombre", "Descripción", "Severidad", "Unidad"), 
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100 if col != "Descripción" else 250)
        
        self.tree.bind("<Double-1>", lambda e: self.edit_sign())
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkButton(self.main_frame, text="Regresar al Menú", command=self.return_menu).pack(pady=10)

    def create_edit_interface(self):
        self.edit_frame = ctk.CTkFrame(self, fg_color="#ffffff")

        header = ctk.CTkFrame(self.edit_frame, fg_color="#f8f9fa", height=40)
        header.pack(fill="x", pady=5, padx=10)

        ctk.CTkButton(header, text="Guardar", width=80, command=self.save_sign).pack(side="left", padx=5)
        ctk.CTkButton(header, text="Cancelar", width=80, command=self.show_main_screen).pack(side="left", padx=5)

        form = ctk.CTkFrame(self.edit_frame)
        form.pack(fill="both", expand=True, padx=20, pady=10)

        labels = ["Nombre del signo:", "Descripción:", "Severidad:", "Unidad:"]
        self.entries = {}

        for i, label in enumerate(labels):
            ctk.CTkLabel(form, text=label).grid(row=i, column=0, sticky="w", pady=5)
        
        self.entries["sign_name"] = ctk.CTkEntry(form, width=400)
        self.entries["sign_name"].grid(row=0, column=1, pady=5)

        self.entries["description"] = ctk.CTkTextbox(form, width=400, height=100)
        self.entries["description"].grid(row=1, column=1, pady=5)

        self.entries["severity"] = ctk.CTkComboBox(
            form, 
            values=["Leve", "Moderado", "Severo"], 
            width=400,
            state="readonly"
        )
        self.entries["severity"].grid(row=2, column=1, pady=5)

        self.entries["unit"] = ctk.CTkEntry(form, width=400)
        self.entries["unit"].grid(row=3, column=1, pady=5)
    
    def load_sign(self):
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM sign"
                cursor.execute(query)
                resultados = cursor.fetchall()

        except Exception as e:
            print(f"Error durante la consulta de signos: {e}")
            Error(self, "Error al consultar las signos.")
            return  

        finally:
            connection.close()

        self.signs = [
            {
                "id_sign": row[0],
                "sign_name": row[1],
                "description": row[2],
                "severity": row[3],       
                "unit": row[4]    
            }
            for row in resultados
        ]

    def load_sample_data(self):
       self.load_sign()

    def update_list(self):
        self.tree.delete(*self.tree.get_children())
        search_term = self.search_var.get().lower()

        for sign in self.signs:
            if search_term in sign["sign_name"].lower():
                self.tree.insert("", "end", values=(
                    sign["id_sign"],
                    sign["sign_name"],
                    sign["description"][:50] + "..." if len(sign["description"]) > 50 else sign["description"],
                    sign["severity"],
                    sign["unit"]
                ))

    def new_sign(self):
        self.current_sign = None
        self.entries["sign_name"].delete(0, 'end')
        self.entries["description"].delete("1.0", "end")
        self.entries["unit"].delete(0, 'end')
        self.show_edit_screen()

    def edit_sign(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un signo primero")
            return
        
        sign_id = self.tree.item(selected[0])['values'][0]
        self.current_sign = next(s for s in self.signs if s['id_sign'] == sign_id)

        # Cargar datos en el formulario
        self.entries["sign_name"].delete(0, 'end')
        self.entries["sign_name"].insert(0, self.current_sign["sign_name"])

        self.entries["description"].delete("1.0", "end")
        self.entries["description"].insert("1.0", self.current_sign["description"])

        self.entries["severity"].set(self.current_sign["severity"])

        self.entries["unit"].delete(0, 'end')
        self.entries["unit"].insert(0, self.current_sign["unit"])

        self.show_edit_screen()

    def delete_sign(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un signo primero")
            return

        sign_id = self.tree.item(selected[0])['values'][0]
        sign_name = self.tree.item(selected[0])['values'][1]

        confirm = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Está seguro de eliminar el signo '{sign_name}'?\nEsta acción no se puede deshacer."
        )
        
        if not confirm:
            return

        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                # Verificar si está asociado a alguna enfermedad
                cursor.execute("SELECT COUNT(*) FROM Disease_Sign WHERE id_sign = %s", (sign_id,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror(
                        "Error", 
                        "No se puede eliminar este signo porque está asociado a enfermedades.\n"
                        "Elimine primero las asociaciones correspondientes."
                    )
                    return

                # Verificar si está asociado a alguna consulta
                cursor.execute("SELECT COUNT(*) FROM Consultation_Sign WHERE id_sign = %s", (sign_id,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror(
                        "Error", 
                        "No se puede eliminar este signo porque está asociado a consultas.\n"
                        "Elimine primero las consultas relacionadas."
                    )
                    return

                # Eliminar el signo
                cursor.execute("DELETE FROM Sign WHERE id_sign = %s", (sign_id,))
                connection.commit()

                # Actualizar lista local
                self.signs = [s for s in self.signs if s['id_sign'] != sign_id]
                self.update_list()
                messagebox.showinfo("Éxito", "Signo eliminado correctamente")

        except Exception as e:
            print(f"Error al eliminar signo: {e}")
            Error(self, f"No se pudo eliminar el signo: {str(e)}")
        finally:
            connection.close()

    def save_sign(self):
        # Obtener valores
        name = self.entries["sign_name"].get().strip()
        description = self.entries["description"].get("1.0", "end-1c").strip()
        severity = self.entries["severity"].get()
        unit = self.entries["unit"].get().strip()

        # Validar campos
        if error := self.validate_sign_name(name):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_description(description):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_severity(severity):
            messagebox.showerror("Error", error)
            return
        if error := self.validate_unit(unit):
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
                if self.current_sign:
                    # Actualizar signo existente
                    query = """
                        UPDATE Sign 
                        SET sign_name = %s, description = %s, severity = %s, unit = %s
                        WHERE id_sign = %s
                    """
                    cursor.execute(query, (
                        name,
                        description,
                        severity,
                        unit,
                        self.current_sign["id_sign"]
                    ))
                else:
                    # Insertar nuevo signo
                    query = """
                        INSERT INTO Sign (sign_name, description, severity, unit)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, (
                        name,
                        description,
                        severity,
                        unit
                    ))
                    # Obtener el ID del nuevo registro
                    new_id = cursor.lastrowid

                connection.commit()

                # Actualizar lista local
                if self.current_sign:
                    self.current_sign.update({
                        "sign_name": name,
                        "description": description,
                        "severity": severity,
                        "unit": unit
                    })
                else:
                    self.signs.append({
                        "id_sign": new_id,
                        "sign_name": name,
                        "description": description,
                        "severity": severity,
                        "unit": unit
                    })

                messagebox.showinfo("Éxito", "Signo guardado correctamente")
                self.show_main_screen()

        except Exception as e:
            print(f"Error al guardar signo: {e}")
            Error(self, f"No se pudo guardar el signo: {str(e)}")
        finally:
            connection.close()

    def show_main_screen(self):
        self.edit_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.update_list()

    def show_edit_screen(self):
        self.main_frame.pack_forget()
        self.edit_frame.pack(fill="both", expand=True)

    def validate_sign_name(self, name):
        if not name.strip():
            return "El nombre del signo no puede estar vacío"
        if len(name) > 100:
            return "El nombre no puede exceder 100 caracteres"
        if not all(c.isalpha() or c.isspace() or c in "áéíóúñÁÉÍÓÚÑ-" for c in name):
            return "El nombre solo puede contener letras, espacios y guiones"
        return None

    def validate_description(self, description):
        if not description.strip():
            return "La descripción no puede estar vacía"
        if len(description) > 500:
            return "La descripción no puede exceder 500 caracteres"
        return None

    def validate_severity(self, severity):
        valid_severities = ["Leve", "Moderado", "Severo"]
        if severity not in valid_severities:
            return "Seleccione una severidad válida"
        return None

    def validate_unit(self, unit):
        if not unit.strip():
            return "La unidad de medida no puede estar vacía"
        if len(unit) > 20:
            return "La unidad no puede exceder 20 caracteres"
        if not all(c.isalpha() or c in "/°%" for c in unit):
            return "Unidad no válida (solo letras y símbolos básicos)"
        return None

    def validate_sign_uniqueness(self, name, current_id=None):
        """Valida que el nombre del signo sea único"""
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return False

        try:
            with connection.cursor() as cursor:
                if current_id:
                    query = "SELECT COUNT(*) FROM Sign WHERE sign_name = %s AND id_sign != %s"
                    cursor.execute(query, (name, current_id))
                else:
                    query = "SELECT COUNT(*) FROM Sign WHERE sign_name = %s"
                    cursor.execute(query, (name,))
                
                return cursor.fetchone()[0] == 0
        finally:
            connection.close()