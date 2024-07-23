import pygame
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# Inicializar Pygame
pygame.init()

# Configuración del juego
ANCHO, ALTO = 300, 300
TAMAÑO_CELDA = 100
LINEA_ANCHO = 15
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Configurar la pantalla
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Tic Tac Toe')

# Configuración del Tablero
tablero = [[' ' for _ in range(3)] for _ in range(3)]
jugador_actual = 'X'

def dibujar_tablero():
    screen.fill(BLANCO)
    for x in range(1, 3):
        pygame.draw.line(screen, NEGRO, (x * TAMAÑO_CELDA, 0), (x * TAMAÑO_CELDA, ALTO), LINEA_ANCHO)
        pygame.draw.line(screen, NEGRO, (0, x * TAMAÑO_CELDA), (ANCHO, x * TAMAÑO_CELDA), LINEA_ANCHO)

def dibujar_movimientos():
    fuente = pygame.font.Font(None, 100)
    for fila in range(3):
        for col in range(3):
            if tablero[fila][col] != ' ':
                texto = fuente.render(tablero[fila][col], True, ROJO if tablero[fila][col] == 'X' else NEGRO)
                rect = texto.get_rect(center=(col * TAMAÑO_CELDA + TAMAÑO_CELDA//2, fila * TAMAÑO_CELDA + TAMAÑO_CELDA//2))
                screen.blit(texto, rect)

def verificar_victoria(jugador):
    for fila in tablero:
        if all([celda == jugador for celda in fila]):
            return True
    for col in range(3):
        if all([tablero[fila][col] == jugador for fila in range(3)]):
            return True
    if all([tablero[i][i] == jugador for i in range(3)]) or all([tablero[i][2-i] == jugador for i in range(3)]):
        return True
    return False

def reiniciar():
    global tablero, jugador_actual
    tablero = [[' ' for _ in range(3)] for _ in range(3)]
    jugador_actual = 'X'

def main():
    global jugador_actual
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                fila, col = y // TAMAÑO_CELDA, x // TAMAÑO_CELDA
                if tablero[fila][col] == ' ':
                    tablero[fila][col] = jugador_actual
                    if verificar_victoria(jugador_actual):
                        print(f"¡Jugador {jugador_actual} gana!")
                        reiniciar()
                    elif all([celda != ' ' for fila in tablero for celda in fila]):
                        print("¡Es un empate!")
                        reiniciar()
                    else:
                        jugador_actual = 'O' if jugador_actual == 'X' else 'X'

        dibujar_tablero()
        dibujar_movimientos()
        pygame.display.update()

if __name__ == "__main__":
    main()
