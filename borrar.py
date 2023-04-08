import json
texto="""\n\nRespuesta: [{\"id\":1,\"Opcion\":\"Explorar el Desierto Infinito\",\"tipo\":\"explorar\"},{\"id\":2,\"Opcion\":\"Buscar una pelea en el Desierto Infinito\",\"tipo\":\"combate\"},{\"id\":3,\"Opcion\":\"Buscar alg\u00fan tesoro en el Desierto Infinito\",\"tipo\":\"explorar\"}]"""

print(texto.split("Respuesta: ")[-1])
opciones = json.loads(texto.split("Respuesta: ")[-1])

# Recorrer la lista de opciones e imprimir el id y la opción
for opcion in opciones:
    print(f"{opcion['id']}-{opcion['Opcion']}")

