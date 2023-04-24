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
from multiprocessing import Pool

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
        self.assertEqual(cuenta.getSaldo(), 100)

        def ingreso(cantidad):
            cuenta.ingresar(cantidad)

        def retiro(cantidad):
            cuenta.retirar(cantidad)

        pool = Pool(10)
        pool.map(ingreso, [100, 50, 20])
        pool.map(retiro, [100, 50, 20])
        pool.close()
        pool.join()

        self.assertEqual(cuenta.getSaldo(), 100)

if __name__ == '__main__':
    unittest.main()
    