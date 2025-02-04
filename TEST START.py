"""Здесь можно запустить класс игрок и попробовать им поуправлять"""


from baze import *
from player import *

player = Player(load_image("stay.png"), 2, 2, 50, 50)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move("up")
            elif event.key == pygame.K_LEFT:
                player.move("left")
            elif event.key == pygame.K_RIGHT:
                player.move("right")

    all_sprites.update()
    player.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    player.update()
    pygame.display.flip()
    clock.tick(FPS)