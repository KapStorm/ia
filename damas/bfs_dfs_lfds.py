import sys
from typing import Optional, Type

ValorType = Type[list[int]]

class Nodo:
    def __init__(self, valor: ValorType, padre: Optional['Nodo'], level: int):
        self.valor = valor
        self.padre = padre
        self.level = level

    def __str__(self) -> str:
        return f"Nodo({self.valor}, {self.padre}, {self.level})"

def god_test(tablero: Nodo) -> bool:
    ataques = 0
    len_tablero = len(tablero.valor)
    for i in range(len_tablero):
        for j in range(i + 1, len_tablero):
            if tablero.valor[i] == tablero.valor[j] or abs(tablero.valor[i] - tablero.valor[j]) == abs(j - i):
                ataques += 2
    return ataques == 0

def expand(nodo: Nodo) -> list[Nodo]:
    os = []
    longitud_valor = len(nodo.valor)
    for index in range(longitud_valor):
        if nodo.valor[index] < longitud_valor - 1:
            nuevo_valor = nodo.valor.copy()
            nuevo_valor[index] += 1
            os.append(Nodo(valor=nuevo_valor, padre=nodo,level = nodo.level))
    return os

def dfs(f: list[Nodo]) -> Optional[Nodo]:
    if not f:
        return None
    nodo = f.pop()
    if god_test(nodo):
        return nodo
    os = expand(nodo)
    f.extend(os)
    return dfs(f)


def bfs(f: list[Nodo]) -> Optional[Nodo]:
    if not f:
        return None
    nodo = f.pop()
    if god_test(nodo):
        return nodo
    os = expand(nodo)
    os.extend(f)
    return dfs(os)

def lfds(f:list[Nodo], limit: int) -> Optional[Nodo]:
    if not f:
        return None
    nodo = f.pop()
    nivel = nodo.level
    if god_test(nodo):
        return nodo
    if nivel < limit:
        os = expand(nodo)
        f.extend(os)    
    return lfds(f, limit) 

def main() -> None:
    tamanio_tablero = 4
    init = [Nodo([0 for _ in range(tamanio_tablero)], None, 0)]
    # TODO: en varios archivos


if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    main()