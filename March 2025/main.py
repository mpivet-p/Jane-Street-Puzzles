# COLS, ROWS = 5, 5
COLS, ROWS = 10, 10
UP, RIGHT, DOWN, LEFT = (-1, 0), (0, 1), (1, 0), (0, -1)
SLASH, BACKSLASH = 1, 2 # 1 = /     2 = \

mirrors = {
    (UP, SLASH): RIGHT, (UP, BACKSLASH): LEFT,
    (DOWN, SLASH): LEFT, (DOWN, BACKSLASH): RIGHT,
    (LEFT, SLASH): DOWN, (LEFT, BACKSLASH): UP,
    (RIGHT, SLASH): UP, (RIGHT, BACKSLASH): DOWN
}


def print_grid(grid: list[list]) -> None:
    for row in range(1, len(grid) - 1):
        print("".join(str(c) for c in grid[row][1:-1]))

def check_laser(grid: list[list], row: int, col: int, dir: tuple[int, int]) -> tuple[bool, tuple]:
    return follow_light_ray(grid, row, col, dir) == grid[row][col]

def follow_light_ray(grid: list[list], row: int, col: int, dir: tuple[int, int]) -> int:
    count = 0
    while True:
        row += dir[0]
        col += dir[1]
        count += 1
        if grid[row][col] != 0:
            break

    if (row > 0 and row < ROWS + 1) and (col > 0 and col < COLS + 1):
        return count * follow_light_ray(grid, row, col, mirrors[(dir, grid[row][col])])
    return count

# Refacto done
def calculate_lasers_lengths(grid: list[list]) -> int:
    sums = [0] * 4
    for i in range(1, COLS + 1):
        if (0, i) not in known_lasers:
            sums[0] += follow_light_ray(grid, 0, i, DOWN)
        if (ROWS + 1, i) not in known_lasers:
            sums[1] += follow_light_ray(grid, ROWS + 1, i, UP)
        if (i, 0) not in known_lasers:
            sums[2] += follow_light_ray(grid, i, 0, RIGHT)
        if (i, COLS + 1) not in known_lasers:
            sums[3] += follow_light_ray(grid, i, COLS + 1, LEFT)

    return sums[0] * sums[1] * sums[2] * sums[3]

# Refacto done
def check_known_lasers(grid: list[list]) -> bool:
    for laser in known_lasers:
        if not check_laser(grid, laser[0], laser[1], known_lasers[laser][1]):
            return False
    return True

def can_place_mirror(grid: list[list], row: int, col: int) -> bool:
    if row > 1 and grid[row - 1][col] != 0:
        return False
    if row < ROWS and grid[row + 1][col] != 0:
        return False
    if col > 1 and grid[row][col - 1] != 0:
        return False
    if col < COLS and grid[row][col + 1] != 0:
        return False
    return True

def solve(grid: list[list], row: int, col: int, changed: bool = True) -> None:
    if changed and check_known_lasers(grid):
        return True
    if row == ROWS and col == COLS:
        return False
    
    if col == COLS:
        next_row = row + 1
        next_col = 1
    else:
        next_row = row
        next_col = col + 1

    if solve(grid, next_row, next_col, changed=False):
        return True

    if not can_place_mirror(grid, row, col):
        return False

    grid[row][col] = SLASH
    if solve(grid, next_row, next_col):
        return True

    grid[row][col] = BACKSLASH
    if solve(grid, next_row, next_col):
        return True

    grid[row][col] = 0
    return False

def tests(grid: list[list[int]]) -> None:
    grid[1][2] = BACKSLASH
    grid[1][5] = BACKSLASH
    grid[2][1] = SLASH
    grid[3][3] = SLASH
    grid[3][5] = SLASH
    grid[4][4] = SLASH
    grid[5][1] = BACKSLASH

    assert check_laser(grid, 0, 3, DOWN) == True
    assert (ret := follow_light_ray(grid, 0, 3, DOWN)) == 9, f"Function returned {ret!r}"

    assert (ret := follow_light_ray(grid, 2, 6, LEFT)) == 75, f"Function returned {ret!r}"
    assert check_laser(grid, 2, 6, LEFT) == True

    assert check_laser(grid, 0, 4, DOWN) == False

    assert check_known_lasers(grid) == True


    grid[1][2] = 0
    grid[1][5] = 0
    grid[2][1] = 0
    grid[3][3] = 0
    grid[3][5] = 0
    grid[4][4] = 0
    grid[5][1] = 0

    print("-> Tests run successfully")

def get_test_map() -> list[list]:
    grid: list[list] = [
        ['.'] * (COLS + 2),
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],        
        ['.'] * (COLS + 2)
    ]
    grid[0][3] = 9
    grid[4][0] = 16
    grid[6][3] = 36
    grid[2][6] = 75

    global known_lasers
    known_lasers = {(0, 3): (9, DOWN), (4, 0): (16, RIGHT), (6, 3): (36, UP), (2, 6): (75, LEFT)}

    return grid

def get_real_map() -> list[list]:
    grid: list[list] = [
        ['.'] * (COLS + 2),
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],
        ['.'] + [0] * COLS + ['.'],        
        ['.'] * (COLS + 2)
    ]
    grid[0][3] = 112
    grid[0][5] = 48
    grid[0][6] = 3087
    grid[0][7] = 9
    grid[0][10] = 1

    grid[2][11] = 4
    grid[3][11] = 27
    grid[7][11] = 16

    grid[4][0] = 27
    grid[8][0] = 12
    grid[9][0] = 225

    grid[11][1] = 2025
    grid[11][4] = 12
    grid[11][5] = 64
    grid[11][6] = 5
    grid[11][8] = 405

    global known_lasers
    known_lasers = {
        (0, 3): (112, DOWN),
        (0, 5): (48, DOWN),
        (0, 6): (3087, DOWN),
        (0, 7): (9, DOWN),
        (0, 10): (1, DOWN),

        (2, 11): (4, LEFT),
        (3, 11): (27, LEFT),
        (7, 11): (16, LEFT),

        (4, 0): (27, RIGHT),
        (8, 0): (12, RIGHT),
        (9, 0): (225, RIGHT),

        (11, 1): (2025, UP),
        (11, 4): (12, UP),
        (11, 5): (64, UP),
        (11, 6): (5, UP),
        (11, 8): (405, UP)
    }

    grid[1][10] = BACKSLASH
    grid[10][6] = SLASH


    return grid

def main():
    # grid = get_test_map()
    grid = get_real_map()

    # tests(grid)

    print(solve(grid, 1, 1))
    print_grid(grid)

    print(calculate_lasers_lengths(grid))

if __name__ == "__main__":
    main()