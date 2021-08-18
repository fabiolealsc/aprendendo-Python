import pygame
pygame.init()


TELA_WIDTH = 800
TELA_HEIGHT = 600

BLK_WIDTH = TELA_WIDTH // 40
BLK_HEIGHT = TELA_HEIGHT // 20

tela = pygame.display.set_mode((TELA_WIDTH, TELA_HEIGHT))


def load_image(img_set, x, y):
    img_orig = img_set.subsurface((x, y), (16, 16))
    img = pygame.transform.scale(img_orig, (BLK_WIDTH, BLK_HEIGHT))
    return img


mapa = [
    "pppppppppppppppppppppppppppppppppppppppp",
    "p                                      p",
    "p     ppppp                            p",
    "p                                      p",
    "p       pppp pppppp                    p",
    "p                pp                    p",
    "p                pp                    p",
    "p          pppppppp                    p",
    "p                                      p",
    "p    pppppp                            p",
    "p                                      p",
    "p                pppppp                p",
    "p                                      p",
    "p                                      p",
    "p                                      p",
    "p           pppppppppppppp             p",
    "p                                      p",
    "p                                      p",
    "p                                      p",
    "pppppppppppppppppppppppppppppppppppppppp"

]

tiles = pygame.image.load("./ClassicRPG_Sheet.png").convert_alpha()
img_grama = load_image(tiles, 7*16, 16)
img_parede = load_image(tiles, 17*16, 0)


class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.vel_x = 0
        self.vel_y = 0
        car_img_1 = load_image(tiles, 0, 0)
        car_img_2 = load_image(tiles, 16, 0)
        car_img_3 = load_image(tiles, 32, 0)
        self.img_list = [car_img_1, car_img_2, car_img_3]
        self.image = car_img_1
        self.img_idx = 0
        self.rect = pygame.Rect((32, 32), (BLK_WIDTH, BLK_HEIGHT))

    def update(self):
        self.image = self.img_list[int(self.img_idx)]
        self.img_idx += 0.1
        if self.img_idx >= len(self.img_list):
            self.img_idx = 0
        self.rect.move_ip(self.vel_x, self.vel_y)

    def processar_evento(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_d:
                self.vel_x = 1
            if e.key == pygame.K_a:
                self.vel_x = -1
            if e.key == pygame.K_s:
                self.vel_y = 1
            if e.key == pygame.K_w:
                self.vel_y = -1
        if e.type == pygame.KEYUP:
            if e.key in [pygame.K_d, pygame.K_a]:
                self.vel_x = 0
            if e.key in [pygame.K_w, pygame.K_s]:
                self.vel_y = 0


heroi = Personagem()
grupo_heroi = pygame.sprite.Group(heroi)

while True:
    for id_linha, linha in enumerate(mapa):
        for id_coluna, caractere in enumerate(linha):
            x = id_coluna * BLK_WIDTH
            y = id_linha * BLK_HEIGHT
            if caractere == "p":
                tela.blit(img_parede, (x, y))
            else:
                tela.blit(img_grama, (x, y))

    grupo_heroi.draw(tela)
    grupo_heroi.update()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        heroi.processar_evento(event)



