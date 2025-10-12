
---

# 🦷 Clasificación de Afecciones Bucales mediante Inteligencia Artificial

Este proyecto implementa un modelo de **Inteligencia Artificial** capaz de detectar y clasificar enfermedades bucales a partir de imágenes capturadas con cámara o cargadas desde un dispositivo.
El sistema fue entrenado con **Teachable Machine (Google)** y posteriormente integrado en una **interfaz gráfica desarrollada en Python (Tkinter)**.

---

## 📘 Descripción del Proyecto

El sistema identifica seis tipos de condiciones bucales:

* 🪥 Cálculos dentales
* 🦷 Caries
* 🩸 Gingivitis
* 💥 Úlcera bucal
* ⚪ Dientes descoloridos
* 😁 Dientes normales

El modelo se entrenó mediante **aprendizaje supervisado** con una **red neuronal convolucional (CNN)**, exportado desde Teachable Machine y adaptado para ejecutarse localmente en Python.

---

## 🧠 Objetivo General

Desarrollar un modelo de IA capaz de clasificar correctamente imágenes bucales en seis categorías con el fin de apoyar el diagnóstico visual en odontología y facilitar la detección preliminar de afecciones.

---

## ⚙️ Estructura del Proyecto

```
📂 proyecto_afecciones_bucales/
├── 📂 code/
│   ├── interfaz.py
│   ├── model/
│   │   ├── keras_model.h5
│   │   └── labels.txt
│   └── utils/
│       └── ...
├── requirements.txt
├── README.md
└── first block documentation.docx
```

---

## 🚀 Instrucciones de Ejecución

### 1️⃣ Clonar el repositorio o descargar los archivos

```bash
git clone https://github.com/tu_usuario/proyecto_afecciones_bucales.git
cd proyecto_afecciones_bucales
```

### 2️⃣ Crear un entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate   # En Linux o Mac
venv\Scripts\activate      # En Windows
```

### 3️⃣ Instalar las dependencias necesarias

Asegúrate de tener el archivo `requirements.txt` en la raíz del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar la aplicación

Corre el script principal ubicado dentro de la carpeta `code`:

```bash
python code/interfaz_ia.py
```

---

## 🖥️ Interfaz de Usuario

La aplicación permite:

* 📸 Cargar una imagen bucal desde el dispositivo.
* 🔍 Procesarla mediante el modelo entrenado.
* 🧾 Mostrar el resultado en pantalla con la probabilidad estimada para cada clase.

---

## 🧩 Dependencias Principales

El archivo `requirements.txt` incluye, entre otras:

* `tensorflow`
* `keras`
* `numpy`
* `pillow`
* `tkinter`
* `opencv-python`

---

## 📊 Dataset

| Parámetro                  | Descripción            |
| -------------------------- | ---------------------- |
| **Número total de clases** | 6                      |
| **Imágenes por clase**     | 600                    |
| **Total de imágenes**      | 3,600                  |
| **Formato**                | JPG / PNG              |
| **Tamaño promedio**        | 224x224 píxeles        |
| **Tipo de aprendizaje**    | Supervisado            |
| **División**               | Entrenamiento / Prueba |

---

## 🧪 Resultados y Evaluación

El modelo alcanzó un desempeño medianamente satisfactory (por el momento) en la identificación de las clases principales.
Las pruebas demostraron una mediana capacidad de generalización pero si una respuesta rápida al clasificar imágenes nuevas.

---

## 🧭 Futuras Mejoras

* Aplicar **data augmentation** para ampliar el dataset.
* Incorporar modelos de **detección de objetos (YOLO, SSD)** para ubicar la zona afectada.
* Integrar la aplicación en una versión móvil o web para **telemedicina dental**.

---

## 👨‍💻 Autor

**José Alfredo Zambrana**
Estudiante de Ingeniería en Inteligencia Artificial
Santa Cruz - Bolivia, 2025

