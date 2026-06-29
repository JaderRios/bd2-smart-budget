import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from crud_facturas import (
    guardar_factura,
    obtener_facturas,
    actualizar_factura,
    eliminar_factura,
    total_facturas,
    monto_total
)

# Helper para Focus Ring (borde azul)
def apply_focus_ring(entry_widget):
    default_border = entry_widget.cget("border_color")
    entry_widget.bind("<FocusIn>", lambda e: entry_widget.configure(border_color="#4318FF", border_width=2))
    entry_widget.bind("<FocusOut>", lambda e: entry_widget.configure(border_color=default_border, border_width=1))

# Helper para Hover Effect en filas
def apply_row_hover(row_frame, children_list, default_color, hover_color):
    def on_enter(e):
        row_frame.configure(fg_color=hover_color)
    def on_leave(e):
        row_frame.configure(fg_color=default_color)
        
    row_frame.bind("<Enter>", on_enter)
    row_frame.bind("<Leave>", on_leave)
    for child in children_list:
        child.bind("<Enter>", on_enter)
        child.bind("<Leave>", on_leave)


class ReporteDashboard(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Dashboard Financiero")
        self.geometry("800x600")
        
        # Detectar Tema
        is_dark = ctk.get_appearance_mode().lower() == "dark"
        bg_color = "#0b1437" if is_dark else "#F4F7FE"
        card_bg = "#111c44" if is_dark else "#ffffff"
        text_color = "#ffffff" if is_dark else "#1b2559"
        sub_text_color = "#a3aed0" if is_dark else "#A3AED0"
        
        self.configure(fg_color=bg_color)
        self.grab_set()
        
        # Titulo Principal
        title = ctk.CTkLabel(self, text="Análisis de Facturación", font=ctk.CTkFont(size=28, weight="bold"), text_color=text_color)
        title.pack(pady=(30, 20))
        
        # Contenedor de KPIs
        kpi_frame = ctk.CTkFrame(self, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=40, pady=10)
        
        # KPI 1
        kpi1 = ctk.CTkFrame(kpi_frame, fg_color=card_bg, corner_radius=15)
        kpi1.pack(side="left", expand=True, fill="both", padx=10)
        ctk.CTkLabel(kpi1, text="Total de Facturas", font=ctk.CTkFont(size=14), text_color=sub_text_color).pack(pady=(15, 0))
        ctk.CTkLabel(kpi1, text=str(total_facturas()), font=ctk.CTkFont(size=32, weight="bold"), text_color=text_color).pack(pady=(0, 15))

        # KPI 2
        kpi2 = ctk.CTkFrame(kpi_frame, fg_color=card_bg, corner_radius=15)
        kpi2.pack(side="right", expand=True, fill="both", padx=10)
        ctk.CTkLabel(kpi2, text="Monto Total Procesado", font=ctk.CTkFont(size=14), text_color=sub_text_color).pack(pady=(15, 0))
        ctk.CTkLabel(kpi2, text=f"S/ {monto_total():.2f}", font=ctk.CTkFont(size=32, weight="bold"), text_color="#05cd99").pack(pady=(0, 15))
        
        # Grafico
        chart_frame = ctk.CTkFrame(self, fg_color=card_bg, corner_radius=15)
        chart_frame.pack(fill="both", expand=True, padx=50, pady=30)
        
        self.dibujar_grafico(chart_frame, is_dark, card_bg, text_color)

    def dibujar_grafico(self, parent_frame, is_dark, face_color, text_color):
        facturas = obtener_facturas()
        if not facturas:
            ctk.CTkLabel(parent_frame, text="No hay datos suficientes para graficar.", text_color="#A3AED0").pack(expand=True)
            return
            
        categorias_monto = {}
        for f in facturas:
            cat = f['categoria']
            categorias_monto[cat] = categorias_monto.get(cat, 0) + f['monto']
            
        labels = list(categorias_monto.keys())
        sizes = list(categorias_monto.values())
        colors = ['#4318FF', '#05cd99', '#FFB547', '#EE5D50', '#8c54ff', '#ff54b0']
        
        # Configurar Matplotlib adaptando al tema
        fig, ax = plt.subplots(figsize=(6, 4), facecolor=face_color)
        ax.set_facecolor(face_color)
        
        # Modificar las etiquetas para que se vean bien en modo oscuro
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=colors[:len(labels)],
            textprops={'fontsize': 11, 'color': text_color}
        )
        
        for autotext in autotexts:
            autotext.set_color('white') # Porcentajes siempre blancos
            
        ax.axis('equal')  
        
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=15)


