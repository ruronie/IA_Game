
from JuegoDeRol import JuegoDeRol
import openai_process 
from Personaje import Personaje
import game_lib
 

OPENAI_APIKEY="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"





juego = JuegoDeRol()

razas_disponibles = [str(raza["nombre"]) for raza in juego.razas]
zonas_disponibles = [str(zona["nombre"]) for zona in juego.zonas]


text=f"""
inventarte una breve historia 100 palabras o menos para un juego de Rol estilo dungeons and dragons
El contexto es el siguiente:
"Existen las razas: {razas_disponibles}" 
"Las zonas disponibles son: {zonas_disponibles}"
"Los datos del protagonista son: {juego.personaje}"
"""

# Create ChatGTP prompt
# question1 = "inventarte breve una historia de como mucho 100 palabras para un juego de Rol estilo dungeons and dragons"
# statement = "Estamos jugando a un juego de rol en un mundo inventado" \
#             "Existen las razas: Humanos, Elfos" \
#             "Las zonas disponibles son: Las Tierras del Sur,Las Montañas de Hierro" \
#             f"Los datos del protagonista son: {juego.personaje}", 

# messages = [
#     {"role": "user", "content": statement},
#     {"role": "user", "content": question1},
# ]
game_lib.imprimir_lentamente("Iniciando partida...")
result=openai_process.getResultsOpenai(text,OPENAI_APIKEY)
text = result['choices'][0]['text']
game_lib.imprimir_lentamente(text)

juego.pedirOpciones()
juego.pedirOpciones()


