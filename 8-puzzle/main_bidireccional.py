import sys
from typing import Optional
from util import obtener_valores_padres, Nodo, animar_tablero


def expand(nodo: Nodo, blacklist: list[Nodo]) -> list[Nodo]:
    def mover_espacio(index: int, nuevo_index: int) -> Nodo:
        nuevo_tablero = Nodo(tablero=nodo.tablero.copy(), padre=nodo, level=nodo.level + 1)
        nuevo_tablero.tablero[index] = nuevo_tablero.tablero[nuevo_index]
        nuevo_tablero.tablero[nuevo_index] = 0
        if not nuevo_tablero.tablero in [x.tablero for x in blacklist]:
            os.append(nuevo_tablero)

    os = []
    longitud_tablero = len(nodo.tablero)
    for index in range(longitud_tablero):
        if nodo.tablero[index] == 0:
            if index % 3 > 0:
                mover_espacio(index, index - 1)
            if index % 3 < 2:
                mover_espacio(index, index + 1)
            if index > 2:
                mover_espacio(index, index - 3)
            if index < 6:
                mover_espacio(index, index + 3)
            break
    return os


def goal_test(nodo: Nodo, blacklist_opuesto: list[Nodo]) -> Optional[tuple[Nodo, Nodo]]:
    for blacklist_nodo in blacklist_opuesto:
        if nodo.tablero == blacklist_nodo.tablero:
            return nodo, blacklist_nodo
    return None


def bfs(f_inicio: list[Nodo], f_final: list[Nodo], blacklist_inicio: list[Nodo], blacklist_final: list[Nodo]) -> Optional[tuple[Nodo, Nodo]]:
    if not f_inicio and not f_final:
        return None
    if f_inicio:
        nodo = f_inicio.pop(0)
        goal_test_inicio = goal_test(nodo, blacklist_final)
        if goal_test_inicio:
            return goal_test_inicio
        blacklist_inicio.append(nodo)
        os = expand(nodo, blacklist_final)
        f_inicio.extend(os)
    if f_final:
        nodo = f_final.pop(0)
        goal_test_final = goal_test(nodo, blacklist_inicio)
        if goal_test_final:
            return goal_test_final
        blacklist_final.append(nodo)
        os = expand(nodo, blacklist_inicio)
        f_final.extend(os)
    return bfs(f_inicio, f_final, blacklist_inicio, blacklist_final)


def recorrido_en_un_nodo(nodo_uno: Nodo, nodo_dos: Nodo) -> list[list[int]]:
    valores_padres_uno = obtener_valores_padres(nodo_uno)
    valores_padres_dos = obtener_valores_padres(nodo_dos)
    if valores_padres_uno[0] == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
        valores_padres_uno.pop()
        return valores_padres_dos + valores_padres_uno[::-1]
    else:
        valores_padres_dos.pop()
        return valores_padres_uno + valores_padres_dos[::-1]



if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    tablero_inicio = Nodo(tablero=[7, 4, 3, 8, 1, 5, 0, 2, 6], padre=None, level=0)
    tablero_final = Nodo(tablero=[1, 2, 3, 4, 5, 6, 7, 8, 0], padre=None, level=0)
    res = bfs(f_inicio=[tablero_inicio], f_final=[tablero_final], blacklist_inicio=[], blacklist_final=[])
    if res:
        a, b = res
        recorrido = recorrido_en_un_nodo(a, b)
        animar_tablero(recorrido)
    else:
        print("Solución no encontrada")
