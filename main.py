import customtkinter as ctk
from typing import Optional
from login import Login
from menu import MenuApp

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración inicial de la ventana principal
        self.title("Sistema de Diagnóstico Médico")
        self.geometry("400x600")
        self.configure(fg_color="#969696")
        
        # Variables de estado
        self.current_user: Optional[str] = None
        
        # Crear frames
        self._setup_frames()
        
        # Mostrar login inicialmente
        self.show_login()
        
    def _setup_frames(self) -> None:
        """Inicializa todos los frames de la aplicación."""
        # Frame de login
        self.login_frame = Login(
            self, 
            on_login_success=self.on_login_success
        )
        
        # Frame del menú principal (se creará después del login)
        self.menu_frame: Optional[MenuApp] = None
        
    def on_login_success(self, username: str) -> None:
      
        self.current_user = username
        self.show_menu()
        
    def show_login(self) -> None:
        """Muestra la pantalla de login."""
        if self.menu_frame:
            self.menu_frame.pack_forget()
            
        self.login_frame.pack(fill="both", expand=True)
        self.geometry("400x600")
        self.title("Inicio de Sesión")
        
    def show_menu(self) -> None:
        """Muestra el menú principal."""
        self.login_frame.pack_forget()
        
        # Crear el menú si no existe, pasando el nombre de usuario
        if not self.menu_frame:
            self.menu_frame = MenuApp(
                self, 
                on_logout=self.logout,
                username=self.current_user
            )
            
        self.menu_frame.pack(fill="both", expand=True)
        self.geometry("1024x600")
        self.title(f"Menú Principal - {self.current_user}")
        
    def logout(self) -> None:
        """Maneja el cierre de sesión."""
        self.current_user = None
        self.show_login()
        self.login_frame.clear_fields()
    

if __name__ == "__main__":
    app = App()
    app.mainloop()