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
    (inp, 43),
]

region_to_check = set([(x, y) for x in range(-1, 2) for y in range(-1, 2)])
region_to_check.remove((0, 0))


def pad(inp):
    padded = list(map(lambda line: list("." + line + "."), inp))
    horizontal_padding = [["."] * len(padded[0])]
    return horizontal_padding + padded + horizontal_padding


def is_accessible(inp, x, y) -> bool:
    result = 0
    for ix, iy in region_to_check:
        result += inp[y + iy][x + ix] == "@"
    return result < 4


def part1(inp: str) -> int:
    inp = pad(inp.split())
    result = 0
    xrange = range(1, len(inp[0]) - 1)
    yrange = range(1, len(inp) - 1)

    for x in xrange:
        for y in yrange:
            if inp[y][x] == "@":
                result += is_accessible(inp, x, y)
    return result


def part2(inp: str) -> int:
    inp = pad(inp.split())
    xrange = range(1, len(inp[0]) - 1)
    yrange = range(1, len(inp) - 1)
    coords = set([(x, y) for x in xrange for y in yrange])
    result = 0
    lastResult = -1

    while result != lastResult:
        lastResult = result
        new_coords = set(coords)
        for x, y in coords:
            if inp[y][x] == "@":
                if is_accessible(inp, x, y):
                    result += 1
                    inp[y][x] = "."
                    new_coords.remove((x, y))
            else:
                new_coords.remove((x, y))
        coords = new_coords
    return result
