import time
import datetime

def imprimir_lentamente(texto, retraso=0.01):
    for letra in texto:
        print(letra, end='', flush=True)
        time.sleep(retraso)
    print()

def guardarPeticion(text):
    # Obtener la fecha y hora actual
    now = datetime.datetime.now()

    # Formatear la fecha y hora en el formato deseado
    formatted_date = now.strftime("%d%m%Y_%H%M%S")

    # Crear el nombre del archivo con la fecha y hora formateadas
    filename = f"{formatted_date}.txt"

    # Crear el archivo con el nombre generado
    with open(filename, "w") as file:
        # Escribir contenido en el archivo si lo deseas
        file.write(text)