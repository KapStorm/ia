import sys
from typing import Optional
from util import obtener_valores_padres, Nodo, animar_tablero


def calcular_distancia_manhattan(nodo: Nodo, numero: int) -> int:
    index = nodo.tablero.index(numero)
    index_target = nodo.target.index(numero)
    return abs(index % 3 - index_target % 3) + abs(index // 3 - index_target // 3)


def goal_test(nodo: Nodo) -> bool:
    return nodo.tablero == nodo.target


def expand(nodo: Nodo) -> list[Nodo]:
    def mover_espacio(index: int, nuevo_index: int) -> Nodo:
        nuevo_tablero = Nodo(tablero=nodo.tablero.copy(), padre=nodo, level=nodo.level + 1, target=nodo.target, es_inverso=nodo.es_inverso)
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
        if nodo.es_inverso:
            cadena = f"{cadena}\n{nodo.tablero}"
        else:
            cadena = f"{nodo.tablero}\n{cadena}"
        nodo = nodo.padre
    print(f"Solución encontrada:\n{nodo.tablero}\n{cadena}")

if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    tablero = [7, 4, 3, 8, 1, 5, 0, 2, 6]
    tablero_fin = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    f = [
        Nodo(tablero=tablero_fin.copy(), padre=None, level=0, target=tablero.copy(), es_inverso=True),
        Nodo(tablero=tablero.copy(), padre=None, level=0, target=tablero_fin.copy(), es_inverso=False)
    ]
    res = a_estrella(f)
    res_values = obtener_valores_padres(res)
    if res:
        print("Solución encontrada!")
        print("Pasos necesarios:", len(res_values) - 1)
        animar_tablero(res_values)
    else:
        print("Solución no encontrada")
