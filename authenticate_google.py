from google.oauth2 import service_account
from googleapiclient.discovery import build

def authenticate_google_sheet(credentials_file):

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    try:
        creds = service_account.Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        return service
    
    except Exception as e:
        print(f"Erro ao autenticar: {e}")
        return None


def get_all_records(service, sheet_id, name_sheet):

    range_ = f"{name_sheet}!A2:Z"
    result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_).execute()
    values = result.get("values", [])

    headers = ["ID","Materiais","Tipo","Migrar / Não migrar", "Status"]
    all_records = [dict(zip(headers, row)) for row in values if row]
    return all_records


def get_ids_by_type(records, tipo_input):

    tipo_input = int(tipo_input)
    
    tipo_map = {
        7: ["pdf", "jpg", "jpeg", "pptx", "xlsx"],  # Materiais
        8: ["mp3", "wav"],  # Áudios
        9: ["mp4"]          # Vídeos
    }
    tipos_arquivo = tipo_map.get(tipo_input, [])
    ids_filtrados = [record['ID'] for record in records if record['Tipo'].lower() in tipos_arquivo]
    return ids_filtrados
