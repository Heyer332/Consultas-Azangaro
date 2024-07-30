import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
def eliminar_espacios(df):
    return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
def eliminar_columnas_vacias_o_repetidas(df):
    threshold = len(df) * 0.7  
    df = df.dropna(axis=1, thresh=threshold)
    for col in df.columns:
        if df[col].nunique() == 1:
            df = df.drop(columns=[col])
    return df
def procesar_archivo(archivo_entrada):
    extension = os.path.splitext(archivo_entrada)[1]
    if extension == '.xlsx':
        df = pd.read_excel(archivo_entrada)
    elif extension == '.csv':
        df = pd.read_csv(archivo_entrada)
    else:
        raise ValueError('Tipo de archivo no soportado: solo se permiten archivos .xlsx y .csv')
    df = eliminar_espacios(df)
    df = eliminar_columnas_vacias_o_repetidas(df)
    return df, extension
def subir_archivo():
    archivo_entrada = filedialog.askopenfilename(
        filetypes=[("Archivos de Excel", "*.xlsx"), ("Archivos CSV", "*.csv")]
    )
    if archivo_entrada:
        try:
            df, extension = procesar_archivo(archivo_entrada)
            archivo_salida = filedialog.asksaveasfilename(
                defaultextension=extension,
                filetypes=[("Archivos de Excel", "*.xlsx"), ("Archivos CSV", "*.csv")]
            )
            if archivo_salida:
                if extension == '.xlsx':
                    df.to_excel(archivo_salida, index=False)
                elif extension == '.csv':
                    df.to_csv(archivo_salida, index=False)
                messagebox.showinfo("Éxito", "Archivo procesado y guardado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
root = tk.Tk()
root.title("Eliminar espacios y columnas en archivos XLSX y CSV")
root.geometry("400x200")
boton_subir = ttk.Button(root, text="Subir archivo", command=subir_archivo)
boton_subir.pack(expand=True)
root.mainloop()