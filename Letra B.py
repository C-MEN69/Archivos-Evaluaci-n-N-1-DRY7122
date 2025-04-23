import requests # type: ignore
import time
from datetime import datetime, timezone
import math

def dibujar_recuadro(titulo, contenido):
    ancho_titulo = len(titulo) + 4  
    ancho_contenido = max(len(line) for line in contenido.split('\n')) + 4
    ancho_total = max(ancho_titulo, ancho_contenido)
    linea_superior = "═" * ancho_total
    print(f"╔{linea_superior}╗")
    print(f"║  {titulo.upper().center(ancho_total - 4)}  ║")
    print(f"╠{'-' * ancho_total}╣")
    for linea in contenido.split('\n'):
        print(f"║  {linea.ljust(ancho_total - 4)}  ║")
    print(f"╚{linea_superior}╝")

print("Evaluación N°1 Programación y Redes Virtualizadas")
print("Integrantes:")
print(" Jorge Boiselle")
print(" Daniel Maturana")
print(" Hector Velasquez ")

integrantes_completos = ["Jorge Boiselle", "Daniel Maturana", "Hector Velasquez"]
nombre_completo = f"{input('Ingrese su nombre: ')} {input('Ingrese su apellido:')}".lower()

if nombre_completo in [integrante.lower() for integrante in integrantes_completos]:
    dibujar_recuadro("Verificación de Integrante", f"Bienvenido {nombre_completo.title()} usuario VIP.")
else:
    dibujar_recuadro("Verificación de Integrante", f"Lo siento, {nombre_completo.title()} no se encuentra en la lista VIP.")
    exit()

codigo_seccion_real = "003V"
codigo_seccion = input("Ingrese su código de sección: ")
if codigo_seccion != codigo_seccion_real:
    dibujar_recuadro("Verificación de Sección", f"Código incorrecto. Se esperaba '{codigo_seccion_real}', ingresaste '{codigo_seccion}'.")
    exit()
else:
    dibujar_recuadro("Verificación de Sección", f"Código correcto: {codigo_seccion}")
    sede = input("Ingrese su sede: ")
    dibujar_recuadro("Sede Ingresada", sede)

def verificar_tipo_acl(numero_acl_str):
    try:
        numero = int(numero_acl_str)
        if 1 <= numero <= 99:
            return f"La ACL {numero} es una ACL Estándar."
        elif 100 <= numero <= 199:
            return f"La ACL {numero} es una ACL Extendida."
        else:
            return f"El número {numero} no corresponde a una lista de acceso estándar o extendida común."
    except ValueError:
        return "Por favor, ingrese un número entero válido."

numero_acl = input("Ingrese el número de ACL IPv4: ")
dibujar_recuadro("Tipo de ACL", verificar_tipo_acl(numero_acl))

def obtener_posicion_iss():
    url = "http://api.open-notify.org/iss-now.json"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        latitude = float(data['iss_position']['latitude'])
        longitude = float(data['iss_position']['longitude'])
        timestamp = data['timestamp']
        return latitude, longitude, timestamp
    except requests.exceptions.RequestException as e:
        return f"Error al obtener la posición de la ISS: {e}", None, None

def calcular_velocidad(lat1, lon1, lat2, lon2, tiempo_segundos):
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    
    R = 6371  
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia_km = R * c

    
    velocidad_kmh = (distancia_km / tiempo_segundos) * 3600
    return velocidad_kmh

if __name__ == "__main__":
    posicion_anterior = []
    tiempo_anterior = None

    while True:
        latitud_actual, longitud_actual, tiempo_actual = obtener_posicion_iss()

        if isinstance(latitud_actual, str): 
            dibujar_recuadro("Error ISS", latitud_actual)
        elif latitud_actual is not None:
            hora_utc = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            contenido_iss = f"Hora de la consulta (UTC): {hora_utc}\n"
            contenido_iss += f"Latitud: {latitud_actual:.4f}, Longitud: {longitud_actual:.4f}"
            dibujar_recuadro("Posición Actual de la ISS", contenido_iss)

            if posicion_anterior is not None and tiempo_anterior is not None:
                tiempo_transcurrido = tiempo_actual - tiempo_anterior
                if tiempo_transcurrido > 0:
                    velocidad_kmh = calcular_velocidad(
                        posicion_anterior[0], posicion_anterior[1],
                        latitud_actual, longitud_actual,
                        tiempo_transcurrido
                    )
                    cambio_latitud_hora = (latitud_actual - posicion_anterior[0]) * (3600 / tiempo_transcurrido)
                    cambio_longitud_hora = (longitud_actual - posicion_anterior[1]) * (3600 / tiempo_transcurrido)
                    velocidad_info = f"Velocidad (aproximada): {velocidad_kmh:.2f} km/h\n"
                    velocidad_info += f"Cambio de Latitud por hora: {cambio_latitud_hora:.4f} grados/hora\n"
                    velocidad_info += f"Cambio de Longitud por hora: {cambio_longitud_hora:.4f} grados/hora"
                    dibujar_recuadro("Velocidad de la ISS", velocidad_info)

            posicion_anterior = (latitud_actual, longitud_actual)
            tiempo_anterior = tiempo_actual

        time.sleep(60)