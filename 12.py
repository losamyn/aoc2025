"""🎄 Solution for Day 12 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 12.py
"""

inp = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""
part1_asserts = [
    (inp, 0),
]
part2_asserts = [
    (inp, None),
]


def part1(inp: str) -> int:
    *shapes, objectives = inp.strip().split("\n\n")
    shapes = [[list(line) for line in shape.split()[1:]] for shape in shapes]
    tile_height = len(shapes[0])
    tile_width = len(shapes[0][0])
    result = 0
    for objective in objectives.split("\n"):
        dim, to_fit = objective.split(": ")
        dim = tuple(int(s) for s in dim.split("x"))
        to_fit = tuple(int(s) for s in to_fit.split(" "))

        tiles_to_fit = sum(to_fit)
        tile_spaces = (dim[0] // tile_width) * (dim[1] // tile_height)
        if tiles_to_fit <= tile_spaces:
            result += 1
            continue
    return result


def part2(inp: str) -> int:
    return 0
