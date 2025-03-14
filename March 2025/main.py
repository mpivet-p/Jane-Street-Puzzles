COLS, ROWS = 5, 5
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

def check_laser(grid: list[list], row: int, col: int, dir: tuple[int, int], goal: int) -> tuple[bool, tuple]:
    return follow_light_ray(grid, row, col, dir) == goal

# def solve(grid):
#     pass

def follow_light_ray(grid: list[list], row: int, col: int, dir: tuple[int, int]) -> int:
    count = 0
    while count == 0 or grid[row][col] == 0:
        row += dir[0]
        col += dir[1]
        count += 1

    if (row > 0 and row < ROWS + 1) and (col > 0 and col < COLS + 1):
        return count * follow_light_ray(grid, row, col, mirrors[(dir, grid[row][col])])
    return count

def calculate_lasers_lengths(grid: list[list]) -> int:
    sums = [0] * 4
    for i in range(1, COLS + 1):
        if grid[0][i] == '.':
            sums[0] += follow_light_ray(grid, 0, i, DOWN)
        if grid[ROWS + 1][i] == '.':
            sums[1] += follow_light_ray(grid, ROWS + 1, i, UP)
    for i in range(1, ROWS + 1):
        if grid[i][0] == '.':
            sums[2] += follow_light_ray(grid, i, 0, RIGHT)
        if grid[i][COLS + 1] == '.':
            sums[3] += follow_light_ray(grid, i, COLS + 1, LEFT)

    return sums[0] * sums[1] * sums[2] * sums[3]

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

    grid[1][2] = BACKSLASH
    grid[1][5] = BACKSLASH
    grid[2][1] = SLASH
    grid[3][3] = SLASH
    grid[3][5] = SLASH
    grid[4][4] = SLASH
    grid[5][1] = BACKSLASH

    print_grid(grid)
    print(check_laser(grid, 0, 3, DOWN, grid[0][3]))
    print(check_laser(grid, 2, 6, LEFT, grid[2][6]))
    print(check_laser(grid, 0, 5, DOWN, 1))
    print(follow_light_ray(grid, 6, 2, UP))
    print(calculate_lasers_lengths(grid))

# Place all the mirrors for the known lasers and then just follow the distances

if __name__ == "__main__":
    main()