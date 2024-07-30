import tkinter as tk
from tkinter import font
from tkinter import ttk,messagebox
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util_ventana as util_ventana
import util_imagenes as util_img

class FormularioMaestroDesign(tk.Tk):

    def __init__(self):
        super().__init__()
        self.logo = util_img.leer_imagen("./imagenes/fond3.jpg", (1400, 1000))
        self.perfil = util_img.leer_imagen("./imagenes/fon.jpg", (100, 100))

        self.dni_entry_var = tk.StringVar()
        self.dni_personal_entry_var = tk.StringVar()
        self.nombre_entry_var = tk.StringVar()
        self.nombre_personal_entry_var = tk.StringVar()

        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.controles_cuerpo()



    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Python GUI')
        self.iconbitmap("./imagenes/log.ico")
        w, h = 1024, 600
        util_ventana.centrar_ventana(self, w, h)

    def paneles(self):
        # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        '''self.menu_left = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=300)
        self.menu_left.pack(side=tk.LEFT, fill='both', expand=False'''

        self.cuerpo_principal = tk.Frame(self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Redes Azàngaro")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                           command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        self.buttonCargarDatos = tk.Button(self.barra_superior, text="Cargar datos", font=("Roboto", 12),
                                           command=self.cargar_datos, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonCargarDatos.pack(side=tk.LEFT, padx=10)

        self.bind_hover_events(self.buttonCargarDatos)
        # Etiqueta de informacion
        self.labelTitulo = tk.Label(self.barra_superior, text="RedDeSalud@minsa.pe")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)

    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 25
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)

        # Etiqueta de perfil
        self.labelPerfil = tk.Label(self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        # Botones del menú lateral

        self.buttonDashBoard = tk.Button(self.menu_lateral)
        self.buttonProfile = tk.Button(self.menu_lateral)
        self.buttonPicture = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)
        self.buttonSettings = tk.Button(self.menu_lateral)

        buttons_info = [
            ("Dashboard", "\uf109", self.buttonDashBoard),
            ("Profile", "\uf007", self.buttonProfile),
            ("Picture", "\uf03e", self.buttonPicture),
            ("Info", "\uf129", self.buttonInfo),
            ("Settings", "\uf013", self.buttonSettings)
        ]

        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)

    def controles_cuerpo(self):
        # Imagen en el cuerpo principal
        label = tk.Label(self.cuerpo_principal, image=self.logo, bg=COLOR_CUERPO_PRINCIPAL)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        self.content=tk.Frame(self.cuerpo_principal, bg=COLOR_BARRA_SUPERIOR)
        self.content.place(relx=0.5, rely=0.49, anchor=tk.CENTER, width=700, height=450)

        # Lista desplegable y botón "Graficar"
        self.selected_chart = tk.StringVar()
        self.chart_menu = ttk.Combobox(self.content, textvariable=self.selected_chart, font=("Arial", 12),
                                       values=["Número de Pacientes por Día", "Número de Pacientes por Especialidad",
                                               "Diagnósticos Más Frecuentes", "Géneros de Pacientes",
                                               "Grupos de Edades", "Etnia", "Financiador",
                                               "Colegiatura del Personal", "Lista por Especialidad",
                                               "Mapa de Calor"])
        self.chart_menu.set("Seleccione el gráfico")
        self.chart_menu.place(relx=0.3, rely=0.1, anchor=tk.CENTER)

        self.generate_button = tk.Button(self.content, text="Graficar", font=("Arial", 12), command=self.generate_chart)
        self.generate_button.place(relx=0.6, rely=0.1, anchor=tk.CENTER)

        # Sección de información del paciente
        self.patient_info_frame = tk.Frame(self.content, bg=COLOR_MENU_LATERAL)
        self.patient_info_frame.place(relx=0.5, rely=0.35, anchor=tk.CENTER, width=620, height=160)

        self.info_header = tk.Label(self.patient_info_frame, text="Información del Paciente", font=("Arial", 16), bg=COLOR_MENU_CURSOR_ENCIMA, fg="black")
        self.info_header.pack(fill=tk.X, pady=5)

        self.dni_label = tk.Label(self.patient_info_frame, text="DNI", font=("Arial", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.dni_label.place(relx=0.1, rely=0.45, anchor=tk.W)

        self.dni_entry = tk.Entry(self.patient_info_frame, textvariable=self.dni_entry_var, font=("Arial", 12), width=30)
        self.dni_entry.place(relx=0.2, rely=0.45, anchor=tk.W)

        self.search_button = tk.Button(self.patient_info_frame, text="Buscar Paciente", font=("Arial", 12), bg=COLOR_MENU_CURSOR_ENCIMA, fg="white", cursor="hand2", command=self.search_patient)
        self.search_button.place(relx=0.8, rely=0.45, anchor=tk.CENTER)

        self.nombre_label=tk.Label(self.patient_info_frame,text="Nombre",font=("Arial",12),bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.nombre_label.place(relx=0.1,rely=0.75,anchor=tk.W)

        self.nombre_entry = tk.Entry(self.patient_info_frame, textvariable=self.nombre_entry_var, font=("Arial", 12),width=44)
        self.nombre_entry.place(relx=0.25, rely=0.75, anchor=tk.W)

        # Sección de información del personal
        self.personnel_info_frame = tk.Frame(self.content, bg=COLOR_MENU_LATERAL)
        self.personnel_info_frame.place(relx=0.5, rely=0.75, anchor=tk.CENTER, width=620, height=160)

        self.personnel_header = tk.Label(self.personnel_info_frame, text="Información del Personal", font=("Arial", 16), bg=COLOR_MENU_CURSOR_ENCIMA, fg="black")
        self.personnel_header.pack(fill=tk.X, pady=5)

        self.dni_personal_label = tk.Label(self.personnel_info_frame, text="DNI", font=("Arial", 12), bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.dni_personal_label.place(relx=0.1, rely=0.45, anchor=tk.W)

        self.dni_personal_entry = tk.Entry(self.personnel_info_frame, textvariable=self.dni_personal_entry_var, font=("Arial", 12), width=30)
        self.dni_personal_entry.place(relx=0.2, rely=0.45, anchor=tk.W)

        self.search_personal_button = tk.Button(self.personnel_info_frame, text="Buscar Personal", font=("Arial", 12), bg=COLOR_MENU_CURSOR_ENCIMA , fg="white", cursor="hand2", command=self.search_personal)
        self.search_personal_button.place(relx=0.8, rely=0.45, anchor=tk.CENTER)

        self.nombre_personal_label = tk.Label(self.personnel_info_frame, text="Nombre", font=("Arial", 12),bg=COLOR_CUERPO_PRINCIPAL, fg="black")
        self.nombre_personal_label.place(relx=0.1, rely=0.75, anchor=tk.W)

        self.nombre_personal_entry = tk.Entry(self.personnel_info_frame, textvariable=self.nombre_personal_entry_var, font=("Arial", 12),width=44)
        self.nombre_personal_entry.place(relx=0.25, rely=0.75, anchor=tk.W)

    def generate_chart(self):
        selected_chart = self.selected_chart.get()
        if selected_chart:
            print(f"Generando gráfico: {selected_chart}")
        else:
            messagebox.showerror("Error", "Seleccione un gráfico para generar")

    def search_patient(self):
        dni = self.dni_entry_var.get()
        # Lógica para buscar paciente por DNI
        print(f"Buscando paciente con DNI: {dni}")

    def search_personal(self):
        dni_personal = self.dni_personal_entry_var.get()
        # Lógica para buscar personal por DNI
        print(f"Buscando personal con DNI: {dni_personal}")

    def cargar_datos(self):
        # Lógica para cargar datos
        print("Cargando datos...")

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

