COLS, ROWS = 5, 5
UP, RIGHT, DOWN, LEFT = (-1, 0), (0, 1), (1, 0), (0, -1)
SLASH, BACKSLASH = 1, 2 # 1 = /     2 = \

mirrors = {
    (UP, SLASH): RIGHT, (UP, BACKSLASH): LEFT,
    (DOWN, SLASH): LEFT, (DOWN, BACKSLASH): RIGHT,
    (LEFT, SLASH): DOWN, (LEFT, BACKSLASH): UP,
    (RIGHT, SLASH): UP, (RIGHT, BACKSLASH): DOWN
}

exec_count = 0

known_lasers = {(0, 3): (9, DOWN), (4, 0): (16, RIGHT), (6, 3): (36, UP), (2, 6): (75, LEFT)}

def print_grid(grid: list[list]) -> None:
    for row in range(1, len(grid) - 1):
        print("".join(str(c) for c in grid[row][1:-1]))

def check_laser(grid: list[list], row: int, col: int, dir: tuple[int, int]) -> tuple[bool, tuple]:
    return follow_light_ray(grid, row, col, dir) == grid[row][col]

def follow_light_ray(grid: list[list], row: int, col: int, dir: tuple[int, int]) -> int:
    count = 0
    while count == 0 or grid[row][col] == 0:
        row += dir[0]
        col += dir[1]
        count += 1

    if (row > 0 and row < ROWS + 1) and (col > 0 and col < COLS + 1):
        return count * follow_light_ray(grid, row, col, mirrors[(dir, grid[row][col])])
    return count

# Refacto done
def calculate_lasers_lengths(grid: list[list]) -> int:
    sums = [0] * 4
    for col in range(1, COLS + 1):
        if (0, col) not in known_lasers:
            sums[0] += follow_light_ray(grid, 0, col, DOWN)
        if (ROWS + 1, col) not in known_lasers:
            sums[1] += follow_light_ray(grid, ROWS + 1, col, UP)
    for row in range(1, ROWS + 1):
        if (row, 0) not in known_lasers:
            sums[2] += follow_light_ray(grid, row, 0, RIGHT)
        if (row, COLS + 1) not in known_lasers:
            sums[3] += follow_light_ray(grid, row, COLS + 1, LEFT)

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

def solve(grid: list[list], row: int, col: int) -> None:
    if check_known_lasers(grid):
        return True
    if row == ROWS and col == COLS:
        return False
    
    if col == COLS:
        next_row = row + 1
        next_col = 1
    else:
        next_row = row
        next_col = col + 1

    if solve(grid, next_row, next_col):
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
    # assert check_laser(grid, -1, 2, DOWN) == True
    assert (ret := follow_light_ray(grid, 0, 2, DOWN)) == 9, f"Function returned {ret!r}"
    assert (ret := follow_light_ray(grid, 1, 4, LEFT)) == 75, f"Function returned {ret!r}"

    assert check_laser(grid, 2, 6, LEFT) == True

    assert check_laser(grid, -1, 4, DOWN) == False


def main():
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

    # grid[1][2] = BACKSLASH
    # grid[1][5] = BACKSLASH
    # grid[2][1] = SLASH
    # grid[3][3] = SLASH
    # grid[3][5] = SLASH
    # grid[4][4] = SLASH
    # grid[5][1] = BACKSLASH

    print_grid(grid)
    # print(check_laser(grid, 0, 3, DOWN))
    # print(check_laser(grid, 2, 6, LEFT))
    # # print(check_laser(grid, 0, 5, DOWN))
    # print(follow_light_ray(grid, 6, 2, UP))
    # print(calculate_lasers_lengths(grid))
    # print(check_known_lasers(grid))
    print(solve(grid, 1, 1))
    print_grid(grid)
    print(calculate_lasers_lengths(grid))
    print(check_known_lasers(grid))


# Place all the mirrors for the known lasers and then just follow the distances

if __name__ == "__main__":
    main()