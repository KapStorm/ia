import sys
import copy

class Nodo:
    def __init__(self, estado, padre=None, nivel=0):
        self.estado = estado  # Representación del estado actual
        self.padre = padre    # Referencia al nodo padre
        self.nivel = nivel    # Profundidad del nodo en el árbol de búsqueda
        self.costo = 0        # Costo actual (profundidad del nodo) g(x)
        self.heuristica = 0   # Heurística de distancia de Manhattan h(x)
    
    def __repr__(self):
        return f"{self.estado} {self.nivel} {self.costo} {self.heuristica}"

def goalTest(estado_actual):
    meta = [1,2,3,4,5,6,7,8,0]
    count = 0
    for fila in range(3):
        for columna in range(3):
            if estado_actual[fila][columna] != meta[fila * 3 + columna]:
                count += 1
    return count

def distancia_manhattan(estado_actual):
    meta = [1,2,3,4,5,6,7,8,0]
    distancia = 0
    for fila in range(3):
        for columna in range(3):
            valor = estado_actual[fila][columna]
            if valor != 0:
                fila_meta, col_meta = divmod(meta.index(valor), 3)
                distancia += abs(fila_meta - fila) + abs(col_meta - columna)
    return distancia

def evaluate(sucesores):
    for sucesor in sucesores:
        sucesor.costo = sucesor.nivel  # Costo actual (profundidad del nodo)
        sucesor.heuristica = distancia_manhattan(sucesor.estado)  # Heurística de distancia de Manhattan

def expand(nodo):
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movimientos posibles: derecha, izquierda, abajo, arriba
    sucesores = []
    # Encontrar la posición de la ficha vacía en el estado actual
    fila_vacia = col_vacia = -1
    for fila in range(3):
        for col in range(3):
            if nodo.estado[fila][col] == 0:
                fila_vacia, col_vacia = fila, col
                break
    # Generar los sucesores válidos
    for movimiento in movimientos:
        fila_nueva, col_nueva = fila_vacia + movimiento[0], col_vacia + movimiento[1]
        if 0 <= fila_nueva < 3 and 0 <= col_nueva < 3:      #verificar que no se salga del margen del tablero
            nuevo_estado = [fila[:] for fila in nodo.estado]  #utilizar slicing para copiar superficialmente la lista completa
            # intercambiar posiciones con la ficha vacía
            nuevo_estado[fila_vacia][col_vacia], nuevo_estado[fila_nueva][col_nueva] = nuevo_estado[fila_nueva][col_nueva], nuevo_estado[fila_vacia][col_vacia]
            sucesores.append(Nodo(nuevo_estado, nodo, nodo.nivel + 1)) # se crea un nodo nuevo para guardar el nuevo estado y lo agrega a la lista de sucesores
    return sucesores

def aEstrella(nodo_inicial):
    F = [nodo_inicial]  # Creamos una lista F que contendrá el nodo inicial
    while F:
        nodo_actual = F.pop(0)
        if goalTest(nodo_actual.estado) == 0:
            print("Se encontró la solución:", nodo_actual.estado)
            return nodo_actual
        sucesores = expand(nodo_actual)
        F.extend(sucesores)
        evaluate(F)
        F.sort(key=lambda x: x.costo + x.heuristica)  # Ordenar la lista de nodos por f(x)
    print("Solución no encontrada")

# Ejemplo de estado inicial
estado_inicial = [
    [7, 4, 3],
    [8, 1, 5],
    [0, 2, 6]
]

# Creamos un nodo inicial
nodo_inicial = Nodo(estado_inicial)

# Ejecutamos el algoritmo A*
res = aEstrella(nodo_inicial)
while res.padre:
    print(res.padre)
    res = res.padre