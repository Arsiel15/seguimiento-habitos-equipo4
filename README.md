# seguimiento-habitos-equipo4

Aplicación para el registro y seguimiento de hábitos saludables como hidratación, sueño y actividad física. Desarrollada como parte del proyecto académico del equipo 4 para la materia de Diseño de Software.

### Estructura del proyecto
seguimiento-habitos-equipo4/
│
├── app/
│   ├── main.py               # Código principal con interfaz Tkinter
│   └── data.json             # Archivo donde se guarda el historial
│
├── docs/                     # Documentación y rúbricas
│
├── dist/
│   └── interfaz.exe          # Ejecutable generado con PyInstaller
│
├── README.md
└── requirements.txt

## ¿Qué hace esta app?

- Permite registrar diariamente:
  - Edad y género
  - Vasos de agua consumidos
  - Horas de sueño
  - Minutos de actividad física
- Genera recomendaciones personalizadas
- Visualiza los últimos registros en pantalla
- Exporta el historial a PDF
- Muestra gráficos de progreso semanal
- Permite eliminar registros individuales o todo el historial

## ¿Cómo se ejecuta?

### Opción 1: Desde el ejecutable

- Ve a la carpeta `dist/`
- Abre el archivo `interfaz.exe`
- ¡Y comienza a registrar tus hábitos!

### Opción 2: Desde el código fuente

Asegúrate de tener Python instalado y ejecuta:

```bash
pip install -r requirements.txt
python app/main.py


