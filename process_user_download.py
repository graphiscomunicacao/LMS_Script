from download_materiais import download_material
from fetch_material_data import fetch_material_data
from authenticate_google import get_all_records, get_ids_by_type

def process_manual_download(auth_token,service, domain_url):

    ids_input = input("Digite o ID ou IDs (separados por vírgula): ")
    tipo_input = input("Digite o tipo: ")

    ids = ids_input.split(",") if "," in ids_input else [ids_input.strip()]

    materials_response = fetch_material_data(ids, tipo_input,domain_url, auth_token)

    if isinstance(materials_response, dict):
        
        materiais_encontrados = materials_response.get("Material", [])
        ids_nao_encontrados = materials_response.get("Ids_Nao_Encontrados", [])

        if materiais_encontrados:
            for material in materiais_encontrados:

                print("\nMaterial encontrado:")
                print("Baixando material de ID: " + str(material.get("ID", "N/A")))
                print("\n")
                
                download_material(material, tipo_input, domain_url)

        else:
            print("Nenhum material encontrado.")
        
        print('\n')

        if ids_nao_encontrados:
            for valor in ids_nao_encontrados:
                print("IDs não encontrados: " + str(valor))
        else:
            print("Todos os IDs foram encontrados.")
    
    else:
        print("Falha ao buscar materiais ou tipo de resposta inesperado.")



def process_automatic_download(auth_token,service, sheet_id, domain_url):
    
    name_sheet = input("Digite o nome da planilha: ")
    tipo_input = input("Digite o tipo: ")


    records = get_all_records(service, sheet_id, name_sheet)
    ids = get_ids_by_type(records, tipo_input)
    print(ids)

    materials_response = fetch_material_data(ids, tipo_input, domain_url, auth_token)

    if isinstance(materials_response, dict):

        materiais_encontrados = materials_response.get("Material", [])
        ids_nao_encontrados = materials_response.get("Ids_Nao_Encontrados", [])
        
        if materiais_encontrados:
            for material in materiais_encontrados:

                print("\nMaterial encontrado:")
                print("ID: " + str(material.get("ID", "N/A")))
                # print("Nome do material: " + material.get("Nome_Material", "N/A"))
                # print("Nome do arquivo: " + material.get("Nome_Arquivo", "N/A"))
                # print("URL do material: " + material.get("URL", "N/A"))
                print("\n")
                
                download_material(material, tipo_input, domain_url)
        


        else:
            print("Nenhum material encontrado.")
        
        print('\n')

        if ids_nao_encontrados:
            for valor in ids_nao_encontrados:
                print("IDs não encontrados: " + str(valor))
        else:
            print("Todos os IDs foram encontrados.")

    else:
        print("Falha ao buscar materiais ou tipo de resposta inesperado.")
