import pandas as pd
import tkinter as tk
from tkinter import font, ttk, filedialog, messagebox, simpledialog
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util_ventana as util_ventana
import util_imagenes as util_img
from data_manager import DataManager  
from graficadora import Graficadora
import os
import tempfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import webbrowser


class FormularioMaestroDesign(tk.Tk):
    def __init__(self):
        super().__init__()

        self.data_manager = DataManager()
        self.fig = None  # Añadido para almacenar la figura actual
        self.logo = util_img.leer_imagen("./imagenes/fond3.jpg", (1400, 1200))
        self.perfil = util_img.leer_imagen("./imagenes/fon.png", (150, 150))
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
        self.title('Python GUI')
        self.iconbitmap("./imagenes/log.ico")
        w, h = 1024, 600
        util_ventana.centrar_ventana(self, w, h)

    def paneles(self):
        self.barra_superior = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        self.cuerpo_principal = tk.Frame(self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):
        font_awesome = font.Font(family='FontAwesome', size=12)

        self.labelTitulo = tk.Label(self.barra_superior, text="Redes Azàngaro")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        self.buttonMenuLateral = tk.Button(self.barra_superior, text="← →", font=font_awesome,
                                           command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        self.buttonCargarDatos = tk.Button(self.barra_superior, text="Cargar datos", font=("Roboto", 12),
                                           command=self.data_manager.button_cargar_datos, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonCargarDatos.pack(side=tk.LEFT, padx=10)

        self.bind_hover_events(self.buttonCargarDatos)

        self.labelTitulo = tk.Label(self.barra_superior, text="RedDeSalud@minsa.pe")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)

        self.buttonHelp = tk.Button(self.barra_superior, text="Ayuda", font=("Roboto", 12), bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white", command=self.show_help)
        self.buttonHelp.pack(side=tk.RIGHT, padx=10)
        self.bind_hover_events(self.buttonHelp)

    def show_profile(self):
        profile_file = "perfil.pdf"
        if os.path.exists(profile_file):
            webbrowser.open_new(profile_file)
        else:
            messagebox.showerror("Error", f"El archivo {profile_file} no se encuentra!")

    def controles_menu_lateral(self):
        ancho_menu = 25
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)

        self.labelPerfil = tk.Label(self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        self.buttonDashBoard = tk.Button(self.menu_lateral, command=self.go_to_dashboard)
        self.buttonProfile = tk.Button(self.menu_lateral, command=self.show_profile)
        self.buttonPrint = tk.Button(self.menu_lateral, command=self.print_figure)
        self.buttonSave = tk.Button(self.menu_lateral, command=self.save_pdf)
        self.buttonSettings = tk.Button(self.menu_lateral, command=self.close_window)

        buttons_info = [
            ("Inicio", "\uf109", self.buttonDashBoard),
            ("Perfil", "\uf007", self.buttonProfile),
            ("Imprimir", "\uf03e", self.buttonPrint),
            ("Guardar Pdf", "\uf129", self.buttonSave),
            ("Salir", "\uf013", self.buttonSettings)
        ]

        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)

    def controles_cuerpo(self):
        label = tk.Label(self.cuerpo_principal, image=self.logo, bg=COLOR_CUERPO_PRINCIPAL)
        label.place(x=0, y=0, relwidth=1, relheight=1)

        self.content = tk.Frame(self.cuerpo_principal, bg=COLOR_BARRA_SUPERIOR)
        self.content.place(relx=0.5, rely=0.49, anchor=tk.CENTER, width=700, height=450)

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

        self.patient_info_frame = tk.Frame(self.content, bg=COLOR_MENU_LATERAL)
        self.patient_info_frame.place(relx=0.5, rely=0.35, anchor=tk.CENTER, width=620, height=160)

        self.info_header = tk.Label(self.patient_info_frame, text="Información del Paciente", font=("Arial", 16), bg=COLOR_MENU_CURSOR_ENCIMA, fg="black")
        self.info_header.pack(fill=tk.X, pady=5)

        self.dni_label = tk.Label(self.patient_info_frame, text="DNI", font=("Arial", 12), bg="lightblue",  fg="black")
        self.dni_label.place(relx=0.1, rely=0.45, anchor=tk.W)

        self.dni_entry = tk.Entry(self.patient_info_frame, textvariable=self.dni_entry_var, font=("Arial", 12), width=30)
        self.dni_entry.place(relx=0.2, rely=0.45, anchor=tk.W)

        self.search_button = tk.Button(self.patient_info_frame, text="Buscar por DNI", font=("Arial", 12), bg=COLOR_MENU_CURSOR_ENCIMA, fg="white", cursor="hand2", command=self.search_patient)
        self.search_button.place(relx=0.8, rely=0.45, anchor=tk.CENTER)

        self.nombre_label = tk.Label(self.patient_info_frame, text="Nombre", font=("Arial", 12), bg="lightblue", fg="black")
        self.nombre_label.place(relx=0.1, rely=0.75, anchor=tk.W)

        self.nombre_entry = tk.Entry(self.patient_info_frame, textvariable=self.nombre_entry_var, font=("Arial", 12), width=34)
        self.nombre_entry.place(relx=0.25, rely=0.75, anchor=tk.W)

        self.search_nombre = tk.Button(self.patient_info_frame, text="Buscar", font=("Arial", 12),
                                       bg=COLOR_MENU_CURSOR_ENCIMA, fg="white", cursor="hand2", command=self.buscar_por_nombre)
        self.search_nombre.place(relx=0.85, rely=0.75, anchor=tk.CENTER)

        self.personnel_info_frame = tk.Frame(self.content, bg=COLOR_MENU_LATERAL)
        self.personnel_info_frame.place(relx=0.5, rely=0.75, anchor=tk.CENTER, width=620, height=160)

        self.personnel_header = tk.Label(self.personnel_info_frame, text="Información del Personal", font=("Arial", 16), bg=COLOR_MENU_CURSOR_ENCIMA, fg="black")
        self.personnel_header.pack(fill=tk.X, pady=5)

        self.dni_personal_label = tk.Label(self.personnel_info_frame, text="DNI", font=("Arial", 12), bg="lightblue", fg="black")
        self.dni_personal_label.place(relx=0.1, rely=0.45, anchor=tk.W)

        self.dni_personal_entry = tk.Entry(self.personnel_info_frame, textvariable=self.dni_personal_entry_var, font=("Arial", 12), width=30)
        self.dni_personal_entry.place(relx=0.2, rely=0.45, anchor=tk.W)

        self.search_personal_button = tk.Button(self.personnel_info_frame, text="Buscar por DNI", font=("Arial", 12), bg=COLOR_MENU_CURSOR_ENCIMA, fg="white", cursor="hand2", command=self.search_personal)
        self.search_personal_button.place(relx=0.8, rely=0.45, anchor=tk.CENTER)

    def generate_chart(self):
        selected_chart = self.selected_chart.get()
        graficadora = Graficadora(self.data_manager.df)
        self.fig = None  # Resetear la figura antes de generar una nueva
        if selected_chart == "Número de Pacientes por Día":
            self.fig = graficadora.plot_patients_per_day(self.content)
        elif selected_chart == "Número de Pacientes por Especialidad":
            self.fig = graficadora.plot_patients_per_specialty(self.content)
        elif selected_chart == "Diagnósticos Más Frecuentes":
            self.fig = graficadora.plot_top_diagnostics(self.content)
        elif selected_chart == "Géneros de Pacientes":
            self.fig = graficadora.plot_patient_genders(self.content)
        elif selected_chart == "Grupos de Edades":
            self.fig = graficadora.plot_age_groups(self.content)
        elif selected_chart == "Etnia":
            self.fig = graficadora.plot_ethnicity(self.content)
        elif selected_chart == "Financiador":
            self.fig = graficadora.plot_financiers(self.content)
        elif selected_chart == "Colegiatura del Personal":
            self.fig = graficadora.plot_personnel_registration(self.content)
        elif selected_chart == "Lista por Especialidad":
            self.fig = graficadora.plot_personnel_by_specialty(self.content)
        elif selected_chart == "Mapa de Calor":
            self.fig = graficadora.plot_heatmap(self.content)
        else:
            messagebox.showerror("Error", "Seleccione un gráfico para generar")

    def search_patient(self):
        dni = self.dni_entry_var.get()
        self.data_manager.buscar_por_numero_documento(dni)

    def buscar_por_nombre(self):
        if self.data_manager.df is None:
            messagebox.showerror("Error", "Please upload a file first")
            return

        nombre = self.nombre_entry.get()
        if not nombre:
            messagebox.showwarning("Advertencia", "Por favor ingrese un nombre.")
            return

        try:
            resultados = self.data_manager.df[self.data_manager.df.apply(lambda row: row.astype(str).str.contains(nombre, case=False).any(), axis=1)]
            resultados = resultados[['Nombres_Paciente', 'Numero_Documento_Paciente']].drop_duplicates()

            resultados_ventana = tk.Toplevel(self)
            resultados_ventana.title("Resultados de la Búsqueda")
            resultados_ventana.geometry("400x300")
            
            resultados_text = tk.Text(resultados_ventana, font=("Arial", 12), height=15, width=50)
            resultados_text.pack(pady=20)

            if not resultados.empty:
                for _, row in resultados.iterrows():
                    resultados_text.insert(tk.END, f"Nombre: {row['Nombres_Paciente']}, Documento: {row['Numero_Documento_Paciente']}\n")
            else:
                resultados_text.insert(tk.END, "No se encontraron coincidencias.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def search_personal(self):
        dni_personal = self.dni_personal_entry_var.get()
        self.data_manager.buscar_por_numero_documento_personal(dni_personal)

    def cargar_datos(self):
        self.data_manager.button_cargar_datos()

    def go_to_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self.controles_cuerpo()

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    def print_figure(self):
        if self.fig is None:
            messagebox.showerror("Error", "No hay gráfico para imprimir. Por favor, genere un gráfico primero.")
            return

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                self.fig.savefig(tmpfile.name)
                tmpfile.close()

                image = Image.open(tmpfile.name)
                image.show("Imprimir")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo imprimir el gráfico: {e}")    

    def show_help(self):
        help_file = "ayuda.pdf"
        if os.path.exists(help_file):
            webbrowser.open_new(help_file)
        else:
            messagebox.showerror("Error", f"El archivo {help_file} no se encuentra!")

    def save_pdf(self):
        if self.fig is None:
            messagebox.showerror("Error", "No hay gráfico para guardar. Por favor, genere un gráfico primero.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if file_path:
            try:
                self.fig.savefig(file_path)
                messagebox.showinfo("Guardar PDF", f"El gráfico ha sido guardado como PDF en {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el gráfico como PDF: {e}")

    def close_window(self):
        confirm = messagebox.askyesno(title="Minsa Azangaro", message="¿Quieres cerrar el programa?")
        if confirm:
            self.destroy()

