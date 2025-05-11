import customtkinter as ctk
from tkinter import ttk, messagebox

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

        self.entries["severity"] = ctk.CTkEntry(form, width=400)
        self.entries["severity"].grid(row=2, column=1, pady=5)

        self.entries["unit"] = ctk.CTkEntry(form, width=400)
        self.entries["unit"].grid(row=3, column=1, pady=5)

    def load_sample_data(self):
        self.signs = [
            {"id": 1, "sign_name": "Glucosa elevada", "description": "Nivel alto de glucosa en sangre", "severity": "Alta", "unit": "mg/dL"},
            {"id": 2, "sign_name": "Presión arterial alta", "description": "Presión sistólica >140 mmHg", "severity": "Moderada", "unit": "mmHg"}
        ]

    def update_list(self):
        self.tree.delete(*self.tree.get_children())
        search_term = self.search_var.get().lower()

        for sign in self.signs:
            if search_term in sign["sign_name"].lower():
                self.tree.insert("", "end", values=(
                    sign["id"],
                    sign["sign_name"],
                    sign["description"][:50] + "..." if len(sign["description"]) > 50 else sign["description"],
                    sign["severity"],
                    sign["unit"]
                ))

    def new_sign(self):
        self.current_sign = None
        self.entries["sign_name"].delete(0, 'end')
        self.entries["description"].delete("1.0", "end")
        self.entries["severity"].delete(0, 'end')
        self.entries["unit"].delete(0, 'end')
        self.show_edit_screen()

    def edit_sign(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un signo primero")
            return
        
        sign_id = self.tree.item(selected[0])['values'][0]
        self.current_sign = next(s for s in self.signs if s['id'] == sign_id)

        self.entries["sign_name"].delete(0, 'end')
        self.entries["sign_name"].insert(0, self.current_sign["sign_name"])

        self.entries["description"].delete("1.0", "end")
        self.entries["description"].insert("1.0", self.current_sign["description"])

        self.entries["severity"].delete(0, 'end')
        self.entries["severity"].insert(0, self.current_sign["severity"])

        self.entries["unit"].delete(0, 'end')
        self.entries["unit"].insert(0, self.current_sign["unit"])

        self.show_edit_screen()

    def delete_sign(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un signo primero")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar el signo seleccionado?"):
            sign_id = self.tree.item(selected[0])['values'][0]
            self.signs = [s for s in self.signs if s['id'] != sign_id]
            self.update_list()

    def save_sign(self):
        name = self.entries["sign_name"].get().strip()
        if not name:
            messagebox.showerror("Error", "El nombre del signo es obligatorio")
            return

        data = {
            "sign_name": name,
            "description": self.entries["description"].get("1.0", "end-1c").strip(),
            "severity": self.entries["severity"].get().strip(),
            "unit": self.entries["unit"].get().strip()
        }

        if self.current_sign:
            self.current_sign.update(data)
        else:
            new_id = max((s["id"] for s in self.signs), default=0) + 1
            data["id"] = new_id
            self.signs.append(data)

        self.show_main_screen()

    def show_main_screen(self):
        self.edit_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        self.update_list()

    def show_edit_screen(self):
        self.main_frame.pack_forget()
        self.edit_frame.pack(fill="both", expand=True)