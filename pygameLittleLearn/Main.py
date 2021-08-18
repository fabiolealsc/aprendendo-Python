# IMPORTAÇÃO DE BIBLIOTECAS########################

import pygame  # IMPORTA O PYGAME
import sys  # IMPORTA AS FUNCOES DE SISTEMA
from pygame.locals import *  # IMPORTA OS LOCAIS DO PYGAME

###################################################

pygame.init()  ##INICIANDO O PYGAME

#######CRIANDO A JANELA DO PYGAME##################

WINDOW_SIZE = (900, 600)  # TAMANHO DA JANELA
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # CRIANDO A JANELA COM O TAMANHO PREDEFINIDO

display = pygame.Surface((600, 400))  # CRIA UMA TELA PARA COLOCAR OS OBJETOS

pygame.display.set_caption("My Pygame")  # MUDA O TITULO DA JANELA

####################################################

#######DEFINIÇÕES###################################

clock = pygame.time.Clock()  # DEFINE A VARIAVEL CLOCK COM A FUNÇÃO CLOCK DO PYGAME.TIME

dirt_image = pygame.image.load('dirt.png')  # COLOCA A IMAGEM PRA DENTRO DE DIRT
TILE_SIZE = dirt_image.get_width()  # DEFINE O TAMANHO DOS TILES

grass_image = pygame.image.load('grass.png')  # COLOCA A IMAGEM PRA DENTRO DE GRASS
grass_esq = pygame.image.load('grass_virado_esquerda.png')
grass_cse = pygame.image.load('grass_cse.png')
grass_csd = pygame.image.load('grass_csd.png')
grass_cid = pygame.image.load('grass_cid.png')
grass_cie = pygame.image.load('grass_cie.png')
####################################################

# GERANDO MAPA ATRAVEZ DE LISTA###############################################################################


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = load_map('map')

#############################################################################################################

global animations_frames
animations_frames = {}


def load_animations(path, frame_durations):     #[7,7]
    global animations_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc)
        animations_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


animation_database = {}
animation_database['run'] = load_animations('player_animations/run', [7, 7])
animation_database['idle'] = load_animations('player_animations/idle', [7, 7, 40])

player_action = 'idle'
player_frame = 0
player_flip = False


#############################################################################################################

# DEFINE O TESTE DE COLISÃO ENTRE DOIS OBJETOS, RETORNANDO UMA LISTA DESSAS COLISÕES


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


######################################################################################

# DEFINE EM QUE LADO ESTA OCORRENDO A COLISÃO DO PERSONAGEM


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True

    return rect, collision_types


#################################################################################

moving_right = False  # VARIAVEL PARA DIREITA
moving_left = False  # VARIAVEL PARA ESQUERDA

player_y_momentum = 0  # VARIAVEL PARA GRAVIDADE
air_timer = 0  # DEFINE UM VARIAVEL PARA VER SE O PERSONAGEM TA NO AR

true_scroll = [0, 0]
# DEFINE A BOX DE COLISÂO DO PLAYER ##################################

player_rect = pygame.Rect(100, 100, 11, 29)  # DEFINE A BOX DE COLISÃO DO PLAYER

background_objects = [[0.25, [120 * 3, 10 * 3, 70 * 3, 400 * 3]], [0.25, [280 * 3, 30 * 3, 40 * 3, 400 * 3]],
                      [0.5, [30 * 3, 40 * 3, 40 * 3, 400 * 3]], [0.5, [130 * 3, 90 * 3, 100 * 3, 400 * 3]],
                      [0.5, [300 * 3, 80 * 3, 120 * 3, 400 * 3]]]

######################################################################

