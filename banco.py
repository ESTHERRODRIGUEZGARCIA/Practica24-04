'''Un banco necesita controlar el acceso a cuentas bancarias y para ello desea hacer un programa de prueba en python
(unitt test, dock test o mock test) que permita lanzar procesos que ingresen y retiren dinero a la vez y comprobar así si el resultado final es el esperado.

Se parte de una cuenta con 100 euros y se pueden tener procesos que ingresen 100 euros, 50 o 20.
También se pueden tener procesos que retiran 100, 50 o 20 euros euros. Se desean tener los siguientes procesos:

40 procesos que ingresan 100
20 procesos que ingresan 50
60 que ingresen 20.
De la misma manera se desean lo siguientes procesos que retiran cantidades.
40 procesos que retiran 100
20 procesos que retiran 50
60 que retiran 20.
Se desea comprobar que tras la ejecución la cuenta tiene exactamente 100 euros, que era la cantidad de la que se disponía al principio.

'''

import unittest
import threading
import time

class CuentaBancaria:
    def __init__(self):
        self.saldo = 100

    def ingresar(self, cantidad):
        self.saldo += cantidad

    def retirar(self, cantidad):
        self.saldo -= cantidad

    def getSaldo(self):
        return self.saldo

class TestCuentaBancaria(unittest.TestCase):
    def test_cuenta(self):
        cuenta = CuentaBancaria()
        hilos = []
        for i in range(40):
            hilo = threading.Thread(target=cuenta.ingresar, args=(100,))
            hilos.append(hilo)
            hilo.start()
        for i in range(20):
            hilo = threading.Thread(target=cuenta.ingresar, args=(50,))
            hilos.append(hilo)
            hilo.start()
        for i in range(60):
            hilo = threading.Thread(target=cuenta.ingresar, args=(20,))
            hilos.append(hilo)
            hilo.start()
        for i in range(40):
            hilo = threading.Thread(target=cuenta.retirar, args=(100,))
            hilos.append(hilo)
            hilo.start()
        for i in range(20):
            hilo = threading.Thread(target=cuenta.retirar, args=(50,))
            hilos.append(hilo)
            hilo.start()
        for i in range(60):
            hilo = threading.Thread(target=cuenta.retirar, args=(20,))
            hilos.append(hilo)
            hilo.start()
        for hilo in hilos:
            hilo.join()
        self.assertEqual(cuenta.getSaldo(), 100)

if __name__ == '__main__':
    unittest.main()

