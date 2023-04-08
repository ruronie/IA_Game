import json
import os
import openai
import random
import datetime

OPENAI_APIKEY="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"

def guardarPeticion(text):
    # Obtener la fecha y hora actual
    now = datetime.datetime.now()

    # Formatear la fecha y hora en el formato deseado
    formatted_date = now.strftime("%d%m%Y_%H%M%S")

    # Crear el nombre del archivo con la fecha y hora formateadas
    filename = f"{formatted_date}.txt"

    # Crear el archivo con el nombre generado
    with open(f'Data\Output\{filename}', "w") as file:
        # Escribir contenido en el archivo si lo deseas
        file.write(text)

def getResultsOpenai(texto,api_key=OPENAI_APIKEY):

    openai.api_key=api_key
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=texto,
    temperature=0.5,
    max_tokens=400,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    guardarPeticion(str(response))

    return response


