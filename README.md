# 📸 Media Sorter Pro

Un script robusto en Python diseñado para automatizar la organización de bibliotecas multimedia masivas. Clasifica fotos y videos analizando metadatos (EXIF) y detecta duplicados visuales mediante algoritmos de Perceptual Hashing, manejando de forma segura colisiones de nombres y archivos corruptos.

## 🚀 Características Principales (Features)

* **Extracción de Metadatos (EXIF):** Organiza automáticamente las imágenes en carpetas cronológicas (`YYYY-MM`) leyendo la etiqueta `DateTimeOriginal`.
* **Detección de Duplicados Avanzada (pHash):** Utiliza Hashing Perceptual (`imagehash`) para identificar imágenes idénticas incluso si han sido alteradas o rotadas (evalúa matrices a 0°, 90°, 180° y 270°).
* **Manejo de Casos Límite (Edge Cases):**
    * **Auto-Renombrador Seguro:** Previene la sobreescritura de archivos (colisión de nombres) agregando sufijos incrementales (ej. `foto_1.jpg`).
    * **Tolerancia a Fallos:** Captura proactivamente errores de parseo en fechas corruptas y envía los archivos a una carpeta segura de contingencia (`Sin_Fecha`).
    * **Archivos Basura:** Identifica y separa automáticamente archivos residuales (ej. `.thm`, `.moff`, `.DS_Store`).
* **Arquitectura Modular:** Separación clara de responsabilidades (Configuraciones, Utilidades y Bucle Principal) facilitando el mantenimiento y futuro Testing Unitario.

## 📂 Estructura del Proyecto

```text
media-sorter/
├── config.py           # Variables de entorno, rutas base y extensiones permitidas
├── utils.py            # Lógica aislada: Auto-renombrado y validación de hashes rotacionales
├── main.py             # CLI, orquestador principal y control de flujo
├── requirements.txt    # Dependencias del proyecto
└── README.md
