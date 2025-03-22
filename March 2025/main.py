from collections import defaultdict

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
        print("".join(r"./\\"[c] for c in grid[row][1:-1]))

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

def check_known_lasers(grid: list[list]) -> bool:
    for laser in known_lasers:
        if not check_laser(grid, laser[0], laser[1], known_lasers[laser][1]):
            # print(laser, follow_light_ray(grid, laser[0], laser[1], known_lasers[laser][1]))
            return False
    return True

def check_previous_lasers(grid: list[list], lasers: list, i: int) -> bool:
    for j in range(i):
        laser = lasers[i]
        if not check_laser(grid, *laser[0], laser[1][1]):
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

def tests(grid: list[list[int]]) -> None:
    grid[1][2] = BACKSLASH
    grid[1][5] = BACKSLASH
    grid[2][1] = SLASH
    grid[3][3] = SLASH
    grid[3][5] = SLASH
    grid[4][4] = SLASH
    grid[5][1] = BACKSLASH

    print_grid(grid)

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

    grid[1][10] = BACKSLASH # Laser v=1
    # grid[8][4] = BACKSLASH # Laser v=12
    # grid[10][6] = SLASH # Laser v=5

    grid[2][9] = BACKSLASH # Laser v=4

    # Laser v=9
    grid[1][7] = BACKSLASH
    grid[4][10] = BACKSLASH

    # # Hypothesis
    # grid[3][2] = BACKSLASH
    # grid[4][3] = BACKSLASH
    # grid[4][5] = BACKSLASH

    return grid

def get_current_mirrors(grid: list[list]) -> list[tuple[int, int, int]]:
    res: list[tuple[int, int, int]] = []

    for r in range(1, ROWS + 1):
        for c in range(1, COLS + 1):
            if grid[r][c] != 0:
                res.append((r, c, grid[r][c]))

    return res

def find_all_mirrors(grid: list[list], laser: tuple, row: int, col: int, dir: tuple[int, int], goal: int) -> None:
    if dir == DOWN or dir == UP:
        generator = range(1, ROWS - row + 2) if dir == DOWN else range(-1 - row, 0)

        for i in generator:
            if goal % i != 0:
                continue

            if goal == abs(i) and (row + i == ROWS + 1 or row + i == 0)\
                and check_laser(grid, *laser[0], laser[1][1]):

                # print(f"Found {dir=} {goal=} {i=} {row=}")
                # print_grid(grid)
                mirror_possibilities[laser].append(get_current_mirrors(grid))
                break

            if not can_place_mirror(grid, row + i, col):
                continue

            prev = grid[row + i][col]

            grid[row + i][col] = SLASH
            find_all_mirrors(grid, laser, row + i, col, mirrors[dir, SLASH], goal // abs(i))
            
            grid[row + i][col] = BACKSLASH
            find_all_mirrors(grid, laser, row + i, col, mirrors[dir, BACKSLASH], goal // abs(i))

            grid[row + i][col] = prev

    elif dir == RIGHT or dir == LEFT:
        generator = range(1, COLS - col + 2) if dir == RIGHT else range(-1 - col, 0)

        for i in generator:
            if goal % i != 0:
                continue

            if goal == abs(i) and (col + i == COLS + 1 or col + i == 0)\
                and check_laser(grid, *laser[0], laser[1][1]):

                # print(f"Found {dir=} {goal=} {i=} {row=}")
                # print_grid(grid)
                mirror_possibilities[laser].append(get_current_mirrors(grid))
                break

            if not can_place_mirror(grid, row, col + i):
                continue

            prev = grid[row][col + i]

            grid[row][col + i] = SLASH
            find_all_mirrors(grid, laser, row, col + i, mirrors[dir, SLASH], goal // abs(i))
            
            grid[row][col + i] = BACKSLASH
            find_all_mirrors(grid, laser, row, col + i, mirrors[dir, BACKSLASH], goal // abs(i))

            grid[row][col + i] = prev

def generate_hypothetical_mirrors(grid: list[list]) -> None:
    t = 0
    for coords, laser in known_lasers.items():
        # print("=================")
        find_all_mirrors(grid, (coords, laser), coords[0], coords[1], laser[1], laser[0])
        t += len(mirror_possibilities[(coords, laser)])
        # print(coords, len(mirror_possibilities[(coords, laser)]))

    print(t)


def check_mirrors_compatibility(grid: list[list], mrs: list[tuple[int, int, int]]) -> bool:
    for r, c, mtype in mrs:
        if not can_place_mirror(grid, r, c) or (grid[r][c] != 0 and grid[r][c] != mtype):
            return False
    return True

def swap_mirrors(grid: list[list[int, str]], mrs: list[tuple[int, int, int]]) -> list[tuple]:
    res = []

    for r, c, m_type in mrs:
        res.append((r, c, grid[r][c]))
        grid[r][c] = m_type

    return res

def solve(grid: list[list[int, str]], lasers: list, i: int) -> bool:
    if i == len(lasers):
        return False

    for mirrors_set in mirror_possibilities[lasers[i]]:
        if check_mirrors_compatibility(grid, mirrors_set):
            backup = swap_mirrors(grid, mirrors_set)

            if check_previous_lasers(grid, lasers, i):
                if (i == len(lasers) - 1 and check_known_lasers(grid)) or solve(grid, lasers, i + 1):
                    return True

            swap_mirrors(grid, backup)

    return False      

def main():
    # grid = get_test_map()
    grid = get_real_map()
    global mirror_possibilities
    mirror_possibilities = defaultdict(list)

    # tests(grid)

    print_grid(grid)
    generate_hypothetical_mirrors(grid)
    # print(mirror_possibilities.keys())
    solve(grid, list(mirror_possibilities.keys()), 0)
    print_grid(grid)
    print(check_known_lasers(grid))

if __name__ == "__main__":
    main()