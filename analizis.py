import pandas as pd
import tkinter as tk
from tkinter import filedialog, Text
def load_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
    )
    if file_path:
        if file_path.endswith(".xlsx"):
            data = pd.read_excel(file_path)
        else:
            data = pd.read_csv(file_path)
        categorical_data = data.select_dtypes(include=['object'])
        variables = categorical_data.columns.tolist()
        unique_values = {column: categorical_data[column].unique().tolist() for column in variables}
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Variables categóricas:\n")
        output_text.insert(tk.END, f"{variables}\n\n")
        output_text.insert(tk.END, "Valores únicos para cada variable:\n")
        for column, values in unique_values.items():
            output_text.insert(tk.END, f"{column}: {values[:10]}\n")
root = tk.Tk()
root.title("Analizador de Datos")
root.geometry("800x600")
load_button = tk.Button(root, text="Cargar Archivo", padx=10, pady=5, command=load_file)
load_button.pack()
output_text = Text(root, wrap=tk.WORD)
output_text.pack(expand=True, fill=tk.BOTH)
root.mainloop()