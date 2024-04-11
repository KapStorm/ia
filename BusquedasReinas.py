import sys
from graficar import dibujar_tablero, Nodo, obtener_valores_padres
from typing import Type

ValorType = Type[list[int]]


def BFS(F: list[Nodo]):  # Breff First Search (Anchura)
    OS: list[Nodo] = []
    if not F:
        return None
    else:
        EA = F.pop(0)
        if (goalTest(EA) == 0):
            return EA
        else:
            OS = expand(EA)
            OS.extend(F)
            return BFS(OS)


def DFS(F: list[Nodo]):  # Deep First Search(Profundidad)
    if not F:
        return False
    else:
        EA = F.pop(0)
        if (goalTest(EA) == 0):
            return EA
        else:
            F[0:0] = expand(EA)  # Slicing yo quiero de la posicion 0 a la 0
            # obtener los valores y remplazarlos por el operando(F) que esta en el otro lado
            return DFS(F)


def LDFS(F: list[Nodo], limite: int):  # Limited Deep First Search
    if not F:
        return False
    else:
        EA = F.pop(0)
        if (goalTest(EA) == 0):
            return EA
    if (EA.nivel < limite):
        F[0:0] = expand(EA)
        return LDFS(F, limite)
    else:
        return EA


def ILDFS(F: list[Nodo], limite: int):  # Iterative Deep First Search
    while True:
        resultado = LDFS(F, limite)
        if (not resultado):
            limite + 1
            return ILDFS(F, limite)
        else:
            break


def GS(F: list[Nodo]):  # Greedy Search (busqueda voraz)
    if not F:
        return False
    else:
        EA = F.pop(0)
        if (goalTest(EA) == 0):
            return EA
        else:
            OS = expand2(EA)
            return GS([evaluate(OS)])


def expand(EA: Nodo) -> list[Nodo]:
    OS: list[Nodo] = []
    for i in range(len(EA.estado)):
        if (EA.estado[i] < len(EA.estado)-1):
            aux = Nodo(EA.estado.copy(), EA, nivel=EA.nivel + 1)
            aux.estado[i] += 1
            OS.append(aux)

    return OS


def expand2(EA: Nodo) -> list[Nodo]:
    OS: list[Nodo] = []
    for i in range(len(EA.estado)):
        for j in range(len(EA.estado)):
            # Validamos si existe una reina en esa posicion para no tomarla en cuenta
            if (EA.estado[i] != j):
                aux = EA.estado.copy()
                aux[i] = j
                OS.append(Nodo(aux, EA, nivel=EA.nivel + 1))

    return OS  # retorno todos los demas hijos


def evaluate(hijos: list[Nodo]) -> Nodo:

    mejor_hijo = sorted([(goalTest(hijo), hijo) for hijo in hijos])[0]

    return Nodo(mejor_hijo[1])


def goalTest(EA: Nodo) -> int:
    reinas = EA.estado
    n = len(reinas)
    ataques = 0
    for i in range(n - 1):  # Iterar sobre las reinas
        for j in range(i + 1, n):  # Iterar sobre las reinas restantes
            if reinas[i] == reinas[j] or abs(reinas[i] - reinas[j]) == abs(i - j):
                ataques += 2

    return ataques


def main() -> None:
    tamanio_tablero = 4
    estado_inicial = [Nodo([0 for _ in range(tamanio_tablero)], None, 0)]
    nodo_Win = BFS(estado_inicial)
    if nodo_Win:
        nodo_Win_values = obtener_valores_padres(nodo_Win)
        print(f'BFS {nodo_Win_values}')
        dibujar_tablero("BFS", tamanio_tablero, nodo_Win_values)
    else:
        print("No se encontró solución para el problema de las N reinas.")


if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    main()
