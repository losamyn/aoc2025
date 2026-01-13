"""🎄 Solution for Day 6 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 06.py
"""

inp = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""

part1_asserts = [
    (inp, 4277556),
]
part2_asserts = [
    (inp, 3263827),
]


def part1(inp: str) -> int:
    inp_all = [line.split() for line in inp.split("\n")]
    while len(inp_all[-1]) <= 0:
        inp_all = inp_all[:-1]
    numbers = [[int(s) for s in tup] for tup in zip(*inp_all[:-1])]
    operators = inp_all[-1]
    result = 0
    for column, operator in zip(numbers, operators):
        if operator == "+":
            result += sum(column)
        else:
            r = 1
            for n in column:
                r *= n
            result += r
    return result


def part2(inp: str) -> int:
    inp_all = inp.split("\n")
    while len(inp_all[-1]) <= 0:
        inp_all = inp_all[:-1]
    operators = inp_all[-1]
    numbers_list = inp_all[:-1]

    result = 0
    left = len(operators)
    right = left
    while left > 0:
        left -= 1
        if operators[left] == " ":
            continue
        numbers_t = list(map(lambda s: s[left:right], numbers_list))
        numbers = [int("".join(c)) for c in zip(*numbers_t)]
        if operators[left] == "+":
            result += sum(numbers)
        else:
            r = 1
            for n in numbers:
                r *= n
            result += r
        left -= 1
        right = left

    return result
