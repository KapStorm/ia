import sys
from typing import Optional, Type

ValorType = Type[list[int]]
#Este aun no jala
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
    expanded_nodes: list[Nodo] = []

    longitud_valor = len(nodo.valor)
    for i in range(longitud_valor):   
        for j in range(longitud_valor):
            if j != nodo.valor[i]:
                nuevo_valor = nodo.valor.copy()
                nuevo_valor[i] = j
                expanded_nodes.append(Nodo(valor=nuevo_valor, padre=nodo, level=nodo.level + 1))
    return expanded_nodes

def evaluate(nodos: list[Nodo]) -> Nodo:
    menores = sorted ([n for n in nodos if god_test(n)], key=lambda x: x.level)
    return menores[0]

def gs(f:list[Nodo]) -> Optional[Nodo]:
    if len(f) == 0:
        return None
    ea = f.pop()

    if god_test(ea):
        return ea
    hijos = expand(ea)
    mejor_hijo = evaluate(hijos)
    return gs(mejor_hijo)

def main() -> None:
    tamanio_tablero = 4
    init = [Nodo([0 for _ in range(tamanio_tablero)], None, 0)]
    gs_res = gs(init)
    print(f'GS {gs_res}')
    
if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    main()


