import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

#Guarda en el Json
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

#Inicio
def cargar_ultimos_habitos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        contenido = f.read()
        if not contenido.strip():
            return []
        try:
            datos = json.loads(contenido)
            return datos[-3:]
        except json.JSONDecodeError:
            return []

def generar_recomendaciones(item):
    recomendaciones = []

    if int(item['sueno']) < 7:
        recomendaciones.append("💤 Duerme al menos 7h. Dormir bien mejora tu salud mental y física.")
    if int(item['agua']) < 6:
        recomendaciones.append("💧 Bebe más agua. 6-8 vasos al día es lo ideal.")
    if int(item['actividad']) < 30:
        recomendaciones.append("🏃‍♂️ Haz más actividad física. Se recomiendan 30+ min diarios.")

    return recomendaciones

def mostrar_ultimos():
    ultimos = cargar_ultimos_habitos()
    historial_texto.config(state=tk.NORMAL)
    historial_texto.delete("1.0", tk.END)
    if not ultimos:
        historial_texto.insert(tk.END, "No hay registros aún.")
        historial_texto.config(state=tk.DISABLED)
        return

    for i, item in enumerate(reversed(ultimos), start=1):
        historial_texto.insert(tk.END, f"{i}. 📅 {item['fecha']} - 🧍 {item['genero']}, {item['edad']} años\n")
        historial_texto.insert(tk.END, f"   💧 {item['agua']} vasos, 💤 {item['sueno']}h sueño, 🏃 {item['actividad']} min\n")
        recomendaciones = generar_recomendaciones(item)
        for r in recomendaciones:
            historial_texto.insert(tk.END, f"⚠️ {r}\n")
        historial_texto.insert(tk.END, "-"*45 + "\n")

    historial_texto.config(state=tk.DISABLED)


def guardar_datos():
    if not (entry_agua.get() and entry_sueno.get() and entry_actividad.get() and entry_edad.get()):
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
        return

    try:
        edad = int(entry_edad.get())
        agua = int(entry_agua.get())
        sueno = int(entry_sueno.get())
        actividad = int(entry_actividad.get())
    except ValueError:
        messagebox.showerror("Error", "Todos los valores deben ser numéricos.")
        return

    datos = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "genero": genero_var.get(),
        "edad": edad,
        "agua": agua,
        "sueno": sueno,
        "actividad": actividad
    }

    try:
        existentes = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                contenido = f.read()
                if contenido.strip():
                    existentes = json.loads(contenido)

        existentes.append(datos)

        with open(DATA_FILE, "w") as f:
            json.dump(existentes, f, indent=4)

        messagebox.showinfo("Éxito", "Hábitos guardados correctamente.")
        entry_agua.delete(0, tk.END)
        entry_sueno.delete(0, tk.END)
        entry_actividad.delete(0, tk.END)
        entry_edad.delete(0, tk.END)
        mostrar_ultimos()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")

def ver_graficos():
    try:
        with open(DATA_FILE, "r") as f:
            datos = json.load(f)

        fechas = [d["fecha"] for d in datos]
        agua = [int(d["agua"]) for d in datos]
        sueno = [int(d["sueno"]) for d in datos]
        actividad = [int(d["actividad"]) for d in datos]

        plt.figure("Progreso semanal", figsize=(10, 6))

        #Agua
        plt.subplot(3, 1, 1)
        plt.bar(fechas, agua, color="skyblue")
        plt.axhline(8, color="gray", linestyle="--", label="Meta: 8 vasos")
        plt.title("💧 Vasos de agua")
        plt.legend()

        #Sueño
        plt.subplot(3, 1, 2)
        plt.bar(fechas, sueno, color="orchid")
        plt.axhline(7, color="gray", linestyle="--", label="Meta: 7 horas")
        plt.title("😴 Horas de sueño")
        plt.legend()

        #Actividad
        plt.subplot(3, 1, 3)
        plt.bar(fechas, actividad, color="lightgreen")
        plt.axhline(30, color="gray", linestyle="--", label="Meta: 30 min")
        plt.title("🏃 Minutos de actividad física")
        plt.legend()

        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron generar los gráficos: {e}")

