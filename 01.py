"""🎄 Solution for Day 1 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 01.py
"""

inp = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

dial_start = 50
dial_size = 100

part1_asserts = [
    (inp, 3),
]
part2_asserts = [
    (inp, 6),
]


def part1(inp: str) -> int:
    dial = dial_start
    result = 0

    inp = inp.replace("L", "-").replace("R", "")
    for amount in map(int, inp.split()):
        dial = (dial + amount) % dial_size
        if dial == 0:
            result += 1
    return result


def part2(inp: str) -> int:
    dial = dial_start
    result = 0

    inp = inp.replace("L", "-").replace("R", "")
    for amount in map(int, inp.split()):
        if amount < 0:
            # Going to the left requires shifting by 1 to properly count zeroes
            new_dial = (dial - 1) % dial_size + amount
            dial = (new_dial + 1) % dial_size
            result += abs(new_dial // dial_size)
        else:
            new_dial = dial + amount
            dial = new_dial % dial_size
            result += abs(new_dial // dial_size)

    return result
