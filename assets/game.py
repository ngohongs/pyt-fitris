import random
import pygame as pg
from assets.block import *
from assets.settings import *
import os

game_folder = os.path.dirname(__file__)
image_folder = os.path.join(game_folder, 'image')
font_folder = os.path.join(game_folder, 'font')
sound_folder = os.path.join(game_folder, 'sound')


# Game class
class Game:
    # Gets speed for each level
    @staticmethod
    def get_speed(input_level):
        if input_level < len(FALL_SPEED_TABLE):
            speed = FALL_SPEED_TABLE[input_level]
        elif len(FALL_SPEED_TABLE) <= input_level < 29:
            speed = 2
        else:
            speed = 1
        return speed

    # Generates another block
    # tries not to repeat the same block shape as before
    @staticmethod
    def get_tetromino(prev_tetromino):
        next_tetromino_index = random.randint(0, 7)
        if next_tetromino_index == 7 or Tetromino(next_tetromino_index) == prev_tetromino:
            return Tetromino(random.randint(0, 6))
        return Tetromino(next_tetromino_index)

    # Initialization of game
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        pg.mixer.init()
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.grid = np.zeros(shape=(TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT, TETRIS_TILE_WIDTH, 3), dtype=np.int16)
        self.clock = pg.time.Clock()
        self.score = 0
        self.level = 0
        self.fall_speed = self.get_speed(self.level)
        self.clear_rows = False
        self.pushed_down = False
        self.running = True
        self.spawn_next = False
        self.full_rows = []
        self.clear_iteration = 0
        self.last_update = 0
        self.current_tetromino = Tetromino(random.randint(0, 6))
        self.next_tetromino = self.get_tetromino(self.current_tetromino)
        self.current_tetromino.spawn(self.grid)
        self.frame_count = 0
        self.cleared_levels = 0
        self.playing = False

        self.TITLE_FONT = pg.font.Font(os.path.join(font_folder, 'ka1.ttf'), 90)
        self.HEADER_FONT = pg.font.Font(os.path.join(font_folder, 'ka1.ttf'), 60)
        self.FONT = pg.font.Font(os.path.join(font_folder, 'PressStart2P-Regular.ttf'), 18)

        self.BACKGROUND = pg.image.load(os.path.join(image_folder, 'background.png')).convert()
        self.HEADER_BORDER = pg.image.load(os.path.join(image_folder, 'headerborder.png')).convert()
        self.TABLE = pg.image.load(os.path.join(image_folder, 'table.png')).convert()
        self.BORDER = pg.image.load(os.path.join(image_folder, 'border.png')).convert()

        self.IBLOCK_IMAGE = pg.image.load(os.path.join(image_folder, 'cyan.png'))
        self.JBLOCK_IMAGE = pg.image.load(os.path.join(image_folder, 'orange.png'))
        self.LBLOCK_IMAGE = pg.image.load(os.path.join(image_folder, 'blue.png'))
        self.OBLOCK_IMAGE = pg.image.load(os.path.join(image_folder, 'yellow.png'))
        self.SBLOCK_IMAGE = pg.image.load(os.path.join(image_folder, 'red.png'))
        self.TBLOCK_IMAGE = pg.image.load(os.path.join(image_folder, 'purple.png'))
        self.ZBLOCK_IMAGE = pg.image.load(os.path.join(image_folder, 'green.png'))

        self.NEXT_IBLOCK = pg.image.load(os.path.join(image_folder, 'iblock.png')).convert()
        self.NEXT_JBLOCK = pg.image.load(os.path.join(image_folder, 'jblock.png')).convert()
        self.NEXT_LBLOCK = pg.image.load(os.path.join(image_folder, 'lblock.png')).convert()
        self.NEXT_OBLOCK = pg.image.load(os.path.join(image_folder, 'oblock.png')).convert()
        self.NEXT_SBLOCK = pg.image.load(os.path.join(image_folder, 'sblock.png')).convert()
        self.NEXT_TBLOCK = pg.image.load(os.path.join(image_folder, 'tblock.png')).convert()
        self.NEXT_ZBLOCK = pg.image.load(os.path.join(image_folder, 'zblock.png')).convert()
        self.NEXT = [self.NEXT_IBLOCK, self.NEXT_JBLOCK, self.NEXT_LBLOCK, self.NEXT_OBLOCK, self.NEXT_SBLOCK,
                     self.NEXT_TBLOCK, self.NEXT_ZBLOCK]

        self.IBLOCK_IMAGE = pg.transform.scale(self.IBLOCK_IMAGE, (TILE_SIZE, TILE_SIZE)).convert()
        self.JBLOCK_IMAGE = pg.transform.scale(self.JBLOCK_IMAGE, (TILE_SIZE, TILE_SIZE)).convert()
        self.LBLOCK_IMAGE = pg.transform.scale(self.LBLOCK_IMAGE, (TILE_SIZE, TILE_SIZE)).convert()
        self.OBLOCK_IMAGE = pg.transform.scale(self.OBLOCK_IMAGE, (TILE_SIZE, TILE_SIZE)).convert()
        self.SBLOCK_IMAGE = pg.transform.scale(self.SBLOCK_IMAGE, (TILE_SIZE, TILE_SIZE)).convert()
        self.TBLOCK_IMAGE = pg.transform.scale(self.TBLOCK_IMAGE, (TILE_SIZE, TILE_SIZE)).convert()
        self.ZBLOCK_IMAGE = pg.transform.scale(self.ZBLOCK_IMAGE, (TILE_SIZE, TILE_SIZE)).convert()
        self.IMAGE = [self.IBLOCK_IMAGE, self.JBLOCK_IMAGE, self.LBLOCK_IMAGE, self.OBLOCK_IMAGE, self.SBLOCK_IMAGE,
                      self.TBLOCK_IMAGE, self.ZBLOCK_IMAGE]

        self.DROP = pg.mixer.Sound(os.path.join(sound_folder, 'drop.wav'))
        self.PRESS_START = pg.mixer.Sound(os.path.join(sound_folder, 'press_start.wav'))
        self.ROTATE_ONE = pg.mixer.Sound(os.path.join(sound_folder, 'rotate.wav'))
        self.ROTATE_TWO = pg.mixer.Sound(os.path.join(sound_folder, 'rotate_other.wav'))
        self.MOVE = pg.mixer.Sound(os.path.join(sound_folder, 'move.wav'))
        self.BUTTON = pg.mixer.Sound(os.path.join(sound_folder, 'button.wav'))
        self.TETRIS = pg.mixer.Sound(os.path.join(sound_folder, 'tetris.wav'))
        self.GAME_OVER = pg.mixer.Sound(os.path.join(sound_folder, 'game_over.wav'))
        self.CLEAR = pg.mixer.Sound(os.path.join(sound_folder, 'clear.wav'))

    # Draws surrounding
    def draw_grid(self):
        self.screen.blit(self.BACKGROUND, (0, 0))
        self.screen.blit(self.HEADER_BORDER, (HEADER_BORDER_X, HEADER_BORDER_Y))
        self.screen.blit(self.NEXT[self.next_tetromino.shape],
                         (TETRIS_LEFT_X + TETRIS_WIDTH, TETRIS_LEFT_Y + TILE_SIZE))
        self.screen.blit(self.TABLE, (TETRIS_LEFT_X - 7 * TILE_SIZE, TETRIS_LEFT_Y + TILE_SIZE))
        self.screen.blit(self.BORDER, (TETRIS_LEFT_X - TILE_SIZE, TETRIS_LEFT_Y - TILE_SIZE))
        pg.draw.rect(self.screen, BLACK, (TETRIS_LEFT_X, TETRIS_LEFT_Y, TETRIS_WIDTH, TETRIS_HEIGHT))
        shown_grid = self.grid[SPAWN_TILE_HEIGHT:, :, :]
        for y, row in enumerate(shown_grid):
            for x in range(row.shape[0]):
                if not np.array_equal(shown_grid[y][x], BLANK_TILE):
                    # pg.draw.rect(screen, grid[y][x], (TETRIS_LEFT_X + x * TILE_SIZE,
                    #                                         TETRIS_LEFT_Y + y * TILE_SIZE,
                    #                                         TILE_SIZE, TILE_SIZE))
                    self.screen.blit(self.IMAGE[tetromino_color.index(tuple(shown_grid[y][x]))],
                                     (TETRIS_LEFT_X + x * TILE_SIZE, TETRIS_LEFT_Y + y * TILE_SIZE))

    # Checks if a line in grid is full
    def check_for_clear(self, full_rows_indexes):
        row_index = 3
        for row in self.grid[SPAWN_TILE_HEIGHT:, :, :]:
            for tile in row:
                if np.array_equal(tile, BLANK_TILE):
                    break
            else:
                full_rows_indexes.append(row_index)
            row_index += 1

    # Clear animation of full line
    def clear_full_rows(self, full_rows_indexes, iteration):
        blank_indexes = [TETRIS_TILE_WIDTH // 2 - iteration - 1, TETRIS_TILE_WIDTH // 2 + iteration]
        for row in full_rows_indexes:
            for column in blank_indexes:
                self.grid[row][column] = BLANK_TILE.copy()

    # Pushes remaining lines after clearing down
    def push_down_rows(self, full_rows_indexes):
        self.grid = np.delete(self.grid, full_rows_indexes, axis=0)
        for i in range(len(full_rows_indexes)):
            self.grid = np.insert(self.grid, 0, BLANK_ROW.copy(), axis=0)

    # Tetris animation
    def tetris_animation(self, switch):
        if switch:
            pg.draw.rect(self.screen, WHITE, (TETRIS_LEFT_X, TETRIS_LEFT_Y, TETRIS_WIDTH, TETRIS_HEIGHT))

    # Draws text
    def draw_text(self):
        header = self.HEADER_FONT.render('FITris', 1, WHITE)
        header_rect = header.get_rect(center=(WINDOW_WIDTH // 2, TETRIS_LEFT_Y // 2 + 20))
        self.screen.blit(header, header_rect)
        level_text = self.FONT.render(str(self.level), 1, WHITE)
        score_text = self.FONT.render(str(self.score), 1, WHITE)
        level_rect = level_text.get_rect(
            center=(TETRIS_LEFT_X - 3 * TILE_SIZE - 15, TETRIS_LEFT_Y + 4 * TILE_SIZE + 20))
        score_rect = score_text.get_rect(
            center=(TETRIS_LEFT_X - 3 * TILE_SIZE - 13, TETRIS_LEFT_Y + 8 * TILE_SIZE + 15))
        self.screen.blit(level_text, level_rect)
        self.screen.blit(score_text, score_rect)

    # Start menu
    def start_menu(self):
        pg.mixer.music.load(os.path.join(sound_folder, 'menu.wav'))
        pg.mixer.music.play(-1)
        self.running = True
        while self.running:
            self.clock.tick(10)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.BUTTON.play()
                        self.running = False
                    if event.key == pg.K_SPACE:
                        pg.mixer.music.stop()
                        self.PRESS_START.play()
                        self.frame_count = 0
                        self.running = False
                        self.playing = True
            self.screen.fill(BLACK)
            title = self.TITLE_FONT.render('Fitris', 1, WHITE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 90))
            self.screen.blit(title, title_rect)

            if self.frame_count < 8:
                text = self.FONT.render('press SPACE to start', 1, WHITE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150))
                self.screen.blit(text, text_rect)

            text = self.FONT.render('ARROWS - to control block', 1, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            self.screen.blit(text, text_rect)

            text = self.FONT.render('X/Z - to rotate', 1, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            self.screen.blit(text, text_rect)

            text = self.FONT.render('ESC - to quit FITRIS', 1, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 110))
            self.screen.blit(text, text_rect)

            self.frame_count = (self.frame_count + 1) % 15
            pg.display.update()

        if self.playing:
            self.game_loop()

    # Game
    def game_loop(self):
        pg.mixer.music.load(os.path.join(sound_folder, 'game.wav'))
        pg.mixer.music.play(-1)
        self.running = True
        game_over = False
        while self.running:
            self.clock.tick(FPS)
            # Update
            if self.cleared_levels >= 10:
                self.cleared_levels += -10
                self.level += 1
                self.fall_speed = self.get_speed(self.level)

            if self.clear_iteration == TETRIS_TILE_WIDTH // 2:
                self.clear_iteration = 0
                self.push_down_rows(self.full_rows)
                self.pushed_down = True

            if self.pushed_down:
                self.clear_rows = False
                self.pushed_down = False

            if self.spawn_next and not self.clear_rows:
                for x, y in self.current_tetromino.positions:
                    if 3 < x < 7 and y == SPAWN_TILE_HEIGHT:
                        self.GAME_OVER.play()
                        game_over = True
                        self.running = False
                self.current_tetromino = self.next_tetromino
                self.next_tetromino = self.get_tetromino(self.next_tetromino)
                self.current_tetromino.spawn(self.grid)
                self.full_rows = []
                self.spawn_next = False

            # Auto fall
            if self.frame_count >= self.fall_speed:
                self.frame_count = 0
                if self.current_tetromino.move_down(self.grid):
                    self.DROP.play()
                    self.spawn_next = True

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN and not self.clear_rows:
                    if event.key == pg.K_ESCAPE:
                        self.BUTTON.play()
                        self.quit()
                    if event.key == pg.K_DOWN:
                        self.MOVE.play()
                        self.current_tetromino.move_down(self.grid)
                        self.score += 1
                    # if event.key == pg.K_UP:
                    #     self.current_tetromino.move_up(self.grid)
                    if event.key == pg.K_LEFT:
                        self.MOVE.play()
                        self.current_tetromino.move_left(self.grid)
                    if event.key == pg.K_RIGHT:
                        self.MOVE.play()
                        self.current_tetromino.move_right(self.grid)
                    if event.key == pg.K_x:
                        self.ROTATE_ONE.play()
                        self.current_tetromino.rotate_right(self.grid)
                    if event.key == pg.K_z:
                        self.ROTATE_TWO.play()
                        self.current_tetromino.rotate_left(self.grid)
                    if event.key == pg.K_SPACE:
                        while not self.current_tetromino.move_down(self.grid):
                            self.score += 1
                        self.spawn_next = True
                        self.DROP.play()

            if not self.clear_rows and self.spawn_next:
                self.full_rows = []
                self.check_for_clear(self.full_rows)
                self.score += SCORE[len(self.full_rows)] * (self.level + 1)
                self.cleared_levels += len(self.full_rows)
                if 0 < len(self.full_rows) < 4 and self.clear_iteration == 0:
                    self.CLEAR.play()
                if len(self.full_rows) == 4 and self.clear_iteration == 0:
                    self.TETRIS.play()

            now = pg.time.get_ticks()
            if self.full_rows and now - self.last_update > 55:
                self.last_update = now
                self.clear_rows = True
                self.clear_full_rows(self.full_rows, self.clear_iteration)
                self.clear_iteration += 1

            if self.score > 999999:
                self.score = 999999
            # Render
            self.draw_grid()
            self.draw_text()
            self.tetris_animation(self.clear_iteration % 2 and len(self.full_rows) == 4)
            pg.display.update()
            self.frame_count += 1

        if game_over:
            self.game_over_menu()

    # Game over screen
    def game_over_menu(self):
        pg.mixer.music.load(os.path.join(sound_folder, 'menu.wav'))
        pg.mixer.music.play(-1)
        self.running = True
        while self.running:
            self.clock.tick(10)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.BUTTON.play()
                        self.running = False
                    if event.key == pg.K_SPACE:
                        pg.mixer.music.stop()
                        self.PRESS_START.play()
                        self.frame_count = 0
                        self.running = False
                        self.playing = True

            self.screen.fill(BLACK)

            title = self.TITLE_FONT.render('GAME', 1, WHITE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 120))
            self.screen.blit(title, title_rect)

            title = self.TITLE_FONT.render('OVER', 1, WHITE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            self.screen.blit(title, title_rect)

            text = self.FONT.render('ESC - to quit FITRIS', 1, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 110))
            self.screen.blit(text, text_rect)

            if self.frame_count < 8:
                text = self.FONT.render('press SPACE to restart', 1, WHITE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150))
                self.screen.blit(text, text_rect)

            self.frame_count = (self.frame_count + 1) % 15
            pg.display.update()

        if self.playing:
            self.restart()
            self.game_loop()

    # Resets the game
    def restart(self):
        self.grid = np.zeros(shape=(TETRIS_TILE_HEIGHT + SPAWN_TILE_HEIGHT, TETRIS_TILE_WIDTH, 3), dtype=np.int16)
        self.score = 0
        self.level = 0
        self.fall_speed = self.get_speed(self.level)
        self.clear_rows = False
        self.pushed_down = False
        self.running = True
        self.spawn_next = False
        self.full_rows = []
        self.clear_iteration = 0
        self.last_update = 0
        self.current_tetromino = Tetromino(random.randint(0, 6))
        self.next_tetromino = self.get_tetromino(self.current_tetromino)
        self.current_tetromino.spawn(self.grid)
        self.frame_count = 0
        self.cleared_levels = 0
        self.playing = False

    # Quits game
    def quit(self):
        self.running = False
        self.playing = False
