import json
import os
import requests

def process_and_upload(json_path, API_URL, BEARER_TOKEN):

    HEADERS = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
    }

    if not os.path.exists(json_path):
        print(f"Arquivo '{json_path}' não encontrado.")
        return
    
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    updated = False

    for material in data:
        if material.get("Upload") == 0:
            nome_material = material["Nome_Material"]
            url_arquivo = material["URL_arquivo"]

            if not os.path.exists(url_arquivo):
                print(f"Arquivo '{url_arquivo}' não encontrado. Pulando upload.")
                continue 

            with open(url_arquivo, "rb") as file_to_upload:
                files = {"file": file_to_upload}
                upload_data = {"name": nome_material}

                try:
                    response = requests.post(API_URL, headers=HEADERS, data=upload_data, files=files)
                    if response.status_code == 200:
                        print(f"Upload concluído para o material '{nome_material}' (ID: {material['Id']}).")
                        material["Upload"] = 1
                        updated = True
                    else:
                        print(f"Falha no upload do material '{nome_material}' (ID: {material['Id']}): {response.text}")
                except Exception as e:
                    print(f"Erro ao fazer upload do material '{nome_material}' (ID: {material['Id']}): {e}")
        else:
            print(f"Material '{material['Nome_Material']}' (ID: {material['Id']}) já foi enviado.")

    if updated:
        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("JSON atualizado com os materiais enviados.")
    else:
        print("Nenhum material necessitava de upload.")
