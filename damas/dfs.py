import sys
from util import dibujar_tablero, Nodo, obtener_valores_padres
from typing import Optional

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
            os.append(Nodo(valor=nuevo_valor, padre=nodo,level = nodo.level + 1))
    return os

def dfs(f: list[Nodo]) -> Optional[Nodo]:
    if not f:
        return None
    nodo = f.pop(0)
    if god_test(nodo):
        return nodo
    os = expand(nodo)
    os.extend(f)
    return dfs(os)

def main() -> None:
    tamanio_tablero = 4
    init = [Nodo([0 for _ in range(tamanio_tablero)], None, 0)]
    dfs_res = dfs(init)
    dfs_res_values = obtener_valores_padres(dfs_res)
    print(f'DFS {dfs_res_values}')
    dibujar_tablero("DFS",tamanio_tablero, dfs_res_values)
    
if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    main()