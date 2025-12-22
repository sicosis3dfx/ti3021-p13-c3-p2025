import requests

# [DÓNDE ESTA LA API?]-----↓
# Usamos mindicador.cl porque agrupa todos los datos (UF, UTM, Dolar, etc)
base_url = "https://mindicador.cl"
# [Protocolo de la API]-----↑

# Ruta o Endpoint que entrega todos los indicadores económicos del día
endpoint_indicadores = "/api"

# Juntamos la URL y el Endpoint para hacer la petición de tipo GET
respuesta = requests.get(f"{base_url}{endpoint_indicadores}")
#                        ↑ = https://mindicador.cl/api

try:
    # Serializamos la información en JSON para trabajarla de forma estructurada
    data = respuesta.json()

    # Mostramos la data rescatada, pero ORDENADA por cada indicador solicitado
    print("-" * 40)
    print("      INDICADORES ECONÓMICOS AL DÍA")
    print("-" * 40)
    
    # 1. Unidad de Fomento (UF)
    print(f"1. Unidad de Fomento (UF): ${data['uf']['valor']}")

    # 2. Índice de Valor Promedio (IVP)
    print(f"2. Índice de valor Promedio (IVP): ${data['ivp']['valor']}")

    # 3. Índice de Precio al Consumidor (IPC)
    # Nota: El IPC es un porcentaje, por eso agregamos el signo %
    print(f"3. Índice de Precio al Consumidor (IPC): {data['ipc']['valor']}%")

    # 4. Unidad Tributaria Mensual (UTM)
    print(f"4. Unidad Tributaria Mensual (UTM): ${data['utm']['valor']}")

    # 5. Dólar Observado
    print(f"5. Dólar -> a Peso Chileno (CLP): ${data['dolar']['valor']}")

    # 6. Euro
    print(f"6. Euro -> a Peso Chileno (CLP): ${data['euro']['valor']}")

    print("-" * 40)

except:
    # Si algo falla (ej: no hay internet), mostramos la respuesta cruda o el error
    print("Hubo un error al consultar la API.")
    print(respuesta)