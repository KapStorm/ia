import copy
import sys


class Nodo:
    def __init__(self, nombre: str, valor: int) -> None:
        self.nombre = nombre
        self.valor = valor
        self.recorrido = []


    def __repr__(self):
        return f"{self.nombre} {self.valor} {self.recorrido}"
    

class Camino:
    def __init__(self,ciudad1: str, ciudad2: str, valor: int) -> None:
        self.ciudad1 = ciudad1
        self.ciudad2 = ciudad2
        self.valor = valor


    def __repr__(self):
        return f"{self.ciudad1} {self.ciudad2} {self.valor}"


def leer_ciudades(ruta = 'ciudades.csv') -> list[Nodo]:
    ciudades: list[Nodo] = []
    with open(ruta, 'r') as file:
        for line in file.readlines():
            nombre, valor = line.split(',')
            ciudades.append(Nodo(nombre=nombre, valor=int(valor)))
    return ciudades


def leer_caminos(ruta = 'caminos.csv') -> list[Camino]:
    caminos: list[Camino] = []
    with open(ruta,'r' ) as file:
        for line in file.readlines():
            ciudad1, ciudad2, valor = line.split(',')
            caminos.append(Camino(ciudad1=ciudad1, ciudad2=ciudad2, valor=int(valor)))
    return caminos


def A(F: list[Nodo]):
    if not F:
        return False
    EA = F.pop(0)
    if goalTest(EA):
        recorrido_nombres = [nodo.nombre for nodo in EA.recorrido]
        print(EA.nombre, EA.valor, recorrido_nombres)
        return True
    OS = expand(EA)
    F.extend(OS)
    OS = evaluate(OS)
    return A(F)


def expand(nodo: Nodo) -> list[Nodo]:
    OS = []
    ciudades = leer_ciudades()
    caminos = leer_caminos()
    for camino in caminos:
        if nodo.nombre == camino.ciudad1:
            ciudad = encontrar_ciudad(camino.ciudad2, ciudades)
        elif nodo.nombre == camino.ciudad2:
            ciudad = encontrar_ciudad(camino.ciudad1, ciudades)
        else:
            continue
        nodo_copy = copy.deepcopy(nodo)
        ciudad.recorrido = [nodo_copy] + nodo_copy.recorrido
        OS.append(ciudad)
    return OS


def encontrar_ciudad(nombre_ciudad: str, ciudades: list[Nodo]) -> Nodo:
  for ciudad in ciudades:
    if ciudad.nombre == nombre_ciudad:
      return ciudad


def obtener_gx(ciudad: Nodo, caminos: list[Camino]) -> int:
    recorrido = copy.deepcopy(ciudad.recorrido)
    contador = 0
    while recorrido:
        temp = recorrido.pop(0)        
        for camino in caminos:
            if ciudad.nombre == camino.ciudad1 and temp.nombre == camino.ciudad2\
                    or ciudad.nombre == camino.ciudad2 and temp.nombre == camino.ciudad1:
                contador += camino.valor
                ciudad = temp
                break
    return contador
      

def evaluate(nodos: list[Nodo]) -> list[Nodo]:
    caminos = leer_caminos()
    nodos_evaluados: list[tuple[Nodo, int]] = []
    for nodo in nodos:
        hx = nodo.valor
        gx = obtener_gx(nodo, caminos)
        fx = gx + hx
        nodos_evaluados.append((nodo, fx))
    nodos_evaluados.sort(key=lambda nodo: nodo[1])
    return [nodo[0] for nodo in nodos_evaluados]

  
def goalTest(EA: Nodo):
    return EA.valor == 0


def main() -> None:
    ciudades = leer_ciudades()
    arad = encontrar_ciudad('Arad', ciudades)
    F = [arad]
    A(F)


if __name__ == '__main__':
    sys.setrecursionlimit(1000000000)
    main()
