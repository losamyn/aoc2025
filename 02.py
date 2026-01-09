"""🎄 Solution for Day 2 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 02.py
"""

inp = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

part1_asserts = [
    (inp, 1227775554),
]
part2_asserts = [
    (inp, 4174379265),
]


def part1_is_invalid_id(product_id: int) -> bool:
    product_id = str(product_id)
    halfway = len(product_id) // 2
    return product_id[:halfway] == product_id[halfway:]


def part1(inp: str) -> int:
    invalid_ids = []

    for range_ in inp.split(","):
        lower, upper = map(int, range_.split("-"))
        invalid_ids += filter(part1_is_invalid_id, range(lower, upper + 1))

    return sum(invalid_ids)


def part2_is_invalid_id(product_id: int) -> bool:
    product_id = str(product_id)
    halfway = len(product_id) // 2
    # Find second occurence of first character
    possible_length = product_id.find(product_id[0], 1)

    while possible_length > 0 and possible_length <= halfway:
        to_check = product_id
        check_until = possible_length * 2
        while True:
            a = to_check[:possible_length]
            b = to_check[possible_length:check_until]
            if a != b:
                break
            if len(to_check) == check_until:
                return True
            to_check = to_check[possible_length:]
        possible_length = product_id.find(product_id[0], possible_length + 1)

    return False


def part2(inp: str) -> str | int | None:
    invalid_ids = []

    for range_ in inp.split(","):
        lower, upper = map(int, range_.split("-"))
        invalid_ids += filter(part2_is_invalid_id, range(lower, upper + 1))

    return sum(invalid_ids)