def exportar_pdf():
    try:
        with open(DATA_FILE, "r") as f:
            datos = json.load(f)

        c = canvas.Canvas("reporte_habitos.pdf", pagesize=letter)
        width, height = letter
        y = height - 50

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Reporte de Hábitos Saludables")
        y -= 30

        c.setFont("Helvetica", 10)
        for item in datos:
            linea = f"{item['fecha']} | Edad: {item.get('edad','-')} | Género: {item.get('genero','-')} | 💧 {item['agua']} vasos | 😴 {item['sueno']}h | 🏃 {item['actividad']} min"
            c.drawString(50, y, linea)
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)

        c.save()
        messagebox.showinfo("Éxito", "Reporte guardado como 'reporte_habitos.pdf'")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar: {e}")

def limpiar_historial():
    confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas borrar todo el historial?")
    if confirm:
        with open(DATA_FILE, "w") as f:
            json.dump([], f, indent=4)
        messagebox.showinfo("Éxito", "Historial borrado exitosamente.")
        mostrar_ultimos()  

def eliminar_registro():
    try:
        ultimos = cargar_ultimos_habitos()
        if not ultimos:
            messagebox.showinfo("Info", "No hay registros para eliminar.")
            return

        num = simpledialog.askinteger("Eliminar registro", f"Número del registro a eliminar (últimos {len(ultimos)})?")
        if num is None:
            return

        if not (1 <= num <= len(ultimos)):
            messagebox.showerror("Error", "Número fuera de rango.")
            return

        #Elimina el registro del final
        del ultimos[-num]

        with open(DATA_FILE, "w") as f:
            json.dump(ultimos, f, indent=4)

        messagebox.showinfo("Éxito", "Registro eliminado.")
        mostrar_ultimos() 
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar: {e}")




#Interfaz
ventana = tk.Tk()
ventana.title("Registro de Hábitos Saludables")
ventana.geometry("500x750")

#Edad
tk.Label(ventana, text="Edad:").pack(pady=(10, 0))
entry_edad = tk.Entry(ventana)
entry_edad.pack()

#Género
tk.Label(ventana, text="👤 Género:").pack(pady=(10, 0))
genero_var = tk.StringVar(value="Prefiero no decir")
genero_combo = ttk.Combobox(ventana, textvariable=genero_var, state="readonly")
genero_combo['values'] = ("Masculino", "Femenino", "Otro", "Prefiero no decir")
genero_combo.pack()

#Hábitos
tk.Label(ventana, text="💧 Vasos de agua:").pack(pady=(10, 0))
entry_agua = tk.Entry(ventana)
entry_agua.pack()

tk.Label(ventana, text="💤 Horas de sueño:").pack(pady=(10, 0))
entry_sueno = tk.Entry(ventana)
entry_sueno.pack()

tk.Label(ventana, text="🏃‍♂️ Minutos de actividad física:").pack(pady=(10, 0))
entry_actividad = tk.Entry(ventana)
entry_actividad.pack()

#Crear un frame para agrupar todos los botones de acciones
acciones_frame = tk.Frame(ventana)
acciones_frame.pack(pady=(10, 0))

#Botón Guardar
btn_guardar = tk.Button(acciones_frame, text="💾 Guardar", command=guardar_datos)
btn_guardar.grid(row=0, column=0, columnspan=2, pady=5)

#Botón progreso semanal
btn_graficos = tk.Button(acciones_frame, text="📊 Ver progreso semanal", command=ver_graficos)
btn_graficos.grid(row=1, column=0, padx=5, pady=2)

#Botón Exportar a PDF
btn_pdf = tk.Button(acciones_frame, text="🧾 Exportar a PDF", command=exportar_pdf)
btn_pdf.grid(row=1, column=1, padx=5, pady=2)

#Botón Limpiar historial
btn_limpiar = tk.Button(acciones_frame, text="🗑️ Limpiar historial", command=limpiar_historial)
btn_limpiar.grid(row=2, column=0, padx=5, pady=2)

#Botón Eliminar un registro
btn_eliminar = tk.Button(acciones_frame, text="❌ Eliminar un registro", command=eliminar_registro)
btn_eliminar.grid(row=2, column=1, padx=5, pady=2)


#Historial
tk.Label(ventana, text="📝 Últimos registros:").pack(pady=5)
historial_texto = tk.Text(ventana, height=15, width=50)
historial_texto.config(state=tk.DISABLED)
historial_texto.pack()

#Fin
mostrar_ultimos()
ventana.mainloop()
