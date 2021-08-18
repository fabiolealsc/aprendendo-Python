import pygame, sys

pygame.init()


WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))
pygame.display.set_caption('Testando Meus Conhecimentos')

clock = pygame.time.Clock()

moving_right = False
moving_left = False
x = 25
y = 0
player_y_moment = 0
air_timer = 0
tiles = [40, 40]
map = [0, 0, 0, 0, 0, 0, 0, 0, 0,
       1, 1, 1, 1, 1, 1, 1, 1, 1,]
cont = 0

while True:


    clock.tick(60)
    display.fill((0,0,0))
    player = pygame.draw.rect(display, (255, 255, 255), (x, y, 25, 25))
    y += player_y_moment
    player_y_moment += 0.2
    if player_y_moment > 3:
        player_y_moment = 3
    if moving_right:
        x += 4
    elif moving_left:
        x -= 4

    if y > 175:
        y = 175
        air_timer = 0
    else:
        air_timer += 1
    tile = pygame.Rect(tiles[0], tiles[1], 20, 20)
    for rect in map:

        if cont <= 9:
            if rect == 0:
                pygame.draw.rect(display, (255, 255, 255), tile, 16, 16)
                tiles[0] += 16
            if rect == 1:
                pygame.draw.rect(display, (255, 0, 255), tile, 0, 0)
            cont += 1
        else:
            tiles[1] = 40
            if rect == 0:
                pygame.draw.rect(display, (255, 255, 255), tile, 0, 0)

                tiles[0] += 40
            if rect == 1:
                tiles[1] = 40
                pygame.draw.rect(display, (255, 0, 255), tile, 36, 32)




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving_right = True
            elif event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_w and air_timer < 6:
                player_y_moment = -6
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving_right = False
            elif event.key == pygame.K_a:
                moving_left = False
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()

