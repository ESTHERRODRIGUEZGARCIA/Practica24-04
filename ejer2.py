import random
import time
import threading

class Ruleta:
    def _init_(self):
        self.numero = 0

    def get_numero(self):
        return self.numero

    def lanzar(self):
        self.numero = random.randint(0, 36)
        time.sleep(0.001)

class Banca:
    def _init_(self):
        self.dinero = 50000
        self.lock = threading.Lock()

    def get_dinero(self):
        return self.dinero

    def incrementar_dinero(self, cantidad):
        with self.lock:
            self.dinero += cantidad

    def decrementar_dinero(self, cantidad):
        with self.lock:
            self.dinero -= cantidad

class Jugador:
    def _init_(self, nombre, dinero):
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

class JugadorNumero(Jugador):
    def _init_(self, nombre, dinero):
        super()._init_(nombre, dinero)

    def jugar(self, ruleta, banca):
        numero = random.randint(1, 36)
        self.decrementar_dinero(10)
        if ruleta.get_numero() == numero:
            self.incrementar_dinero(360)
        else:
            banca.incrementar_dinero(10)

class JugadorParImpar(Jugador):
    def _init_(self, nombre, dinero):
        super()._init_(nombre, dinero)

    def jugar(self, ruleta, banca):
        par_impar = random.randint(0, 1)
        self.decrementar_dinero(10)
        if par_impar == 0:
            if ruleta.get_numero() % 2 == 0:
                self.incrementar_dinero(20)
            else:
                banca.incrementar_dinero(10)
        else:
            if ruleta.get_numero() % 2 != 0:
                self.incrementar_dinero(20)
            else:
                banca.incrementar_dinero(10)

class JugadorMartingala(Jugador):
    def _init_(self, nombre, dinero):
        super()._init_(nombre, dinero)
        self.apuesta = 10

    def jugar(self, ruleta, banca):
        numero = random.randint(1, 36)
        self.decrementar_dinero(self.apuesta)
        if ruleta.get_numero() == numero:
            self.incrementar_dinero(360)
            self.apuesta = 10
        else:
            self.apuesta *= 2


class JugadaThread(threading.Thread):
    def _init_(self, jugador, ruleta):
        super()._init_()
        self.jugador = jugador
        self.ruleta = ruleta

    def run(self):
        self.jugador.jugar(self.ruleta)

def main():
    ruleta = Ruleta()
    banca = Banca()
    jugadores = []
    for i in range(4):
        jugadores.append(JugadorNumero("Jugador " + str(i), 1000))
    for i in range(4):
        jugadores.append(JugadorParImpar("Jugador " + str(i), 1000))
    for i in range(4):
        jugadores.append(JugadorMartingala("Jugador " + str(i), 1000))

    threads = []
    for jugador in jugadores:
        thread = threading.Thread(target=jugador.jugar, args=(ruleta,))
        threads.append(thread)

    while banca.get_dinero() > 0: #se crea el bucle para que la banca no se quede sin dinero
        ruleta.lanzar()
        if ruleta.get_numero() != 0: #si sale el 0, todos los jugadores pierden
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            threads = []
            for jugador in jugadores:
                if jugador.get_dinero() < 0: #si el jugador pierde, la banca gana
                    banca.incrementar_dinero(-jugador.get_dinero()) #se le resta el dinero al jugador
                    jugador.incrementar_dinero(jugador.get_dinero()) #se le suma el dinero al jugador
        else:
            break #si sale el 0, se acaba el juego

    for jugador in jugadores: #se crea el bucle para que se muestre el dinero de cada jugador
        print(jugador.get_nombre() + ": " + str(jugador.get_dinero())) #se muestra el dinero de cada jugador
        print("Apuesta: " + str(jugador.get_dinero() - 1000)) #se muestra la apuesta de cada jugador

    print("Banca: " + str(banca.get_dinero())) #se muestra el dinero de la banca


if __name__ == "_main_" :
    main()