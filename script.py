import sys
from PIL import Image
import exifread
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import hashlib
import shutil
from pathlib import Path
import argparse
from datetime import datetime

path = "/Users/juangozzi/Desktop/pruebas"

extensiones_videos = (".mpg", ".avi")
extensiones_basura = (".moff", ".thm")

path_basura = path + "/" + "basura"
path_videos = path + "/" + "videos"
path_repetidas = path + "/" + "repetidas"


for root, dirs, files in Path(path).walk():
    print(f"Current Directory: {root}")
    for file in files:
        match file:
            case ".DS_Store":
                continue
            case _ if file.lower().endswith(extensiones_videos):
                print(f"  El archivo {file} es un video, lo mando a la carpeta de videos.")
                path_videos.mkdir(parents=True, exist_ok=True)
                shutil.move(str(root / file), str(path_videos / file))
                continue
            case _ if file.lower().endswith(extensiones_basura):
                print(f" El archivo {file} es basura, lo mando a la carpeta de la basura.")
                path_basura.mkdir(parents=True, exist_ok=True)
                shutil.move(str(root / file), str(path_basura / file))
                continue
            case _:
                with open(root / file, "rb") as f:
                    tags = exifread.process_file(f)
                    rawDate = tags.get("EXIF DateTimeOriginal", "Sin fecha EXIF")
                    try:   
                        date_str = str(rawDate) # paso a string el fecha                   
                        fecha_objeto = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S") # parsea la fecha como cadena a objeto datetime
                        nombre_carpeta = fecha_objeto.strftime("%Y-%m") # parsea de tipo datetime a cadena con el formato que paso ahi
                    except:
                        print(f"  ⚠️ Error de formato en fecha de {file}: {date_str}")
                newPath = root / nombre_carpeta
                newPath.mkdir(parents=True, exist_ok=True)
                shutil.move(str(root / file), str(newPath / file))

