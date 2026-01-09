"""🎄 Solution for Day 4 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 04.py
"""

inp = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
part1_asserts = [
    (inp, 13),
]
part2_asserts = [
    (inp, None),
]


def pad(inp):
    padded = list(map(lambda line: "." + line + ".", inp))
    horizontal_padding = ["." * len(padded[0])]
    return horizontal_padding + padded + horizontal_padding


def is_accessible(inp, x, y) -> bool:
    result = -(inp[y][x] == "@")  # -True is equal to -1
    for ix in range(-1, 2):
        for iy in range(-1, 2):
            result += inp[y + iy][x + ix] == "@"
    return result < 4


def part1(inp: str) -> int:
    inp = pad(inp.split())
    result = 0
    for x in range(1, len(inp[0]) - 1):
        for y in range(1, len(inp) - 1):
            if inp[y][x] == "@":
                result += is_accessible(inp, x, y)
    return result


def part2(inp: str) -> int:
    return None
