import tkinter as tk
from tkinter import filedialog, messagebox
#from PIL import Image, ImageTk
from osuFileHandler import OsuFileHandler
import os

def replace_hold_notes(file_path):
    sections = {
        "[General]": [],
        "[Editor]": [],
        "[Metadata]": [],
        "[Difficulty]": [],
        "[Events]": [],
        "[TimingPoints]": [],
        "[HitObjects]": []
    }
    
    with open(file_path, 'r', encoding='utf-8') as file:  # codificación UTF-8
        lines = file.readlines()

    current_section = None

    for line in lines:
        line = line.strip()
        if line in sections:
            current_section = line
            sections[current_section].append(line + '\n')
        elif current_section:
            if current_section == "[Metadata]" and line.startswith("Version:"):
                version = line.split(":", 1)[1].strip()
                new_version = f"{version} (noLN)"
                sections[current_section].append(f"Version:{new_version}\n")
            elif current_section == "[HitObjects]":
                parts = line.split(',')
                if len(parts) >= 6 and int(parts[5].split(':')[0]) > 0:
                    hitsound = parts[4]
                    extras = parts[5] if len(parts) > 5 else "0:0:0:0:"
                    sections[current_section].append(f"{parts[0]},{parts[1]},{parts[2]},1,{hitsound},{extras}\n")
                else:
                    sections[current_section].append(line + '\n')
            else:
                sections[current_section].append(line + '\n')
        else:
            continue

    output_file_path = os.path.splitext(file_path)[0] + '_modificado.osu'
    with open(output_file_path, 'w', encoding='utf-8') as file:  
        file.write("osu file format v14\n")
        
        for section in sections:
            if sections[section]:
                file.write(''.join(sections[section]))
                file.write('\n')

    return output_file_path


def select_file():
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo .osu",
        filetypes=[("osu! files", "*.osu")]
    )
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)
        #load_image(file_path)

# def load_image(file_path):
#     nombre_imagen = OsuFileHandler.obtener_nombre_imagen(file_path)
#     if nombre_imagen:
#         ruta_imagen = os.path.join(os.path.dirname(file_path), nombre_imagen)
#         if os.path.exists(ruta_imagen):
#             image = Image.open(ruta_imagen)
#             image = image.resize((150, 150))  # Redimensionar imagen si es necesario
#             img_tk = ImageTk.PhotoImage(image)
#             label_image.config(image=img_tk)
#             label_image.image = img_tk  # Guardar la referencia para evitar recolección de basura
#         else:
#             messagebox.showerror("Error", f"No se encontró la imagen: {ruta_imagen}")

def apply_changes():
    file_path = entry_file_path.get()
    if not file_path:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo .osu.")
        return

    try:
        output_file_path = replace_hold_notes(file_path)
        messagebox.showinfo("Éxito", f"Los cambios se han aplicado. El archivo modificado se guardó como:\n{output_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo:\n{e}")

# ventana principal
root = tk.Tk()
root.title("osu!Mania LN remover")
root.geometry("600x400") 

# Configurar estilos
root.configure(bg="#1e1e1e")
root.resizable(False, False)  # No permite cambiar el tamaño de la ventana
root.overrideredirect(False)  # Asegura que la barra de título esté presente
font_style = ("Arial", 13)
button_style = {"bg": "#007acc", "fg": "#ffffff", "font": font_style, "bd": 0, "relief": "flat"}

# Ruta del archivo
frame_file = tk.Frame(root, bg="#1e1e1e")
frame_file.pack(pady=20, padx=20, fill="x")
label_file = tk.Label(frame_file, text="Archivo .osu:", bg="#1e1e1e", fg="#ffffff", font=font_style)
label_file.pack(side="left", padx=(0, 10))

entry_file_path = tk.Entry(frame_file, width=40, font=font_style)
entry_file_path.pack(side="left", fill="x", expand=True)
btn_browse = tk.Button(frame_file, text="Buscar", command=select_file, **button_style)
btn_browse.pack(side="left", padx=(10, 0))

label_txt = tk.Label(text="730XX" , bg="#1e1e1e", fg="#ffffff", font=font_style)
label_txt.pack(side="bottom", pady=(120,0), padx=(520,0))

# Boton para aplicar los cambios
btn_apply = tk.Button(root, text="Eliminar LNS", command=apply_changes, **button_style)
btn_apply.pack(pady=20)

# Label para mostrar la imagen
label_image = tk.Label(root, bg="#1e1e1e")
label_image.place(x=20, y=220)  # Posiciona la imagen en la esquina inferior izquierda

# Ejecutar la aplicación
root.mainloop()
