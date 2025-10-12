import os
import shutil
import random

def separar_imagenes_una_carpeta(carpeta_origen, carpeta_destino, num_imagenes=300):
    # Crear la carpeta de destino si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    # Recorrer todas las subcarpetas en la carpeta de origen
    for subcarpeta in os.listdir(carpeta_origen):
        ruta_subcarpeta = os.path.join(carpeta_origen, subcarpeta)
        
        # Verificar si es una carpeta
        if os.path.isdir(ruta_subcarpeta):
            # Obtener lista de imágenes en la subcarpeta
            imagenes = [f for f in os.listdir(ruta_subcarpeta) 
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            
            # Seleccionar aleatoriamente las imágenes
            num_a_copiar = min(num_imagenes, len(imagenes))
            imagenes_seleccionadas = random.sample(imagenes, num_a_copiar)
            
            # Copiar las imágenes seleccionadas
            for imagen in imagenes_seleccionadas:
                ruta_origen = os.path.join(ruta_subcarpeta, imagen)
                # Crear nuevo nombre de archivo con el prefijo de la subcarpeta
                nuevo_nombre = f"{subcarpeta}_{imagen}"
                ruta_destino = os.path.join(carpeta_destino, nuevo_nombre)
                shutil.copy2(ruta_origen, ruta_destino)
            
            print(f"Se copiaron {num_a_copiar} imágenes de la carpeta {subcarpeta}")

if __name__ == "__main__":
    # Solicitar las rutas al usuario
    carpeta_origen = input("Ingrese la ruta de la carpeta de origen: ")
    carpeta_destino = input("Ingrese la ruta de la carpeta de destino: ")
    
    try:
        separar_imagenes_una_carpeta(carpeta_origen, carpeta_destino)
        print("¡Proceso completado exitosamente!")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")