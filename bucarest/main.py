import copy
import os
import sys
import csv
from typing import Optional


dir_path = os.path.dirname(os.path.realpath(__file__))


class Ciudad:
    def __init__(self, nombre: str, valor: int, padre: Optional['Ciudad'] = None) -> None:
        self.nombre = nombre
        self.valor = valor
        self.padre = padre


class Camino:
    def __init__(self, ciudad1: str, ciudad2: str, valor: int) -> None:
        self.ciudad1 = ciudad1
        self.ciudad2 = ciudad2
        self.valor = valor


def leer_ciudades(ruta=f'{dir_path}/ciudades.csv') -> list[Ciudad]:
    with open(ruta, 'r') as file:
        reader = csv.DictReader(file)
        return [Ciudad(nombre=line['nombre'], valor=int(line['valor'])) for line in reader]


def leer_caminos(ruta=f'{dir_path}/caminos.csv') -> list[Camino]:
    with open(ruta, 'r') as file:
        reader = csv.DictReader(file)
        return [Camino(ciudad1=line['ciudad1'], ciudad2=line['ciudad2'], valor=int(line['valor'])) for line in reader]


def a_estrella(f: list[Ciudad], ciudades: list[Ciudad], caminos: list[Camino]) -> Optional[Ciudad]:
    if not f:
        return None
    ea = f.pop(0)
    if goalTest(nodo=ea):
        return ea
    os = expand(nodo=ea, ciudades=ciudades, caminos=caminos)
    f.extend(os)
    f = evaluate(nodos=f, caminos=caminos)
    return a_estrella(f, ciudades=ciudades, caminos=caminos)


def expand(nodo: Ciudad, ciudades: list[Ciudad], caminos: list[Camino]) -> list[Ciudad]:
    os = []
    for camino in caminos:
        if nodo.nombre == camino.ciudad1:
            ciudad = encontrar_ciudad(
                nombre_ciudad=camino.ciudad2, ciudades=ciudades)
        elif nodo.nombre == camino.ciudad2:
            ciudad = encontrar_ciudad(
                nombre_ciudad=camino.ciudad1, ciudades=ciudades)
        else:
            continue
        nodo_copy = copy.deepcopy(nodo)
        ciudad.padre = nodo_copy
        os.append(ciudad)
    return os


def encontrar_ciudad(nombre_ciudad: str, ciudades: list[Ciudad]) -> Ciudad:
    for ciudad in ciudades:
        if ciudad.nombre == nombre_ciudad:
            return ciudad


def obtener_gx(nodo: Ciudad, caminos: list[Camino]) -> int:
    contador = 0
    while nodo.padre:
        for camino in caminos:
            if nodo.nombre == camino.ciudad1 and nodo.padre.nombre == camino.ciudad2\
                    or nodo.nombre == camino.ciudad2 and nodo.padre.nombre == camino.ciudad1:
                contador += camino.valor
                nodo = nodo.padre
                break
    return contador


def evaluate(nodos: list[Ciudad], caminos: list[Camino]) -> list[Ciudad]:
    class Tupla:
        def __init__(self, nodo: Ciudad, fx: int) -> None:
            self.nodo = nodo
            self.fx = fx

    nodos_evaluados: list[Tupla] = []
    for nodo in nodos:
        hx = nodo.valor
        gx = obtener_gx(nodo=nodo, caminos=caminos)
        if nodo.valor == 0:
            return [nodo]
        fx = gx + hx
        nodos_evaluados.append(Tupla(nodo=nodo, fx=fx))
    nodos_evaluados.sort(key=lambda nodo: nodo.fx)
    return [nodo.nodo for nodo in nodos_evaluados]


def goalTest(nodo: Ciudad) -> bool:
    return nodo.valor == 0


def imprimir_recorrido(nodo: Ciudad) -> None:
    cadena = f'{nodo.nombre}'
    while nodo.padre:
        nodo = nodo.padre
        cadena = f'{nodo.nombre} -> {cadena}'
    print(cadena)


def main() -> None:
    ciudades = leer_ciudades()
    caminos = leer_caminos()
    arad = encontrar_ciudad('Arad', ciudades)
    f = [arad]
    resultado = a_estrella(f, ciudades, caminos)
    if resultado:
        imprimir_recorrido(resultado)
    else:
        print('No se encontró solución')


if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    main()
