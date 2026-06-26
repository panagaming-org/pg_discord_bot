import requests

# 1. Asegúrate de que esta URL sea la ruta real de tu Blueprint (api o view)
URL = "http://127.0.0.1:5000/api/security/reports/add"

# 2. Las llaves ahora mapean 1:1 con tu backend Flask
report_data = {
    "username": "RosaMelano",
    "action_type": "Baneo",
    "target_platform": "discord",
    "target_user_id": "342342634634534534",
    "reason": "Por enviar enlaces de Onlyfans.",
    "evidence_url": [],  # Tu backend busca esto con data.get('evidence_url')
    "active": True, 
    "expires_at": ""     # Se enviará vacío y tu filtro lo convertirá en None
}

try:
    print("🚀 Enviando reporte como JSON al servidor...")
    
    response = requests.post(URL, json=report_data)

    if response.status_code in [200, 201]:
        print("✅ ¡Reporte creado exitosamente!")
        print("Respuesta del servidor:", response.text)
    else:
        print(f"❌ Error en el servidor. Código de estado: {response.status_code}")
        print("Respuesta del servidor:", response.text)
    
except requests.exceptions.ConnectionError:
    print("🔥 Error: No se puede conectar con el servidor. ¿Está Flask corriendo?")
except Exception as e:
    print(f"⚠️ Ocurrió un error inesperado: {e}")