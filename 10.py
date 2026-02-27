"""🎄 Solution for Day 10 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 10.py
"""

inp = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
inp2 = """[.#...#] (2,4) (3,4) (0,2,3,5) (0,1,2,3) (1,3,4,5) {26,32,28,47,23,20}
"""
inp3 = """[#...#####.] (0,1,4,6,8,9) (1,2,3,5,6,8,9) (0,2,3,4,5,6,8) (0,4,5,6,7) (1,2,9) (2,5,9) (2,4,6,7) (0,3,4,6,9) {52,30,67,53,55,67,72,17,36,68}
"""
part1_asserts = [
    (inp, 7),
]
part2_asserts = [
    (inp, 33),
    (inp2, 49),
    (inp3, 102),
]


def parse_line(line):
    goal, *buttons, joltage = line.split()
    goal = [c == "#" for c in goal.strip("[]")]
    buttons = [tuple(map(int, button.strip("()").split(","))) for button in buttons]
    joltage = list(map(int, joltage.strip("{}").split(",")))
    return goal, buttons, joltage


def calculate_steps(goal, buttons):
    # Work backwards, start with the goal and try to get to all False
    state = list(goal)
    current_buttons = set(buttons)
    queue = [(state, current_buttons)]
    while len(queue):
        state, current_buttons = queue.pop(0)
        if not any(state):
            # state is all False, found solution
            return len(buttons) - len(current_buttons)
        # Find buttons for the indicator that has least available buttons to press
        buttons_to_press = current_buttons
        for i, indicator in enumerate(state):
            if indicator:
                filtered_buttons = [button for button in current_buttons if i in button]
                if len(filtered_buttons) < len(buttons_to_press):
                    buttons_to_press = filtered_buttons
        # Press all the buttons found prior and add them to queue
        for button in buttons_to_press:
            new_state = list(state)
            for ind in button:
                new_state[ind] = not new_state[ind]
            queue.append((new_state, current_buttons - {button}))
    print("Failed to find solution for: ", goal)
    return 0


def calculate_steps_two(goal, buttons):
    # Could not figure this one out myself, using the approach described in following post:
    # https://old.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory
    aug_matrix = [
        [int(row in button) for button in buttons] + [joltage]
        for row, joltage in enumerate(goal)
    ]
    rows_n = len(aug_matrix)
    columns_n = len(aug_matrix[0])
    # RREF -- making the assumption that all divisions will be whole integers
    for current_row in range(rows_n):
        # Find next non-zero row, swap it to current row
        current_column = columns_n
        to_swap = current_row
        for row_i in range(current_row, rows_n):
            first_one = next((i for i, x in enumerate(aug_matrix[row_i]) if x), None)
            if first_one is not None and first_one < current_column:
                current_column = first_one
                to_swap = row_i
            if current_column == current_row:
                break
        if current_column == columns_n:
            break
        if to_swap != current_row:
            # Swap rows
            tmp = aug_matrix[to_swap]
            aug_matrix[to_swap] = aug_matrix[current_row]
            aug_matrix[current_row] = tmp
        # Scale current row
        scale = aug_matrix[current_row][current_column]
        for i in range(current_column, columns_n):
            if aug_matrix[current_row][i] % scale:
                print(
                    "RREF warning: cant divide ",
                    aug_matrix[current_row][i],
                    " by ",
                    scale,
                    " --- ",
                    goal,
                )
            aug_matrix[current_row][i] = aug_matrix[current_row][i] / scale
        # Subtract current row from other rows
        for i in range(rows_n):
            scale = aug_matrix[i][current_column]
            if i == current_row or scale == 0:
                continue
            for j in range(current_column, columns_n):
                aug_matrix[i][j] -= aug_matrix[current_row][j] * scale
    return int(sum([row[-1] for row in aug_matrix]))


def part1(inp: str) -> int:
    result = 0
    for line in inp.strip().split("\n"):
        goal, buttons, _ = parse_line(line)
        result += calculate_steps(goal, buttons)
    return result


def part2(inp: str) -> int:
    result = 0
    for line in inp.strip().split("\n"):
        _, buttons, goal = parse_line(line)
        result += calculate_steps_two(goal, buttons)
    return result
