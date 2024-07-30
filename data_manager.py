import pandas as pd
from tkinter import filedialog, messagebox, ttk, Toplevel, Canvas
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import seaborn as sns
from random import choice
import calendar
import numpy as np
import matplotlib.pyplot as plt

class DataManager:
    def __init__(self):
        self.df = pd.DataFrame()
        self.my_table = None
        self.error_info = None

    def button_cargar_datos(self):
        file_name = filedialog.askopenfilename(
            initialdir="./csv files",
            title="Open A File",
            filetypes=(("Excel files", "*.xlsx;*.xls"), ("csv files", "*.csv"), ("All Files", "*.*"))
        )
        if file_name:
            try:
                if file_name.endswith('.csv'):
                    self.df = pd.read_csv(file_name)
                else:
                    self.df = pd.read_excel(file_name)
                
                required_columns = ['Numero_Documento_Paciente', 'Numero_Documento_Personal']
                if not any(col in self.df.columns for col in required_columns):
                    messagebox.showerror("Error", "Archivo no compatible")
                    return
            except ValueError:
                messagebox.showerror("Error", "El archivo no se puede abrir!")
            except FileNotFoundError:
                messagebox.showerror("Error", "El archivo no se encuentra!")

    def display_data(self):
        self.clear_table_data()
        self.my_table["column"] = list(self.df.columns)
        self.my_table["show"] = "headings"
        for column in self.my_table["column"]:
            self.my_table.heading(column, text=column)
        for column_name in self.my_table["column"]:
            self.my_table.column(column_name, width=60)
        df_rows_old = self.df.to_numpy()
        df_rows_refreshed = [list(item) for item in df_rows_old]
        for row in df_rows_refreshed:
            self.my_table.insert("", "end", values=row)
        self.my_table.place(x=5, y=5, width=310, height=630)
        self.fill_comboboxes()

    def clear_table_data(self):
        self.my_table.delete(*self.my_table.get_children())

    def clear_data(self):
        self.df = pd.DataFrame()
        self.clear_table_data()
        self.error_info.config(text="Datos limpiados. Cargue nuevos datos.")
        self.clear_bar()
        self.clear_scatter()
        self.clear_pie()
        self.clear_line()

    def fill_comboboxes(self):
        pass

    def buscar_por_numero_documento(self, numero_documento):
        try:
            numero_documento = str(numero_documento)
            registros = self.df[self.df['Numero_Documento_Paciente'].astype(str) == numero_documento]
            if registros.empty:
                messagebox.showerror("Error", f"No se encontró ningún registro con el Número de Documento {numero_documento}")
                return
            nombres = registros['Nombres_Paciente'].values[0]
            apellido_paterno = registros['Apellido_Paterno_Paciente'].values[0]
            apellido_materno = registros['Apellido_Materno_Paciente'].values[0]
            edad = registros['Edad_Reg'].values[0]
            veces_atendidas = registros.shape[0]
            diagnósticos = registros['Descripcion_Item'].dropna().unique().tolist()
            window = tk.Tk()
            window.title("Información del Paciente")
            labels = ["Nombres", "Apellido Paterno", "Apellido Materno", "Edad", "Veces Atendidas", "Diagnósticos"]
            values = [nombres, apellido_paterno, apellido_materno, edad, veces_atendidas, diagnósticos]
            for i, label in enumerate(labels):
                ttk.Label(window, text=label).grid(column=0, row=i, padx=10, pady=5)
                if label == "Diagnósticos":
                    for j, diagnostico in enumerate(values[i], start=1):
                        ttk.Label(window, text=f"Diagnóstico {j}: {diagnostico}").grid(column=1, row=i+j-1, padx=10, pady=5)
                else:
                    ttk.Label(window, text=values[i]).grid(column=1, row=i, padx=10, pady=5)
            window.mainloop()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def buscar_por_numero_documento_personal(self, numero_documento):
        try:
            numero_documento = str(numero_documento)
            registros = self.df[self.df['Numero_Documento_Personal'].astype(str) == numero_documento]
            if registros.empty:
                messagebox.showerror("Error", f"No se encontró ningún registro con el Número de Documento {numero_documento}")
                return
            nombre = registros['Nombres_Personal'].values[0]
            apellido_paterno = registros['Apellido_Paterno_Personal'].values[0]
            apellido_materno = registros['Apellido_Materno_Personal'].values[0]
            especialidad = registros['Descripcion_Profesion'].values[0]
            estado_trabajo = registros['Descripcion_Condicion'].values[0]
            edad = registros['Edad_Reg'].values[0]
            registros['Fecha_Atencion'] = pd.to_datetime(registros['Fecha_Atencion'])
            dias_trabajados = registros['Fecha_Atencion'].nunique()
            window = tk.Tk()
            window.title("Información del Personal de Salud")
            info_frame = ttk.Frame(window)
            info_frame.grid(column=0, row=0, padx=10, pady=5)
            labels = ["Nombre", "Apellido Paterno", "Apellido Materno", "Especialidad", "Estado de Trabajo", "Edad", "Días Trabajados"]
            values = [nombre, apellido_paterno, apellido_materno, especialidad, estado_trabajo, edad, dias_trabajados]
            for i, label in enumerate(labels):
                ttk.Label(info_frame, text=label).grid(column=0, row=i, padx=10, pady=5, sticky=tk.W)
                ttk.Label(info_frame, text=values[i]).grid(column=1, row=i, padx=10, pady=5, sticky=tk.W)
            registros['Día'] = registros['Fecha_Atencion'].dt.day
            resumen = registros.groupby(['Día', 'Id_Turno']).size().reset_index(name='Pacientes_Atendidos')
            columns = ('Día', 'Pacientes Atendidos', 'Turno')
            tree = ttk.Treeview(info_frame, columns=columns, show='headings')
            tree.heading('Día', text='Día')
            tree.heading('Pacientes Atendidos', text='Pacientes Atendidos')
            tree.heading('Turno', text='Turno')
            for index, row in resumen.iterrows():
                dia = row['Día']
                pacientes_atendidos = row['Pacientes_Atendidos']
                turno = row['Id_Turno']
                tree.insert('', tk.END, values=(f"{dia:02d}", pacientes_atendidos, turno))
            tree.grid(column=0, row=len(labels), columnspan=2, pady=10)
            hist_frame = ttk.Frame(window)
            hist_frame.grid(column=1, row=0, padx=10, pady=5, rowspan=2)
            fig, ax = plt.subplots()
            sns.kdeplot(data=registros, x='Día', ax=ax, fill=True)
            ax.set_xlabel('Día')
            ax.set_ylabel('Densidad de Pacientes Atendidos')
            ax.set_title('Distribución de Pacientes Atendidos por Día')
            canvas = FigureCanvasTkAgg(fig, master=hist_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()
            window.mainloop()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_bar(self):
        pass

    def clear_scatter(self):
        pass

    def clear_pie(self):
        pass

    def clear_line(self):
        pass
