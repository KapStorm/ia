import math
from random import randint
import random

path_to_follow: list[tuple[int, int]] = [
    (1, 8),
    (8, 1),
    (1, 4),
    (4, 5),
    (5, 3),
    (3, 4),
    (4, 3),
    (3, 1),
    (1, 9),
    (9, 1),
    (1, 3),
    (3, 1),
    (1, 10)
]

table = [
    11, 0, 0, 0,
    0, 0, 0, 0,
    9, 0, 0, 10,
    8, 0, 0, 0
]

values_name = {
    1: "E. Trabajo",
    2: "Destrozadora",
    3: "Sierra Cinta",
    4: "Canteadora",
    5: "Cepillo",
    6: "Trompo",
    7: "Esclopeadora",
    8: "Mat. Prima",
    9: "Triplay",
    10: "Almacen",
    11: "Banio",
    0: "Vacio"
}


def create_table() -> list[int]:
    def add_value(table: list[int], value: int) -> None:
        random = randint(0, len(table) - 1)
        if table[random] == 0:
            table[random] = value
        else:
            add_value(table, value)

    new_table = table.copy()
    for i in range(7):
        add_value(new_table, i + 1)
    return new_table


def fitness(individue: list[int]) -> int:
    distance = 0
    for (start, end) in path_to_follow:
        start_x_pos = individue.index(start) % 4 * 2 - 1
        start_y_pos = individue.index(start) // 4 * 2 - 1
        end_x_pos = individue.index(end) % 4 * 2 - 1
        end_y_pos = individue.index(end) // 4 * 2 - 1
        distance += math.sqrt((end_x_pos - start_x_pos) **
                              2 + (end_y_pos - start_y_pos) ** 2)
    return distance * 2


def mutate(individue: list[int], mutation_probability: float) -> list[int]:
    def next_index(table: list[int], number: int) -> int:
        random = randint(0, len(table) - 1)
        if table[random] == number or new_individue[random] >= 8:
            return next_index(table, number)
        else:
            return random

    new_individue = individue.copy()
    for i in range(len(new_individue)):
        if new_individue[i] < 8 and random.random() < mutation_probability:
            new_index = next_index(new_individue, i)
            new_individue[i], new_individue[new_index] = new_individue[new_index], new_individue[i]
    return new_individue


def main() -> None:
    pobation_size = 10
    generations = 100
    poblation = [create_table() for _ in range(pobation_size)]
    for generation in range(generations):
        print(f"Generation: {generation}")
        print(poblation)
        poblation.sort(key=fitness)
        new_poblation = poblation[:2]
        for p in poblation[2:]:
            new_poblation.append(mutate(p, 0.2))
        poblation = new_poblation
        best = poblation[0]
        print(f'Best: {best}')
        print(f'Fitness: {fitness(best)}')
        print()
    print(fitness(poblation[0]))


if __name__ == "__main__":
    main()
