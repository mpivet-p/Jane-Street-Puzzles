COLS = 5
ROWS = 5
UP, RIGHT, DOWN, LEFT = (-1, 0), (0, 1), (1, 0), (0, -1)
mirrors = {
    (UP, 1): RIGHT, (UP, 2): LEFT,
    (DOWN, 1): LEFT, (DOWN, 2): RIGHT,
    (LEFT, 1): DOWN, (LEFT, 2): UP,
    (RIGHT, 1): UP, (RIGHT, 2): DOWN
} # 1 = /     2 = \

def print_grid(grid):
    for row in range(1, len(grid) - 1):
        print("".join(str(c) for c in grid[row][1:-1]))

def check_laser(grid: list[list], row: int, col: int, dir: tuple[int, int], goal: int) -> tuple[bool, tuple]:
    # print(f"{row=} {col=} {goal=}")
    count = 0
    while count == 0 or grid[row][col] == 0:
        row += dir[0]
        col += dir[1]
        count += 1
    # print(f"Exiting while loop: {row=} {col=} {count=} {grid[row][col]=}")


    if (row > 0 and row < ROWS + 1) and (col > 0 and col < COLS + 1):
        return check_laser(grid, row, col, mirrors[(dir, grid[row][col])], goal // count)
    return count == goal

def main():
    grid = [
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

    grid[2][1] = 1
    grid[5][1] = 2
    grid[3][3] = 1
    grid[1][5] = 2
    print_grid(grid)
    print(check_laser(grid, 0, 3, DOWN, grid[0][3]))
    print(check_laser(grid, 2, 6, LEFT, grid[2][6]))
    print(check_laser(grid, 0, 5, DOWN, 1))

# Place all the mirrors for the known lasers and then just follow the distances

if __name__ == "__main__":
    main()