while True:  ########LOOPING DO JOGO##################################

    display.fill((119, 119, 255))  # PINTA O FUNDO DO DISPLAY

    true_scroll[0] += (player_rect.x - true_scroll[0] - 250) / 10  # DEFINE A ROLAGEM DA TELA NO X
    true_scroll[1] += (player_rect.y - true_scroll[1] - 200) / 10  # DEFINE A ROLAGEM DA TELA NO Y
    scroll = true_scroll.copy()  # COPIA PRA DENTRO DE SCROLL O TRUE SCROLL
    scroll[0] = int(scroll[0])  # FAZ COM QUE A POSIÇÃO X DO SCROLL VIRE INTEIRO
    scroll[1] = int(scroll[1])  # FAZ COM QUE A POSIÇÃO Y DO SCROLL VIRE INTEIRO

    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 250, 900, 600))  # DESENHA FUNDO

    #####################################################################
    ### DESENHA RETANGULOS NO FUNDO COM OS PARAMETROS PREDEFINIDOS E SISTEMA DE SCROLL

    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0],
                               background_object[1][1] - scroll[1] * background_object[0], background_object[1][2],
                               background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (4, 222, 150), obj_rect)
        else:
            pygame.draw.rect(display, (9, 91, 85), obj_rect)

    #####################################################################################

    # DESENHANDO O MAPA NA TELA#######################################

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                display.blit(grass_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '3':
                display.blit(grass_esq, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '4':
                display.blit(grass_cse, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '5':
                display.blit(grass_csd, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '6':
                display.blit(grass_cid, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '7':
                display.blit(grass_cie, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    ##################################################################

    # MOVIMENTOS FRENTE E TRAS##########################################

    player_movement = [0, 0]

    if moving_right:
        player_movement[0] += 2

    if moving_left:
        player_movement[0] -= 2

    # EFEITO DE QUEDA DO PLAYER#######################################

    player_movement[1] += player_y_momentum  # A LOCALIZAÇÃO Y DO PLAYER VAI RECEBER ELE MAIS O PLAYER MOMENTO
    player_y_momentum += 0.2  # VAI SEMPRE ACRESCENTAR 0.2 NO PLAYER MOMENTO
    if player_y_momentum > 6:  # SE O MOMENTO FOR MAIOR QUE 6 ELE RECEBE 6, LIMITANDO A VELOCIDADE DE QUEDA
        player_y_momentum = 6

    if player_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = False
    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')
    if player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = True

    ##################################################################
    ######################################################################

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:  # SE OCORRER COLISÃO COM SOLO ENTÃO O TEMPO NO AR ZERA E O MOMENTO DO Y TB.
        player_y_momentum = 0
        air_timer = 0
    else:  # SE O BONECO NÃO ESTIVER COLIDINDO COM O SOLO O TEMPO NO AR AUMENTA
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animations_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img, player_flip, False), (
        player_rect.x - scroll[0], player_rect.y - scroll[1]))  # DESENHA O PLAYER NO DISPLAY NA POSIÇÃO rect+scroll

    # TESTANDO OS EVENTOS NO PYGAME#########################################

    for event in pygame.event.get():  # CRIA "EVENT" DO TIPO PEGANDO EVENTOS NO PYGAME
        if event.type == pygame.QUIT:  # SE O TIPO DO EVENTO FOR PYGAME SAIR ENTAO
            pygame.quit()  # FECHA PYGAME
            sys.exit()  # FECHA TUDO

        ########################################################################

        # VERIFICA SE AS TECLAS FORAM PRECIONADAS###########################

        if event.type == pygame.KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True

            # VERIFICA SE A TECLA DO PULO FOI PRECIONADA E FAZ PULAR O TEMPO NO AR FOR MENOR QUE 6##

            if event.key == K_w:
                if air_timer < 6:
                    player_y_momentum = -6

            ########################################################################################

        ####################################################################

        # VERIFICA SE AS TECLAS FORAM LARGADAS##############################

        if event.type == pygame.KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False

        ####################################################################

    surf = pygame.transform.scale(display, WINDOW_SIZE)  # DEFINE O SURFACE COMO O DISPLAY AUMENTADO O TAMANHO
    screen.blit(surf, (0, 0))  # DESENHA O SURFACE NO SCREEN
    pygame.display.update()  # ATUALIZA A TELA
    clock.tick(60)  # DEFINE O TEMPO QUE O LOOPING RODA, EM MS(COLOCANDO O TEMPO NO OBJECT TICK DA FUNÇÃO CLOCK)
