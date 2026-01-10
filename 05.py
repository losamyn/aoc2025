"""🎄 Solution for Day 5 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 05.py
"""

inp = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
part1_asserts = [
    (inp, 3),
]
part2_asserts = [
    (inp, None),
]


def part1(inp: str) -> int:
    # Can probably be optimized by compiling an ordered, non-overlapping ranges list
    ranges, ids = map(str.split, inp.split("\n\n"))
    ranges = list(map(lambda r: tuple(map(int, r.split("-"))), ranges))
    ids = map(int, ids)
    result = 0
    for id in ids:
        for lower, upper in ranges:
            if id >= lower and id <= upper:
                result += 1
                break
    return result


def part2(inp: str) -> int:
    return None
