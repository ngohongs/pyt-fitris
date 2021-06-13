from assets.settings import *
# Module for manipulation with blocks


# Spawn locations for each block
IBLOCK = np.array([
    [3, 2], [4, 2], [5, 2], [6, 2]
])

JBLOCK = np.array([
    [4, 1], [5, 1], [6, 1], [6, 2]
])

OBLOCK = np.array([
    [4, 1], [5, 1], [4, 2], [5, 2]
])

LBLOCK = np.array([
    [4, 1], [5, 1], [6, 1], [4, 2]
])

SBLOCK = np.array([
    [5, 1], [6, 1], [4, 2], [5, 2]
])

TBLOCK = np.array([
    [5, 2], [4, 1], [5, 1], [6, 1]
])

ZBLOCK = np.array([
    [4, 1], [5, 1], [5, 2], [6, 2]
])

# Center of rotation for each block at their spawn time
IBLOCK_CENTER = np.array([4, 2], dtype=np.int16)
JBLOCK_CENTER = np.array([5, 1], dtype=np.int16)
LBLOCK_CENTER = np.array([5, 1], dtype=np.int16)
OBLOCK_CENTER = np.array([4, 2], dtype=np.int16)
SBLOCK_CENTER = np.array([5, 2], dtype=np.int16)
TBLOCK_CENTER = np.array([5, 1], dtype=np.int16)
ZBLOCK_CENTER = np.array([5, 2], dtype=np.int16)

# Color for each block
# used before finalization of block rendering
IBLOCK_COLOR = (0, 240, 240)
JBLOCK_COLOR = (0, 0, 240)
LBLOCK_COLOR = (240, 160, 0)
OBLOCK_COLOR = (240, 240, 0)
SBLOCK_COLOR = (0, 240, 0)
TBLOCK_COLOR = (160, 0, 240)
ZBLOCK_COLOR = (240, 0, 0)

# Rotation state
# J-block, L-block, T-block spawn NES version of Tetris upside down,
# whereas in Super Rotation System for Tetris these blocks with their
# flatside down.
#
# source: https://harddrop.com/wiki/SRS
IBLOCK_ROT = 0
JBLOCK_ROT = 2
LBLOCK_ROT = 2
OBLOCK_ROT = 0
SBLOCK_ROT = 0
TBLOCK_ROT = 2
ZBLOCK_ROT = 0

# Matrices for rotation blocks
#
# source: https://www.youtube.com/watch?v=yIpk5TJ_uaI
CLOCKWISE = np.array([
    [0, -1],
    [1, 0],
], dtype=np.int16)

COUNTER_CLOCKWISE = np.array([
    [0, 1],
    [-1, 0]
], dtype=np.int16)

ROTATION = [CLOCKWISE, COUNTER_CLOCKWISE]

# Offset data for each piece
#
# source: https://harddrop.com/wiki/SRS
JLSTZ_OFFSET = np.array([
    [[+0, +0], [+0, +0], [+0, +0], [+0, +0], [+0, +0]],
    [[+0, +0], [+1, +0], [+1, +1], [+0, -2], [+1, -2]],
    [[+0, +0], [+0, +0], [+0, +0], [+0, +0], [+0, +0]],
    [[+0, +0], [-1, +0], [-1, +1], [+0, -2], [-1, -2]]
], dtype=np.int16)

I_OFFSET = np.array([
    [[+0, +0], [-1, +0], [+2, +0], [-1, +0], [+2, +0]],
    [[-1, +0], [+0, +0], [+0, +0], [+0, -1], [+0, +2]],
    [[-1, -1], [+1, -1], [-2, -1], [+1, +0], [-2, +0]],
    [[+0, -1], [+0, -1], [+0, -1], [+0, +1], [+0, -2]]
], dtype=np.int16)

O_OFFSET = np.array([
    [[+0, +0]],
    [[+0, +1]],
    [[-1, +1]],
    [[-1, +0]]
], dtype=np.int16)