class FacturaModal(ctk.CTkToplevel):
    def __init__(self, parent, on_close_callback, factura=None):
        super().__init__(parent)
        self.on_close_callback = on_close_callback
        self.factura = factura
        self.is_edit = factura is not None
        
        self.title("Editar Factura" if self.is_edit else "Nueva Factura")
        self.geometry("450x550")
        self.configure(fg_color=("#F4F7FE", "#0b1437"))
        self.grab_set() 
        
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#111c44"), corner_radius=15)
        card.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(card, text="Editar Factura" if self.is_edit else "Registro de Facturas", font=ctk.CTkFont(size=22, weight="bold"), text_color=("#1b2559", "#ffffff")).pack(pady=25)

        self.txt_usuario = ctk.CTkEntry(card, width=300, height=40, corner_radius=8, placeholder_text="ID de Usuario", border_color=("#E2E8F0", "#2b3674"))
        self.txt_usuario.pack(pady=(0, 15))
        apply_focus_ring(self.txt_usuario)

        self.txt_empresa = ctk.CTkEntry(card, width=300, height=40, corner_radius=8, placeholder_text="Empresa", border_color=("#E2E8F0", "#2b3674"))
        self.txt_empresa.pack(pady=(0, 15))
        apply_focus_ring(self.txt_empresa)

        self.txt_monto = ctk.CTkEntry(card, width=300, height=40, corner_radius=8, placeholder_text="Monto (S/)", border_color=("#E2E8F0", "#2b3674"))
        self.txt_monto.pack(pady=(0, 15))
        apply_focus_ring(self.txt_monto)

        self.txt_categoria = ctk.CTkEntry(card, width=300, height=40, corner_radius=8, placeholder_text="Categoría", border_color=("#E2E8F0", "#2b3674"))
        self.txt_categoria.pack(pady=(0, 25))
        apply_focus_ring(self.txt_categoria)

        if self.is_edit:
            self.txt_usuario.insert(0, str(self.factura['usuario_id']))
            self.txt_usuario.configure(state="disabled") 
            self.txt_empresa.insert(0, self.factura['empresa'])
            self.txt_monto.insert(0, str(self.factura['monto']))
            self.txt_categoria.insert(0, self.factura['categoria'])

        btn_guardar = ctk.CTkButton(card, text="Actualizar" if self.is_edit else "Guardar Factura", height=45, command=self.guardar, fg_color="#05CD99" if not self.is_edit else "#FFB547", hover_color="#04A37A" if not self.is_edit else "#E09C34", text_color="white", corner_radius=8, font=ctk.CTkFont(size=15, weight="bold"))
        btn_guardar.pack(pady=10, fill="x", padx=40)
        
    def guardar(self):
        usuario_id_str = self.txt_usuario.get().strip()
        empresa_str = self.txt_empresa.get().strip()
        monto_str = self.txt_monto.get().strip()
        categoria_str = self.txt_categoria.get().strip()

        if not usuario_id_str or not empresa_str or not monto_str or not categoria_str:
            messagebox.showwarning("Campos incompletos", "Por favor, llene todos los campos.")
            return

        try:
            usuario_id_val = int(usuario_id_str)
        except ValueError:
            messagebox.showwarning("Error de formato", "El Usuario ID debe ser un número entero.")
            return

        try:
            monto_val = float(monto_str)
        except ValueError:
            messagebox.showwarning("Error de formato", "El Monto debe ser un valor numérico.")
            return

        try:
            if self.is_edit:
                actualizar_factura(usuario_id_val, empresa_str, monto_val, categoria_str)
                messagebox.showinfo("Éxito", "Factura actualizada")
            else:
                guardar_factura(usuario_id_val, empresa_str, monto_val, categoria_str)
                messagebox.showinfo("Éxito", "Factura guardada")
            
            self.on_close_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error Interno", f"Ocurrió un error al guardar en la base de datos: {e}")


