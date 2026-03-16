import pygame

class Menu:
    def __init__(self, window):
        self.window = window
        self.largura = window.get_width()
        self.altura = window.get_height()

        # Cores
        self.PRETO = (0, 0, 0)
        self.BRANCO = (255, 255, 255)
        self.AMARELO = (255, 215, 0)

        # Fonte
        self.fonte_titulo = pygame.font.Font("assets/fonts/pixel.ttf", 48)
        self.fonte_menu = pygame.font.Font("assets/fonts/pixel.ttf", 20)
        self.fonte_controles = pygame.font.Font("assets/fonts/pixel.ttf", 14)

        # Background
        self.bg = pygame.image.load("assets/images/backgrounds/bg.png")
        self.bg = pygame.transform.scale(self.bg, (self.largura, self.altura))

        # Música
        pygame.mixer.music.load("assets/sounds/menu-music.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # -1 = loop infinito

        self.ativo = True

    def run(self):
        while self.ativo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.ativo = False  # sai do menu e inicia o jogo
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            # Desenha background
            self.window.blit(self.bg, (0, 0))

            # Título
            titulo = self.fonte_titulo.render("BUNNY Jumper", True, self.AMARELO)
            self.window.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 100))

            # Instrução
            iniciar = self.fonte_menu.render("Pressione ENTER para jogar", True, self.BRANCO)
            self.window.blit(iniciar, (self.largura // 2 - iniciar.get_width() // 2, 250))

            # Controles
            controles = [
                "CONTROLES:",
                "Setas <- -> : Mover",
                "SPACE : Pular",
                "ESC : Sair",
            ]
            for i, linha in enumerate(controles):
                texto = self.fonte_controles.render(linha, True, self.BRANCO)
                self.window.blit(texto, (self.largura // 2 - texto.get_width() // 2, 350 + i * 30))

            pygame.display.flip()