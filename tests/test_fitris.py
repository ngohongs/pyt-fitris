import pytest
from assets.game import *
from assets.block import *
from numpy.testing import assert_equal


@pytest.fixture
def iblock():
    return Tetromino(0)


@pytest.fixture
def tblock():
    return Tetromino(5)


@pytest.fixture
def lblock():
    return Tetromino(2)


@pytest.fixture
def grid():
    return np.zeros(shape=(TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT, TETRIS_TILE_WIDTH, 3), dtype=np.int16)


@pytest.fixture
def game():
    return Game()


@pytest.fixture
def iblock_rotated_right():
    rotation_grid = np.zeros(shape=(TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT, TETRIS_TILE_WIDTH, 3), dtype=np.int16)
    for x, y in [(5, 1), (5, 2), (5, 3), (5, 4)]:
        rotation_grid[y][x] = IBLOCK_COLOR
    return rotation_grid


@pytest.fixture
def tblock_rotated_left():
    rotation_grid = np.zeros(shape=(TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT, TETRIS_TILE_WIDTH, 3), dtype=np.int16)
    for x, y in [(5, 1), (5, 2), (5, 3), (6, 2)]:
        rotation_grid[y][x] = TBLOCK_COLOR
    return rotation_grid


@pytest.fixture
def lblock_rotated_kick():
    rotation_grid = np.zeros(shape=(TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT, TETRIS_TILE_WIDTH, 3), dtype=np.int16)
    for x, y in [(0, 7), (1, 7), (2, 7), (0, 8)]:
        rotation_grid[y][x] = LBLOCK_COLOR
    return rotation_grid


def test_rotate_iblock(grid, iblock, iblock_rotated_right):
    iblock.spawn(grid)
    iblock.rotate_right(grid)
    assert_equal(grid, iblock_rotated_right)


def test_move_rotate_tblock(grid, tblock, tblock_rotated_left):
    tblock.spawn(grid)
    tblock.move_down(grid)
    tblock.rotate_left(grid)
    assert_equal(grid, tblock_rotated_left)


def test_rotate_kick_lblock(grid, lblock, lblock_rotated_kick):
    lblock.spawn(grid)
    lblock.rotate_left(grid)
    for _ in range(6):
        lblock.move_left(grid)
        lblock.move_down(grid)
    lblock.rotate_right(grid)
    assert_equal(grid, lblock_rotated_kick)


def test_get_level_speed(game):
    assert game.get_speed(2) == 38
    assert game.get_speed(7) == 13
    assert game.get_speed(13) == 4
    assert game.get_speed(123) == 1


def test_check_clear(game, grid):
    game.grid = grid
    for x in range(10):
        game.grid[9][x] = IBLOCK_COLOR
        game.grid[16][x] = TBLOCK_COLOR
        game.grid[21][x] = IBLOCK_COLOR
    game.grid[21][2] = (0, 0, 0)
    full_rows_test = []
    game.check_for_clear(full_rows_test)
    assert full_rows_test == [9, 16]


def test_check_collisions(grid, iblock):
    grid[3][5] = TBLOCK_COLOR
    iblock.spawn(grid)
    iblock.positions += [0, 1]
    assert iblock.check_collisions(grid)


def test_push_down(game, grid):
    game.grid = grid
    for x in range(10):
        game.grid[TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT - 2][x] = IBLOCK_COLOR
        game.grid[TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT - 1][x] = TBLOCK_COLOR
    full_rows = []
    game.grid[TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT - 3][0] = ZBLOCK_COLOR
    game.grid[TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT - 3][2] = ZBLOCK_COLOR
    game.grid[TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT - 3][4] = ZBLOCK_COLOR
    game.check_for_clear(full_rows)
    game.push_down_rows(full_rows)
    expected = np.zeros(shape=(TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT, TETRIS_TILE_WIDTH, 3), dtype=np.int16)
    expected[TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT - 1][0] = ZBLOCK_COLOR
    expected[TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT - 1][2] = ZBLOCK_COLOR
    expected[TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT - 1][4] = ZBLOCK_COLOR
    assert_equal(game.grid, expected)
