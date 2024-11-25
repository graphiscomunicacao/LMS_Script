from process_user_download import process_manual_download, process_automatic_download
from authenticate_google import authenticate_google_sheet
import os
from dotenv import load_dotenv
from upload_user import process_and_upload
import pyfiglet

def bannerLMS():
    ascii_banner = pyfiglet.figlet_format("LMS SCRIPT")
    print(ascii_banner + "\n")

def main():

    bannerLMS()

    load_dotenv(dotenv_path=("config.env"))
    domain_url = os.getenv("DOMAIN_URL")
    credentials_file = os.getenv("CREDENTIALS_FILE")
    sheet_id = os.getenv("SHEET_ID")
    auth_token = os.getenv("AUTH_TOKEN")
    API_URL = os.getenv("API_URL")
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")
    JSON_FILE = os.path.join("Uploads", "upload.json")


    if not domain_url or not credentials_file or not sheet_id or not auth_token:
        print("Erro: Algumas variáveis de ambiente não foram definidas corretamente no arquivo .env.")
        print("Certifique-se de que o arquivo .env contém as variáveis DOMAIN_URL, CREDENTIALS_FILE, SHEET_ID e AUTH_TOKEN.")
        return

    service = authenticate_google_sheet(credentials_file)

    if service:
        modo = input("Escolha o modo: (1) Manual ou (2) Automático: ")
        print("\n")
        
        if modo == "1":
            process_manual_download(auth_token, service, domain_url)
            process_and_upload(JSON_FILE,API_URL,BEARER_TOKEN)
        elif modo == "2":
            process_automatic_download(auth_token, service, sheet_id,domain_url)
            process_and_upload(JSON_FILE,API_URL,BEARER_TOKEN)
        else:
            print("Modo inválido.")
    else:
        print("Não foi possível autenticar a planilha do Google.")


if __name__ == "__main__":
    main()
