import customtkinter as ctk
from image_file import find_image
from patient import PatientManager
from newuser import NewUser
from disease import DiseaseManager
from signs import SignManager
from symptoms import SymptomManager
from tests import TestManager
from intelligentdiagnosis import DiagnosisManagement

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

        patient_img = find_image("images/patient.png", 50)
        patient_button = ctk.CTkButton(
            menuScreen,
            text="", 
            image=patient_img, 
            width=200, 
            height=200, 
            fg_color="#FFFFFF", 
            command=self.Btn_product
        )

        patient_button.image = patient_button
        patient_button.place(x=100, y=20)

        disease_img = find_image("images/disease.png", 70)
        disease_button = ctk.CTkButton(
            menuScreen,
            text="", 
            image=disease_img, 
            width=200, 
            height=200, 
            fg_color="#FFFFFF", 
            command=self.Btn_sales
        )

        disease_button.image = disease_button
        disease_button.place(x=400, y=20)

        sign_img = find_image("images/sign.png", 70)
        sign_button = ctk.CTkButton(
            menuScreen,
            text="", 
            image=sign_img, 
            width=200, 
            height=200, 
            fg_color="#FFFFFF", 
            command=self.Btn_Signs
        )

        sign_button.image = sign_button
        sign_button.place(x=700, y=20)

        symptom_img = find_image("images/symptom.png", 70)
        symptom_button = ctk.CTkButton(
            menuScreen,
            text="", 
            image=symptom_img, 
            width=200, 
            height=200, 
            fg_color="#FFFFFF", 
            command=self.Btn_Symptom
        )

        symptom_button.image = symptom_button
        symptom_button.place(x=100, y=300)

        test_img = find_image("images/test.png", 70)
        test_button = ctk.CTkButton(
            menuScreen,
            text="", 
            image=test_img, 
            width=200, 
            height=200, 
            fg_color="#FFFFFF", 
            command=self.Btn_Test
        )

        test_button.image = test_button
        test_button.place(x=400, y=300)

        diagnostic_img = find_image("images/diagnostic.png", 70)
        diagnostic_button = ctk.CTkButton(
            menuScreen,
            text="", 
            image=diagnostic_img, 
            width=200, 
            height=200, 
            fg_color="#FFFFFF", 
            command=self.Btn_Diagnosis
        )

        diagnostic_button.image = diagnostic_button
        diagnostic_button.place(x=700, y=300)

        self.newPatient = PatientManager(self, self.show_Menu_Screen)
        self.newUser = NewUser(self, self.show_back_to_MainScreen)
        self.newDisease = DiseaseManager(self, self.Disease_show_back_to_MainScreen)
        self.newSign = SignManager(self, self.Sign_show_back_to_MainScreen)
        self.newSymptom = SymptomManager(self, self.Symptom_show_back_to_MainScreen)
        self.newTest = TestManager(self, self.Test_show_back_to_MainScreen)
        self.newDiagnosis = DiagnosisManagement(self, self.Diagnosis_show_back_to_MainScreen)


        self.bind("<Button-1>", self.close_dropdown)
        self.dropdown_frame.bind("<Button-1>", lambda e: e.stop_propagation())
        

    
    def Btn_product(self):
        self.main_frame.pack_forget()
        self.newPatient.pack(fill="both", expand=True)

    def show_Menu_Screen(self):
        self.newPatient.pack_forget()  # Ocultar la segunda pantalla
        self.main_frame.pack(fill="both", expand=True)  # Mostrar la primera pantalla

    def show_back_to_MainScreen(self):
        self.newUser.pack_forget()  # Ocultar la segunda pantalla
        self.main_frame.pack(fill="both", expand=True)  # Mostrar la primera pantalla

    def Disease_show_back_to_MainScreen(self):
        self.newDisease.pack_forget()  # Ocultar la segunda pantalla
        self.main_frame.pack(fill="both", expand=True)  # Mostrar la primera pantalla
    
    def Sign_show_back_to_MainScreen(self):
        self.newSign.pack_forget()  # Ocultar la segunda pantalla
        self.main_frame.pack(fill="both", expand=True)  # Mostrar la primera pantalla
    
    def Symptom_show_back_to_MainScreen(self):
        self.newSymptom.pack_forget()  # Ocultar la segunda pantalla
        self.main_frame.pack(fill="both", expand=True)  # Mostrar la primera pantalla
    
    def Test_show_back_to_MainScreen(self):
        self.newTest.pack_forget()  # Ocultar la segunda pantalla
        self.main_frame.pack(fill="both", expand=True)  # Mostrar la primera pantalla
    
    def Diagnosis_show_back_to_MainScreen(self):
        self.newDiagnosis.pack_forget()  # Ocultar la segunda pantalla
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
        self.main_frame.pack_forget()
        self.newDisease.pack(fill="both", expand=True)

    def Btn_Signs(self):
        self.main_frame.pack_forget()
        self.newSign.pack(fill="both", expand=True)

    def Btn_Symptom(self):
        self.main_frame.pack_forget()
        self.newSymptom.pack(fill="both", expand=True)
    
    def Btn_Test(self):
        self.main_frame.pack_forget()
        self.newTest.pack(fill="both", expand=True)
    
    def Btn_Diagnosis(self):
        self.main_frame.pack_forget()
        self.newDiagnosis.pack(fill="both", expand=True)

