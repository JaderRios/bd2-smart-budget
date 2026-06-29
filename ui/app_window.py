import customtkinter as ctk
from ui.views.mongo_view import MongoView
from ui.views.oracle_view import OracleView

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SmartBudget FinTech - Pro Dashboard")
        self.geometry("1250x800")
        
        # Grid principal: 1 fila, 2 columnas (Sidebar y Main Content)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # === SIDEBAR ===
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1b2559")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        # Logotipo
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="SmartBudget", font=ctk.CTkFont(size=24, weight="bold"), text_color="#ffffff")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(40, 40))

        # Botones de navegación con borde indicador
        self.btn_mongo = ctk.CTkButton(
            self.sidebar_frame, 
            text="Facturas (Mongo)", 
            command=self.show_mongo_view, 
            height=45, 
            fg_color="transparent", 
            text_color="#ffffff", 
            hover_color="#2b3674", 
            font=ctk.CTkFont(size=15, weight="bold"), 
            corner_radius=8, 
            anchor="w",
            border_spacing=10
        )
        self.btn_mongo.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_oracle = ctk.CTkButton(
            self.sidebar_frame, 
            text="Core Bancario (Oracle)", 
            command=self.show_oracle_view, 
            height=45, 
            fg_color="transparent", 
            text_color="#ffffff", 
            hover_color="#2b3674", 
            font=ctk.CTkFont(size=15, weight="bold"), 
            corner_radius=8, 
            anchor="w",
            border_spacing=10
        )
        self.btn_oracle.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Switch de Tema Oscuro/Claro al final de la barra
        self.switch_theme = ctk.CTkSwitch(
            self.sidebar_frame, 
            text="Modo Oscuro", 
            command=self.toggle_theme, 
            text_color="#ffffff", 
            font=ctk.CTkFont(size=13, weight="bold"), 
            progress_color="#4318FF"
        )
        self.switch_theme.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="s")

        self.status_label = ctk.CTkLabel(self.sidebar_frame, text="System: Online", text_color="#05cd99", font=ctk.CTkFont(size=12, weight="bold"))
        self.status_label.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="s")

        # === CONTENEDOR PRINCIPAL ===
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=("#F4F7FE", "#0b1437"))
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Inicializar vistas
        self.mongo_view = MongoView(self.main_container)
        self.oracle_view = OracleView(self.main_container)

        # Mostrar por defecto
        self.show_mongo_view()

    def toggle_theme(self):
        if self.switch_theme.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def show_mongo_view(self):
        # Efecto indicador visual: Borde grueso en el botón activo
        self.btn_mongo.configure(fg_color="#4318FF", border_width=2, border_color="#ffffff")
        self.btn_oracle.configure(fg_color="transparent", border_width=0)
        
        self.oracle_view.grid_forget()
        self.mongo_view.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        self.mongo_view.refresh_data()

    def show_oracle_view(self):
        self.btn_oracle.configure(fg_color="#4318FF", border_width=2, border_color="#ffffff")
        self.btn_mongo.configure(fg_color="transparent", border_width=0)
        
        self.mongo_view.grid_forget()
        self.oracle_view.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        self.oracle_view.refresh_view()
