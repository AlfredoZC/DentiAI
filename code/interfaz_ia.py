import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import tensorflow as tf
import os
import threading
from datetime import datetime

class InterfazIA:
    def __init__(self, root):
        self.root = root
        self.root.title("Diagnóstico Dental con IA")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar el modelo de IA
        self.modelo = None
        self.labels = []
        self.cargar_modelo()
        
        # Variables para la cámara
        self.cap = None
        self.capturando = False
        self.camara_activa = False
        self.canvas = None
        
        # Crear la interfaz
        self.crear_interfaz()
        
    def cargar_modelo(self):
        """Carga el modelo de IA entrenado"""
        try:
            modelo_path = "TeachableMachineModel/converted_keras/keras_model.h5"
            labels_path = "TeachableMachineModel/converted_keras/labels.txt"
            
            if os.path.exists(modelo_path) and os.path.exists(labels_path):
                self.modelo = tf.keras.models.load_model(modelo_path)
                
                # Cargar labels
                with open(labels_path, 'r', encoding='utf-8') as f:
                    self.labels = [line.strip().split(' ', 1)[1] for line in f.readlines()]
                
                print(f"Modelo cargado exitosamente. Clases: {self.labels}")
            else:
                messagebox.showerror("Error", "No se encontró el modelo de IA")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el modelo: {str(e)}")
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica"""
        # Título principal
        titulo = tk.Label(
            self.root, 
            text="🔍 Diagnóstico Dental con Inteligencia Artificial",
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        titulo.pack(pady=20)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Frame para botones
        botones_frame = tk.Frame(main_frame, bg='#f0f0f0')
        botones_frame.pack(pady=20)
        
        # Botón para subir imagen
        btn_subir = tk.Button(
            botones_frame,
            text="📁 Subir Imagen",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            command=self.subir_imagen,
            cursor='hand2'
        )
        btn_subir.pack(side='left', padx=10)
        
        # Botón para activar/desactivar cámara
        self.btn_camara = tk.Button(
            botones_frame,
            text="📷 Activar Cámara",
            font=("Arial", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=10,
            command=self.toggle_camara,
            cursor='hand2'
        )
        self.btn_camara.pack(side='left', padx=10)
        
        # Botón para tomar foto (solo activo cuando cámara está encendida)
        self.btn_tomar_foto = tk.Button(
            botones_frame,
            text="📸 Tomar Foto",
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=10,
            command=self.tomar_foto,
            cursor='hand2',
            state='disabled'
        )
        self.btn_tomar_foto.pack(side='left', padx=10)
        
        # Frame para mostrar imagen
        imagen_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        imagen_frame.pack(expand=True, fill='both', pady=10)
        
        # Label para mostrar imagen
        self.label_imagen = tk.Label(
            imagen_frame,
            text="Selecciona una imagen o toma una foto",
            font=("Arial", 14),
            bg='white',
            fg='#7f8c8d'
        )
        self.label_imagen.pack(expand=True)
        
        # Frame para resultados
        resultados_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='raised', bd=2)
        resultados_frame.pack(fill='x', pady=10)
        
        # Título de resultados
        titulo_resultados = tk.Label(
            resultados_frame,
            text="📊 Resultados del Diagnóstico",
            font=("Arial", 14, "bold"),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        titulo_resultados.pack(pady=10)
        
        # Frame con scrollbar para resultados
        resultados_scroll_frame = tk.Frame(resultados_frame, bg='#ecf0f1')
        resultados_scroll_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Crear scrollbar
        scrollbar = tk.Scrollbar(resultados_scroll_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Crear canvas para el texto con scrollbar
        self.canvas = tk.Canvas(
            resultados_scroll_frame,
            yscrollcommand=scrollbar.set,
            bg='#ecf0f1',
            height=200
        )
        self.canvas.pack(side='left', fill='both', expand=True)
        
        # Configurar scrollbar
        scrollbar.config(command=self.canvas.yview)
        
        # Frame para el contenido del canvas
        self.frame_contenido = tk.Frame(self.canvas, bg='#ecf0f1')
        self.canvas.create_window((0, 0), window=self.frame_contenido, anchor='nw')
        
        # Label para mostrar resultados
        self.label_resultados = tk.Label(
            self.frame_contenido,
            text="Los resultados aparecerán aquí",
            font=("Arial", 12),
            bg='#ecf0f1',
            fg='#34495e',
            wraplength=750,
            justify='left'
        )
        self.label_resultados.pack(pady=10, padx=10)
        
        # Frame para información adicional
        info_frame = tk.Frame(main_frame, bg='#f0f0f0')
        info_frame.pack(fill='x', pady=5)
        
        info_text = tk.Label(
            info_frame,
            text="💡 Consejo: Para mejores resultados, asegúrate de que la imagen esté bien iluminada y enfocada",
            font=("Arial", 10, "italic"),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        info_text.pack()
    
    def subir_imagen(self):
        """Permite al usuario seleccionar una imagen desde el disco"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            self.procesar_imagen(archivo)
    
    def toggle_camara(self):
        """Activa o desactiva la cámara"""
        if not self.camara_activa:
            self.activar_camara()
        else:
            self.desactivar_camara()
    
    def activar_camara(self):
        """Activa la cámara para captura en tiempo real"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "No se pudo acceder a la cámara")
                return
            
            self.camara_activa = True
            self.capturando = True
            
            # Actualizar botones
            self.btn_camara.config(text="📷 Desactivar Cámara", bg='#95a5a6')
            self.btn_tomar_foto.config(state='normal')
            
            # Actualizar label
            self.label_imagen.config(
                text="Cámara activada - Haz clic en 'Tomar Foto' para capturar",
                fg='#27ae60'
            )
            
            # Iniciar captura en un hilo separado
            threading.Thread(target=self.capturar_video, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al acceder a la cámara: {str(e)}")
    
    def desactivar_camara(self):
        """Desactiva la cámara"""
        self.capturando = False
        self.camara_activa = False
        
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        
        # Actualizar botones
        self.btn_camara.config(text="📷 Activar Cámara", bg='#e74c3c')
        self.btn_tomar_foto.config(state='disabled')
        
        # Actualizar label
        self.label_imagen.config(
            text="Selecciona una imagen o toma una foto",
            fg='#7f8c8d'
        )
        cv2.destroyAllWindows()
    
    def tomar_foto(self):
        """Toma una foto de lo que está capturando la cámara"""
        if not self.camara_activa or self.cap is None:
            messagebox.showwarning("Advertencia", "Primero debes activar la cámara")
            return
        
        try:
            ret, frame = self.cap.read()
            if ret:
                # Guardar imagen temporal
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                temp_path = f"temp_capture_{timestamp}.jpg"
                cv2.imwrite(temp_path, frame)
                
                # Mostrar la imagen capturada
                imagen = Image.open(temp_path)
                imagen_resized = imagen.resize((400, 300), Image.Resampling.LANCZOS)
                imagen_tk = ImageTk.PhotoImage(imagen_resized)
                self.label_imagen.config(image=imagen_tk, text="")
                self.label_imagen.image = imagen_tk
                
                # Procesar la imagen capturada
                self.procesar_imagen(temp_path)
                
                # Limpiar archivo temporal
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al tomar foto: {str(e)}")
    
    def capturar_video(self):
        """Captura video desde la cámara"""
        while self.capturando and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                # Mostrar el frame en la interfaz
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                frame_resized = frame_pil.resize((400, 300), Image.Resampling.LANCZOS)
                frame_tk = ImageTk.PhotoImage(frame_resized)
                
                self.label_imagen.config(image=frame_tk, text="")
                self.label_imagen.image = frame_tk
            
            self.root.update()
        
        # Si llegamos aquí, la cámara se desactivó
        if self.camara_activa:
            self.desactivar_camara()
    
    def procesar_imagen(self, ruta_imagen):
        """Procesa la imagen y realiza la predicción"""
        try:
            if self.modelo is None:
                messagebox.showerror("Error", "El modelo de IA no está cargado")
                return
            
            # Cargar y preprocesar la imagen
            imagen = Image.open(ruta_imagen)
            imagen_rgb = imagen.convert('RGB')
            
            # Mostrar la imagen en la interfaz
            imagen_resized = imagen_rgb.resize((400, 300), Image.Resampling.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen_resized)
            self.label_imagen.config(image=imagen_tk, text="")
            self.label_imagen.image = imagen_tk
            
            # Preprocesar para el modelo
            imagen_modelo = imagen_rgb.resize((224, 224), Image.Resampling.LANCZOS)
            imagen_array = np.array(imagen_modelo)
            imagen_array = np.expand_dims(imagen_array, axis=0)
            imagen_array = imagen_array.astype('float32') / 255.0
            
            # Realizar predicción
            predicciones = self.modelo.predict(imagen_array)
            clase_predicha = np.argmax(predicciones[0])
            confianza = predicciones[0][clase_predicha] * 100
            
            # Mostrar resultados
            self.mostrar_resultados(clase_predicha, confianza, predicciones[0])
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la imagen: {str(e)}")
    
    def mostrar_resultados(self, clase_predicha, confianza, todas_predicciones):
        """Muestra los resultados de la predicción"""
        nombre_clase = self.labels[clase_predicha] if clase_predicha < len(self.labels) else "Desconocido"
        
        # Resultado principal
        resultado_principal = f"""🎯 DIAGNÓSTICO PRINCIPAL:
{nombre_clase}
Confianza: {confianza:.1f}%