tetromino = [
    IBLOCK, JBLOCK, LBLOCK, OBLOCK, SBLOCK, TBLOCK, ZBLOCK
]
tetromino_color = [
    IBLOCK_COLOR, JBLOCK_COLOR, LBLOCK_COLOR, OBLOCK_COLOR, SBLOCK_COLOR, TBLOCK_COLOR, ZBLOCK_COLOR
]
tetromino_center = [
    IBLOCK_CENTER, JBLOCK_CENTER, LBLOCK_CENTER, OBLOCK_CENTER, SBLOCK_CENTER, TBLOCK_CENTER, ZBLOCK_CENTER
]

tetromino_rotation = [
    IBLOCK_ROT, JBLOCK_ROT, LBLOCK_ROT, OBLOCK_ROT, SBLOCK_ROT, TBLOCK_ROT, ZBLOCK_ROT
]

tetromino_offsets = [
    I_OFFSET, JLSTZ_OFFSET, JLSTZ_OFFSET, O_OFFSET, JLSTZ_OFFSET, JLSTZ_OFFSET, JLSTZ_OFFSET
]

# Block class
class Tetromino:
    # Initialization of block
    def __init__(self, shape_idx):
        self.shape = shape_idx
        self.positions = tetromino[shape_idx].copy()
        self.center = tetromino_center[shape_idx].copy()
        self.color = tetromino_color[shape_idx]
        self.rotation = tetromino_rotation[shape_idx]

    # Removes block from grid
    def remove_from_grid(self, grid):
        for x, y in self.positions:
            grid[y][x] = (0, 0, 0)

    # Checks if the block collides  with any other block or is out of bounds
    def check_collisions(self, grid):
        for x, y in self.positions:
            if TETRIS_TILE_WIDTH <= x or x < 0 or TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT <= y:
                return True
            if not np.array_equal(grid[y][x], BLANK_TILE):
                return True

        return False

    # Spawn the block in the grid
    def spawn(self, grid):
        for x, y in self.positions:
            grid[y][x] = self.color

    # Moves the block
    def move(self, grid, dx=0, dy=0):
        self.remove_from_grid(grid)

        prev_center = self.center.copy()
        prev_positions = self.positions.copy()

        self.center += [dx, dy]
        self.positions += [dx, dy]

        if self.check_collisions(grid):
            self.center = prev_center
            self.positions = prev_positions
            self.spawn(grid)
            return True
        self.spawn(grid)
        return False

    def move_left(self, grid):
        return self.move(grid, dx=-1)

    def move_right(self, grid):
        return self.move(grid, dx=1)

    def move_down(self, grid):
        return self.move(grid, dy=1)

    def move_up(self, grid):
        return self.move(grid, dy=-1)

    # Rotates block
    def rotate(self, grid, direction):
        self.remove_from_grid(grid)

        if direction == 0:
            next_rotation = (self.rotation + 4 + 1) % 4
        else:
            next_rotation = (self.rotation + 4 - 1) % 4

        prev_positions = self.positions.copy()

        rotated_positions = []
        for x, y in self.positions - self.center:
            rotated_positions += [(ROTATION[direction] @ np.array([[x], [y]], dtype=np.int16)).sum(axis=1)]
        rotated_positions = np.array(rotated_positions) + self.center

        for i in range(tetromino_offsets[self.shape].shape[1]):
            offset = tetromino_offsets[self.shape][self.rotation][i] - tetromino_offsets[self.shape][next_rotation][i]
            self.positions = rotated_positions.copy() + offset
            if not self.check_collisions(grid):
                self.rotation = next_rotation
                self.center += offset
                self.spawn(grid)
                return False
        self.positions = prev_positions
        self.spawn(grid)
        return True

    def rotate_right(self, grid):
        return self.rotate(grid, 0)

    def rotate_left(self, grid):
        return self.rotate(grid, 1)

    def __eq__(self, other):
        return self.color == other.color
