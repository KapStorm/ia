import sys
from typing import Optional


class Nodo:
    def __init__(self, tablero: list[int], padre: Optional['Nodo'], level: int):
        self.tablero = tablero
        self.padre = padre
        self.level = level

    def __repr__(self) -> str:
        return f"Nodo({self.tablero}, {self.padre}, {self.level})"


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
    return nodo.tablero == [1, 2, 3, 4, 5, 6, 7, 8, 0]


def expand(nodo: Nodo) -> list[Nodo]:
    def mover_espacio(index: int, nuevo_index: int) -> Nodo:
        nuevo_tablero = Nodo(tablero=nodo.tablero.copy(), padre=nodo, level=nodo.level + 1)
        nuevo_tablero.tablero[index] = nuevo_tablero.tablero[nuevo_index]
        nuevo_tablero.tablero[nuevo_index] = 0
        return nuevo_tablero

    os = []
    longitud_tablero = len(nodo.tablero)
    for index in range(longitud_tablero):
        if nodo.tablero[index] == 0:
            if index % 3 > 0:
                os.append(mover_espacio(index, index - 1))
            if index % 3 < 2:
                os.append(mover_espacio(index, index + 1))
            if index > 2:
                os.append(mover_espacio(index, index - 3))
            if index < 6:
                os.append(mover_espacio(index, index + 3))
            break
    return os


def evaluate(nodo: Nodo) -> int:
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


def a_estrella(f: list[Nodo]) -> Optional[Nodo]:
    if not f:
        return None
    f.sort(key=lambda x: x.level + evaluate(x))
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
    res = a_estrella([nodo_inicial])
    if res:
        imprimir_recorrido(res)
    else:
        print("Solución no encontrada")
