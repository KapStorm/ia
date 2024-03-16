import sys
from typing import Optional
from util import dibujar_tablero, Nodo, obtener_valores_padres

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

def ldfs(f:list[Nodo], limit: int) -> Optional[Nodo]:
    if not f:
        return None
    nodo = f.pop(0)
    nivel = nodo.level
    if god_test(nodo):
        return nodo
    if nivel < limit:
        os = expand(nodo)
        os.extend(f)
        return ldfs(os, limit)   
    return ldfs(f, limit) 

def main() -> None:
    tamanio_tablero = 4
    init = [Nodo([0 for _ in range(tamanio_tablero)], None, 0)]
    lfds_res = ldfs(init, 6)
    if lfds_res is not None:
        ldfs_res_values = obtener_valores_padres(lfds_res)
        print(f'LDFS {ldfs_res_values}')
        dibujar_tablero("LDFS",tamanio_tablero, ldfs_res_values)
    
if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    main()