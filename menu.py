import customtkinter as ctk
from image_file import find_image
from product import Product
from newuser import NewUser


class MenuApp(ctk.CTkFrame):
    def __init__(self, master, on_logout):
        super().__init__(master)
        self.on_logout = on_logout
        self.main_frame = ctk.CTkFrame(self, width=1024, height=600, corner_radius=0, fg_color="#969696")
        self.main_frame.place(x=0,y=0)
        self.main_frame.pack(fill="both", expand=True)

        top_frame = ctk.CTkFrame(self.main_frame, width=1024, height=50, corner_radius=0, fg_color="#FFFFFF")
        #top_frame.place(x=0,y=0)
        top_frame.pack(fill="both", expand=True)
        
        menuScreen = ctk.CTkFrame(self.main_frame, width=1024, height=550, corner_radius=0, fg_color="#969696")
        menuScreen.place(x=0,y=50)
        menuScreen.pack(fill="both", expand=True)
        
        name = str("Hola, Juan!")

        user_icon = find_image("images/login.png", 30)
        self.user_button = ctk.CTkButton(
            top_frame,
            text="",
            image=user_icon,
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#e0e0e0",
            command=self.toggle_dropdown
        )
        self.user_button.pack(side="right", padx=10, pady=10)
        
        # Dropdown (ahora hijo de main_frame)
        self.dropdown_frame = ctk.CTkFrame(self.main_frame, width=120, height=100, corner_radius=5)
        self.dropdown_visible = False
        
        # Opciones del dropdown
        options = ["Crear usuario", "Cambiar de usuario", "Cerrar sesión"]
        for opt in options:
            btn = ctk.CTkButton(
                self.dropdown_frame,
                text=opt,
                width=110,
                height=25,
                anchor="w",
                fg_color="transparent",
                hover_color="#e0e0e0",
                text_color="#000000",
                command=lambda o=opt: self.handle_dropdown(o)
            )
            btn.pack(pady=2, fill="x", padx=5)

        seller_label = ctk.CTkLabel(top_frame, text=name, font=("Arial", 20, "bold"), text_color="#000000")
        seller_label.pack(pady=(0, 0))  # Espaciado entre elementos

        product_img = find_image("images/products.png", 50)
        product_button = ctk.CTkButton(
            menuScreen,
            text="", 
            image=product_img, 
            width=200, 
            height=200, 
            fg_color="#FFFFFF", 
            command=self.Btn_product
        )

        product_button.image = product_img
        product_button.place(x=100, y=20)

        sales_img = find_image("images/sales.png", 70)
        sales_button = ctk.CTkButton(
            menuScreen,
            text="", 
            image=sales_img, 
            width=200, 
            height=200, 
            fg_color="#FFFFFF", 
            command=self.Btn_sales
        )

        sales_button.image = sales_img
        sales_button.place(x=400, y=20)

        reports_img = find_image("images/report.png", 70)
        reports_button = ctk.CTkButton(
            menuScreen,
            text="", 
            image=reports_img, 
            width=200, 
            height=200, 
            fg_color="#FFFFFF", 
            command=self.Btn_sales
        )

        reports_button.image = reports_img
        reports_button.place(x=700, y=20)

        clients_img = find_image("images/clients.png", 70)
        clients_button = ctk.CTkButton(
            menuScreen,
            text="", 
            image=clients_img, 
            width=200, 
            height=200, 
            fg_color="#FFFFFF", 
            command=self.Btn_sales
        )

        clients_button.image = clients_img
        clients_button.place(x=100, y=300)

        workers_img = find_image("images/worker.png", 70)
        workers_button = ctk.CTkButton(
            menuScreen,
            text="", 
            image=workers_img, 
            width=200, 
            height=200, 
            fg_color="#FFFFFF", 
            command=self.Btn_sales
        )

        workers_button.image = workers_img
        workers_button.place(x=400, y=300)

        settings_img = find_image("images/settings.png", 70)
        settings_button = ctk.CTkButton(
            menuScreen,
            text="", 
            image=settings_img, 
            width=200, 
            height=200, 
            fg_color="#FFFFFF", 
            command=self.Btn_sales
        )

        settings_button.image = settings_img
        settings_button.place(x=700, y=300)

        self.productScreen = Product(self, self.show_Menu_Screen)
        self.newUser = NewUser(self, self.show_back_to_MainScreen)

        self.bind("<Button-1>", self.close_dropdown)
        self.dropdown_frame.bind("<Button-1>", lambda e: e.stop_propagation())
        

    
    def Btn_product(self):
        self.main_frame.pack_forget()
        self.productScreen.pack(fill="both", expand=True)

    def show_Menu_Screen(self):
        self.productScreen.pack_forget()  # Ocultar la segunda pantalla
        self.main_frame.pack(fill="both", expand=True)  # Mostrar la primera pantalla

    def show_back_to_MainScreen(self):
        self.newUser.pack_forget()  # Ocultar la segunda pantalla
        self.main_frame.pack(fill="both", expand=True)  # Mostrar la primera pantalla

    def toggle_dropdown(self):
        if self.dropdown_visible:
            self.dropdown_frame.place_forget()
        else:
            # Obtener posición absoluta del botón
            btn_x = self.user_button.winfo_rootx()
            btn_y = self.user_button.winfo_rooty()
            btn_height = self.user_button.winfo_height()
            
            # Calcular posición relativa al main_frame
            main_x = self.main_frame.winfo_rootx()
            main_y = self.main_frame.winfo_rooty()
            
            # Posicionar el dropdown debajo del botón
            x = btn_x - main_x + self.user_button.winfo_width() - 120
            y = btn_y - main_y + btn_height
            
            self.dropdown_frame.place(x=x, y=y)
            self.dropdown_frame.lift()  # Asegurar que esté encima de otros elementos
        self.dropdown_visible = not self.dropdown_visible

    def close_dropdown(self, event):
        if self.dropdown_visible:
            # Verificar clic fuera del dropdown y del botón
            if not self.dropdown_frame.winfo_contain(event.x_root, event.y_root):
                if not self.user_button.winfo_contain(event.x_root, event.y_root):
                    self.dropdown_frame.place_forget()
                    self.dropdown_visible = False

    def handle_dropdown(self, option):
        print(f"Opción seleccionada: {option}")
        if option == "Crear usuario":
            self.main_frame.pack_forget()
            self.newUser.pack(fill="both", expand=True)
        elif option == "Cambiar de usuario":
            self.destroy()  # Cierra la ventana actual
            self.on_logout()
        elif option == "Cerrar":
            self.master.destroy()
        self.toggle_dropdown()

    def Btn_sales(self):
        print("")

