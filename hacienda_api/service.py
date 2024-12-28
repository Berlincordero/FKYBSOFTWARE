# hacienda_api/services.py
import requests

def consultar_hacienda(cedula):
    """
    Llama a la API pública de Hacienda CR y devuelve un dict con:
      - success: bool
      - data: dict con el JSON recibido
      - error: string si hubo error
    """
    url = f"https://api.hacienda.go.cr/fe/ae?identificacion={cedula}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"Error {response.status_code} al consultar Hacienda."}
    except Exception as e:
        return {"success": False, "error": f"Excepción al consultar Hacienda: {str(e)}"}
