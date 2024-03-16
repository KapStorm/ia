import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Type, Optional

ValorType = Type[list[int]]

class Nodo:
    def __init__(self, valor: ValorType, padre: Optional['Nodo'], level: int):
        self.valor = valor
        self.padre = padre
        self.level = level

    def __str__(self) -> str:
        return f"Nodo({self.valor}, {self.padre}, {self.level})"
    
def obtener_valores_padres(nodo: Nodo) -> list[ValorType]:
    valores_padres = [nodo.valor]
    padre_actual = nodo.padre
    while padre_actual:
        valores_padres.append(padre_actual.valor)
        padre_actual = padre_actual.padre
    return valores_padres[::-1]

def dibujar_tablero(algoritmo: str, tamanio_tablero: int, posiciones: list[ValorType]) -> None:
    fig, ax = plt.subplots()
    fig.suptitle(f'{algoritmo} - Problema de las N reinas')
    ax.set_title('Solución')
    ax.set_xlim(0, tamanio_tablero)
    ax.set_ylim(0, tamanio_tablero)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Dibujar el tablero
    for i in range(tamanio_tablero):
        for j in range(tamanio_tablero):
            color = 'white' if (i + j) % 2 == 0 else 'black'
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color))
    
    def actualizar(i, puntos=[]):
        if puntos:
            for punto in puntos:
                punto.remove()
            puntos.clear()
        
        if i < len(posiciones):
            for j, i in enumerate(posiciones[i]):
                punto = ax.text(j + 0.5, i + 0.5, '♕', color='red', fontsize=40, ha='center', va='center')
                puntos.append(punto)
    
    a = FuncAnimation(fig, actualizar, frames=len(posiciones), fargs=([],), interval=1000, repeat=False)
    plt.show()