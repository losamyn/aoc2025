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


def compute_lookup_table(buttons, state_length):
    # Constructs a dictionary mapping the patterns created to all possible button combinations
    # Binary representation of key represents which joltage is odd in final stage
    # Iterate in a gray code pattern, visiting all possible combinations by having to only push 1 button at a time
    state = [False] * state_length
    button_combination = set()
    i_last = 0
    result = {tuple(state): [tuple(button_combination)]}
    for i in range(1, 1 << len(buttons)):
        # Calculate Gray Code number, representing next button combination
        i_gray = i ^ (i >> 1)
        # Find next button to press from old state
        diff = i_gray ^ i_last
        i_last = i_gray
        to_press = 0
        while not diff & 1:
            to_press += 1
            diff >>= 1
        # Update button combination
        if to_press in button_combination:
            button_combination.remove(to_press)
        else:
            button_combination.add(to_press)
        # Press the button
        for index in buttons[to_press]:
            state[index] = not state[index]
        # Add button combination to the resulting state
        s = tuple(state)
        if s in result:
            result[s].append(tuple(button_combination))
        else:
            result[s] = [tuple(button_combination)]
    return result


def iterate_part_two(
    goal: list[int], buttons: list[tuple[int, ...]], lookup_table, level=0
) -> int | None:
    # Returns a list with all possible button press amounts
    # Calculate even/odd pattern for current goal
    pattern = tuple(i & 1 for i in goal)
    # Lookup the pattern to find possible button presses resulting in this pattern
    if pattern not in lookup_table:
        # Pattern not possible
        return None
    combinations = lookup_table[pattern]
    results = []
    for combo in combinations:
        # Press the buttons in the combo
        new_goal = list(goal)
        for button_index in combo:
            for index in buttons[button_index]:
                new_goal[index] -= 1
        # Special cases:
        if any(joltage < 0 for joltage in new_goal):
            # Not a valid outcome, we exceeded at least one of the joltages
            continue
        if not any(new_goal):
            # new_goal is all zeroes, we found a possible solution
            results.append(len(combo))
            continue
        # Next iteration:
        half_goal = [joltage // 2 for joltage in new_goal]
        half_result = iterate_part_two(half_goal, buttons, lookup_table, level + 1)
        if half_result:
            results.append(len(combo) + (2 * half_result))
    if results:
        return min(results)
    else:
        return None


def calculate_steps_two(goal, buttons):
    # Could not figure this one out myself, using the approach described in following post:
    # https://old.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory
    lookup_table = compute_lookup_table(buttons, len(goal))
    result = iterate_part_two(goal, buttons, lookup_table)
    return result


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
        subresult = calculate_steps_two(goal, buttons)
        if subresult:
            result += subresult
    return result
