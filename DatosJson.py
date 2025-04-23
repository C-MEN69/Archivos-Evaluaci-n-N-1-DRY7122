import json
from datetime import datetime, timedelta

# Abrimos el archivo JSON y lo cargamos en la variable ourjson
with open('myfile.json', 'r') as archivo:
    ourjson = json.load(archivo)

# Obtener el token desde el JSON
token = ourjson.get('access_token', 'Token no encontrado')

# Obtener el tiempo de expiración en segundos
expires_in = ourjson.get('expires_in')

if expires_in:
    # Suponemos que el token fue generado ahora mismo
    issued_time = datetime.now()
    expiration_time = issued_time + timedelta(seconds=expires_in)
    tiempo_restante = expiration_time - datetime.now()

    # Mostrar resultados
    print(f"Token: {token}")
    print(f"Tiempo restante antes de que el Token caduque es: {tiempo_restante}")
else:
    print("No se encontró la clave 'expires_in' en el archivo JSON.")
