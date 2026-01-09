"""🎄 Solution for Day 3 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 03.py
"""

inp = """987654321111111
811111111111119
234234234234278
818181911112111
"""
part1_asserts = [
    (inp, 357),
]
part2_asserts = [
    (inp, 3121910778619),
]


def part1(inp: str) -> int:
    result = 0
    for bank in inp.split():
        # string characters can be compared, only convert to int at end
        first = max(bank[:-1])
        bank_rest = bank[bank.find(first) + 1 :]
        joltage = first + max(bank_rest)
        result += int(joltage)

    return result


def part2(inp: str) -> int:
    result = 0
    for bank in inp.split():
        joltage = ""
        for i_bat in range(-11, 1):
            possible_bats = bank[:i_bat] if i_bat < 0 else bank
            next_bat = max(possible_bats)
            bank = bank[bank.find(next_bat) + 1 :]
            joltage = joltage + next_bat
        result += int(joltage)

    return result
