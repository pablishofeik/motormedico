import customtkinter as ctk
from tkinter import ttk, messagebox
from conection import ConectionDB
from ErrorPopUp import Error

class SymptomManager(ctk.CTkFrame):
    def __init__(self, master, return_menu):
        super().__init__(master)
        self.return_menu = return_menu

        self.symptoms = []
        self.current_symptom = None

        ctk.set_appearance_mode("light")
        self.configure(fg_color="#ffffff")

        self.create_main_interface()
        self.create_edit_interface()
        self.load_sample_data()

        self.show_main_screen()

    def load_symptom(self):
        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM symptom"
                cursor.execute(query)
                resultados = cursor.fetchall()

        except Exception as e:
            print(f"Error durante la consulta de signos: {e}")
            Error(self, "Error al consultar las signos.")
            return  

        finally:
            connection.close()

        self.symptoms = [
            {
                "id_symptom": row[0],
                "symptom_name": row[1],
                "description": row[2],
                "intensity": row[3],       
                "duration": row[4]    
            }
            for row in resultados
        ]

    def create_main_interface(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff")

        toolbar = ctk.CTkFrame(self.main_frame, fg_color="#f8f9fa", height=40)
        toolbar.pack(fill="x", pady=5, padx=10)

        ctk.CTkButton(toolbar, text="Nuevo", width=80, command=self.new_symptom).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Editar", width=80, command=self.edit_symptom).pack(side="left", padx=5)
        ctk.CTkButton(toolbar, text="Eliminar", width=80, command=self.delete_symptom).pack(side="left", padx=5)

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(toolbar, textvariable=self.search_var, placeholder_text="Buscar síntoma...", width=250)
        search_entry.pack(side="right", padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self.update_list())

        self.tree = ttk.Treeview(
            self.main_frame,
            columns=("ID", "Nombre", "Descripción", "Intensidad", "Duración"),
            show="headings"
        )

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100 if col != "Descripción" else 250)

        self.tree.bind("<Double-1>", lambda e: self.edit_symptom())
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkButton(self.main_frame, text="Regresar al Menú", command=self.return_menu).pack(pady=10)

    def create_edit_interface(self):
        self.edit_frame = ctk.CTkFrame(self, fg_color="#ffffff")

        header = ctk.CTkFrame(self.edit_frame, fg_color="#f8f9fa", height=40)
        header.pack(fill="x", pady=5, padx=10)

        ctk.CTkButton(header, text="Guardar", width=80, command=self.save_symptom).pack(side="left", padx=5)
        ctk.CTkButton(header, text="Cancelar", width=80, command=self.show_main_screen).pack(side="left", padx=5)

        form = ctk.CTkFrame(self.edit_frame)
        form.pack(fill="both", expand=True, padx=20, pady=10)

        labels = ["Nombre del síntoma:", "Descripción:", "Intensidad:", "Duración:"]
        self.entries = {}

        for i, label in enumerate(labels):
            ctk.CTkLabel(form, text=label).grid(row=i, column=0, sticky="w", pady=5)

        self.entries["symptom_name"] = ctk.CTkEntry(form, width=400)
        self.entries["symptom_name"].grid(row=0, column=1, pady=5)

        self.entries["description"] = ctk.CTkTextbox(form, width=400, height=100)
        self.entries["description"].grid(row=1, column=1, pady=5)

        self.entries["intensity"] = ctk.CTkEntry(form, width=400)
        self.entries["intensity"].grid(row=2, column=1, pady=5)

        self.entries["duration"] = ctk.CTkEntry(form, width=400)
        self.entries["duration"].grid(row=3, column=1, pady=5)

    def load_sample_data(self):
        self.load_symptom()

    def update_list(self):
        self.tree.delete(*self.tree.get_children())
        search_term = self.search_var.get().lower()

        for symptom in self.symptoms:
            if search_term in symptom["symptom_name"].lower():
                self.tree.insert("", "end", values=(
                    symptom["id_symptom"],
                    symptom["symptom_name"],
                    symptom["description"][:50] + "..." if len(symptom["description"]) > 50 else symptom["description"],
                    symptom["intensity"],
                    symptom["duration"]
                ))

    def new_symptom(self):
        self.current_symptom = None
        self.entries["symptom_name"].delete(0, 'end')
        self.entries["description"].delete("1.0", "end")
        self.entries["intensity"].delete(0, 'end')
        self.entries["duration"].delete(0, 'end')
        self.show_edit_screen()

    def edit_symptom(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un síntoma primero")
            return

        symptom_id = self.tree.item(selected[0])['values'][0]
        self.current_symptom = next(s for s in self.symptoms if s['id_symptom'] == symptom_id)

        self.entries["symptom_name"].delete(0, 'end')
        self.entries["symptom_name"].insert(0, self.current_symptom["symptom_name"])

        self.entries["description"].delete("1.0", "end")
        self.entries["description"].insert("1.0", self.current_symptom["description"])

        self.entries["intensity"].delete(0, 'end')
        self.entries["intensity"].insert(0, self.current_symptom["intensity"])

        self.entries["duration"].delete(0, 'end')
        self.entries["duration"].insert(0, self.current_symptom["duration"])

        self.show_edit_screen()

    def delete_symptom(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un sintoma primero")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar el sintoma seleccionado?"):
            symptom_id = self.tree.item(selected[0])['values'][0]

            db = ConectionDB()
            connection = db.connect()

            if connection is None:
                Error(self, "No se pudo conectar a la base de datos")
                return

            try:
                with connection.cursor() as cursor:
                    query = "DELETE FROM symptom WHERE id_symptom = %s"
                    cursor.execute(query, (symptom_id,))
                    connection.commit()

            except Exception as e:
                print(f"Error al eliminar el sintoma: {e}")
                Error(self, "Ocurrió un error al eliminar el sintoma.")
            finally:
                connection.close()

            # También eliminar de la lista local
            self.symptoms = [s for s in self.symptoms if s['id_symptom'] != symptom_id]
            self.update_list()
            messagebox.showinfo("Éxito", "Sintoma eliminado correctamente")

    def save_symptom(self):
        name = self.entries["symptom_name"].get().strip()
        if not name:
            messagebox.showerror("Error", "El nombre del síntoma es obligatorio")
            return

        data = {
            "symptom_name": name,
            "description": self.entries["description"].get("1.0", "end-1c").strip(),
            "intensity": self.entries["intensity"].get().strip(),
            "duration": self.entries["duration"].get().strip()
        }

        db = ConectionDB()
        connection = db.connect()

        if connection is None:
            Error(self, "No se pudo conectar a la base de datos")
            return

        try:
            with connection.cursor() as cursor:
                if self.current_symptom:
                    # Actualizar síntoma existente
                    query = """
                        UPDATE Symptom SET
                            symptom_name = %s,
                            description = %s,
                            intensity = %s,
                            duration = %s
                        WHERE id_symptom = %s
                    """
                    cursor.execute(query, (
                        data["symptom_name"],
                        data["description"],
                        data["intensity"],
                        data["duration"],
                        self.current_symptom["id_symptom"]
                    ))
                else:
                    # Insertar nuevo síntoma
                    query = """
                        INSERT INTO Symptom (symptom_name, description, intensity, duration)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, (
                        data["symptom_name"],
                        data["description"],
                        data["intensity"],
                        data["duration"]
                    ))

                connection.commit()

        except Exception as e:
            print(f"Error al guardar síntoma: {e}")
            Error(self, "Error al guardar el síntoma.")
            return

        finally:
            connection.close()

        self.show_main_screen()
        messagebox.showinfo("Éxito", "Síntoma guardado correctamente")

    def show_main_screen(self):
        self.edit_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.load_symptom()
        self.update_list()

    def show_edit_screen(self):
        self.main_frame.pack_forget()
        self.edit_frame.pack(fill="both", expand=True)