'''
Se desea simular los posibles beneficios de diversas estrategias de juego en un casino.
La ruleta francesa es un juego en el que hay una ruleta con 37 números (del 0 al 36).
Cada 3000 milisegundos el croupier saca un número al azar y los diversos hilos apuestan para ver si ganan.
Todos los hilos empiezan con 1.000 euros y la banca (que controla la ruleta) con 50.000. Cuando los jugadores pierden dinero, la banca incrementa su saldo.

Se puede jugar a un número concreto. Habrá 4 hilos que eligen números al azar del 1 al 36 (no el 0) y restarán 10 euros de su saldo para apostar a ese ese número.
Si sale su número su saldo se incrementa en 360 euros (36 veces lo apostado).

Se puede jugar a par/impar. Habrá 4 hilos que eligen al azar si apuestan a que saldrá un número par o un número impar.
Siempre restan 10 euros para apostar y si ganan incrementan su saldo en 20 euros.

Se puede jugar a la «martingala». Habrá 4 hilos que eligen números al azar. Elegirán un número y empezarán restando 10 euros de su saldo para apostar a ese número.
Si ganan incrementan su saldo en 360 euros. Si pierden jugarán el doble de su apuesta anterior (es decir, 20, luego 40, luego 80, y así sucesivamente)

La banca acepta todas las apuestas pero nunca paga más dinero del que tiene.

Si sale el 0, todo el mundo pierde y la banca se queda con todo el dinero.

'''

import random
import time


class Ruleta: # singleton
    def __init__(self):
        self.numero = 0

    def get_numero(self):
        return self.numero

    def lanzar(self):
        self.numero = random.randint(0, 36)
        time.sleep(0.001)

class Banca:
    def __init__(self):
        self.dinero = 50000

    def get_dinero(self):
        return self.dinero

    def incrementar_dinero(self, cantidad):
        self.dinero += cantidad

    def decrementar_dinero(self, cantidad):
        self.dinero -= cantidad

class Jugador: #se crea el jugador

    def __init__(self, nombre, dinero):
        self.nombre = nombre
        self.dinero = dinero

    def get_nombre(self):
        return self.nombre

    def get_dinero(self):
        return self.dinero

    def incrementar_dinero(self, cantidad):
        self.dinero += cantidad

    def decrementar_dinero(self, cantidad):
        self.dinero -= cantidad



class JugadorNumero(Jugador): #se crea el jugador numero i
    def __init__(self, nombre, dinero):
        super().__init__(nombre, dinero)

    def jugar(self, ruleta):
        numero = random.randint(1, 36)
        self.decrementar_dinero(10)
        if ruleta.get_numero() == numero:
            self.incrementar_dinero(360)

class JugadorParImpar(Jugador):
    def __init__(self, nombre, dinero):
        super().__init__(nombre, dinero)

    def jugar(self, ruleta):
        par_impar = random.randint(0, 1)
        self.decrementar_dinero(10)
        if par_impar == 0:
            if ruleta.get_numero() % 2 == 0:
                self.incrementar_dinero(20)
        else:
            if ruleta.get_numero() % 2 != 0:
                self.incrementar_dinero(20)

class JugadorMartingala(Jugador):
    def __init__(self, nombre, dinero): #se crea el jugador martingala
        super().__init__(nombre, dinero) #se llama al constructor de la clase padre
        self.apuesta = 10 #se crea la apuesta

    def jugar(self, ruleta):
        numero = random.randint(1, 36)
        self.decrementar_dinero(self.apuesta)
        if ruleta.get_numero() == numero:
            self.incrementar_dinero(360)
            self.apuesta = 10
        else:
            self.apuesta *= 2

def main(): #se crea la ruleta, la banca y los jugadores
    ruleta = Ruleta()
    banca = Banca()
    jugadores = []
    for i in range(4):
        jugadores.append(JugadorNumero("Jugador " + str(i), 1000))
    for i in range(4):
        jugadores.append(JugadorParImpar("Jugador " + str(i), 1000))
    for i in range(4):
        jugadores.append(JugadorMartingala("Jugador " + str(i), 1000))

    while banca.get_dinero() > 0: #se crea el bucle para que la banca no se quede sin dinero
        ruleta.lanzar()
        if ruleta.get_numero() != 0: #si sale el 0, todos los jugadores pierden
            for jugador in jugadores: #se crea el bucle para que los jugadores jueguen
                jugador.jugar(ruleta)
                if jugador.get_dinero() < 0: #si el jugador pierde, la banca gana
                    banca.incrementar_dinero(-jugador.get_dinero()) #se le resta el dinero al jugador
                    jugador.incrementar_dinero(jugador.get_dinero()) #se le suma el dinero al jugador
        else:
            break #si sale el 0, se acaba el juego

    for jugador in jugadores: #se crea el bucle para que se muestre el dinero de cada jugador
        print(jugador.get_nombre() + ": " + str(jugador.get_dinero())) #se muestra el dinero de cada jugador
        print("Apuesta: " + str(jugador.get_dinero() - 1000)) #se muestra la apuesta de cada jugador

    print("Banca: " + str(banca.get_dinero())) #se muestra el dinero de la banca


if __name__ == "__main__":
    main()
