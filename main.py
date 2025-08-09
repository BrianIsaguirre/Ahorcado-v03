import pygame
import sys
import os
from faker import Faker

pygame.init()

#Configuración de ventana
WIDTH, HEIGHT = 1000, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ahorcado con Stickman")

#Colores y fuentes del texto
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LETTER_FONT = pygame.font.SysFont('arial', 30)
WORD_FONT = pygame.font.SysFont('arial', 50)

#Texto bienvenida
def mostrar_bienvenida():
    win.fill(WHITE)
    bienvenida = WORD_FONT.render("Bienvenido al ahorcado de la granja", True, BLACK)
    win.blit(bienvenida, ((WIDTH - bienvenida.get_width()) // 2, HEIGHT // 2 - bienvenida.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)  # 2 segundos

#Generar palabra secreta
fake = Faker()
word_list = ["gallina", "vaca", "caballo", "oveja", "perro", "gato", "toro", "yegua", "burro", "cerdo", "pato", "conejo", "cuyo"]
palabra_secreta = fake.random_element(elements=word_list)
letras_adivinadas = []
errores = 0
max_errores = 6

#Cargar imágenes
images = [
    pygame.image.load(os.path.join("images", "man1.png")),
    pygame.image.load(os.path.join("images", "man2.png"))
]

#Posiciones base
muñeco_x = 50   #Posicion del stickman
muñeco_y = 50
texto_x = WIDTH - 350  #Posicion del texto
final_text_x = WIDTH // 2 + 100  #Posicion del texto final

def draw(perdiste=False):
    win.fill(WHITE)

    #Mostrar la imagen: normal o de perdida
    if perdiste:
        win.blit(images[1], (muñeco_x, muñeco_y))
    else:
        win.blit(images[0], (muñeco_x, muñeco_y))

    #Mostrar errores
    err_text = LETTER_FONT.render(f"Errores: {errores}/{max_errores}", True, BLACK)
    win.blit(err_text, (texto_x, 100))

    #Mostrar palabra
    display_word = " ".join([l if l in letras_adivinadas else "_" for l in palabra_secreta])
    text = WORD_FONT.render(display_word, True, BLACK)
    win.blit(text, (texto_x, 200))

    pygame.display.update()

#Bienvenida del jugador
mostrar_bienvenida()

#Lógica del juego
corriendo = True
juego_terminado = False
perdio = False

while corriendo:
    draw(perdiste=perdio)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        elif event.type == pygame.KEYDOWN and not juego_terminado:
            letra = event.unicode.lower()
            if letra.isalpha() and letra not in letras_adivinadas:
                letras_adivinadas.append(letra)
                if letra not in palabra_secreta:
                    errores += 1

    #Comprobar condiciones
    if not juego_terminado:
        if errores >= max_errores:
            mensaje = "Perdiste"
            juego_terminado = True
            perdio = True
        elif all(l in letras_adivinadas for l in palabra_secreta):
            mensaje = "¡Ganaste!"
            juego_terminado = True

    #Mostrar mensaje final
    if juego_terminado:
        draw(perdiste=perdio)
        pygame.time.delay(500)
        win.fill(WHITE)

        #Mostrar imagen final
        if perdio:
            win.blit(images[1], (muñeco_x, muñeco_y))
        else:
            win.blit(images[0], (muñeco_x, muñeco_y))

        #Posicion del texto de la palabra correcta
        msg = WORD_FONT.render(mensaje, True, BLACK)
        sub = WORD_FONT.render(f"La palabra era: {palabra_secreta}", True, BLACK)
        win.blit(msg, (final_text_x, HEIGHT//2 - msg.get_height()))
        win.blit(sub, (final_text_x, HEIGHT//2 + 20))

        pygame.display.update()
        pygame.time.delay(3000)
        corriendo = False

pygame.quit()
sys.exit()
