import shutil
import logging
import exifread
import argparse
import imagehash
from config import * 
from PIL import Image
from utils import isRepeat 
from datetime import datetime

# hides some annoying messages
logging.getLogger('exifread').setLevel(logging.ERROR)

# the unique images set
og_photos = set()


archivos_procesados_totales = 0
archivos_resultantes = 0

parser = argparse.ArgumentParser(description="Media Sorter: Ordena tus fotos y videos automáticamente.")

parser.add_argument("origen", type=str, help="Ruta de la carpeta o pendrive que querés ordenar")

args = parser.parse_args()

SOURCE_PATH = Path(args.origen)

if not SOURCE_PATH.exists() or not SOURCE_PATH.is_dir():
    print(f"❌ Error: La ruta '{SOURCE_PATH}' no existe o no es una carpeta válida.")
    exit(1)

print(f"🚀 Iniciando Media Sorter en: {SOURCE_PATH}")
print("-" * 40)

for root, dirs, files in SOURCE_PATH.walk():
    for file in files:
        match file:
            # "Secret" file from macOS, we ignore it
            case ".DS_Store":
                continue

            case _ if file.lower().endswith(VIDEO_EXT):
                PATH_VIDEOS.mkdir(parents=True, exist_ok=True)
                shutil.move(str(root / file), str(PATH_VIDEOS / file))
                archivos_procesados_totales += 1
                archivos_resultantes += 1
                continue

            case _ if file.lower().endswith(TASH_EXT):
                PATH_TASH.mkdir(parents=True, exist_ok=True)
                shutil.move(str(root / file), str(PATH_TASH / file))
                archivos_procesados_totales += 1
                continue

            case _:
                # Cuando entra aca es pq el archivo es un .jpg, por lo que lo abro en modo lectura binaria
                with open(root / file, "rb") as f:

                    # una vez con el archivo abierto, llamo a la funcion que ve si sus 4 posibles hashes ya fueron procesados
                    # si fue asi, entonces la imagen actual es repetida y debe ir donde le toca
                    if isRepeat(f, og_photos):
                        PATH_REPEATED.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(root / file), str(PATH_REPEATED))
                        archivos_procesados_totales += 1

                    # sino, debo agregar alguno de sus hashes al set y debo ubicarla donde corresponde
                    else:
                            # obtengo los metadatos EXIF de la imagen, para separar el DateTimeOriginal
                            tags = exifread.process_file(f)
                            # abro (devuelta) la imagen actual
                            tmp = Image.open(f)
                            # parseo a string el hash de la imagen actual
                            actualHash = str(imagehash.phash(tmp))
                            # agrego el hash de la actual al set
                            og_photos.add(actualHash)
                            # obtengo la fecha de captura de la foto
                            rawDate = tags.get("EXIF DateTimeOriginal", "Sin fecha EXIF")

                            # prevision de errores innecesaria
                            date_str = str(rawDate)                    
                            fecha_objeto = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S") 
                            nombre_carpeta = fecha_objeto.strftime("%Y-%m") 

                            newPath = FINAL_PATH / nombre_carpeta
                            newPath.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(root / file), str(newPath / file))
                            archivos_procesados_totales += 1
                            archivos_resultantes += 1



print(f"Archivos resultantes: {archivos_resultantes}")
print(f"Archivos procesados: {archivos_procesados_totales}")