"""
        
        # Todas las predicciones
        todas_predicciones_texto = "📊 TODAS LAS PREDICCIONES:\n"
        for i, (clase, prob) in enumerate(zip(self.labels, todas_predicciones * 100)):
            todas_predicciones_texto += f"• {clase}: {prob:.1f}%\n"
        
        # Recomendaciones basadas en el diagnóstico
        recomendaciones = self.obtener_recomendaciones(nombre_clase)
        
        resultado_completo = resultado_principal + todas_predicciones_texto + recomendaciones
        
        # Actualizar el label de resultados
        self.label_resultados.config(text=resultado_completo)
        
        # Actualizar el scroll del canvas
        self.frame_contenido.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def obtener_recomendaciones(self, diagnostico):
        """Proporciona recomendaciones basadas en el diagnóstico"""
        recomendaciones = {
            "Calculos": "\n💡 RECOMENDACIÓN: Consulta con un dentista para limpieza profesional (profilaxis).",
            "Caries": "\n💡 RECOMENDACIÓN: Visita urgente al dentista para tratamiento de la caries.",
            "Gingivitis": "\n💡 RECOMENDACIÓN: Mejora tu higiene bucal y consulta al dentista.",
            "Ulcera bucal": "\n💡 RECOMENDACIÓN: Evita alimentos ácidos y consulta si persiste más de 2 semanas.",
            "Dientes descoloridos": "\n💡 RECOMENDACIÓN: Consulta sobre opciones de blanqueamiento dental.",
            "Dientes Normales": "\n💡 RECOMENDACIÓN: ¡Excelente! Mantén tu higiene bucal actual."
        }
        
        return recomendaciones.get(diagnostico, "\n💡 RECOMENDACIÓN: Consulta con un profesional dental.")
    
    def __del__(self):
        """Limpia recursos al cerrar"""
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

def main():
    root = tk.Tk()
    app = InterfazIA(root)
    
    # Manejar cierre de ventana
    def on_closing():
        app.desactivar_camara()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
