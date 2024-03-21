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
        start_x_pos = individue.index(start) % 4 + 0.5
        start_y_pos = individue.index(start) // 4 + 0.5
        end_x_pos = individue.index(end) % 4 + 0.5
        end_y_pos = individue.index(end) // 4 + 0.5
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


def initialization(poblation_size: int) -> list[list[int]]:
    return [create_table() for _ in range(poblation_size)]


def selection(poblation: list[list[int]], fathers_to_select: int) -> list[list[int]]:
    poblation.sort(key=fitness)
    return poblation[:fathers_to_select]


def crossover(candidates: list[list[int]]) -> list[int]:
    new_individual = candidates[0].copy()
    for number in range(1, 9):  # Cambiado a 9 para incluir el 8
        random_candidate = random.choice(candidates)
        random_candidate_number_index = random_candidate.index(number)
        new_individual_number_index = new_individual.index(number)
        if random_candidate_number_index == new_individual_number_index:
            continue
        new_individual[random_candidate_number_index], new_individual[new_individual_number_index] = \
            new_individual[new_individual_number_index], new_individual[random_candidate_number_index]
    return new_individual


def mutation(candidate: list[int], poblation_size: int) -> list[list[int]]:
    new_poblation = []
    while len(new_poblation) < poblation_size:
        new_poblation.append(mutate(candidate, 0.3))
    return new_poblation


def main() -> None:
    poblation_size = 10
    generations = 200
    poblation = initialization(poblation_size)
    for generation in range(generations):
        print(f"Generation: {generation + 1}")
        print("5 Muestras")
        print(f"{poblation[:5]}...")
        candidates = selection(poblation, 2)
        best = candidates[0]
        print(f'Best: {best}')
        print(f'Fitness: {fitness(best)}')
        print()
        crossover_res = crossover(candidates)
        new_poblation = mutation(crossover_res, poblation_size)
        if not generation == generations - 1:
            poblation = new_poblation
    print(fitness(poblation[0]))


if __name__ == "__main__":
    main()
    # print([1, 2, 3, 4, 5][2:])
    # for _ in range(100):
    #     candidates = [[11, 7, 0, 0, 2, 3, 4, 0, 9, 1, 5, 10, 8, 0, 0, 6], [11, 7, 0, 0, 5, 3, 4, 0, 9, 6, 2, 10, 8, 0, 0, 1], [11, 7, 0, 0, 2, 3,
    #                                                                                                                            4, 0, 9, 1, 5, 10, 8, 6, 0, 0], [11, 0, 0, 0, 5, 3, 4, 2, 9, 1, 0, 10, 8, 6, 7, 0], [11, 7, 0, 0, 3, 2, 4, 1, 9, 0, 6, 10, 8, 0, 5, 0]]
    #     # if len(set(crossover(candidates))) != 12:
    #     print(candidates)
