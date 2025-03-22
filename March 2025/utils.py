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

    # Pre-positioning mirors for lasers with only 1 possibility
    grid[1][10] = BACKSLASH # Laser v=1
    grid[2][9] = BACKSLASH # Laser v=4
    grid[1][7] = BACKSLASH # Laser v=9
    grid[4][10] = BACKSLASH # ^^^^^^^^^

    return grid, known_lasers, ROWS, COLS


def get_test_map() -> list[list]:
    # Overriding COLS and ROWS to fit the test map size
    ROWS, COLS = 5, 5

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

    known_lasers = {
        (0, 3): (9, DOWN),
        (4, 0): (16, RIGHT),
        (6, 3): (36, UP),
        (2, 6): (75, LEFT)
    }

    return grid, known_lasers, ROWS, COLS