# osu_file_handler.py
from tkinter import filedialog, messagebox
class OsuFileHandler:
    @staticmethod
    def obtener_nombre_imagen(ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lines = archivo.readlines()
                for line in lines:
                    if line.startswith('0,0,'):
                        # Extraer el nombre de la imagen entre comillas
                        nombre_imagen = line.split(',')[2].replace('"', '').strip()
                        return nombre_imagen
        except UnicodeDecodeError:
            messagebox.showerror("Error", f"No se pudo decodificar el archivo: {ruta_archivo}")
        return None
    #tilin tail
