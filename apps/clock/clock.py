import sys
import pygame
from pathlib import Path
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Miffy Clock")
center = (WIDTH // 2, HEIGHT // 2)

clock = pygame.time.Clock()

BASE_DIR = Path(__file__).resolve().parent
RESOURCE_DIR = BASE_DIR / "resources"
IMAGE_DIR = RESOURCE_DIR / "images"
FONT_DIR = RESOURCE_DIR / "fonts"

clock_center_img = pygame.image.load(
    IMAGE_DIR / "clock_center.png"
).convert_alpha()

minute_hand_img = pygame.image.load(
    IMAGE_DIR / "minute_hand.png"
).convert_alpha()

hour_hand_img = pygame.image.load(
    IMAGE_DIR / "hour_hand.png"
).convert_alpha()

font = pygame.font.Font(
    FONT_DIR / "DS-DIGI.TTF",
    50
)

def blit_rotated(image, angle, pos):
    rotated = pygame.transform.rotozoom(image, -angle, 1)
    rect = rotated.get_rect(center=pos)
    screen.blit(rotated, rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    now = datetime.now()

    seconds = now.second
    minutes = now.minute + seconds / 60
    hours = (now.hour % 12) + minutes / 60

    minute_angle = minutes * 6
    hour_angle = hours * 30

    day_text = now.strftime("%A, %B %d")
    time_text = now.strftime("%I:%M %p")

    screen.fill((60, 97, 143))

    blit_rotated(minute_hand_img, minute_angle, center)
    blit_rotated(hour_hand_img, hour_angle, center)

    screen.blit(clock_center_img, clock_center_img.get_rect(center=center))

    date_surface = font.render(day_text, True, (255, 255, 255))
    screen.blit(date_surface, (10, HEIGHT - 60))

    time_surface = font.render(time_text, True, (255, 255, 255))
    time_rect = time_surface.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))
    screen.blit(time_surface, time_rect)

    pygame.display.flip()
    clock.tick(60)