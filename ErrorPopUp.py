import customtkinter as ctk

class Error(ctk.CTkToplevel):
    def __init__(self, parent, mensaje):
        super().__init__(parent)

        self.geometry("400x200")
        self.title("Error")
        self.configure(fg_color="#D9534F")
        self.resizable(False, False)
        self.grab_set()

        message_label = ctk.CTkLabel(
            self,
            text=mensaje,
            font=("Arial", 18),
            text_color="white",
            anchor="center"
        )
        message_label.pack(pady=(40, 20), padx=20)

        close_button = ctk.CTkButton(
            self,
            text="Cerrar",
            width=100,
            height=40,
            corner_radius=10,
            fg_color="#FFFFFF",
            text_color="#000000",
            command=self.destroy
        )
        close_button.pack(pady=(20, 0))

        self.center_window(parent)

    def center_window(self, parent):
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        x = parent_x + (parent_width // 2) - (400 // 2)
        y = parent_y + (parent_height // 2) - (200 // 2)
        self.geometry(f"+{x}+{y}")