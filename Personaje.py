class Personaje:
    def __init__(self, nombre=None, raza=None, clase=None, fuerza=None, destreza=None, inteligencia=None, zona=None, vida=100):
        if nombre is None:
            personaje = self.crear_personaje()
            self.nombre = personaje["nombre"]
            self.raza = personaje["raza"]
            self.clase = personaje["clase"]
            self.fuerza = personaje["fuerza"]
            self.destreza = personaje["destreza"]
            self.inteligencia = personaje["inteligencia"]
            self.zona = personaje["zona"]
        else:
            self.nombre = nombre
            self.raza = raza
            self.clase = clase
            self.fuerza = fuerza
            self.destreza = destreza
            self.inteligencia = inteligencia
            self.zona = zona
        self.vida = vida

    def crear_personaje(self,razas,zonas):
        # Inicializamos la variable que usaremos para comprobar si la suma de la fuerza, destreza e inteligencia es igual a 15
        suma_atributos = 0

        # Obtener las razas y zonas disponibles
        razas_disponibles = [raza["id"] for raza in razas]
        zonas_disponibles = [zona["id"] for zona in zonas]
    

    

        # Solicitamos al usuario que introduzca los datos necesarios para crear un personaje
        nombre = input("Introduce el nombre de tu personaje: ")
        # raza = input("Introduce la raza de tu personaje: ")
        # clase = input("Introduce la clase de tu personaje: ")
        # zona = input("Introduce la zona de incicio de tu personaje: ")

        # Solicitar la raza y la zona al usuario
        raza = input(f"Ingresa la raza ({', '.join(razas_disponibles)}): ")
        while raza not in razas_disponibles:
            raza = input(f"Raza inválida. Ingresa la raza ({', '.join(razas_disponibles)}): ")
        
        zona = input(f"Ingresa la zona ({', '.join(zonas_disponibles)}): ")
        while zona not in zonas_disponibles:
            zona = input(f"Zona inválida. Ingresa la zona ({', '.join(zonas_disponibles)}): ")

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

        # Creamos un diccionario con los datos introducidos por el usuario
        personaje = {"nombre": nombre,
                     "raza": raza,
                     "clase": "",
                     "fuerza": fuerza,
                     "destreza": destreza,
                     "inteligencia": inteligencia,
                     "zona":zona,
                     "vida": 100}

        # Devolvemos el diccionario con los datos del personaje
        return personaje
    
    def __str__(self):
        return f"Nombre: {self.nombre}\nRaza: {self.raza}\nFuerza: {self.fuerza}\nDestreza: {self.destreza}\nInteligencia: {self.inteligencia}\nZona: {self.zona}"

