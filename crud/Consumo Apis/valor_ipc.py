import requests
# [DÓNDE ESTA LA API?]-----↓
base_url = "https://mindicador.cl"
# [Protocolo de la API]-----↑

# Ruta o Endpoint que me dice el valor del IPC
endpoint_ipc = "/api/ipc"

# Juntamos la URL y el Endpoint para hacer la petición de tipo GET
respuesta = requests.get(f"{base_url}{endpoint_ipc}")
#                        ↑ = https://mindicador.cl/api/ipc

try:
    # Serializamos la información en JSON para trabajarla de forma estructurada
    data = respuesta.json()
    
    # [FILTRADO DE DATOS]-----↓
    # 1. PRIMERO extraemos el valor (antes de intentar imprimirlo)
    valor_actual = data['serie'][0]['valor'] 
    
    # Lo imprimimos usando la variable 'valor_actual'
    print(f"Índice de Precio al Consumidor (IPC): {valor_actual}%")

except:
    print(respuesta)