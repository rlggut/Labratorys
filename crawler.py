import os
import pathlib
import shutil
import zipfile
import subprocess
import zlib

output_path = os.path.join(os.getcwd(), "Pics.zip")  # Путь к выходному архиву на рабочем столе

temp_FilesDir = os.path.join(os.getcwd(), "temp")  # Создаем директорию для размещения временных файлов
os.makedirs(temp_FilesDir, exist_ok=True)
Files=os.listdir(os.getcwd())

while(len(Files)):
    path=Files[0]
    Files.pop(0)
    if(not os.path.exists(path)):
        continue
    if(os.path.isdir(path)):
        folder_consist = os.listdir(path)
        for item in folder_consist:
            Files.append(os.path.join(path,item))
    else:
        if(".png" in path or ".jpg" in path):
            try:
                shutil.copy(path,temp_FilesDir)
            except:
                print("Coping failed: ", path)
                continue

with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as archive:
    for fileName in os.listdir(temp_FilesDir):
        archive.write(os.path.join(temp_FilesDir, fileName),fileName)
    archive.close()

shutil.rmtree(temp_FilesDir)

print("Archive pics is saved as Pics.zip")