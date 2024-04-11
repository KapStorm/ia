import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Type

ValorType = Type[list[int]]

class Nodo:
    def __init__(self, estado: ValorType, padre: None, nivel: int):
        # Inicialización de un nodo en el árbol de búsqueda.
        self.estado = estado  
        self.padre = padre  
        self.nivel = nivel  

    def __str__(self) -> str:
        # Método para imprimir un nodo.
        return f"Nodo({self.estado}, {self.padre}, {self.nivel})"
    
def obtener_valores_padres(nodo: Nodo) -> list[ValorType]:
    # Función para obtener los valores de todos los nodos padres de un nodo dado.
    valores_padres = [nodo.estado]  # Inicialmente, agregamos el valor del nodo dado.
    padre_actual = nodo.padre
    while padre_actual:
        valores_padres.append(padre_actual.estado)  # Agregamos el valor del nodo padre.
        padre_actual = padre_actual.padre  # Movemos al nodo padre siguiente.
    return valores_padres[::-1]  # Invertimos la lista para obtener el orden correcto de los nodos padres.

def dibujar_tablero(algoritmo: str, tamanio_tablero: int, posiciones: list[ValorType]) -> None:
    # Función para visualizar animaciones del tablero con las posiciones de las reinas.
    fig, ax = plt.subplots()  
    fig.suptitle(f'{algoritmo} -  TABLERO N REINAS') 
    ax.set_title('Equipo - 6') 
    ax.set_xlim(0, tamanio_tablero)  # Establecer límites en el eje x.
    ax.set_ylim(0, tamanio_tablero) 
    ax.set_aspect('equal') 
    ax.set_xticks([])  # Ocultar las marcas del eje x.
    ax.set_yticks([])  
    
    # Dibujar el tablero con casillas alternadas de color blanco y gris.
    for i in range(tamanio_tablero):
        for j in range(tamanio_tablero):
            color = 'white' if (i + j) % 2 == 0 else 'gray'
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color))
    
    def actualizar(i, puntos=[]):
        # Función para actualizar el tablero en cada fotograma de la animación.
        if puntos:
            # Si hay puntos (posiciones anteriores de las reinas), eliminarlos antes de dibujar los nuevos.
            for punto in puntos:
                punto.remove()
            puntos.clear()
        
        if i < len(posiciones):
            # Si todavía hay posiciones por mostrar, dibujar las reinas en sus posiciones actuales.
            for j, i in enumerate(posiciones[i]):
                punto = ax.text(j + 0.5, i + 0.5, '♞', color='black', fontsize=40, ha='center', va='center')
                puntos.append(punto)  # Agregar el punto al registro de puntos para su eliminación posterior.
    
    # Crear una animación que llama a la función 'actualizar' para cada fotograma.
    animacion = FuncAnimation(fig, actualizar, frames=len(posiciones), fargs=([],), interval=1000, repeat=False)
    plt.show()  # Mostrar la animación.

