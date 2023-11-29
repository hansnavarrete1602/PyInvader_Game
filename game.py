# formula colisión: D=sqrt((x2-x1)^2 + (y2-y2)^2)
import sys
import time
import pygame
import random
import math
from pygame import mixer
import io

# inicializar pygame
pygame.init()

# crear pantalla
pantalla = pygame.display.set_mode((800, 600))  # W H

# titulo e icono
pygame.display.set_caption('Invasion Espacial')
icono = pygame.image.load('extraterrestre.png')  # 32px
pygame.display.set_icon(icono)
fondo = pygame.image.load('cielo-3d-espacio-abstracto-estrellas-nebulosa.jpg')

# agregar musica
mixer.music.load('dark-underworld-144813.mp3')
mixer.music.set_volume(.2)
mixer.music.play(-1)  # -1 se repite siempre


# convertir fuentes a bytes
def fuente_bytes(font):
    with open(font, 'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)


f1_bytes = fuente_bytes('Moghes.otf')
f2_bytes = fuente_bytes('Geoform-ExtraBold.otf')

# variables del jugador
img_jugador = pygame.image.load('robotica.png')  # 64px
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0
jugador_y_cambio = 0

# variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('nave-extraterrestre.png'))  # 64px
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(0, 120))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# variables de la bala
balas = []
img_bala = pygame.image.load('bala.png')  # 32px
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 2
bala_visible = False

# puntaje
puntaje = 0
fuente = pygame.font.Font(f1_bytes, 40)
texto_x = 10
texto_y = 10

# texto final del juego
fuente_final = pygame.font.Font(f2_bytes, 100)

# plus
tiempo_cooldown = 0
TIEMPO_COOLDOWN_DESEADO = 0.5  # 0.5 segundos de cooldown


# crear texto final
def texto_final():
    mi_fuente_final = fuente_final.render('Game Over', True, (255, 0, 0))
    pantalla.blit(mi_fuente_final, (100, 225))


# función mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'Score: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# function jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# function enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# function disparar_bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x+16, y+10))


# función detectar colisiones
def hay_colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    if distancia < 30:
        return True
    else:
        return False


# loop del juego
se_ejecuta = True
while se_ejecuta:
    pantalla.blit(fondo, (0, 0))
    # pantalla.fill((205, 144, 228))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            se_ejecuta = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            tiempo_actual = pygame.time.get_ticks() / 1000  # Tiempo actual en segundos
            if event.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            elif event.key == pygame.K_RIGHT:
                jugador_x_cambio = +1
            elif event.key == pygame.K_SPACE and tiempo_actual - tiempo_cooldown >= TIEMPO_COOLDOWN_DESEADO:
                sonido_bala = mixer.Sound('laser-gun-shot-sound-future-sci-fi-lazer-wobble-chakongaudio-174883.mp3')
                sonido_bala.set_volume(.5)
                sonido_bala.play()
                nueva_bala = {
                    'x': jugador_x,
                    'y': jugador_y,
                    'vel': -5
                }
                balas.append(nueva_bala)
                tiempo_cooldown = tiempo_actual  # Reinicia el tiempo de cooldown
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    jugador_x += jugador_x_cambio
    # mantener dentro de los bordes
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    for e in range(cantidad_enemigos):
        # fin del juego
        if enemigo_y[e] > 436:
            mixer.music.stop()
            sonido_final = mixer.Sound('dead-walking-mp3-14594.mp3')
            sonido_final.set_volume(.2)
            sonido_final.play()
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            jugador_y = 1000
            texto_final()
            balas.clear()
            time.sleep(5)
            break

        enemigo_x[e] += enemigo_x_cambio[e]
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = (enemigo_x_cambio[e])
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -(enemigo_x_cambio[e])
            enemigo_y[e] += enemigo_y_cambio[e]

        # colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala['x'], bala['y'])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound('voice-fire-55076.mp3')
                sonido_colision.set_volume(.4)
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                enemigo_x_cambio[e] = enemigo_x_cambio[e] + 0.2
        enemigo(enemigo_x[e], enemigo_y[e], e)

    # movimiento bala
    for bala in balas:
        bala["y"] += bala["vel"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)
    pygame.display.update()





'''
elif event.key == pygame.K_UP:
    jugador_y_cambio = -0.7
elif event.key == pygame.K_DOWN:
    jugador_y_cambio = +0.7


elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
    jugador_y_cambio = 0


if jugador_y <= 190:
    jugador_y = 190
elif jugador_y >= 536:
    jugador_y = 536

'''