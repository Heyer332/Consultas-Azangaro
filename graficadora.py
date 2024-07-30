from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import seaborn as sns
from random import choice
import calendar
import numpy as np
import matplotlib.pyplot as plt

COLORS = ['green', 'red', 'purple', 'brown', 'blue']

class Graficadora:
    def __init__(self, df):
        self.df = df

    def plot_patients_per_day(self, canvas):
        if not self.df.empty:
            grouped_df = self.df.groupby(['Fecha_Atencion']).size().reset_index(name='Count')
            fig = Figure(figsize=(10, 10), dpi=63)
            ax = fig.add_subplot(111)
            ax.plot(grouped_df['Fecha_Atencion'], grouped_df['Count'], marker='o')
            ax.set_title("Número de Pacientes por Día")
            ax.set_ylabel("Número de Pacientes")
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True)
            chart = FigureCanvasTkAgg(fig, master=canvas)
            chart.draw()
            chart.get_tk_widget().pack()
            return fig

    def plot_patients_per_specialty(self, canvas):
        if not self.df.empty:
            grouped_df = self.df.groupby(['Fecha_Atencion', 'Descripcion_Profesion']).size().reset_index(name='Count')
            simplified_df = grouped_df[['Fecha_Atencion', 'Descripcion_Profesion', 'Count']]
            total_patients_by_specialty = simplified_df.groupby('Descripcion_Profesion')['Count'].sum().reset_index()
            sorted_specialties = total_patients_by_specialty.sort_values(by='Count', ascending=False)['Descripcion_Profesion']
            pivot_df = simplified_df.pivot_table(index='Fecha_Atencion', columns='Descripcion_Profesion', values='Count', aggfunc='sum', fill_value=0)
            pivot_df = pivot_df[sorted_specialties]

            fig = Figure(figsize=(20, 20), dpi=80)
            ax = fig.add_subplot(111)
            pivot_df.plot(kind='line', marker='o', ax=ax)
            ax.set_title("Número de Pacientes Atendidos por Día por Cada Especialidad")
            ax.set_xlabel("Fecha de Atención")
            ax.set_ylabel("Número de Pacientes")
            ax.legend(title='Especialidad')
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True)
            chart = FigureCanvasTkAgg(fig, master=canvas)
            chart.draw()
            chart.get_tk_widget().pack()
            return fig

    def plot_top_diagnostics(self, canvas):
        if not self.df.empty:
            diagnostics_counts = self.df['Descripcion_Item'].value_counts().reset_index()
            diagnostics_counts.columns = ['Descripcion_Item', 'Count']
            top_diagnostics = diagnostics_counts.head(10)
            others_count = diagnostics_counts['Count'][10:].sum()
            others_row = pd.DataFrame([['Otros', others_count]], columns=['Descripcion_Item', 'Count'])
            top_diagnostics = pd.concat([top_diagnostics, others_row], ignore_index=True)

            fig = Figure(figsize=(7, 5), dpi=100)
            ax = fig.add_subplot(111)
            sns.barplot(x='Count', y='Descripcion_Item', hue='Descripcion_Item', data=top_diagnostics, palette='viridis', ax=ax, dodge=False, legend=False)
            ax.set_xlabel('Cantidad')
            ax.set_ylabel('Descripción del Ítem')
            ax.set_title('Distribución de los 10 diagnósticos más frecuentes')
            chart = FigureCanvasTkAgg(fig, master=canvas)
            chart.draw()
            chart.get_tk_widget().pack()
            return fig

    def plot_patient_genders(self, canvas=None):
        if not self.df.empty:
            gender_counts = self.df['Genero'].value_counts()
            fig = Figure(figsize=(7, 5), dpi=100)
            ax = fig.add_subplot(111)
            ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=COLORS, startangle=140)
            ax.set_title("Distribución de Géneros de Pacientes")
            if canvas is None:
                plt.show()
            else:
                chart = FigureCanvasTkAgg(fig, master=canvas)
                chart.draw()
                chart.get_tk_widget().pack()
            return fig

    def plot_age_groups(self, canvas):
        if not self.df.empty:
            age_groups = self.df['Grupo_Edad'].value_counts()
            fig = Figure(figsize=(7, 5), dpi=100)
            ax = fig.add_subplot(111)
            ax.bar(age_groups.index, age_groups, color=choice(COLORS))
            ax.set_title("Distribución por Grupos de Edades")
            ax.set_xlabel("Grupo de Edad")
            ax.set_ylabel("Cantidad")
            chart = FigureCanvasTkAgg(fig, master=canvas)
            chart.draw()
            chart.get_tk_widget().pack()
            return fig

    def plot_ethnicity(self, canvas):
        if not self.df.empty:
            ethnicity_counts = self.df['Descripcion_Etnia'].value_counts()
            fig = Figure(figsize=(7, 5), dpi=100)
            ax = fig.add_subplot(111)
            ax.pie(ethnicity_counts, labels=ethnicity_counts.index, autopct='%1.1f%%', colors=COLORS, startangle=140)
            ax.set_title("Distribución por Etnia")
            chart = FigureCanvasTkAgg(fig, master=canvas)
            chart.draw()
            chart.get_tk_widget().pack()
            return fig

    def plot_financiers(self, canvas):
        if not self.df.empty:
            financier_counts = self.df['Descripcion_Financiador'].value_counts()
            fig = Figure(figsize=(7, 5), dpi=100)
            ax = fig.add_subplot(111)
            ax.pie(financier_counts, labels=financier_counts.index, autopct='%1.1f%%', colors=COLORS, startangle=140)
            ax.set_title("Distribución por Financiador")
            chart = FigureCanvasTkAgg(fig, master=canvas)
            chart.draw()
            chart.get_tk_widget().pack()
            return fig

    def plot_personnel_registration(self, canvas):
        if not self.df.empty:
            registration_counts = self.df['Descripcion_Colegio'].value_counts()
            fig = Figure(figsize=(7, 5), dpi=100)
            ax = fig.add_subplot(111)
            ax.bar(registration_counts.index, registration_counts, color=choice(COLORS))
            ax.set_title("Colegiatura del Personal")
            ax.set_xlabel("Colegiatura")
            ax.set_ylabel("Cantidad")
            chart = FigureCanvasTkAgg(fig, master=canvas)
            chart.draw()
            chart.get_tk_widget().pack()
            return fig

    def plot_personnel_by_specialty(self, canvas):
        if not self.df.empty:
            specialty_registration = self.df.groupby(['Descripcion_Profesion', 'Descripcion_Colegio']).size().unstack(fill_value=0)
            fig = Figure(figsize=(10, 10), dpi=100)
            ax = fig.add_subplot(111)
            specialty_registration.plot(kind='bar', stacked=True, ax=ax, color=COLORS)
            ax.set_title("Lista por Especialidad (Colegiado o No Colegiado)")
            ax.set_xlabel("Especialidad")
            ax.set_ylabel("Cantidad")
            ax.legend(title='Colegiatura')
            chart = FigureCanvasTkAgg(fig, master=canvas)
            chart.draw()
            chart.get_tk_widget().pack()
            return fig

    def plot_heatmap(self, canvas):
        if not self.df.empty:
            self.df['Fecha_Atencion'] = pd.to_datetime(self.df['Fecha_Atencion'], format='%Y-%m-%d', errors='coerce')
            self.df = self.df.dropna(subset=['Fecha_Atencion'])
            self.df['Cantidad'] = 1
            self.df['Año'] = self.df['Fecha_Atencion'].dt.year
            self.df['Mes'] = self.df['Fecha_Atencion'].dt.month
            self.df['Día'] = self.df['Fecha_Atencion'].dt.day
            primer_registro = self.df.iloc[0]
            anio = primer_registro['Año']
            mes = primer_registro['Mes']
            dias_del_mes = calendar.monthrange(anio, mes)[1]
            df_mes = self.df[(self.df['Año'] == anio) & (self.df['Mes'] == mes)]
            tabla_pivot = df_mes.pivot_table(index='Día', values='Cantidad', aggfunc='sum', fill_value=0)
            calendario = np.zeros((6, 7))
            primer_dia_semana = calendar.monthrange(anio, mes)[0]
            dia = 1
            for semana in range(6):
                for dia_semana in range(7):
                    if semana == 0 and dia_semana < primer_dia_semana:
                        continue
                    if dia > dias_del_mes:
                        continue
                    if dia in tabla_pivot.index:
                        calendario[semana, dia_semana] = tabla_pivot.loc[dia]
                    dia += 1

            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(calendario, annot=True, fmt=".0f", cmap="YlGnBu", cbar=True, linewidths=.6, 
                        xticklabels=['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'], yticklabels=range(1, 6), ax=ax)
            ax.set_title(f'Mapa de Calor de Personas Atendidas en {calendar.month_name[mes]} {anio}')
            ax.set_xlabel('Día de la Semana')
            ax.set_ylabel('Semana del Mes')
            max_personas = self.df.groupby('Fecha_Atencion')['Cantidad'].sum().max()
            min_personas = self.df.groupby('Fecha_Atencion')['Cantidad'].sum().min()
            plt.figtext(0.5, -0.05, f'Máximo de personas atendidas en un día: {max_personas}', ha='center', fontsize=12)
            plt.figtext(0.5, -0.1, f'Mínimo de personas atendidas en un día: {min_personas}', ha='center', fontsize=12)
            chart = FigureCanvasTkAgg(fig, master=canvas)
            chart.draw()
            chart.get_tk_widget().pack()
            return fig
