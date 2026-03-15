import pygame

#Setup
pygame.init()
LARGURA, ALTURA = 800, 500
window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Froggy Jump")
clock = pygame.time.Clock()
FPS = 60

#Cores
VERDE = (34, 200, 68)
AZUL_CLARO = (135, 206, 235)
BRANCO = (255, 255, 255)
PRETO = (255, 0, 0)

print("Setup OK!")

#Loop principal
while True:
    clock.tick(FPS) #limita o jogo a 60 frames por segundo

    #Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    #Desenho
    window.fill(AZUL_CLARO)
    pygame.draw.rect(window, VERDE, (0, 450, 800, 50)) #chão verde

    pygame.display.flip() # atualiza a tela
