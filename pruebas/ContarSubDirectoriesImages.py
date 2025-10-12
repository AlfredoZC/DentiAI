#!/usr/bin/env python3
import os
import argparse
from pathlib import Path

# Extensiones de imagen comunes (añade/quita según necesites)
IMAGE_EXTS = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff",
    ".webp", ".heic", ".heif", ".raw", ".arw", ".cr2", ".nef", ".orf", ".rw2"
}

def es_imagen(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in IMAGE_EXTS

def contar_en_directorio(d: Path, profundo: bool) -> int:
    if profundo:
        # Cuenta en todos los niveles dentro del subdirectorio
        total = 0
        for root, dirs, files in os.walk(d):
            for f in files:
                if Path(f).suffix.lower() in IMAGE_EXTS:
                    total += 1
        return total
    else:
        # Solo el nivel inmediato del subdirectorio
        return sum(1 for p in d.iterdir() if es_imagen(p))

def main():
    parser = argparse.ArgumentParser(
        description="Cuenta cuántas imágenes hay en los subdirectorios de una carpeta."
    )
    parser.add_argument("root", type=Path, help="Ruta del directorio raíz que contiene subdirectorios.")
    parser.add_argument("--profundo", "-p", action="store_true",
                        help="Si se activa, cuenta recursivamente (todos los niveles) dentro de cada subdirectorio.")
    parser.add_argument("--csv", type=Path, default=None,
                        help="Ruta para guardar el reporte en CSV (opcional).")
    parser.add_argument("--incluir-vacios", action="store_true",
                        help="Mostrar también subdirectorios con 0 imágenes.")
    args = parser.parse_args()

    if not args.root.exists() or not args.root.is_dir():
        print(f"ERROR: '{args.root}' no es un directorio válido.")
        return

    # Tomamos SOLO subdirectorios inmediatos
    subdirs = [p for p in args.root.iterdir() if p.is_dir()]
    if not subdirs:
        print("No se encontraron subdirectorios.")
        return

    filas = []
    total_global = 0
    for sd in sorted(subdirs, key=lambda x: x.name.lower()):
        conteo = contar_en_directorio(sd, args.profundo)
        total_global += conteo
        if args.incluir_vacios or conteo > 0:
            filas.append((sd.name, conteo))

    # Impresión en tabla simple
    ancho_nombre = max((len(n) for n, _ in filas), default=10)
    print(f"{'Subdirectorio'.ljust(ancho_nombre)}  Imágenes")
    print(f"{'-'*ancho_nombre}  --------")
    for nombre, cnt in filas:
        print(f"{nombre.ljust(ancho_nombre)}  {cnt}")
    print("-" * (ancho_nombre + 10))
    print(f"{'TOTAL'.ljust(ancho_nombre)}  {total_global}")

    # Guardar CSV si se pidió
    if args.csv:
        try:
            import csv
            args.csv.parent.mkdir(parents=True, exist_ok=True)
            with args.csv.open("w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["subdirectorio", "imagenes"])
                for nombre, cnt in filas:
                    w.writerow([nombre, cnt])
                w.writerow(["TOTAL", total_global])
            print(f"\nReporte CSV guardado en: {args.csv}")
        except Exception as e:
            print(f"\nNo se pudo guardar el CSV: {e}")

if __name__ == "__main__":
    main()
