from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Nodo:
    def __init__(self, tablero: list[int], padre: Optional['Nodo'], level: int, target: list[int] = [], es_inverso: bool = False):
        self.tablero = tablero
        self.padre = padre
        self.level = level
        self.target = target
        self.es_inverso = es_inverso

    def __repr__(self) -> str:
        return f"Nodo({self.tablero}, {self.padre}, {self.level})"
    
def obtener_valores_padres(nodo: Nodo) -> list[int]:
    valores_padres = [nodo.tablero]
    padre_actual = nodo.padre
    while padre_actual:
        valores_padres.append(padre_actual.tablero)
        padre_actual = padre_actual.padre
    if nodo.es_inverso:
        return valores_padres
    else:
        return valores_padres[::-1]

def dibujar_tablero(tablero_values: list[int]) -> None:
    tablero = np.array(tablero_values).reshape(3, 3)
    for i in range(3):
        for j in range(3):
            plt.text(j, i, tablero[i, j], ha='center', va='center', fontsize=20, color='black' if tablero[i, j] != 0 else 'white')
    plt.imshow(tablero, cmap='viridis', interpolation='nearest')
    plt.axis('off')
    
def animar_tablero(tablero_values: list[int]) -> None:
    # Función de animación
    def update(frame):
        plt.clf()
        dibujar_tablero(tablero_values[frame])
        plt.title(f"Paso {frame + 1}")
        
    fig = plt.figure()
    animation = FuncAnimation(fig, update, frames=len(tablero_values), interval=1000, repeat=False)
    plt.show()    