import requests
# [DÓNDE ESTA LA API?]-----↓
base_url = "https://mindicador.cl"
# [Protocolo de la API]-----↑

# Ruta o Endpoint que me dice el valor de la UF
endpoint_uf = "/api/uf"

# Juntamos la URL y el Endpoint para hacer la petición de tipo GET
respuesta = requests.get(f"{base_url}{endpoint_uf}")
#                        ↑ = https://mindicador.cl/api/uf

try:
    # Serializamos la información en JSON para trabajarla de forma estructurada
    data = respuesta.json()
    
    # [FILTRADO DE DATOS]-----↓
    # 1. PRIMERO extraemos el valor (antes de intentar imprimirlo)
    valor_actual = data['serie'][0]['valor'] 
    
    # Lo imprimimos usando la variable 'valor_actual'
    print(f"Valor Unidad de Fomento (UF): ${valor_actual}")

except:
    print(respuesta)