import customtkinter as ctk
from tkinter import messagebox

from crud_facturas import (
    guardar_factura,
    obtener_facturas,
    actualizar_factura,
    eliminar_factura,
    total_facturas,
    monto_total
)

from crud_oracle import obtener_usuarios, obtener_cuentas

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("SmartBudget FinTech - Pro Dashboard")
app.geometry("1000x700")

# ----------------- FUNCIONES MONGODB -----------------
def refrescar_dashboard():
    # En caso de querer actualizar contadores globales
    pass

def guardar():
    try:
        guardar_factura(int(txt_usuario.get()), txt_empresa.get(), float(txt_monto.get()), txt_categoria.get())
        messagebox.showinfo("Éxito", "Factura guardada")
        limpiar()
        mostrar()
    except Exception as e:
        messagebox.showerror("Error", "Datos incorrectos")

def mostrar():
    txt_resultado_mongo.delete("1.0", "end")
    facturas = obtener_facturas()
    if len(facturas) == 0:
        txt_resultado_mongo.insert("end", "No existen facturas registradas.\n")
        return
    for f in facturas:
        txt_resultado_mongo.insert("end", f"Usuario: {f['usuario_id']} | Empresa: {f['empresa']} | Monto: S/{f['monto']} | Categoria: {f['categoria']}\n")
        txt_resultado_mongo.insert("end", "-"*80 + "\n")

def actualizar():
    try:
        actualizar_factura(int(txt_usuario.get()), txt_empresa.get(), float(txt_monto.get()), txt_categoria.get())
        messagebox.showinfo("Éxito", "Factura actualizada")
        limpiar()
        mostrar()
    except:
        messagebox.showerror("Error", "No se pudo actualizar")

def limpiar():
    txt_usuario.delete(0, "end")
    txt_empresa.delete(0, "end")
    txt_monto.delete(0, "end")
    txt_categoria.delete(0, "end")

def eliminar():
    try:
        eliminar_factura(int(txt_usuario.get()))
        messagebox.showinfo("Éxito", "Factura eliminada")
        limpiar()
        mostrar()
    except:
        messagebox.showerror("Error", "No se pudo eliminar")

def reporte():
    ventana = ctk.CTkToplevel()
    ventana.title("Reporte Financiero")
    ventana.geometry("400x250")
    ctk.CTkLabel(ventana, text="REPORTE FINANCIERO", font=("Arial",22,"bold")).pack(pady=15)
    ctk.CTkLabel(ventana, text=f"Facturas Registradas: {total_facturas()}", font=("Arial",14)).pack(pady=10)
    ctk.CTkLabel(ventana, text=f"Monto Total: S/ {monto_total()}", font=("Arial",14)).pack(pady=10)

# ----------------- FUNCIONES ORACLE -----------------
def mostrar_usuarios_oracle():
    txt_resultado_oracle.delete("1.0", "end")
    usuarios = obtener_usuarios()
    if not usuarios:
        txt_resultado_oracle.insert("end", "No hay usuarios en Oracle o falló la conexión.\n")
        return
    for u in usuarios:
        txt_resultado_oracle.insert("end", f"ID: {u[0]} | Nombre: {u[1]} {u[2]} | Correo: {u[3]}\n")
        txt_resultado_oracle.insert("end", "-"*80 + "\n")

def mostrar_cuentas_oracle():
    txt_resultado_oracle.delete("1.0", "end")
    cuentas = obtener_cuentas()
    if not cuentas:
        txt_resultado_oracle.insert("end", "No hay cuentas bancarias en Oracle o falló la conexión.\n")
        return
    for c in cuentas:
        txt_resultado_oracle.insert("end", f"Cuenta: {c[0]} | Usuario: {c[1]} | Banco: {c[2]} | Nro: {c[3]} | Saldo: S/{c[4]}\n")
        txt_resultado_oracle.insert("end", "-"*80 + "\n")


# ----------------- INTERFAZ PRINCIPAL -----------------
# Título Principal
titulo = ctk.CTkLabel(app, text="💰 SmartBudget FinTech Dashboard", font=("Arial", 32, "bold"), text_color="#00A3FF")
titulo.pack(pady=(20, 10))

# Crear un TabView para separar MONGODB de ORACLE
tabview = ctk.CTkTabview(app, width=900, height=550)
tabview.pack(padx=20, pady=10, fill="both", expand=True)

tabview.add("📊 MongoDB (Facturas)")
tabview.add("🏦 Oracle (Gestión Core)")

