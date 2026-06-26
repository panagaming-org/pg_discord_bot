import requests
import settings.settings as settings 

URL_BASE = settings.get_api_backend()

def get_domains():
    url = f"{URL_BASE}/security/banned-domains"
        
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
    
async def post_report(report_data):
    url = f"{URL_BASE}/security/reports/add"
    try:
        response = requests.post(url, json=report_data)

        if response.status_code in [200, 201]:
            print("Reporte creado exitosamente!!")
        else:
            print(f"❌ Error en el servidor. Código de estado: {response.status_code}")
            print("Respuesta del servidor:", response.text)
        
    except requests.exceptions.ConnectionError:
        print("Error: No se puede conectar con el servidor.")
    except Exception as e:
        print(f"Error inesperado: ", e)