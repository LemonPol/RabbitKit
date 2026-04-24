from pathlib import Path
import json
import random
import sys
import time

import pygame


pygame.init()

WIDTH, HEIGHT = 800, 480
FPS = 60

BASE_DIR = Path(__file__).resolve().parent
RESOURCE_DIR = BASE_DIR / "resources"
IMAGE_DIR = RESOURCE_DIR / "images"
FONT_DIR = RESOURCE_DIR / "fonts"
SAVE_FILE = BASE_DIR / "data.json"

BG_COLOR = (60, 97, 143)
WHITE = (255, 255, 255)

MODES = ["Water", "Food", "Play"]
ACTION_MODES = {
    "Water": "Watering",
    "Food": "Feeding",
    "Play": "Playing",
}

ICON_SPACING = 200
ICON_Y = HEIGHT - 100
ICON_BASE_X = WIDTH // 2 - 90

# Snake game variables
GRID_SIZE = 32
SNAKE_MOVE_FRAMES = 10

snake = [(WIDTH // 2 + 16, HEIGHT // 2 + 16)]
snake_direction = (1, 0)
snake_pending_direction = (1, 0)
snake_segment_directions = [(1, 0)]
snake_head = snake[0]
snake_tail = snake[-1]
snake_move_timer = 0
snake_length = 5

FOOD_TYPES = ["Carrot", "Cucumber"]

food = (random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
        random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)
food_type = random.choice(FOOD_TYPES)


screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Miffy Menu")

clock = pygame.time.Clock()
font = pygame.font.Font(FONT_DIR / "DS-DIGI.TTF", 50)


def load_image(name):
    return pygame.image.load(IMAGE_DIR / name).convert_alpha()


images = {
    "clock_center": load_image("clock_center.png"),
    "highlight": load_image("highlight.png"),
    "Water": load_image("water_icon.png"),
    "Food": load_image("food_icon.png"),
    "Play": load_image("play_icon.png"),
    "snake_head": load_image("snake_head.png"),
    "snake_body": load_image("snake_body.png"),
    "snake_corner": load_image("snake_corner.png"),
    "snake_tail": load_image("snake_tail.png"),
    "food_carrot": load_image("food_carrot.png"),
    "food_cucumber": load_image("food_cucumber.png"),
}


stats = {
    "water": 25,
    "food": 25,
    "play": 25,
}

mode = None
selected_index = 1  # Food


def quit_game():
    save_game()
    pygame.quit()
    sys.exit()


def save_game():
    save_data = {
        **stats,
        "timestamp": time.time(),
    }

    with open(SAVE_FILE, "w") as file:
        json.dump(save_data, file, indent=4)


def load_game():
    if not SAVE_FILE.exists():
        return

    with open(SAVE_FILE, "r") as file:
        save_data = json.load(file)

    for key in stats:
        stats[key] = save_data.get(key, stats[key])

    apply_offline_decay(save_data.get("timestamp"))


def apply_offline_decay(timestamp):
    if timestamp is None:
        return

    time_elapsed = time.time() - timestamp
    frames_passed = time_elapsed * FPS

    expected_decrease = frames_passed / 172811
    variance = expected_decrease ** 0.5 if expected_decrease > 0 else 0

    for key in stats:
        decrease = int(expected_decrease + random.gauss(0, variance))
        stats[key] = max(0, stats[key] - decrease)


def update_passive_decay():
    seed = random.randint(0, 500)

    if seed == 0:
        stats["water"] -= 1
    elif seed == 10:
        stats["food"] -= 1
    elif seed == 100:
        stats["play"] -= 1

    for key in stats:
        stats[key] = max(0, stats[key])


def handle_idle_input():
    global mode, selected_index

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if event.type != pygame.KEYDOWN:
            continue

        if event.key == pygame.K_ESCAPE:
            quit_game()
        elif event.key == pygame.K_RIGHT:
            selected_index = (selected_index + 1) % len(MODES)
        elif event.key == pygame.K_LEFT:
            selected_index = (selected_index - 1) % len(MODES)
        elif event.key == pygame.K_RETURN:
            selected_mode = MODES[selected_index]
            mode = ACTION_MODES[selected_mode]

            if mode == "Feeding":
                reset_feeding_game()


def handle_feeding_input():
    x_movement = 0
    y_movement = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if event.type != pygame.KEYDOWN:
            continue

        if event.key == pygame.K_ESCAPE:
            quit_game()

        if event.key == pygame.K_LEFT:
            x_movement -= 1
        elif event.key == pygame.K_RIGHT:
            x_movement += 1
        elif event.key == pygame.K_UP:
            y_movement -= 1
        elif event.key == pygame.K_DOWN:
            y_movement += 1

    return x_movement, y_movement

def icon_position(index):
    x = ICON_BASE_X + (index - 1) * ICON_SPACING
    return x, ICON_Y


def draw_stats():
    y = 10

    for label, value in stats.items():
        text = font.render(f"{label.title()}: {value}", True, WHITE)
        screen.blit(text, (10, y))
        y += 40


def draw_menu():
    highlight_pos = icon_position(selected_index)
    screen.blit(images["highlight"], highlight_pos)

    for index, mode_name in enumerate(MODES):
        screen.blit(images[mode_name], icon_position(index))


def draw_idle():
    screen.fill(BG_COLOR)

    draw_stats()
    draw_menu()

    center = (WIDTH // 2, HEIGHT // 2)
    clock_rect = images["clock_center"].get_rect(center=center)
    screen.blit(images["clock_center"], clock_rect)

    pygame.display.flip()


def run_idle_mode():
    handle_idle_input()
    update_passive_decay()
    draw_idle()
    clock.tick(FPS)


def run_watering_mode():
    pass

def reset_feeding_game():
    global snake, snake_direction, snake_pending_direction
    global snake_segment_directions, snake_head, snake_tail
    global snake_move_timer, snake_length

    start_x = (WIDTH // 2) // GRID_SIZE * GRID_SIZE
    start_y = (HEIGHT // 2) // GRID_SIZE * GRID_SIZE

    snake = [(start_x - i * GRID_SIZE, start_y) for i in range(5)]
    snake_direction = (1, 0)
    snake_pending_direction = (1, 0)
    snake_segment_directions = [(1, 0)] * len(snake)
    snake_head = snake[0]
    snake_tail = snake[-1]
    snake_move_timer = 0
    snake_length = 5

def spawn_food():
    while True:
        new_food = (
            random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
            random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
        )

        if new_food not in snake:
            return new_food


def end_feeding_game():
    global mode
    mode = None


def step_feeding_game(x_movement, y_movement):
    global snake, snake_direction, snake_pending_direction
    global snake_segment_directions, snake_head, snake_tail
    global snake_move_timer, snake_length
    global food, food_type
    global stats, SNAKE_MOVE_FRAMES

    if x_movement != 0 or y_movement != 0:
        new_direction = (x_movement, y_movement)

        if new_direction != (-snake_direction[0], -snake_direction[1]):
            snake_pending_direction = new_direction

    snake_move_timer += 1

    if snake_move_timer < SNAKE_MOVE_FRAMES:
        return

    snake_move_timer = 0
    snake_direction = snake_pending_direction

    old_head = snake[0]
    new_head = (
        old_head[0] + snake_direction[0] * GRID_SIZE,
        old_head[1] + snake_direction[1] * GRID_SIZE,
    )

    # Hit edge = game over
    if (
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT
    ):
        end_feeding_game()
        return

    # Hit self = game over
    if new_head in snake:
        end_feeding_game()
        return

    snake.insert(0, new_head)
    snake_segment_directions.insert(0, snake_direction)

    if new_head == food:
        snake_length += 1
        stats["food"] = min(25, stats["food"] + 1)
        SNAKE_MOVE_FRAMES = max(5, SNAKE_MOVE_FRAMES - 1)
        food = spawn_food()
        food_type = random.choice(FOOD_TYPES)

    while len(snake) > snake_length:
        snake.pop()
        snake_segment_directions.pop()

    snake_head = snake[0]
    snake_tail = snake[-1]

DIR_TO_ANGLE = {
    (1, 0): 0,      # right
    (0, -1): 90,    # up
    (-1, 0): 180,   # left
    (0, 1): 270,    # down
}


def direction_between(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]

    return (
        dx // GRID_SIZE,
        dy // GRID_SIZE,
    )


def draw_sprite_centered(sprite, grid_pos, angle=0):
    rotated = pygame.transform.rotate(sprite, angle)
    rect = rotated.get_rect(center=(
        grid_pos[0] + GRID_SIZE // 2,
        grid_pos[1] + GRID_SIZE // 2,
    ))
    screen.blit(rotated, rect)


def corner_angle(dir_to_prev, dir_to_next):
    dirs = {dir_to_prev, dir_to_next}

    if dirs == {(1, 0), (0, 1)}:
        return 0
    if dirs == {(0, 1), (-1, 0)}:
        return 270
    if dirs == {(-1, 0), (0, -1)}:
        return 180
    if dirs == {(0, -1), (1, 0)}:
        return 90

    return 0

def draw_feeding_game():
    screen.fill(BG_COLOR)

    for index, segment in enumerate(snake):

        if len(snake) < 2:
            pygame.display.flip()
            return

        if index == 0:
            direction = direction_between(snake[1], snake[0])
            draw_sprite_centered(images["snake_head"], segment, DIR_TO_ANGLE[direction])

        elif index == len(snake) - 1:
            direction = direction_between(snake[-2], snake[-1])
            draw_sprite_centered(images["snake_tail"], segment, DIR_TO_ANGLE[direction])

        else:
            dir_to_prev = direction_between(segment, snake[index - 1])
            dir_to_next = direction_between(segment, snake[index + 1])

            if dir_to_prev == dir_to_next or dir_to_prev == (-dir_to_next[0], -dir_to_next[1]):
                # straight body
                if dir_to_prev[0] != 0:
                    angle = 0
                else:
                    angle = 90

                draw_sprite_centered(images["snake_body"], segment, angle)

            else:
                # corner body
                angle = corner_angle(dir_to_prev, dir_to_next)
                draw_sprite_centered(images["snake_corner"], segment, angle)

    food_sprite = images[f"food_{food_type.lower()}"]
    draw_sprite_centered(food_sprite, food)

    pygame.display.flip()

def run_feeding_mode():
    x_movement, y_movement = handle_feeding_input()
    step_feeding_game(x_movement, y_movement)
    draw_feeding_game()
    clock.tick(FPS)


def run_playing_mode():
    pass

load_game()

while True:
    if mode == "Watering":
        run_watering_mode()
    elif mode == "Feeding":
        run_feeding_mode()
    elif mode == "Playing":
        run_playing_mode()
    else:
        run_idle_mode()