"""🎄 Solution for Day 9 of Advent of Code 2026 🎄

Usage:

uv run adventofcode run 09.py
"""

from bisect import bisect, insort

inp = """7,1 
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
part1_asserts = [
    (inp, 50),
]
part2_asserts = [
    (inp, 24),
]


class MovieTheater:
    """Represents the tile floor"""

    UNASSIGNED = -1
    EMPTY_TILE = 0
    RED_TILE = 1
    EDGE_TILE = 2
    GREEN_TILE = 3
    # compressed table representing the tile floor.
    floor_c: list[list[int]]
    # Lookup tables to translate coordinates
    decompress_x: list[int]
    decompress_y: list[int]
    compress_x: dict[int, int]
    compress_y: dict[int, int]
    # Keep track of vertical edges
    edges_by_y: list[list[int]]

    def __repr__(self) -> str:
        translation = {
            self.UNASSIGNED: " ",
            self.EMPTY_TILE: ".",
            self.RED_TILE: "#",
            self.EDGE_TILE: "+",
            self.GREEN_TILE: "X",
        }
        repr = []
        for row in self.floor_c:
            line = "".join([translation[tile] for tile in row])
            repr.append(line)
        return "\n".join(repr)

    def __calculate_coord_space(self, red_tiles: list[tuple[int, int]]):
        self.decompress_x = sorted({x for x, _ in red_tiles})
        self.decompress_y = sorted({y for _, y in red_tiles})
        self.compress_x = {}
        for i, x in enumerate(self.decompress_x):
            self.compress_x[x] = i
        self.compress_y = {}
        for i, y in enumerate(self.decompress_y):
            self.compress_y[y] = i

    def __initalise_floor_c(self, red_tiles: list[tuple[int, int]]):
        self.floor_c = [
            [self.UNASSIGNED for x in self.decompress_x] for y in self.decompress_y
        ]
        last_tile = red_tiles[-1]
        for tile in red_tiles:
            # Mark the red tile on the floor
            x = self.compress_x[tile[0]]
            y = self.compress_y[tile[1]]
            self.floor_c[y][x] = self.RED_TILE
            # Mark the green tiles between current and last red tile
            last_x = self.compress_x[last_tile[0]]
            last_y = self.compress_y[last_tile[1]]
            x_range = sorted([x, last_x])
            x_range[0] += 1
            y_range = sorted([y, last_y])
            y_range[0] += 1
            for j in range(*y_range):
                self.floor_c[j][x] = self.EDGE_TILE
            for i in range(*x_range):
                self.floor_c[y][i] = self.EDGE_TILE
            last_tile = tile

    def __compile_edges(self, red_tiles: list[tuple[int, int]]):
        self.edges_by_y = [list() for _ in self.decompress_y]
        last_tile = red_tiles[-1]
        for tile in red_tiles:
            y = self.compress_y[tile[1]]
            last_y = self.compress_y[last_tile[1]]
            if y == last_y:
                # Only track vertical edges
                continue

            x = self.compress_x[tile[0]]
            y_range = sorted([y, last_y])
            for j in range(*y_range):
                insort(self.edges_by_y[j], x)
            last_tile = tile

    def __init__(self, red_tiles: list[tuple[int, int]]) -> None:
        # loops in __initalise_floor_c and __compile_edges are very similar, but I prefer readability over optimization
        self.__calculate_coord_space(red_tiles)
        self.__initalise_floor_c(red_tiles)
        self.__compile_edges(red_tiles)

    def is_rectangle_tiled(self, x_bounds: list[int], y_bounds: list[int]) -> bool:
        x_low = self.compress_x[x_bounds[0]]
        x_high = self.compress_x[x_bounds[1]]
        y_low = self.compress_y[y_bounds[0]]
        y_high = self.compress_y[y_bounds[1]]
        for y in range(y_low, y_high + 1):
            for x in range(x_low, x_high + 1):
                if self.floor_c[y][x] == self.UNASSIGNED:
                    # Check if tile is inside the polygon
                    if bisect(self.edges_by_y[y], x) % 2:
                        self.floor_c[y][x] = self.GREEN_TILE
                    else:
                        self.floor_c[y][x] = self.EMPTY_TILE
                        return False
                elif self.floor_c[y][x] == self.EMPTY_TILE:
                    return False
        return True


def part1(inp: str) -> int:
    tiles = [
        (int(a), int(b))
        for a, b in [line.split(",") for line in inp.strip().split("\n")]
    ]
    corner_pairs = [(a, b) for a in range(len(tiles)) for b in range(a + 1, len(tiles))]
    biggest_area = 0
    for index_a, index_b in corner_pairs:
        a_x, a_y = tiles[index_a]
        b_x, b_y = tiles[index_b]
        area = (1 + abs(a_x - b_x)) * (1 + abs(a_y - b_y))
        if area > biggest_area:
            biggest_area = area
    return biggest_area


def part2(inp: str) -> int:
    red_tiles = [
        (int(a), int(b))
        for a, b in [line.split(",") for line in inp.strip().split("\n")]
    ]
    theater = MovieTheater(red_tiles)
    corner_pairs = [
        (a, b) for a in range(len(red_tiles)) for b in range(a + 1, len(red_tiles))
    ]
    biggest_area = 0
    for index_a, index_b in corner_pairs:
        a_x, a_y = red_tiles[index_a]
        b_x, b_y = red_tiles[index_b]
        area = (1 + abs(a_x - b_x)) * (1 + abs(a_y - b_y))
        x_bounds = sorted([a_x, b_x])
        y_bounds = sorted([a_y, b_y])
        if area > biggest_area and theater.is_rectangle_tiled(x_bounds, y_bounds):
            biggest_area = area
    return biggest_area
