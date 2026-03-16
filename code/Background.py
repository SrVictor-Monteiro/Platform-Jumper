import pygame

class Background:
    def __init__(self, window):
        # Construtor
        self.window = window
        self.largura = window.get_width()
        self.altura = window.get_height()

        # Camadas do parallax com suas velocidades
        # Quanto menor a velocidade, mais longe parece estar
        self.camadas = [
            {"img": self._carregar("1.png"), "x": 0, "vel": 0.0},  # Céu parado
            {"img": self._carregar("2.png"), "x": 0, "vel": 0.8},  # Nuvens
            {"img": self._carregar("3.png"), "x": 0, "vel": 1.5},  # Colinas atrás
            {"img": self._carregar("5.png"), "x": 0, "vel": 2.0},  # Colinas frente
            {"img": self._carregar("6.png"), "x": 0, "vel": 3.0},  # Árvore menor
            {"img": self._carregar("7.png"), "x": 0, "vel": 3.5},  # Árvore maior
            {"img": self._carregar("8.png"), "x": 0, "vel": 3.5},  # Chão
        ]

    def _carregar(self, nome):
        # Carrega e redimensiona a imagem para o tamanho da janela
        img = pygame.image.load(f"assets/images/backgrounds/nature_1/{nome}").convert_alpha()
        return pygame.transform.scale(img, (self.largura, self.altura))

    def update(self, direcao):
        # Atualiza a posição de cada camada
        # direcao: -1 = esquerda, 1 = direita, 0 = parado
        for camada in self.camadas:
            camada["x"] -= direcao * camada["vel"]

            # Loop infinito — quando sai da tela volta para o início
            if camada["x"] <= -self.largura:
                camada["x"] = 0
            if camada["x"] >= self.largura:
                camada["x"] = 0

    def draw(self):
        # Desenha cada camada duas vezes para criar loop infinito
        for camada in self.camadas:
            self.window.blit(camada["img"], (camada["x"], 0))
            self.window.blit(camada["img"], (camada["x"] + self.largura, 0))
            self.window.blit(camada["img"], (camada["x"] - self.largura, 0))