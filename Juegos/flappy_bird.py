import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO_PANTALLA = 400
ALTO_PANTALLA = 600

# Colores
COLOR_FONDO = (135, 206, 235)  # Azul cielo
COLOR_TEXTO = (255, 255, 255)  # Blanco

# Crear la pantalla del juego
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Flappy Bird')

# Reloj para controlar la tasa de fotogramas
reloj = pygame.time.Clock()

# Fuente para el texto
fuente = pygame.font.SysFont(None, 48)

# Clase para el pájaro
class Pajaro:
    def __init__(self):
        self.imagen = pygame.image.load('Juegos/utils/img/flappy_bird.png')  # Cargar imagen del pájaro
        self.imagen = pygame.transform.scale(self.imagen, (40, 40))  # Escalar la imagen a 40x40 píxeles
        self.rect = self.imagen.get_rect(center=(50, ALTO_PANTALLA // 2))
        self.velocidad = 0
        self.gravedad = 0.5
        self.salto = -10

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def mover(self):
        self.velocidad += self.gravedad
        self.rect.y += self.velocidad

    def saltar(self):
        self.velocidad = self.salto

# Clase para las tuberías
class Tuberia:
    def __init__(self, x):
        self.x = x
        self.ancho = 70
        self.altura = random.randint(150, 400)
        self.velocidad = 3

    def dibujar(self, pantalla):
        # Parte superior de la tubería
        pygame.draw.rect(pantalla, (34, 139, 34), (self.x, 0, self.ancho, self.altura))  # Verde
        # Parte inferior de la tubería
        pygame.draw.rect(pantalla, (34, 139, 34), (self.x, self.altura + 150, self.ancho, ALTO_PANTALLA))

    def mover(self):
        self.x -= self.velocidad

    def colision(self, pajaro):
        # Verificar colisión con el pájaro
        if pajaro.rect.colliderect(pygame.Rect(self.x, 0, self.ancho, self.altura)) or \
           pajaro.rect.colliderect(pygame.Rect(self.x, self.altura + 150, self.ancho, ALTO_PANTALLA - self.altura - 150)):
            return True
        return False

def pantalla_inicio():
    # Pantalla de inicio
    pantalla.fill(COLOR_FONDO)
    texto = fuente.render('Pulsa Espacio para Jugar', True, COLOR_TEXTO)
    texto_rect = texto.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
    pantalla.blit(texto, texto_rect)
    pygame.display.update()

    # Esperar a que el jugador presione la tecla de espacio
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    esperando = False

# Función principal del juego
def juego():
    pajaro = Pajaro()
    tuberias = [Tuberia(ANCHO_PANTALLA + 100)]
    puntuacion = 0

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pajaro.saltar()

        # Mover y dibujar el pájaro
        pajaro.mover()

        # Dibujar el fondo
        pantalla.fill(COLOR_FONDO)

        # Dibujar el pájaro
        pajaro.dibujar(pantalla)

        # Mover y dibujar las tuberías
        for tuberia in tuberias:
            tuberia.mover()
            tuberia.dibujar(pantalla)

            # Verificar colisión
            if tuberia.colision(pajaro):
                corriendo = False

            # Contar puntuación
            if tuberia.x + tuberia.ancho < pajaro.rect.x and not hasattr(tuberia, 'puntuado'):
                puntuacion += 1
                tuberia.puntuado = True

        # Añadir nuevas tuberías
        if tuberias[-1].x < ANCHO_PANTALLA - 300:
            tuberias.append(Tuberia(ANCHO_PANTALLA))

        # Eliminar tuberías que ya no se ven
        if tuberias[0].x < -tuberias[0].ancho:
            tuberias.pop(0)

        # Verificar si el pájaro toca el suelo o el techo
        if pajaro.rect.y + pajaro.rect.height > ALTO_PANTALLA or pajaro.rect.y < 0:
            corriendo = False

        # Dibujar la puntuación en pantalla
        texto_puntuacion = fuente.render(f'Puntuación: {puntuacion}', True, COLOR_TEXTO)
        pantalla.blit(texto_puntuacion, (10, 10))

        # Actualizar pantalla
        pygame.display.update()

        # Controlar la tasa de fotogramas
        reloj.tick(60)

    print(f"Puntuación final: {puntuacion}")

# Ejecutar la pantalla de inicio
pantalla_inicio()

# Ejecutar el juego
while True:
    juego()
    pantalla_inicio()  # Volver a la pantalla de inicio después de que el juego termine
