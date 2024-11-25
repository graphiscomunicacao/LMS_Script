import requests

def fetch_material_data(ids, tipo,domain_url, auth_token):

    url = f"{domain_url}/APIs/downloadApi.php"
    print(f"URL da requisição: {url}")

    headers = {
        "Authorization": f"{auth_token}",
        "Content-Type": "application/json"
    }
    
    int_id = list(map(int, ids))
    int_tipo = int(tipo)

    payload = [{"id": id, "tipo": int_tipo} for id in int_id]

    try:
        response = requests.post(url, json=payload, headers=headers)
        print('\n')
        print("Status code da resposta:", response.status_code)
        
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "sucesso":
            print('\n')
            print("Erro na resposta da API:", data)
            return []

        materials = data.get("Material", [])
        notFoundId = data.get("Ids_Nao_Encontrados", [])
        
        return {
            "Material": materials,
            "Ids_Nao_Encontrados": notFoundId
        }

    
    except requests.exceptions.RequestException as e:
        print("Erro ao fazer requisição:", e)
        return []