import sys
from typing import Optional
from util import obtener_valores_padres, Nodo, animar_tablero


def calcular_distancia_manhattan(nodo: Nodo, numero: int) -> int:
    current_index = nodo.tablero.index(numero)
    if numero == 0:
        target_index = 8
    else:
        target_index = numero - 1
    pos_x_primero = current_index % 3
    pos_y_primero = int(current_index / 3)
    pos_x_segundo = target_index % 3
    pos_y_segundo = int(target_index / 3)
    return abs(pos_x_primero - pos_x_segundo) + abs(pos_y_primero - pos_y_segundo)


def goal_test(nodo: Nodo) -> bool:
    return (nodo) == 0


def mover_espacio(nodo: Nodo, index: int, nuevo_index: int) -> Nodo:
    nuevo_tablero = Nodo(tablero=nodo.tablero.copy(),
                         padre=nodo, level=nodo.level + 1)
    nuevo_tablero.tablero[index] = nuevo_tablero.tablero[nuevo_index]
    nuevo_tablero.tablero[nuevo_index] = 0
    return nuevo_tablero


def expand(nodo: Nodo) -> list[Nodo]:
    os = []
    longitud_tablero = len(nodo.tablero)
    for index in range(longitud_tablero):
        if nodo.tablero[index] == 0:
            # Checar si se puede expandir a la derecha
            if index % 3 > 0:
                os.append(mover_espacio(nodo, index, index - 1))
            # Checar si se puede expandir a la izquierda
            if index % 3 < 2:
                os.append(mover_espacio(nodo, index, index + 1))
            # Checar si se puede expandir hacia arriba
            if index > 2:
                os.append(mover_espacio(nodo, index, index - 3))
            # Checar si se puede expandir a abajo
            if index < 6:
                os.append(mover_espacio(nodo, index, index + 3))
            break
    return os


def calcular_hx(nodo: Nodo) -> int:
    return sum([
        calcular_distancia_manhattan(nodo, 1),
        calcular_distancia_manhattan(nodo, 2),
        calcular_distancia_manhattan(nodo, 3),
        calcular_distancia_manhattan(nodo, 4),
        calcular_distancia_manhattan(nodo, 5),
        calcular_distancia_manhattan(nodo, 6),
        calcular_distancia_manhattan(nodo, 7),
        calcular_distancia_manhattan(nodo, 8)
    ])


def evaluate(nodos: list[Nodo]) -> list[Nodo]:
    class Tupla:
        def __init__(self, nodo: Nodo, fx: int) -> None:
            self.nodo = nodo
            self.fx = fx

    nodos_evaluados: list[Tupla] = []
    for nodo in nodos:
        hx = calcular_hx(nodo)
        fx = nodo.level + hx
        nodos_evaluados.append(Tupla(nodo=nodo, fx=fx))
    nodos_evaluados.sort(key=lambda nodo: nodo.fx)
    return [nodo.nodo for nodo in nodos_evaluados]


def a_estrella(f: list[Nodo]) -> Optional[Nodo]:
    if not f:
        return None
    # Es para sacar el fx de todos y ordernalos al a vez
    f.sort(key=lambda nodo: nodo.level + calcular_hx(nodo))
    nodo = f.pop(0)
    if goal_test(nodo):
        return nodo
    os = expand(nodo)
    f.extend(os)
    return a_estrella(f)


def imprimir_recorrido(nodo: Nodo) -> None:
    cadena = ""
    while nodo.padre:
        cadena = f"{nodo.tablero}\n{cadena}"
        nodo = nodo.padre
    print(f"Solución encontrada:\n{nodo.tablero}\n{cadena}")


if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    tablero = [7, 4, 3, 8, 1, 5, 0, 2, 6]
    nodo_inicial = Nodo(tablero, None, 0)
    f = [nodo_inicial]
    res = a_estrella(f)
    res_values = obtener_valores_padres(res)
    if res:
        print("Solución encontrada!")
        print("Pasos necesarios:", len(res_values) - 1)
        animar_tablero(res_values)
    else:
        print("Solución no encontrada")
