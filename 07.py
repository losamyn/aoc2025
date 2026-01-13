"""🎄 Solution for Day 7 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 07.py
"""

inp = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

part1_asserts = [
    (inp, 21),
]
part2_asserts = [
    (inp, 40),
]


def part1(inp: str) -> int:
    lines = [list(line) for line in inp.split("\n")]
    result = 0
    for i in range(1, len(lines)):
        for j in range(len(lines[i])):
            if lines[i - 1][j] == "|" or lines[i - 1][j] == "S":
                if lines[i][j] == "^":
                    result += 1
                    lines[i][j - 1] = "|"
                    lines[i][j + 1] = "|"
                elif lines[i][j] == ".":
                    lines[i][j] = "|"
    return result


def part2(inp: str) -> int:
    inp = inp.strip().replace(".", "0").replace("S", "1")
    lines = [list(line) for line in inp.split("\n")]
    lines = [[-1 if c == "^" else int(c) for c in line] for line in lines]

    for i in range(1, len(lines)):
        for j in range(len(lines[i])):
            if lines[i - 1][j] > 0:
                if lines[i][j] < 0:
                    lines[i][j - 1] += lines[i - 1][j]
                    lines[i][j + 1] += lines[i - 1][j]
                else:
                    lines[i][j] += lines[i - 1][j]

    return sum(lines[-1])