# === TAB MONGODB ===
# Dividir en dos columnas (Izquierda: Formulario, Derecha: Lista)
frame_form = ctk.CTkFrame(tabview.tab("📊 MongoDB (Facturas)"), width=350, corner_radius=10)
frame_form.pack(side="left", fill="y", padx=10, pady=10)

frame_lista = ctk.CTkFrame(tabview.tab("📊 MongoDB (Facturas)"), corner_radius=10)
frame_lista.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Formulario (Izquierda)
ctk.CTkLabel(frame_form, text="Registro de Facturas", font=("Arial", 20, "bold")).pack(pady=15)

ctk.CTkLabel(frame_form, text="Usuario ID").pack(anchor="w", padx=20)
txt_usuario = ctk.CTkEntry(frame_form, width=300)
txt_usuario.pack(padx=20, pady=(0, 10))

ctk.CTkLabel(frame_form, text="Empresa").pack(anchor="w", padx=20)
txt_empresa = ctk.CTkEntry(frame_form, width=300)
txt_empresa.pack(padx=20, pady=(0, 10))

ctk.CTkLabel(frame_form, text="Monto (S/)").pack(anchor="w", padx=20)
txt_monto = ctk.CTkEntry(frame_form, width=300)
txt_monto.pack(padx=20, pady=(0, 10))

ctk.CTkLabel(frame_form, text="Categoría").pack(anchor="w", padx=20)
txt_categoria = ctk.CTkEntry(frame_form, width=300)
txt_categoria.pack(padx=20, pady=(0, 20))

# Botones de Acción Formulario
btn_guardar = ctk.CTkButton(frame_form, text="Guardar Factura", command=guardar, fg_color="#28a745", hover_color="#218838")
btn_guardar.pack(pady=5, padx=20, fill="x")

btn_actualizar = ctk.CTkButton(frame_form, text="Actualizar Factura", command=actualizar, fg_color="#ffc107", text_color="black", hover_color="#e0a800")
btn_actualizar.pack(pady=5, padx=20, fill="x")

btn_eliminar = ctk.CTkButton(frame_form, text="Eliminar Factura", command=eliminar, fg_color="#dc3545", hover_color="#c82333")
btn_eliminar.pack(pady=5, padx=20, fill="x")

btn_limpiar = ctk.CTkButton(frame_form, text="Limpiar Campos", command=limpiar, fg_color="gray", hover_color="darkgray")
btn_limpiar.pack(pady=5, padx=20, fill="x")

# Lista y Reportes (Derecha)
ctk.CTkLabel(frame_lista, text="Lista de Facturas", font=("Arial", 20, "bold")).pack(pady=(15,5))

btn_mostrar = ctk.CTkButton(frame_lista, text="Refrescar Lista", command=mostrar)
btn_mostrar.pack(pady=5)

txt_resultado_mongo = ctk.CTkTextbox(frame_lista, width=500, height=350, font=("Consolas", 14))
txt_resultado_mongo.pack(padx=20, pady=10, fill="both", expand=True)

btn_reporte = ctk.CTkButton(frame_lista, text="Generar Reporte Financiero", command=reporte, fg_color="#17a2b8", hover_color="#138496")
btn_reporte.pack(pady=10)

# === TAB ORACLE ===
# Dividir en Botones Arriba y Resultados Abajo
frame_oracle_btns = ctk.CTkFrame(tabview.tab("🏦 Oracle (Gestión Core)"), fg_color="transparent")
frame_oracle_btns.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(frame_oracle_btns, text="Módulos Core (Oracle)", font=("Arial", 20, "bold")).pack(pady=(10, 20))

btn_usuarios_oracle = ctk.CTkButton(frame_oracle_btns, text="👥 Ver Usuarios", command=mostrar_usuarios_oracle, fg_color="#e63946", hover_color="#d62828", font=("Arial", 16, "bold"), height=40)
btn_usuarios_oracle.pack(side="left", padx=20, expand=True)

btn_cuentas_oracle = ctk.CTkButton(frame_oracle_btns, text="💳 Ver Cuentas Bancarias", command=mostrar_cuentas_oracle, fg_color="#e63946", hover_color="#d62828", font=("Arial", 16, "bold"), height=40)
btn_cuentas_oracle.pack(side="right", padx=20, expand=True)

txt_resultado_oracle = ctk.CTkTextbox(tabview.tab("🏦 Oracle (Gestión Core)"), width=800, height=400, font=("Consolas", 14))
txt_resultado_oracle.pack(padx=20, pady=10, fill="both", expand=True)

# Inicializar
app.mainloop()
