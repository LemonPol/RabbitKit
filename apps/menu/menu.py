from pathlib import Path
import subprocess
import pygame
import sys

WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Miffy Menu")
center = (WIDTH // 2, HEIGHT // 2)
clock = pygame.time.Clock()

def spawn_program(program, exit_code=0):
    subprocess.run(program, check=True)

app_index = 0
open_lock = False

BASE_DIR = Path(__file__).resolve().parent
RESOURCE_DIR = BASE_DIR / "resources"
IMAGE_DIR = RESOURCE_DIR / "images"
FONT_DIR = RESOURCE_DIR / "fonts"

clock_img = pygame.image.load(
    IMAGE_DIR / "clock.png"
).convert_alpha()

tamagotchi_img = pygame.image.load(
    IMAGE_DIR / "tamagotchi.png"
).convert_alpha()


chat_img = pygame.image.load(
    IMAGE_DIR / "chat.png"
).convert_alpha()


apps = [
    ["Clock", "C:\\Users\\Lemon\\Downloads\\RabbitKit-main\\RabbitKit-main\\apps\\clock\\clock.py"],
    ["Tamagotchi", "C:\\Users\\Lemon\\Downloads\\RabbitKit-main\\RabbitKit-main\\apps\\tamagotchi\\tamagotchi.py"],
    ["Chat", "C:\\Users\\Lemon\\Downloads\\RabbitKit-main\\RabbitKit-main\\apps\\chat\\chat.py"]
]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and not open_lock:
            if event.key == pygame.K_1:
                open_lock = True
                spawn_program(['py.exe', 'C:\\Users\\Lemon\\Downloads\\RabbitKit-main\\RabbitKit-main\\apps\\clock\\clock.py'])
                open_lock = False
            elif event.key == pygame.K_LEFT:
                app_index = (app_index - 1) % len(apps)
                print(apps[app_index][0])
            elif event.key == pygame.K_RIGHT:
                app_index = (app_index + 1) % len(apps)
                print(apps[app_index][0])
            elif event.key == pygame.K_RETURN:
                open_lock = True
                spawn_program(['py.exe', apps[app_index][1]])
                open_lock = False
    
    screen.fill((60, 97, 143))

    if apps[app_index][0] == "Clock":
        screen.blit(clock_img, clock_img.get_rect(center=center))
    elif apps[app_index][0] == "Tamagotchi":
        screen.blit(tamagotchi_img, tamagotchi_img.get_rect(center=center))
    elif apps[app_index][0] == "Chat":
        screen.blit(chat_img, chat_img.get_rect(center=center))
    
    clock.tick(60)
    pygame.display.flip()