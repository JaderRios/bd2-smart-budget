import customtkinter as ctk
from tkinter import messagebox
from crud_oracle import (
    obtener_usuarios, crear_usuario, actualizar_usuario, eliminar_usuario,
    obtener_cuentas, crear_cuenta, actualizar_cuenta, eliminar_cuenta,
    obtener_categorias, crear_categoria, actualizar_categoria, eliminar_categoria,
    obtener_transacciones, crear_transaccion, actualizar_transaccion, eliminar_transaccion,
    obtener_metas, crear_meta, actualizar_meta, eliminar_meta,
    obtener_estados, crear_estado, actualizar_estado, eliminar_estado
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


# --- MODALES ---

class UsuarioModal(ctk.CTkToplevel):
    def __init__(self, parent, on_close_callback, usuario=None):
        super().__init__(parent)
        self.on_close_callback = on_close_callback
        self.usuario = usuario
        self.is_edit = usuario is not None
        
        self.title("Editar Usuario" if self.is_edit else "Nuevo Usuario")
        self.geometry("450x500")
        self.configure(fg_color=("#F4F7FE", "#0b1437"))
        self.grab_set() 
        
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#111c44"), corner_radius=15)
        card.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(card, text="Editar Usuario" if self.is_edit else "Registro de Usuario", font=ctk.CTkFont(size=22, weight="bold"), text_color=("#1b2559", "#ffffff")).pack(pady=25)

        self.txt_nombre = ctk.CTkEntry(card, width=300, height=40, corner_radius=8, placeholder_text="Nombre", border_color=("#E2E8F0", "#2b3674"))
        self.txt_nombre.pack(pady=(0, 15))
        apply_focus_ring(self.txt_nombre)

        self.txt_apellido = ctk.CTkEntry(card, width=300, height=40, corner_radius=8, placeholder_text="Apellidos", border_color=("#E2E8F0", "#2b3674"))
        self.txt_apellido.pack(pady=(0, 15))
        apply_focus_ring(self.txt_apellido)

        self.txt_correo = ctk.CTkEntry(card, width=300, height=40, corner_radius=8, placeholder_text="Correo Electrónico", border_color=("#E2E8F0", "#2b3674"))
        self.txt_correo.pack(pady=(0, 25))
        apply_focus_ring(self.txt_correo)

        if self.is_edit:
            self.id_usuario = self.usuario[0]
            self.txt_nombre.insert(0, self.usuario[1])
            self.txt_apellido.insert(0, self.usuario[2])
            self.txt_correo.insert(0, self.usuario[3])

        btn_guardar = ctk.CTkButton(card, text="Actualizar" if self.is_edit else "Guardar Usuario", height=45, command=self.guardar, fg_color="#4318FF" if not self.is_edit else "#FFB547", hover_color="#3311db" if not self.is_edit else "#E09C34", text_color="white", corner_radius=8, font=ctk.CTkFont(size=15, weight="bold"))
        btn_guardar.pack(pady=10, fill="x", padx=40)
        
    def guardar(self):
        nombre_str = self.txt_nombre.get().strip()
        apellido_str = self.txt_apellido.get().strip()
        correo_str = self.txt_correo.get().strip()

        if not nombre_str or not apellido_str or not correo_str:
            messagebox.showwarning("Campos incompletos", "Por favor, llene todos los campos del usuario.")
            return

        if "@" not in correo_str or "." not in correo_str:
            messagebox.showwarning("Correo Inválido", "Por favor ingrese un correo electrónico válido.")
            return

        try:
            if self.is_edit:
                success = actualizar_usuario(self.id_usuario, nombre_str, apellido_str, correo_str)
                if success: messagebox.showinfo("Éxito", "Usuario actualizado")
                else: raise Exception("Error SQL al actualizar")
            else:
                success = crear_usuario(nombre_str, apellido_str, correo_str)
                if success: messagebox.showinfo("Éxito", "Usuario guardado")
                else: raise Exception("Error SQL al insertar")
            
            self.on_close_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la solicitud: {e}")


class CuentaModal(ctk.CTkToplevel):
    def __init__(self, parent, on_close_callback, cuenta=None):
        super().__init__(parent)
        self.on_close_callback = on_close_callback
        self.cuenta = cuenta
        self.is_edit = cuenta is not None
        
        self.title("Editar Cuenta" if self.is_edit else "Nueva Cuenta")
        self.geometry("450x550")
        self.configure(fg_color=("#F4F7FE", "#0b1437"))
        self.grab_set() 
        
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#111c44"), corner_radius=15)
        card.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(card, text="Editar Cuenta" if self.is_edit else "Registro de Cuenta", font=ctk.CTkFont(size=22, weight="bold"), text_color=("#1b2559", "#ffffff")).pack(pady=(20, 15))

        ctk.CTkLabel(card, text="Asignar al Usuario:", font=ctk.CTkFont(size=13), text_color=("#A3AED0", "#8f9bba")).pack(anchor="w", padx=45)
        self.usuarios_db = obtener_usuarios()
        self.usuarios_str_list = [f"{u[0]} - {u[1]} {u[2]} ({u[3]})" for u in self.usuarios_db]
        
        self.txt_usuario_id = ctk.CTkComboBox(card, width=300, height=40, corner_radius=8, values=self.usuarios_str_list, dropdown_font=ctk.CTkFont(size=12))
        self.txt_usuario_id.pack(pady=(5, 15))
        self.txt_usuario_id.bind("<KeyRelease>", self.filtrar_usuarios)

        self.txt_banco = ctk.CTkEntry(card, width=300, height=40, corner_radius=8, placeholder_text="Nombre del Banco", border_color=("#E2E8F0", "#2b3674"))
        self.txt_banco.pack(pady=(0, 15))
        apply_focus_ring(self.txt_banco)

        self.txt_numero = ctk.CTkEntry(card, width=300, height=40, corner_radius=8, placeholder_text="Número de Cuenta", border_color=("#E2E8F0", "#2b3674"))
        self.txt_numero.pack(pady=(0, 15))
        apply_focus_ring(self.txt_numero)
        
        self.txt_saldo = ctk.CTkEntry(card, width=300, height=40, corner_radius=8, placeholder_text="Saldo Inicial (S/)", border_color=("#E2E8F0", "#2b3674"))
        self.txt_saldo.pack(pady=(0, 25))
        apply_focus_ring(self.txt_saldo)

        if self.is_edit:
            self.id_cuenta = self.cuenta[0]
            id_u = self.cuenta[5]
            user_str = next((s for s in self.usuarios_str_list if s.startswith(f"{id_u} - ")), str(id_u))
            self.txt_usuario_id.set(user_str)
            self.txt_usuario_id.configure(state="disabled")
            self.txt_banco.insert(0, self.cuenta[2])
            self.txt_numero.insert(0, self.cuenta[3])
            self.txt_saldo.insert(0, str(self.cuenta[4]))

        btn_guardar = ctk.CTkButton(card, text="Actualizar" if self.is_edit else "Guardar Cuenta", height=45, command=self.guardar, fg_color="#05CD99" if not self.is_edit else "#FFB547", hover_color="#04A37A" if not self.is_edit else "#E09C34", text_color="white", corner_radius=8, font=ctk.CTkFont(size=15, weight="bold"))
        btn_guardar.pack(pady=10, fill="x", padx=40)
        
    def filtrar_usuarios(self, event):
        busqueda = self.txt_usuario_id.get().lower()
        if not busqueda:
            self.txt_usuario_id.configure(values=self.usuarios_str_list)
            return
        filtrados = [u for u in self.usuarios_str_list if busqueda in u.lower()]
        self.txt_usuario_id.configure(values=filtrados[:10]) 
        
    def guardar(self):
        usuario_seleccionado = self.txt_usuario_id.get().strip()
        banco_str = self.txt_banco.get().strip()
        numero_str = self.txt_numero.get().strip()
        saldo_str = self.txt_saldo.get().strip()

        if not usuario_seleccionado or not banco_str or not numero_str or not saldo_str:
            messagebox.showwarning("Campos incompletos", "Por favor, llene todos los campos de la cuenta.")
            return

        try:
            usuario_id_str = usuario_seleccionado.split(" - ")[0]
            usuario_id_val = int(usuario_id_str)
        except (ValueError, IndexError):
            messagebox.showwarning("Error de formato", "El Usuario ID debe ser un número entero válido.")
            return

        try:
            saldo_val = float(saldo_str)
        except ValueError:
            messagebox.showwarning("Error de formato", "El Saldo debe ser un valor numérico válido.")
            return

        try:
            if self.is_edit:
                success = actualizar_cuenta(self.id_cuenta, banco_str, numero_str, saldo_val)
                if success: messagebox.showinfo("Éxito", "Cuenta actualizada")
                else: raise Exception("Error SQL al actualizar")
            else:
                success = crear_cuenta(usuario_id_val, banco_str, numero_str, saldo_val)
                if success: messagebox.showinfo("Éxito", "Cuenta guardada")
                else: raise Exception("Error SQL al insertar (Verifica que el Usuario ID exista)")
            
            self.on_close_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la cuenta: {e}")


class CategoriaModal(ctk.CTkToplevel):
    def __init__(self, parent, on_close_callback, categoria=None):
        super().__init__(parent)
        self.on_close_callback = on_close_callback
        self.categoria = categoria
        self.is_edit = categoria is not None
        
        self.title("Editar Categoría" if self.is_edit else "Nueva Categoría")
        self.geometry("450x450")
        self.configure(fg_color=("#F4F7FE", "#0b1437"))
        self.grab_set() 
        
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#111c44"), corner_radius=15)
        card.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(card, text="Editar Categoría" if self.is_edit else "Registro de Categoría", font=ctk.CTkFont(size=22, weight="bold"), text_color=("#1b2559", "#ffffff")).pack(pady=25)

        self.txt_nombre = ctk.CTkEntry(card, width=300, height=40, corner_radius=8, placeholder_text="Nombre de Categoría", border_color=("#E2E8F0", "#2b3674"))
        self.txt_nombre.pack(pady=(0, 15))
        apply_focus_ring(self.txt_nombre)

        ctk.CTkLabel(card, text="Tipo de Categoría:", font=ctk.CTkFont(size=13), text_color=("#A3AED0", "#8f9bba")).pack(anchor="w", padx=45)
        self.txt_tipo = ctk.CTkComboBox(card, width=300, height=40, values=["INGRESO", "GASTO"])
        self.txt_tipo.pack(pady=(5, 25))

        if self.is_edit:
            self.id_categoria = self.categoria[0]
            self.txt_nombre.insert(0, self.categoria[1])
            self.txt_tipo.set(self.categoria[2])

        btn_guardar = ctk.CTkButton(card, text="Actualizar" if self.is_edit else "Guardar Categoría", height=45, command=self.guardar, fg_color="#4318FF" if not self.is_edit else "#FFB547", hover_color="#3311db" if not self.is_edit else "#E09C34", text_color="white", corner_radius=8, font=ctk.CTkFont(size=15, weight="bold"))
        btn_guardar.pack(pady=10, fill="x", padx=40)
        
    def guardar(self):
        nombre_str = self.txt_nombre.get().strip()
        tipo_str = self.txt_tipo.get().strip()

        if not nombre_str or not tipo_str:
            messagebox.showwarning("Campos incompletos", "Por favor, llene todos los campos.")
            return

        try:
            if self.is_edit:
                success = actualizar_categoria(self.id_categoria, nombre_str, tipo_str)
                if success: messagebox.showinfo("Éxito", "Categoría actualizada")
                else: raise Exception("Error SQL al actualizar")
            else:
                success = crear_categoria(nombre_str, tipo_str)
                if success: messagebox.showinfo("Éxito", "Categoría guardada")
                else: raise Exception("Error SQL al insertar")
            
            self.on_close_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la categoría: {e}")


class TransaccionModal(ctk.CTkToplevel):
    def __init__(self, parent, on_close_callback, transaccion=None):
        super().__init__(parent)
        self.on_close_callback = on_close_callback
        self.transaccion = transaccion
        self.is_edit = transaccion is not None
        
        self.title("Editar Transacción" if self.is_edit else "Nueva Transacción")
        self.geometry("450x620")
        self.configure(fg_color=("#F4F7FE", "#0b1437"))
        self.grab_set() 
        
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#111c44"), corner_radius=15)
        card.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(card, text="Editar Transacción" if self.is_edit else "Registrar Transacción", font=ctk.CTkFont(size=22, weight="bold"), text_color=("#1b2559", "#ffffff")).pack(pady=(15, 10))

        # Cuentas
        ctk.CTkLabel(card, text="Cuenta Bancaria origen/destino:", font=ctk.CTkFont(size=13), text_color=("#A3AED0", "#8f9bba")).pack(anchor="w", padx=45)
        self.cuentas_db = obtener_cuentas()
        self.cuentas_str_list = [f"{c[0]} - Cuenta {c[3]} ({c[2]})" for c in self.cuentas_db]
        self.txt_cuenta = ctk.CTkComboBox(card, width=300, height=40, values=self.cuentas_str_list)
        self.txt_cuenta.pack(pady=(5, 12))

        # Categorías
        ctk.CTkLabel(card, text="Categoría:", font=ctk.CTkFont(size=13), text_color=("#A3AED0", "#8f9bba")).pack(anchor="w", padx=45)
        self.categorias_db = obtener_categorias()
        self.categorias_str_list = [f"{cat[0]} - {cat[1]} ({cat[2]})" for cat in self.categorias_db]
        self.txt_categoria = ctk.CTkComboBox(card, width=300, height=40, values=self.categorias_str_list)
        self.txt_categoria.pack(pady=(5, 12))

        self.txt_monto = ctk.CTkEntry(card, width=300, height=40, placeholder_text="Monto de la Transacción (S/)", border_color=("#E2E8F0", "#2b3674"))
        self.txt_monto.pack(pady=(0, 12))
        apply_focus_ring(self.txt_monto)

        ctk.CTkLabel(card, text="Tipo de Transacción:", font=ctk.CTkFont(size=13), text_color=("#A3AED0", "#8f9bba")).pack(anchor="w", padx=45)
        self.txt_tipo = ctk.CTkComboBox(card, width=300, height=40, values=["INGRESO", "GASTO"])
        self.txt_tipo.pack(pady=(5, 12))

        self.txt_desc = ctk.CTkEntry(card, width=300, height=40, placeholder_text="Descripción corta", border_color=("#E2E8F0", "#2b3674"))
        self.txt_desc.pack(pady=(0, 15))
        apply_focus_ring(self.txt_desc)

        if self.is_edit:
            self.id_transaccion = self.transaccion[0]
            id_cu = self.transaccion[7]
            cu_str = next((s for s in self.cuentas_str_list if s.startswith(f"{id_cu} - ")), str(id_cu))
            self.txt_cuenta.set(cu_str)
            self.txt_cuenta.configure(state="disabled")

            id_cat = self.transaccion[8]
            cat_str = next((s for s in self.categorias_str_list if s.startswith(f"{id_cat} - ")), str(id_cat))
            self.txt_categoria.set(cat_str)
            self.txt_categoria.configure(state="disabled")

            self.txt_monto.insert(0, str(self.transaccion[4]))
            self.txt_tipo.set(self.transaccion[5])
            if self.transaccion[6]:
                self.txt_desc.insert(0, self.transaccion[6])

        btn_guardar = ctk.CTkButton(card, text="Actualizar" if self.is_edit else "Registrar (Stored Proc)", height=45, command=self.guardar, fg_color="#05CD99" if not self.is_edit else "#FFB547", hover_color="#04A37A" if not self.is_edit else "#E09C34", text_color="white", corner_radius=8, font=ctk.CTkFont(size=15, weight="bold"))
        btn_guardar.pack(pady=10, fill="x", padx=40)

    def guardar(self):
        cuenta_sel = self.txt_cuenta.get()
        categoria_sel = self.txt_categoria.get()
        monto_str = self.txt_monto.get().strip()
        tipo_str = self.txt_tipo.get()
        desc_str = self.txt_desc.get().strip()

        if not cuenta_sel or not categoria_sel or not monto_str:
            messagebox.showwarning("Campos incompletos", "Por favor llene los campos obligatorios.")
            return

        try:
            id_cuenta = int(cuenta_sel.split(" - ")[0])
            id_categoria = int(categoria_sel.split(" - ")[0])
            monto_val = float(monto_str)
        except Exception:
            messagebox.showwarning("Error de formato", "El Monto debe ser numérico y las relaciones válidas.")
            return

        try:
            if self.is_edit:
                success = actualizar_transaccion(self.id_transaccion, monto_val, tipo_str, desc_str)
                if success: messagebox.showinfo("Éxito", "Transacción modificada")
                else: raise Exception("Error SQL")
            else:
                success = crear_transaccion(id_cuenta, id_categoria, monto_val, tipo_str, desc_str)
                if success: messagebox.showinfo("Éxito", "Transacción registrada exitosamente. Saldo de cuenta bancaria actualizado automáticamente.")
                else: raise Exception("Error SQL en Stored Procedure. Verifica fondos o IDs.")
            
            self.on_close_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al registrar transacción: {e}")


class MetaAhorroModal(ctk.CTkToplevel):
    def __init__(self, parent, on_close_callback, meta=None):
        super().__init__(parent)
        self.on_close_callback = on_close_callback
        self.meta = meta
        self.is_edit = meta is not None
        
        self.title("Editar Meta" if self.is_edit else "Nueva Meta de Ahorro")
        self.geometry("450x600")
        self.configure(fg_color=("#F4F7FE", "#0b1437"))
        self.grab_set() 
        
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#111c44"), corner_radius=15)
        card.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(card, text="Editar Meta" if self.is_edit else "Crear Meta de Ahorro", font=ctk.CTkFont(size=22, weight="bold"), text_color=("#1b2559", "#ffffff")).pack(pady=(15, 10))

        # Usuarios
        ctk.CTkLabel(card, text="Usuario asignado:", font=ctk.CTkFont(size=13), text_color=("#A3AED0", "#8f9bba")).pack(anchor="w", padx=45)
        self.usuarios_db = obtener_usuarios()
        self.usuarios_str_list = [f"{u[0]} - {u[1]} {u[2]}" for u in self.usuarios_db]
        self.txt_usuario = ctk.CTkComboBox(card, width=300, height=40, values=self.usuarios_str_list)
        self.txt_usuario.pack(pady=(5, 12))

        self.txt_nombre = ctk.CTkEntry(card, width=300, height=40, placeholder_text="Nombre de la Meta (ej. Compras)", border_color=("#E2E8F0", "#2b3674"))
        self.txt_nombre.pack(pady=(0, 12))
        apply_focus_ring(self.txt_nombre)

        self.txt_objetivo = ctk.CTkEntry(card, width=300, height=40, placeholder_text="Monto Objetivo (S/)", border_color=("#E2E8F0", "#2b3674"))
        self.txt_objetivo.pack(pady=(0, 12))
        apply_focus_ring(self.txt_objetivo)

        self.txt_actual = ctk.CTkEntry(card, width=300, height=40, placeholder_text="Monto Actual Ahorrado (S/)", border_color=("#E2E8F0", "#2b3674"))
        self.txt_actual.pack(pady=(0, 12))
        apply_focus_ring(self.txt_actual)

        self.txt_limite = ctk.CTkEntry(card, width=300, height=40, placeholder_text="Fecha Límite (YYYY-MM-DD)", border_color=("#E2E8F0", "#2b3674"))
        self.txt_limite.pack(pady=(0, 12))
        apply_focus_ring(self.txt_limite)

        ctk.CTkLabel(card, text="Estado de la Meta:", font=ctk.CTkFont(size=13), text_color=("#A3AED0", "#8f9bba")).pack(anchor="w", padx=45)
        self.txt_estado = ctk.CTkComboBox(card, width=300, height=40, values=["EN_PROCESO", "CUMPLIDA", "CANCELADA"])
        self.txt_estado.pack(pady=(5, 15))

        if self.is_edit:
            self.id_meta = self.meta[0]
            id_u = self.meta[7]
            u_str = next((s for s in self.usuarios_str_list if s.startswith(f"{id_u} - ")), str(id_u))
            self.txt_usuario.set(u_str)
            self.txt_usuario.configure(state="disabled")

            self.txt_nombre.insert(0, self.meta[2])
            self.txt_objetivo.insert(0, str(self.meta[3]))
            self.txt_actual.insert(0, str(self.meta[4]))
            if self.meta[5]:
                self.txt_limite.insert(0, self.meta[5])
            self.txt_estado.set(self.meta[6])

        btn_guardar = ctk.CTkButton(card, text="Actualizar" if self.is_edit else "Guardar Meta", height=45, command=self.guardar, fg_color="#4318FF" if not self.is_edit else "#FFB547", hover_color="#3311db" if not self.is_edit else "#E09C34", text_color="white", corner_radius=8, font=ctk.CTkFont(size=15, weight="bold"))
        btn_guardar.pack(pady=10, fill="x", padx=40)

    def guardar(self):
        usr_sel = self.txt_usuario.get()
        nombre_str = self.txt_nombre.get().strip()
        obj_str = self.txt_objetivo.get().strip()
        act_str = self.txt_actual.get().strip()
        limite_str = self.txt_limite.get().strip()
        estado_str = self.txt_estado.get()

        if not usr_sel or not nombre_str or not obj_str or not act_str:
            messagebox.showwarning("Campos incompletos", "Por favor complete todos los datos.")
            return

        try:
            id_usuario = int(usr_sel.split(" - ")[0])
            obj_val = float(obj_str)
            act_val = float(act_str)
        except Exception:
            messagebox.showwarning("Error de formato", "Los montos deben ser valores numéricos válidos.")
            return

        try:
            if self.is_edit:
                success = actualizar_meta(self.id_meta, nombre_str, obj_val, act_val, limite_str, estado_str)
                if success: messagebox.showinfo("Éxito", "Meta actualizada")
                else: raise Exception("Error SQL")
            else:
                success = crear_meta(id_usuario, nombre_str, obj_val, act_val, limite_str, estado_str)
                if success: messagebox.showinfo("Éxito", "Meta registrada")
                else: raise Exception("Error SQL")
            
            self.on_close_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la meta: {e}")


class EstadoCuentaModal(ctk.CTkToplevel):
    def __init__(self, parent, on_close_callback, estado_c=None):
        super().__init__(parent)
        self.on_close_callback = on_close_callback
        self.estado_c = estado_c
        self.is_edit = estado_c is not None
        
        self.title("Editar Estado" if self.is_edit else "Nuevo Estado de Cuenta")
        self.geometry("450x550")
        self.configure(fg_color=("#F4F7FE", "#0b1437"))
        self.grab_set() 
        
        card = ctk.CTkFrame(self, fg_color=("#ffffff", "#111c44"), corner_radius=15)
        card.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(card, text="Editar Estado" if self.is_edit else "Crear Estado de Cuenta", font=ctk.CTkFont(size=22, weight="bold"), text_color=("#1b2559", "#ffffff")).pack(pady=(15, 10))

        # Cuentas
        ctk.CTkLabel(card, text="Cuenta Bancaria:", font=ctk.CTkFont(size=13), text_color=("#A3AED0", "#8f9bba")).pack(anchor="w", padx=45)
        self.cuentas_db = obtener_cuentas()
        self.cuentas_str_list = [f"{c[0]} - Cuenta {c[3]}" for c in self.cuentas_db]
        self.txt_cuenta = ctk.CTkComboBox(card, width=300, height=40, values=self.cuentas_str_list)
        self.txt_cuenta.pack(pady=(5, 12))

        self.txt_inicio = ctk.CTkEntry(card, width=300, height=40, placeholder_text="Fecha Inicio (YYYY-MM-DD)", border_color=("#E2E8F0", "#2b3674"))
        self.txt_inicio.pack(pady=(0, 12))
        apply_focus_ring(self.txt_inicio)

        self.txt_fin = ctk.CTkEntry(card, width=300, height=40, placeholder_text="Fecha Fin (YYYY-MM-DD)", border_color=("#E2E8F0", "#2b3674"))
        self.txt_fin.pack(pady=(0, 12))
        apply_focus_ring(self.txt_fin)

        self.txt_sinicial = ctk.CTkEntry(card, width=300, height=40, placeholder_text="Saldo Inicial (S/)", border_color=("#E2E8F0", "#2b3674"))
        self.txt_sinicial.pack(pady=(0, 12))
        apply_focus_ring(self.txt_sinicial)

        self.txt_sfinal = ctk.CTkEntry(card, width=300, height=40, placeholder_text="Saldo Final (S/)", border_color=("#E2E8F0", "#2b3674"))
        self.txt_sfinal.pack(pady=(0, 25))
        apply_focus_ring(self.txt_sfinal)

        if self.is_edit:
            self.id_estado = self.estado_c[0]
            id_c = self.estado_c[6]
            c_str = next((s for s in self.cuentas_str_list if s.startswith(f"{id_c} - ")), str(id_c))
            self.txt_cuenta.set(c_str)
            self.txt_cuenta.configure(state="disabled")

            self.txt_inicio.insert(0, self.estado_c[2])
            self.txt_fin.insert(0, self.estado_c[3])
            self.txt_sinicial.insert(0, str(self.estado_c[4]))
            self.txt_sfinal.insert(0, str(self.estado_c[5]))

        btn_guardar = ctk.CTkButton(card, text="Actualizar" if self.is_edit else "Guardar Estado", height=45, command=self.guardar, fg_color="#05CD99" if not self.is_edit else "#FFB547", hover_color="#04A37A" if not self.is_edit else "#E09C34", text_color="white", corner_radius=8, font=ctk.CTkFont(size=15, weight="bold"))
        btn_guardar.pack(pady=10, fill="x", padx=40)

    def guardar(self):
        c_sel = self.txt_cuenta.get()
        inicio_str = self.txt_inicio.get().strip()
        fin_str = self.txt_fin.get().strip()
        ini_val_str = self.txt_sinicial.get().strip()
        fin_val_str = self.txt_sfinal.get().strip()

        if not c_sel or not inicio_str or not fin_str or not ini_val_str or not fin_val_str:
            messagebox.showwarning("Campos incompletos", "Por favor complete todos los datos.")
            return

        try:
            id_cuenta = int(c_sel.split(" - ")[0])
            ini_val = float(ini_val_str)
            fin_val = float(fin_val_str)
        except Exception:
            messagebox.showwarning("Error de formato", "Los saldos deben ser numéricos.")
            return

        try:
            if self.is_edit:
                success = actualizar_estado(self.id_estado, inicio_str, fin_str, ini_val, fin_val)
                if success: messagebox.showinfo("Éxito", "Estado de cuenta actualizado")
                else: raise Exception("Error SQL")
            else:
                success = crear_estado(id_cuenta, inicio_str, fin_str, ini_val, fin_val)
                if success: messagebox.showinfo("Éxito", "Estado de cuenta registrado")
                else: raise Exception("Error SQL")
            
            self.on_close_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")


# --- CLASE PRINCIPAL VIEW ---

class OracleView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Cabecera superior
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(5, 10))
        
        self.lbl_title = ctk.CTkLabel(self.header_frame, text="Core Bancario (Oracle)", font=ctk.CTkFont(size=26, weight="bold"), text_color=("#1b2559", "#ffffff"))
        self.lbl_title.pack(side="left", padx=10)
        
        self.txt_search = ctk.CTkEntry(self.header_frame, placeholder_text="Buscar en tabla...", width=250, height=40, corner_radius=8, border_width=1, border_color=("#E2E8F0", "#2b3674"))
        self.txt_search.pack(side="left", padx=30)
        self.txt_search.bind("<KeyRelease>", lambda e: self.refresh_view())
        apply_focus_ring(self.txt_search)
        
        self.btn_add = ctk.CTkButton(self.header_frame, text="+ Nuevo Registro", command=self.open_add_modal, height=40, fg_color="#1b2559", hover_color="#2b3674", font=ctk.CTkFont(weight="bold", size=14), corner_radius=8)
        self.btn_add.pack(side="right", padx=10)

        # Contenedor de KPIs superiores (Métricas)
        self.kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_container.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 15))
        self.dibujar_kpi_cards()

        # Tabs extendidos con corrección de contraste para inactivos
        self.tab_control = ctk.CTkSegmentedButton(
            self, 
            values=["Usuarios", "Cuentas", "Categorías", "Transacciones", "Metas de Ahorro", "Estados de Cuenta"], 
            command=self.switch_view, 
            selected_color="#4318FF", 
            unselected_color=("#e2e8f0", "#1b2559"), 
            selected_hover_color="#3311db", 
            text_color=("#475569", "#a3aed0"), # Gris oscuro contrastante en modo claro, gris suave en modo oscuro
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.tab_control.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 15))
        self.tab_control.set("Usuarios")
        
        self.current_view = "usuarios"

        # Tabla (ScrollableFrame)
        self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=15, fg_color=("#ffffff", "#111c44"), border_width=1, border_color=("#E2E8F0", "#1b2559"))
        self.scroll_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.refresh_view()

    def dibujar_kpi_cards(self):
        for w in self.kpi_container.winfo_children():
            w.destroy()

        users_count = len(obtener_usuarios())
        accounts = obtener_cuentas()
        accounts_count = len(accounts)
        total_bal = sum(c[4] for c in accounts)

        card_bg = ("#ffffff", "#111c44")
        text_color = ("#1b2559", "#ffffff")
        sub_text_color = ("#A3AED0", "#8f9bba")

        # Card 1: Usuarios
        c1 = ctk.CTkFrame(self.kpi_container, fg_color=card_bg, corner_radius=12, height=75, border_width=1, border_color=("#E2E8F0", "#1b2559"))
        c1.pack(side="left", expand=True, fill="both", padx=5)
        c1.pack_propagate(False)
        ctk.CTkLabel(c1, text="Total Usuarios", font=ctk.CTkFont(size=11, weight="bold"), text_color=sub_text_color, anchor="w").pack(padx=15, pady=(8,0))
        ctk.CTkLabel(c1, text=str(users_count), font=ctk.CTkFont(size=20, weight="bold"), text_color=text_color, anchor="w").pack(padx=15)

        # Card 2: Cuentas
        c2 = ctk.CTkFrame(self.kpi_container, fg_color=card_bg, corner_radius=12, height=75, border_width=1, border_color=("#E2E8F0", "#1b2559"))
        c2.pack(side="left", expand=True, fill="both", padx=5)
        c2.pack_propagate(False)
        ctk.CTkLabel(c2, text="Cuentas Core", font=ctk.CTkFont(size=11, weight="bold"), text_color=sub_text_color, anchor="w").pack(padx=15, pady=(8,0))
        ctk.CTkLabel(c2, text=str(accounts_count), font=ctk.CTkFont(size=20, weight="bold"), text_color=text_color, anchor="w").pack(padx=15)

        # Card 3: Capital
        c3 = ctk.CTkFrame(self.kpi_container, fg_color=card_bg, corner_radius=12, height=75, border_width=1, border_color=("#E2E8F0", "#1b2559"))
        c3.pack(side="left", expand=True, fill="both", padx=5)
        c3.pack_propagate(False)
        ctk.CTkLabel(c3, text="Capital Concentrado", font=ctk.CTkFont(size=11, weight="bold"), text_color=sub_text_color, anchor="w").pack(padx=15, pady=(8,0))
        ctk.CTkLabel(c3, text=f"S/ {total_bal:,.2f}", font=ctk.CTkFont(size=18, weight="bold"), text_color="#05cd99", anchor="w").pack(padx=15)

    def switch_view(self, value):
        mapping = {
            "Usuarios": "usuarios",
            "Cuentas": "cuentas",
            "Categorías": "categorias",
            "Transacciones": "transacciones",
            "Metas de Ahorro": "metas",
            "Estados de Cuenta": "estados"
        }
        self.current_view = mapping.get(value, "usuarios")
        self.txt_search.delete(0, "end")
        self.refresh_view()

    def refresh_view(self):
        self.limpiar_tabla()
        self.dibujar_kpi_cards() # Refrescar métricas arriba
        getattr(self, f"mostrar_{self.current_view}")()

    def open_add_modal(self):
        modal_class = {
            "usuarios": UsuarioModal,
            "cuentas": CuentaModal,
            "categorias": CategoriaModal,
            "transacciones": TransaccionModal,
            "metas": MetaAhorroModal,
            "estados": EstadoCuentaModal
        }[self.current_view]
        modal_class(self, self.refresh_view)

    def open_edit_modal(self, record):
        modal_class = {
            "usuarios": UsuarioModal,
            "cuentas": CuentaModal,
            "categorias": CategoriaModal,
            "transacciones": TransaccionModal,
            "metas": MetaAhorroModal,
            "estados": EstadoCuentaModal
        }[self.current_view]
        modal_class(self, self.refresh_view, record)

    def eliminar_registro(self, record_id):
        if not messagebox.askyesno("Confirmar", f"¿Desea eliminar este registro ID {record_id}?"):
            return
            
        success = False
        if self.current_view == "usuarios":
            success = eliminar_usuario(record_id)
        elif self.current_view == "cuentas":
            success = eliminar_cuenta(record_id)
        elif self.current_view == "categorias":
            success = eliminar_categoria(record_id)
        elif self.current_view == "transacciones":
            success = eliminar_transaccion(record_id)
        elif self.current_view == "metas":
            success = eliminar_meta(record_id)
        elif self.current_view == "estados":
            success = eliminar_estado(record_id)
            
        if success:
            self.refresh_view()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el registro por dependencias SQL.")

    def limpiar_tabla(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

    def generar_cabecera(self, columnas):
        header_row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        header_row.pack(fill="x", pady=(15, 10), padx=20)
        for col_name, col_width in columnas:
            ctk.CTkLabel(header_row, text=col_name, width=col_width, anchor="w", font=ctk.CTkFont(size=14, weight="bold"), text_color=("#A3AED0", "#8f9bba")).pack(side="left")
        ctk.CTkLabel(header_row, text="Acciones", width=160, font=ctk.CTkFont(size=14, weight="bold"), text_color=("#A3AED0", "#8f9bba")).pack(side="right")

    def renderizar_filas(self, dataset, format_funcs, row_pills=None):
        if not dataset:
            ctk.CTkLabel(self.scroll_frame, text="No se encontraron registros.", text_color=("#A3AED0", "#8f9bba"), font=ctk.CTkFont(size=15)).pack(pady=40)
            return

        row_bg = ("#F4F7FE", "#1b2559")
        row_hover = ("#e9effd", "#233375")

        for row_data in dataset:
            row = ctk.CTkFrame(self.scroll_frame, corner_radius=10, fg_color=row_bg, height=60)
            row.pack(fill="x", pady=6, padx=10)
            row.pack_propagate(False)
            
            row_labels = []
            
            # Dibujar columnas
            for index, (col_width, align, font_style, text_color) in enumerate(format_funcs):
                val = str(row_data[index]) if row_data[index] is not None else ""
                
                # Check si esta columna debe renderizarse como una pastilla (Pill)
                if row_pills and index in row_pills:
                    pill_colors = row_pills[index](val)
                    p_frame = ctk.CTkFrame(row, fg_color=pill_colors[0], corner_radius=12, width=col_width-15, height=26)
                    p_frame.pack(side="left", padx=(10 if index == 0 else 0, 15))
                    p_frame.pack_propagate(False)
                    
                    lbl_val = ctk.CTkLabel(p_frame, text=val.upper(), text_color=pill_colors[1], font=ctk.CTkFont(size=10, weight="bold"), anchor="center")
                    lbl_val.pack(fill="both", expand=True)
                    row_labels.extend([p_frame, lbl_val])
                else:
                    lbl_val = ctk.CTkLabel(row, text=val, width=col_width, anchor=align, text_color=text_color, font=font_style)
                    lbl_val.pack(side="left", padx=(10 if index == 0 else 0, 0))
                    row_labels.append(lbl_val)
            
            # Acciones
            actions = ctk.CTkFrame(row, fg_color="transparent")
            actions.pack(side="right", padx=10)
            btn_edit = ctk.CTkButton(actions, text="Editar", width=70, height=30, fg_color="#FFB547", hover_color="#E09C34", command=lambda r=row_data: self.open_edit_modal(r))
            btn_edit.pack(side="left", padx=5)
            btn_del = ctk.CTkButton(actions, text="Borrar", width=70, height=30, fg_color="#EE5D50", hover_color="#D14E42", command=lambda r_id=row_data[0]: self.eliminar_registro(r_id))
            btn_del.pack(side="left", padx=5)
            
            # Aplicar Hover
            apply_row_hover(row, row_labels, row_bg, row_hover)

        # Pie de tabla
        footer = ctk.CTkLabel(self.scroll_frame, text=f"Mostrando {len(dataset)} registros de Oracle en tiempo real. Conexión segura SSL.", font=ctk.CTkFont(size=11, weight="bold"), text_color=("#A3AED0", "#8f9bba"))
        footer.pack(pady=(20, 10))

    # --- PILL COLOR RETRIEVER MAPS ---
    
    def get_tipo_pill(self, val):
        if val.upper() == "INGRESO":
            return ("#DCFCE7", "#15803d") # Verde
        else:
            return ("#FEE2E2", "#b91c1c") # Rojo

    def get_meta_pill(self, val):
        v = val.upper()
        if v == "CUMPLIDA":
            return ("#DCFCE7", "#15803d") # Verde
        elif v == "CANCELADA":
            return ("#FEE2E2", "#b91c1c") # Rojo
        else:
            return ("#FEF3C7", "#b45309") # Ámbar

    # --- RENDERIZADORES PARTICULARES ---

    def mostrar_usuarios(self):
        usuarios = obtener_usuarios()
        query = self.txt_search.get().lower()
        if query:
            usuarios = [u for u in usuarios if query in u[1].lower() or query in u[2].lower() or query in u[3].lower()]
            
        self.generar_cabecera([("ID", 60), ("Nombre", 180), ("Apellidos", 180), ("Correo", 220)])
        
        self.renderizar_filas(usuarios, [
            (60, "w", ctk.CTkFont(size=14, weight="bold"), ("#1b2559", "#ffffff")),
            (180, "w", ctk.CTkFont(size=14), ("#1b2559", "#ffffff")),
            (180, "w", ctk.CTkFont(size=14), ("#1b2559", "#ffffff")),
            (220, "w", ctk.CTkFont(size=14), ("#707EAE", "#a3aed0"))
        ])

    def mostrar_cuentas(self):
        cuentas = obtener_cuentas()
        query = self.txt_search.get().lower()
        if query:
            cuentas = [c for c in cuentas if query in c[2].lower() or query in c[3].lower() or query in str(c[1]).lower()]
            
        self.generar_cabecera([("ID", 60), ("Propietario", 120), ("Banco", 160), ("Nro. Cuenta", 180), ("Saldo", 120)])
        
        self.renderizar_filas(cuentas, [
            (60, "w", ctk.CTkFont(size=14, weight="bold"), ("#1b2559", "#ffffff")),
            (120, "w", ctk.CTkFont(size=14), ("#1b2559", "#ffffff")),
            (160, "w", ctk.CTkFont(size=14), ("#1b2559", "#ffffff")),
            (180, "w", ctk.CTkFont(size=14), ("#707EAE", "#a3aed0")),
            (120, "w", ctk.CTkFont(size=15, weight="bold"), "#05cd99")
        ])

    def mostrar_categorias(self):
        categorias = obtener_categorias()
        query = self.txt_search.get().lower()
        if query:
            categorias = [cat for cat in categorias if query in cat[1].lower() or query in cat[2].lower()]
            
        self.generar_cabecera([("ID", 80), ("Nombre Categoría", 250), ("Tipo", 180)])
        
        self.renderizar_filas(categorias, [
            (80, "w", ctk.CTkFont(size=14, weight="bold"), ("#1b2559", "#ffffff")),
            (250, "w", ctk.CTkFont(size=14, weight="bold"), ("#1b2559", "#ffffff")),
            (180, "w", ctk.CTkFont(size=14), ("#4318FF", "#8c54ff"))
        ], row_pills={2: self.get_tipo_pill})

    def mostrar_transacciones(self):
        transacciones = obtener_transacciones()
        query = self.txt_search.get().lower()
        if query:
            transacciones = [t for t in transacciones if query in t[1].lower() or query in t[2].lower() or query in t[5].lower() or (t[6] and query in t[6].lower())]
            
        self.generar_cabecera([("ID", 50), ("Cuenta", 150), ("Categoría", 130), ("Fecha", 140), ("Monto", 100), ("Tipo", 100), ("Detalle", 120)])
        
        self.renderizar_filas(transacciones, [
            (50, "w", ctk.CTkFont(size=13, weight="bold"), ("#1b2559", "#ffffff")),
            (150, "w", ctk.CTkFont(size=13), ("#707EAE", "#a3aed0")),
            (130, "w", ctk.CTkFont(size=13, weight="bold"), ("#1b2559", "#ffffff")),
            (140, "w", ctk.CTkFont(size=13), ("#1b2559", "#ffffff")),
            (100, "w", ctk.CTkFont(size=14, weight="bold"), "#05cd99"),
            (100, "w", ctk.CTkFont(size=13, weight="bold"), ("#4318FF", "#8c54ff")),
            (120, "w", ctk.CTkFont(size=13), ("#707EAE", "#a3aed0"))
        ], row_pills={5: self.get_tipo_pill})

    def mostrar_metas(self):
        metas = obtener_metas()
        query = self.txt_search.get().lower()
        if query:
            metas = [m for m in metas if query in m[1].lower() or query in m[2].lower() or query in m[6].lower()]
            
        self.generar_cabecera([("ID", 50), ("Usuario", 150), ("Nombre Meta", 150), ("Objetivo", 100), ("Ahorrado", 100), ("Límite", 100), ("Estado", 130)])
        
        self.renderizar_filas(metas, [
            (50, "w", ctk.CTkFont(size=13, weight="bold"), ("#1b2559", "#ffffff")),
            (150, "w", ctk.CTkFont(size=13), ("#1b2559", "#ffffff")),
            (150, "w", ctk.CTkFont(size=13, weight="bold"), ("#1b2559", "#ffffff")),
            (100, "w", ctk.CTkFont(size=13), ("#707EAE", "#a3aed0")),
            (100, "w", ctk.CTkFont(size=14, weight="bold"), "#05cd99"),
            (100, "w", ctk.CTkFont(size=13), ("#1b2559", "#ffffff")),
            (130, "w", ctk.CTkFont(size=13, weight="bold"), ("#4318FF", "#8c54ff"))
        ], row_pills={6: self.get_meta_pill})

    def mostrar_estados(self):
        estados = obtener_estados()
        query = self.txt_search.get().lower()
        if query:
            estados = [e for e in estados if query in e[1].lower()]
            
        self.generar_cabecera([("ID", 60), ("Nro. Cuenta", 180), ("Fecha Inicio", 130), ("Fecha Fin", 130), ("Saldo Inicial", 120), ("Saldo Final", 120)])
        
        self.renderizar_filas(estados, [
            (60, "w", ctk.CTkFont(size=13, weight="bold"), ("#1b2559", "#ffffff")),
            (180, "w", ctk.CTkFont(size=13), ("#707EAE", "#a3aed0")),
            (130, "w", ctk.CTkFont(size=13), ("#1b2559", "#ffffff")),
            (130, "w", ctk.CTkFont(size=13), ("#1b2559", "#ffffff")),
            (120, "w", ctk.CTkFont(size=13), ("#1b2559", "#ffffff")),
            (120, "w", ctk.CTkFont(size=14, weight="bold"), "#05cd99")
        ])
