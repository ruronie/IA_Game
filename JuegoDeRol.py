import random
from Personaje import Personaje
import game_lib
import openai_process
import json
import re


class JuegoDeRol:

    def __init__(self):
        self.nombre_juego = self.generar_nombre_juego()
        #self.razas = ["Humanos", "Elfos", "Enanos", "Orcos", "Gnomos", "Medio-elfos", "Dragones"]
        self.razas = [   
            {"id": 1, "nombre": "Humano", "descripcion": "Raza humana"},   
            {"id": 2, "nombre": "Elfo", "descripcion": "Raza elfa"},                   
            {"id": 3, "nombre": "Enano", "descripcion": "Raza enana"},   
            {"id": 4, "nombre": "Orco", "descripcion": "Raza orca"},    
            {"id": 5, "nombre": "Gnomo", "descripcion": "Raza gnoma"}
            ]

        self.zonas =[
            {"id": 1, "nombre": "Bosque Encantado", "descripcion": "Un frondoso bosque lleno de magia y misterio."},
            {"id": 2, "nombre": "Montañas de Fuego", "descripcion": "Unas montañas volcánicas llenas de peligros y tesoros."},
            {"id": 3, "nombre": "Cavernas Oscuras", "descripcion": "Unas cavernas laberínticas llenas de criaturas tenebrosas."},
            {"id": 4, "nombre": "Ciudad Perdida", "descripcion": "Una ciudad en ruinas que guarda antiguos secretos."},
            {"id": 5, "nombre": "Desierto Infinito", "descripcion": "Un vasto desierto lleno de peligros y oportunidades."},
        ]
        #self.zonas = ["Las Tierras del Sur", "Las Montañas de Hierro", "La Costa del Mar del Este", "El Desierto del Oeste", "El Bosque de la Noche Eterna"]
        self.mostrar_info()
        self.personaje=self.crear_personaje()
        print(str(self.personaje))
        
    def mostrar_info(self):
        #game_lib.imprimir_lentamente(self.generar_introduccion())
        print(self.generar_introduccion())
        print("Razas:")
        for raza in self.razas:
            print(str(raza["id"])+"-"+raza["nombre"])
        print("Zonas:")
        for zona in self.zonas:
            print(str(zona["id"])+"-"+zona["nombre"])
        

    def generar_nombre_juego(self):
        lista_nombres = ['Reino de la Fantasía', 'Cronicas del Reino', 'Leyendas y Mitos', 'Aventuras en la Tierra Media', 'Tierras Olvidadas', 'Los Reinos de Hierro', 'Mundos de la Magia']
        return random.choice(lista_nombres)

    def generar_introduccion(self):
        return f'Bienvenidos a {self.nombre_juego}, un mundo de fantasía lleno de peligros y aventuras. En este mundo, podrás elegir entre diferentes razas, cada una con sus habilidades y debilidades, y explorar las diversas zonas del reino, cada una con sus propios desafíos. Prepárate para sumergirte en una historia llena de magia, batallas épicas y misterios por resolver. ¡Que comience la aventura!'
     
    def crear_personaje(self):
        # Inicializamos la variable que usaremos para comprobar si la suma de la fuerza, destreza e inteligencia es igual a 15
        suma_atributos = 0

        # Obtener las razas y zonas disponibles
        razas_disponibles = [str(raza["id"]) for raza in self.razas]
        zonas_disponibles = [str(zona["id"]) for zona in self.zonas]

        # Solicitamos al usuario que introduzca los datos necesarios para crear un personaje
        nombre = input("Introduce el nombre de tu personaje: ")
        # raza = input("Introduce la raza de tu personaje: ")
        # clase = input("Introduce la clase de tu personaje: ")
        # zona = input("Introduce la zona de incicio de tu personaje: ")

        # Solicitar la raza y la zona al usuario
        raza_id = input(f"Ingresa la raza ({', '.join(razas_disponibles)}): ")
        while raza_id not in razas_disponibles:
            raza_id = input(f"Raza inválida. Ingresa la raza ({', '.join(razas_disponibles)}): ")
        
        zona_id = input(f"Ingresa la zona ({', '.join(zonas_disponibles)}): ")
        while zona_id not in zonas_disponibles:
            zona_id = input(f"Zona inválida. Ingresa la zona ({', '.join(zonas_disponibles)}): ")

        while suma_atributos != 15:
            # Pedimos al usuario que introduzca los valores de fuerza, destreza e inteligencia
            fuerza = int(input("Introduce la fuerza de tu personaje (de 1 a 10): "))
            destreza = int(input("Introduce la destreza de tu personaje (de 1 a 10): "))
            inteligencia = int(input("Introduce la inteligencia de tu personaje (de 1 a 10): "))

            # Comprobamos si la suma de la fuerza, destreza e inteligencia es igual a 15
            suma_atributos = fuerza + destreza + inteligencia

            if suma_atributos != 15:
                if suma_atributos > 15:
                    print("La suma de los atributos es mayor que 15, te sobran", suma_atributos - 15, "puntos.")
                else:
                    print("La suma de los atributos es menor que 15, te faltan", 15 - suma_atributos, "puntos.")
                print("Por favor, vuelve a introducir los valores de fuerza, destreza e inteligencia.\n")

        
        return Personaje(nombre=nombre, raza=list(filter(lambda raza: str(raza["id"]) == raza_id, self.razas))[0], zona=list(filter(lambda zona: str(zona["id"]) == zona_id, self.zonas))[0], fuerza=fuerza, destreza=destreza, inteligencia=inteligencia)
    
    def pedirOpciones(self):
        razas_disponibles = [str(raza["nombre"]) for raza in self.razas]
        zonas_disponibles = [str(zona["nombre"]) for zona in self.zonas]
        text=f"""
            Soy {self.personaje.raza["nombre"]} me encuentro en {self.personaje.zona["nombre"]}, ¿Que puedo hacer?
            necesito que me des un json con opciones en este formato: {{"id": id, "Opcion":opcion, "tipo":tipo}}
            Donde los tipos validos son combate, explorar.
            contexto:
            "Estamos jugando a un juego de rol en un mundo inventado"
            "Existen las razas: {razas_disponibles}" 
            "Las zonas disponibles son: {zonas_disponibles}"
            "Los datos del protagonista son: {self.personaje}"
            """
        result=openai_process.getResultsOpenai(text)
        text = result['choices'][0]['text']

        #print(text.split("Respuesta: ")[-1])
        text = re.sub(r'\n', '', text)
        opciones = json.loads(text.split("Respuesta: ")[-1])

        # Recorrer la lista de opciones e imprimir el id y la opción
        for opcion in opciones:
            print(f"{opcion['id']}-{opcion['Opcion']}")


        opcion_encontrada = None

        # Pedir al usuario que seleccione una opción hasta que proporcione una opción válida
        while opcion_encontrada is None:
            opcion_seleccionada = input("Seleccione una opción por su id: ")
            
            # Buscar la opción seleccionada en la lista de opciones
            for opcion in opciones:
                if opcion['id'] == int(opcion_seleccionada):
                    opcion_encontrada = opcion
                    break
            
            # Si no se encuentra la opción, mostrar un mensaje de error
            if opcion_encontrada is None:
                print("Opción inválida")

        # Procesar la opción encontrada
        print(f"Ha seleccionado la opción {opcion_encontrada['Opcion']} de tipo {opcion_encontrada['tipo']}")


        request=f"""
        Elijo la opcion {opcion_encontrada['Opcion']} escribe una breve historia de que es lo que ha pasado  
        necesito que me des la respuesta en formato json {{"resultado":resultado, "objeto_encontrado": {{"nombre": nombre_objeto, "tipo_objeto": tipo_objeto}}}}
        El resultado tiene que ser que ha ocurrido al realizar la accion
        El objeto_encontrado puede venir vacio, en caso de que toque un objeto se debe de indicar el nombre en el resultado
        los tipos de objeto pueden ser armas, armaduras y consumibles
        """


        result=openai_process.getResultsOpenai(request)
        text = result['choices'][0]['text']

        #print(text.split("Respuesta: ")[-1])
        resultado = json.loads(text.split("Respuesta: ")[-1])
        print(resultado['resultado'])

