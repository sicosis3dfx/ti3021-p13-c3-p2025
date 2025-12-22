# ==============================================================================
# Archivo: flet_ecotech_final.py
# Alumno: Angelo
# Versión: V22 (Refactorización a POO - Estructura Docente)
# ==============================================================================

import flet as ft
from ecotech_final import Database, Auth, Finance
import datetime
import time 

class EcoTechApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.configurar_pagina()
        
        # --- Estado de la Aplicación (Variables Globales de la Clase) ---
        self.usuario_sesion = None
        self.db = None
        
        # --- Inicializar BD ---
        try:
            self.db = Database()
            self.db.create_all_tables()
        except Exception as e:
            self.page.add(ft.Text(f"Error crítico BD: {e}", color="red"))
            return

        # --- Iniciar App ---
        self.ir_a_bienvenida()

    def configurar_pagina(self):
        self.page.title = "EcoTech Finanzas"
        self.page.window_width = 450
        self.page.window_height = 800
        self.page.theme_mode = "light"
        self.page.horizontal_alignment = "center"
        self.page.padding = 0
        
        # Constantes de diseño
        self.COLOR_TEAL = "teal"
        self.COLOR_VERDE = "green"
        self.gradient_fondo = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#004d40", "#66bb6a"], 
        )

    # ==========================================================================
    # PANTALLAS (VISTAS)
    # ==========================================================================

    def ir_a_bienvenida(self):
        self.page.clean()
        
        contenido = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ECO, size=100, color="white"),
                ft.Text("EcoTech Finanzas", size=35, weight="bold", color="white"),
                ft.Text("Monitor de Indicadores Financieros", size=16, color="white70"),
                ft.Container(height=50),
                ft.ElevatedButton(
                    "Ingresar al Portal", 
                    on_click=lambda _: self.ir_a_login(), 
                    width=250, height=50, bgcolor="white", color=self.COLOR_TEAL
                ),
            ], alignment="center", horizontal_alignment="center"),
            gradient=self.gradient_fondo, expand=True, alignment=ft.alignment.center
        )
        self.page.add(contenido)

    def ir_a_login(self):
        self.page.clean()
        
        # Controles locales
        self.txt_user = ft.TextField(label="Usuario", prefix_icon=ft.Icons.PERSON, width=280, border_radius=10, bgcolor="white")
        self.txt_pass = ft.TextField(label="Contraseña", prefix_icon=ft.Icons.LOCK, password=True, can_reveal_password=True, width=280, border_radius=10, bgcolor="white")
        self.lbl_mensaje = ft.Text(color="red", weight="bold")

        tarjeta = ft.Container(
            bgcolor="white", padding=30, border_radius=20,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK45),
            content=ft.Column([
                ft.Text("Bienvenido", size=25, weight="bold", color=self.COLOR_TEAL),
                ft.Container(height=20),
                self.txt_user, self.txt_pass,
                ft.Container(height=20),
                ft.ElevatedButton("Entrar", on_click=self.procesar_login, width=280, height=45, bgcolor=self.COLOR_TEAL, color="white"),
                ft.Container(height=10),
                ft.TextButton("Crear cuenta nueva", on_click=lambda _: self.ir_a_registro()),
                self.lbl_mensaje
            ], alignment="center", horizontal_alignment="center")
        )
        self.page.add(ft.Container(content=tarjeta, gradient=self.gradient_fondo, expand=True, alignment=ft.alignment.center))

    def ir_a_registro(self):
        self.page.clean()
        
        self.txt_user = ft.TextField(label="Usuario", prefix_icon=ft.Icons.PERSON, width=280, border_radius=10, bgcolor="white")
        self.txt_pass = ft.TextField(label="Contraseña", prefix_icon=ft.Icons.LOCK, password=True, can_reveal_password=True, width=280, border_radius=10, bgcolor="white")
        self.lbl_mensaje = ft.Text(color="red", weight="bold")
        
        tarjeta = ft.Container(
            bgcolor="white", padding=30, border_radius=20,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK45),
            content=ft.Column([
                ft.Text("Nueva Cuenta", size=25, weight="bold", color=self.COLOR_VERDE),
                ft.Container(height=20),
                self.txt_user, self.txt_pass,
                ft.Container(height=20),
                ft.ElevatedButton("Registrarme", on_click=self.procesar_registro, width=280, height=45, bgcolor=self.COLOR_VERDE, color="white"),
                ft.Container(height=10),
                ft.OutlinedButton("Cancelar", on_click=lambda _: self.ir_a_login(), width=280),
                self.lbl_mensaje 
            ], alignment="center", horizontal_alignment="center")
        )
        self.page.add(ft.Container(content=tarjeta, gradient=self.gradient_fondo, expand=True, alignment=ft.alignment.center))

    def ir_a_dashboard(self):
        self.page.clean()
        
        # Inicializamos objeto finanzas
        self.finanzas = Finance(self.db, self.usuario_sesion)
        
        # Elementos UI
        self.lbl_resultado_api = ft.Text("Selecciona un indicador", size=22, weight="bold", color=self.COLOR_TEAL)
        self.tabla_dashboard = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Ind", weight="bold", color=self.COLOR_TEAL)), 
                ft.DataColumn(ft.Text("Valor/Detalle", weight="bold", color=self.COLOR_TEAL)),
                ft.DataColumn(ft.Text("Origen", weight="bold", color=self.COLOR_TEAL)),
            ], 
            heading_row_color=ft.Colors.TEAL_50,
            column_spacing=10,
            rows=[]
        )
        
        # Cargar datos iniciales
        self.actualizar_tabla_dashboard()

        # Botones de indicadores
        def btn(t, d):
            return ft.ElevatedButton(t, data=d, on_click=self.consultar_indicador, bgcolor=ft.Colors.TEAL_50, color=self.COLOR_TEAL)

        filas_botones = ft.Column([
            ft.Row([btn("UF", "uf"), btn("Dólar", "dolar"), btn("Euro", "euro")], alignment="center"),
            ft.Container(height=5),
            ft.Row([btn("UTM", "utm"), btn("IPC", "ipc"), btn("IVP", "ivp")], alignment="center")
        ])

        header = ft.Container(
            padding=15, gradient=ft.LinearGradient(colors=[self.COLOR_TEAL, self.COLOR_VERDE]),
            content=ft.Row([
                ft.Icon(ft.Icons.PERSON, color="white"),
                ft.Text(f"Hola, {self.usuario_sesion}", weight="bold", color="white"),
                ft.Container(expand=True),
                ft.TextButton("Historial", icon=ft.Icons.HISTORY, style=ft.ButtonStyle(color=ft.Colors.WHITE), on_click=lambda _: self.ir_a_reportes())
            ])
        )

        btn_analisis = ft.ElevatedButton(
            "Análisis Anual", icon=ft.Icons.CALENDAR_MONTH, 
            bgcolor=ft.Colors.ORANGE_50, color=ft.Colors.ORANGE_900, width=145,
            on_click=lambda _: self.ir_a_analisis_anual()
        )
        
        btn_fecha = ft.ElevatedButton(
            "Por fecha", icon=ft.Icons.DATE_RANGE, 
            bgcolor=ft.Colors.BLUE_50, color=ft.Colors.BLUE_900, width=145,
            on_click=lambda _: self.ir_a_consulta_fecha()
        )

        contenido = ft.Column([
            ft.Container(height=20),
            self.lbl_resultado_api,
            ft.Container(height=20),
            filas_botones,
            ft.Container(height=20),
            ft.Row([btn_analisis, btn_fecha], alignment="center"),
            ft.Divider(),
            ft.Text("Últimos Movimientos", weight="bold"),
            self.tabla_dashboard
        ], horizontal_alignment="center", scroll="auto", expand=True)

        footer = ft.Container(
            padding=15, bgcolor=ft.Colors.GREY_100, alignment=ft.alignment.center,
            content=ft.ElevatedButton("Cerrar Sesión", on_click=lambda _: self.ir_a_login(), color="red", bgcolor="white")
        )
        self.page.add(ft.Column([header, contenido, footer], spacing=0, expand=True))

    def ir_a_reportes(self):
        self.page.clean()
        
        header = ft.Container(
            bgcolor=self.COLOR_TEAL, padding=15, 
            content=ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: self.ir_a_dashboard()),
                ft.Text("Historial Completo", size=18, weight="bold", color="white"),
            ])
        )

        col_reporte = ft.Column(scroll="auto", expand=True, horizontal_alignment="center")
        datos = Finance(self.db, self.usuario_sesion).get_history()
        
        for fila in datos:
            valor = fila[1]
            origen = fila[4]
            fecha_hora = fila[3].strftime("%d-%m-%Y %H:%M")
            
            if valor == 0:
                titulo = f"{fila[0].upper()} - RESUMEN ANUAL"
                subtitulo = f"Fuente: {origen}\nConsultado: {fecha_hora}"
                icono, color = ft.Icons.DATE_RANGE, "orange"
            else:
                titulo = f"{fila[0].upper()}: ${valor}"
                subtitulo = f"Fuente: {origen}\nConsultado: {fecha_hora}"
                icono, color = ft.Icons.MONETIZATION_ON, self.COLOR_TEAL

            col_reporte.controls.append(ft.Container(
                margin=5, padding=10, bgcolor="white", border_radius=10, border=ft.border.all(1, "grey300"),
                content=ft.ListTile(
                    leading=ft.Icon(icono, color=color, size=30),
                    title=ft.Text(titulo, weight="bold", size=14),
                    subtitle=ft.Text(subtitulo, size=11, color="grey")
                )
            ))

        self.page.add(ft.Column([header, col_reporte], expand=True, spacing=0))

    def ir_a_consulta_fecha(self):
        self.page.clean()
        
        header = ft.Container(
            bgcolor="blue", padding=15, 
            content=ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: self.ir_a_dashboard()),
                ft.Text("Consulta por Fecha", size=18, weight="bold", color="white"),
            ])
        )

        lbl_advertencia = ft.Text("", color="orange", size=13, weight="bold")
        hoy = datetime.datetime.now()
        fecha_hoy_str = f"{hoy.day}-{hoy.month}-{hoy.year}"
        
        self.txt_fecha = ft.TextField(label="Fecha (DD-MM-YYYY)", value=fecha_hoy_str, width=250)
        self.lbl_res_fecha = ft.Text("", size=20, weight="bold", color="blue")

        def cambio_indicador(e):
            if self.dd_ind.value in ["ipc", "utm"]:
                mes_ant = hoy.month - 1
                anio_ant = hoy.year
                if mes_ant == 0:
                    mes_ant = 12
                    anio_ant -= 1
                fecha_sugerida = f"01-{mes_ant}-{anio_ant}"
                lbl_advertencia.value = f"💡 IPC/UTM Mensual. Se ajustó fecha al {fecha_sugerida}."
                self.txt_fecha.value = fecha_sugerida 
            else:
                lbl_advertencia.value = ""
                self.txt_fecha.value = fecha_hoy_str 
            self.page.update()

        self.dd_ind = ft.Dropdown(
            label="Indicador", width=250, value="dolar", 
            options=[
                ft.dropdown.Option("dolar"), ft.dropdown.Option("uf"), ft.dropdown.Option("euro"), 
                ft.dropdown.Option("utm"), ft.dropdown.Option("ipc"), ft.dropdown.Option("ivp")
            ],
            on_change=cambio_indicador
        )
        
        def ejecutar(e):
            self.lbl_res_fecha.value = "Consultando..."
            self.page.update()
            val = Finance(self.db, self.usuario_sesion).get_indicator(self.dd_ind.value, self.txt_fecha.value)
            
            if val == -1:
                self.lbl_res_fecha.value = "Sin datos para esa fecha."
                self.lbl_res_fecha.color = "red"
            else:
                self.lbl_res_fecha.value = f"Valor: ${val}"
                self.lbl_res_fecha.color = "green"
            self.page.update()

        contenido = ft.Column([
            ft.Container(height=20),
            ft.Text("Selecciona indicador y fecha exacta:", size=16),
            ft.Container(height=20),
            self.dd_ind,
            lbl_advertencia,
            self.txt_fecha,
            ft.Text("(Recuerda usar días hábiles para Dólar, UF, Euro, etc.)", size=12, color="grey"),
            ft.Container(height=20),
            ft.ElevatedButton("Consultar", on_click=ejecutar, bgcolor="blue", color="white", width=200),
            ft.Divider(),
            self.lbl_res_fecha
        ], horizontal_alignment="center", expand=True)

        self.page.add(ft.Column([header, contenido], expand=True))

    def ir_a_analisis_anual(self):
        self.page.clean()
        
        header = ft.Container(
            bgcolor="orange", padding=15, 
            content=ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: self.ir_a_dashboard()),
                ft.Text("Análisis Anual", size=18, weight="bold", color="white"),
            ])
        )

        dd_ind = ft.Dropdown(label="Indicador", width=180, value="dolar", options=[
            ft.dropdown.Option("dolar"), ft.dropdown.Option("uf"), ft.dropdown.Option("euro"), 
            ft.dropdown.Option("utm"), ft.dropdown.Option("ipc"), ft.dropdown.Option("ivp")
        ])
        txt_y = ft.TextField(label="Año", value=str(datetime.datetime.now().year), width=100)
        
        col_res = ft.Column(scroll="auto", expand=True, horizontal_alignment="center")
        lbl_st = ft.Text("")

        def ejecutar(e):
            col_res.controls.clear()
            lbl_st.value = "Consultando..."
            self.page.update()
            
            datos = Finance(self.db, self.usuario_sesion).get_yearly_data(dd_ind.value, txt_y.value)
            
            if not datos:
                lbl_st.value = "Sin datos."
            else:
                lbl_st.value = f"{len(datos)} registros."
                lbl_st.color = "green"
                for i in datos:
                    col_res.controls.append(ft.Container(
                        margin=5, padding=10, width=320, bgcolor="white", border_radius=10, border=ft.border.all(1, "grey300"),
                        content=ft.Row([
                            ft.Text(i['fecha'][:10], weight="bold"),
                            ft.Container(expand=True),
                            ft.Text(f"${i['valor']}", color="blue", weight="bold")
                        ])
                    ))
            self.page.update()

        self.page.add(ft.Column([
            header, ft.Container(height=10),
            ft.Row([dd_ind, txt_y], alignment="center"),
            ft.ElevatedButton("Consultar", on_click=ejecutar, bgcolor="orange", color="white"),
            lbl_st, ft.Divider(), col_res
        ], expand=True, horizontal_alignment="center"))

    # ==========================================================================
    # LÓGICA DE NEGOCIO (Manejadores de Eventos)
    # ==========================================================================

    def procesar_login(self, e):
        user = self.txt_user.value
        pwd = self.txt_pass.value
        if not user or not pwd:
            self.lbl_mensaje.value = "Ingresa tus credenciales"
            self.lbl_mensaje.color = "red"
            self.page.update()
            return
        
        resp = Auth.login(self.db, user, pwd)
        
        if resp["success"]:
            self.lbl_mensaje.value = f"Bienvenido {user}"
            self.lbl_mensaje.color = "green"
            self.page.update()
            time.sleep(1.5) 
            self.usuario_sesion = user
            self.ir_a_dashboard()
        else:
            self.lbl_mensaje.value = resp["message"]
            self.lbl_mensaje.color = "red"
            self.page.update()

    def procesar_registro(self, e):
        user = self.txt_user.value
        pwd = self.txt_pass.value
        if not user or not pwd:
            self.lbl_mensaje.value = "Faltan datos"
            self.lbl_mensaje.color = "red"
            self.page.update()
            return
        
        resp = Auth.register(self.db, user, pwd)
        
        if resp["success"]:
            self.lbl_mensaje.value = "Registrado de manera exitosa"
            self.lbl_mensaje.color = "green"
            self.page.update()
            time.sleep(1.5)
            self.ir_a_login()
        else:
            self.lbl_mensaje.value = resp["message"]
            self.lbl_mensaje.color = "red"
            self.page.update()

    def consultar_indicador(self, e):
        ind = e.control.data 
        valor = self.finanzas.get_indicator(ind)
        if valor != -1:
            self.lbl_resultado_api.value = f"{ind.upper()}: ${valor}"
            self.actualizar_tabla_dashboard()
        else:
            self.lbl_resultado_api.value = "Datos no disponibles"
        self.page.update()

    def actualizar_tabla_dashboard(self):
        datos = self.finanzas.get_history()
        self.tabla_dashboard.rows.clear()
        if datos:
            for fila in datos[:5]: 
                indicador = fila[0].upper()
                valor = fila[1]
                origen = fila[4]
                
                if valor == 0:
                    texto_valor = "ANUAL"
                    color_valor = "orange"
                else:
                    texto_valor = f"${valor}"
                    color_valor = "black"

                origen_corto = origen.replace("https://mindicador.cl/api", "API").replace("https://", "")
                
                self.tabla_dashboard.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(indicador, weight="bold")),
                    ft.DataCell(ft.Text(texto_valor, color=color_valor, weight="bold", size=12)),
                    ft.DataCell(ft.Text(origen_corto, size=10, color="grey")),
                ]))
        self.page.update()

# --- ARRANQUE DE LA CLASE ---
if __name__ == "__main__":
    ft.app(target=EcoTechApp)