class MongoView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Cabecera
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(10, 20))
        
        self.lbl_title = ctk.CTkLabel(self.header_frame, text="Gestión de Facturas", font=ctk.CTkFont(size=26, weight="bold"), text_color=("#1b2559", "#ffffff"))
        self.lbl_title.pack(side="left", padx=10)
        
        self.txt_search = ctk.CTkEntry(self.header_frame, placeholder_text="Buscar por empresa/categoria...", width=250, height=40, corner_radius=8, border_width=1, border_color=("#E2E8F0", "#2b3674"))
        self.txt_search.pack(side="left", padx=30)
        self.txt_search.bind("<KeyRelease>", lambda e: self.refresh_data())
        apply_focus_ring(self.txt_search)
        
        self.btn_add = ctk.CTkButton(self.header_frame, text="+ Nueva Factura", command=self.open_add_modal, height=40, fg_color="#4318FF", hover_color="#3311db", font=ctk.CTkFont(weight="bold", size=14), corner_radius=8)
        self.btn_add.pack(side="right", padx=10)

        self.btn_report = ctk.CTkButton(self.header_frame, text="Ver Reporte Dashboard", command=self.open_report, height=40, fg_color=("#ffffff", "#111c44"), border_width=1, border_color=("#E2E8F0", "#2b3674"), text_color=("#1b2559", "#ffffff"), hover_color=("#F4F7FE", "#2b3674"), font=ctk.CTkFont(weight="bold", size=14), corner_radius=8)
        self.btn_report.pack(side="right", padx=10)
        
        # Tabla Principal
        self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=15, fg_color=("#ffffff", "#111c44"), border_width=1, border_color=("#E2E8F0", "#1b2559"))
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def open_add_modal(self):
        FacturaModal(self, self.refresh_data)
        
    def open_edit_modal(self, factura):
        FacturaModal(self, self.refresh_data, factura=factura)

    def open_report(self):
        ReporteDashboard(self)

    def eliminar(self, usuario_id):
        if messagebox.askyesno("Confirmar", f"¿Eliminar factura del usuario {usuario_id}?"):
            eliminar_factura(int(usuario_id))
            self.refresh_data()

    def get_color_for_category(self, cat):
        # Asigna un color sutil y moderno estilo pastilla
        cat_lower = cat.lower()
        if "servicio" in cat_lower or "agua" in cat_lower or "luz" in cat_lower:
            return ("#E0F2FE", "#0284c7") # Azul
        elif "entretenimiento" in cat_lower or "ocio" in cat_lower or "netflix" in cat_lower:
            return ("#F3E8FF", "#7e22ce") # Púrpura
        elif "comida" in cat_lower or "alimento" in cat_lower or "restaurante" in cat_lower:
            return ("#FEF3C7", "#b45309") # Ámbar
        else:
            return ("#F1F5F9", "#475569") # Gris/Slate

    def refresh_data(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        facturas = obtener_facturas()
        query = self.txt_search.get().lower()
        
        if query:
            facturas = [f for f in facturas if query in f['empresa'].lower() or query in f['categoria'].lower()]
        
        # Headers
        header_row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        header_row.pack(fill="x", pady=(15, 10), padx=20)
        ctk.CTkLabel(header_row, text="Usuario ID", width=120, anchor="w", font=ctk.CTkFont(size=14, weight="bold"), text_color=("#A3AED0", "#8f9bba")).pack(side="left")
        ctk.CTkLabel(header_row, text="Empresa", width=220, anchor="w", font=ctk.CTkFont(size=14, weight="bold"), text_color=("#A3AED0", "#8f9bba")).pack(side="left")
        ctk.CTkLabel(header_row, text="Categoría", width=170, anchor="w", font=ctk.CTkFont(size=14, weight="bold"), text_color=("#A3AED0", "#8f9bba")).pack(side="left")
        ctk.CTkLabel(header_row, text="Monto", width=120, anchor="w", font=ctk.CTkFont(size=14, weight="bold"), text_color=("#A3AED0", "#8f9bba")).pack(side="left")
        ctk.CTkLabel(header_row, text="Acciones", width=160, font=ctk.CTkFont(size=14, weight="bold"), text_color=("#A3AED0", "#8f9bba")).pack(side="right")
        
        if not facturas:
            ctk.CTkLabel(self.scroll_frame, text="No se encontraron facturas.", text_color=("#A3AED0", "#8f9bba"), font=ctk.CTkFont(size=15)).pack(pady=40)
            return

        for f in facturas:
            row_bg = ("#F4F7FE", "#1b2559")
            row_hover = ("#e9effd", "#233375")
            
            row = ctk.CTkFrame(self.scroll_frame, corner_radius=10, fg_color=row_bg, height=60)
            row.pack(fill="x", pady=6, padx=10)
            row.pack_propagate(False)

            lbl_id = ctk.CTkLabel(row, text=str(f['usuario_id']), width=120, anchor="w", text_color=("#1b2559", "#ffffff"), font=ctk.CTkFont(size=14, weight="bold"))
            lbl_id.pack(side="left", padx=(10,0))
            
            lbl_emp = ctk.CTkLabel(row, text=f['empresa'], width=220, anchor="w", text_color=("#1b2559", "#ffffff"), font=ctk.CTkFont(size=14))
            lbl_emp.pack(side="left")
            
            # Pill badge para Categoría
            bg_pill, txt_pill = self.get_color_for_category(f['categoria'])
            pill_frame = ctk.CTkFrame(row, fg_color=bg_pill, corner_radius=12, width=150, height=26)
            pill_frame.pack(side="left", padx=(0, 20))
            pill_frame.pack_propagate(False)
            lbl_cat = ctk.CTkLabel(pill_frame, text=f['categoria'].upper(), text_color=txt_pill, font=ctk.CTkFont(size=10, weight="bold"), anchor="center")
            lbl_cat.pack(fill="both", expand=True)

            lbl_monto = ctk.CTkLabel(row, text=f"S/ {f['monto']:.2f}", width=120, anchor="w", text_color="#05cd99", font=ctk.CTkFont(size=15, weight="bold"))
            lbl_monto.pack(side="left")
            
            actions_frame = ctk.CTkFrame(row, fg_color="transparent")
            actions_frame.pack(side="right", padx=10)
            
            btn_edit = ctk.CTkButton(actions_frame, text="Editar", width=70, height=30, fg_color="#FFB547", hover_color="#E09C34", text_color="#ffffff", corner_radius=6, font=ctk.CTkFont(weight="bold"), command=lambda fc=f: self.open_edit_modal(fc))
            btn_edit.pack(side="left", padx=5)
            
            btn_del = ctk.CTkButton(actions_frame, text="Borrar", width=70, height=30, fg_color="#EE5D50", hover_color="#D14E42", text_color="#ffffff", corner_radius=6, font=ctk.CTkFont(weight="bold"), command=lambda uid=f['usuario_id']: self.eliminar(uid))
            btn_del.pack(side="left", padx=5)
            
            # Aplicar efecto hover
            apply_row_hover(row, [lbl_id, lbl_emp, pill_frame, lbl_cat, lbl_monto], row_bg, row_hover)

        # Pie de tabla informativo
        footer = ctk.CTkLabel(self.scroll_frame, text=f"Mostrando {len(facturas)} facturas de MongoDB en tiempo real. Sincronización activa.", font=ctk.CTkFont(size=11, weight="bold"), text_color=("#A3AED0", "#8f9bba"))
        footer.pack(pady=(20, 10))
