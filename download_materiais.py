import requests
import json
import os
from tipo_input_string import tipo_input_string

def download_material(material, tipo_input, domain_url):

    if (tipo_input != "8"):
    
        tipo_input_stg = tipo_input_string(tipo_input)

        download_dir = os.path.join("Downloads", tipo_input_stg)
        os.makedirs(download_dir, exist_ok=True)
        
        upload_dir = os.path.join("Uploads")
        os.makedirs(upload_dir, exist_ok=True)

        id_material = material.get("ID")
        nome_material = material.get("Nome_Material")
        url = material.get("URL")
        urlDownload = f"{domain_url}{url}"

        file_path = os.path.join(download_dir, nome_material)
        json_path = os.path.join(upload_dir, "upload.json")

        try:
            response = requests.get(urlDownload, stream=True)
            response.raise_for_status()
            
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            path = file_path.replace("\\", "/")
            print(f"Arquivo '{nome_material}' baixado com sucesso em '{path}'.")

        except requests.exceptions.RequestException as e:
            path = None
            print(f"Erro ao baixar '{nome_material}': {e}")
            # return

        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as json_file:
                try:
                    all_uploads = json.load(json_file)
                except json.JSONDecodeError:
                    all_uploads = []
        else:
            all_uploads = []

        ids_existentes = {str(material.get("Id")) for material in all_uploads}

        if str(id_material) in ids_existentes:
            print(f"Material com ID '{id_material}' já está salvo em '{json_path}'.")
            return

        upload_data = {
            "Id": id_material,
            "Nome_Material": nome_material,
            "URL_arquivo": path if path is not None else "",
            "Tipo": tipo_input,
            "Upload": 0
        }

        all_uploads.append(upload_data)

        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(all_uploads, json_file, ensure_ascii=False, indent=4)
        
        print(f"Informações do material adicionadas a '{json_path}'.")

    else:
        tipo_input = tipo_input_string (tipo_input)
        download_dir = os.path.join("Downloads", tipo_input)
        os.makedirs(download_dir, exist_ok=True)

        nome_material= material.get("Nome_Material")
        url = material.get("URL")
        
        json_path = os.path.join(download_dir, f"LinkUteis.json")

        try:

            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as json_file:
                    all_materials = json.load(json_file)
            else:
                all_materials = []

            urls_existentes = {material["URL"] for material in all_materials}

            if url in urls_existentes:
                print(f"Material com a URL '{url}' já está salvo em '{json_path}'.")
                return
        
            material_data = {
                "Nome_Material": nome_material,
                "URL": url
            }
            
            all_materials.append(material_data)
            
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(all_materials, json_file, ensure_ascii=False, indent=4)
            print(f"Informações do material adicionadas a '{json_path}'.")

        except requests.exceptions.RequestException as e:
            print(f"Erro ao sal '{nome_material}': {e}")

        
        
