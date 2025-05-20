import os

path = r"C:\HETIC\2024-2025\Data_api_web\velib-460309-c175ee433eeb.json"

if os.path.isfile(path):
    print("Fichier trouvé !")
else:
    print("Fichier NON trouvé, vérifie le chemin.")