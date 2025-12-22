import requests
# [DÓNDE ESTA LA API?]-----↓
base_url = "https://cl.dolarapi.com"
# [Protocolo de la API]-----↑

# Ruta o Endpoint que me dice el precio del dolar según CLP
endpoint_dolar = "/v1/cotizaciones/usd"

# Juntamos la URL y el Endpoint para hacer la petición de tipo GET
respuesta = requests.get(f"{base_url}{endpoint_dolar}")
#                        ↑ = https://cl.dolarapi.com/v1/cotizaciones/usd

try:
    # Serializamos la información en JSON para trabajarla de forma estructurada
    data = respuesta.json()
    # Mostramos la data rescatada de la respuesta 
    print(data)
except:
    print(respuesta)
