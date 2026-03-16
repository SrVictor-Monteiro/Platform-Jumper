import pygame

class Player:
    def __init__(self, window):
        # Construtor
        self.window = window
        self.x = 100
        self.y = 350
        self.velocidade = 4
        self.vel_y = 0
        self.gravidade = 0.5
        self.no_chao = False  # Controle de pulo
        self.escala = 3  # Tamanho do personagem na tela
        self.frame_atual = 0
        self.contador_frames = 0
        self.velocidade_animacao = 8  # A cada quantos ticks troca o frame
        self.virado = False  # False = direita, True = esquerda
        self.estado = "idle"  # Estado inicial
        self.direcao = 0  # Direção do movimento

        # Spritesheets: (caminho, num_frames, largura_frame, altura_frame)
        self.sprites = {
            "idle": self._carregar("assets/images/player/Idle.png", 4, 42, 29),
            "run":  self._carregar("assets/images/player/Run.png",  6, 42, 28),
            "jump": self._carregar("assets/images/player/Jump.png", 8, 42, 32),
            "hurt": self._carregar("assets/images/player/Hurt.png", 4, 42, 29),
            "death":self._carregar("assets/images/player/Death.png",8, 42, 31),
        }

    def _carregar(self, caminho, num_frames, larg, alt):
        # Carrega e divide o spritesheet em frames individuais
        sheet = pygame.image.load(caminho).convert_alpha()
        frames = []
        for i in range(num_frames):
            frame = sheet.subsurface((i * larg, 0, larg, alt))
            frame = pygame.transform.scale(frame, (larg * self.escala, alt * self.escala))
            frames.append(frame)
        return frames

    def _animar(self):
        # Troca o frame da animação
        self.contador_frames += 1
        if self.contador_frames >= self.velocidade_animacao:
            self.contador_frames = 0
            self.frame_atual = (self.frame_atual + 1) % len(self.sprites[self.estado])

    def move(self):
        # Captura teclas pressionadas
        teclas = pygame.key.get_pressed()
        estado_anterior = self.estado
        self.direcao = 0  # Sem movimento por padrão

        # Movimento horizontal
        if teclas[pygame.K_RIGHT]:
            self.direcao = 1  # Sinaliza para o mundo mover
            self.virado = False
            if self.no_chao:
                self.estado = "run"
        elif teclas[pygame.K_LEFT]:
            self.direcao = -1  # Sinaliza para o mundo mover
            self.virado = True
            if self.no_chao:
                self.estado = "run"
        else:
            if self.no_chao:
                self.estado = "idle"

        # Pulo
        if teclas[pygame.K_SPACE] and self.no_chao:
            self.vel_y = -12  # Força do pulo
            self.no_chao = False
            self.estado = "jump"

        # Gravidade
        self.vel_y += self.gravidade
        self.y += self.vel_y

        # Chão
        if self.y >= 350:
            self.y = 350
            self.vel_y = 0
            self.no_chao = True

        # Reseta frame ao trocar estado
        if self.estado != estado_anterior:
            self.frame_atual = 0
            self.contador_frames = 0

        self._animar()

    def draw(self):
        # Desenha o personagem na tela
        frame = self.sprites[self.estado][self.frame_atual]
        if self.virado:
            frame = pygame.transform.flip(frame, True, False)  # Espelha horizontalmente
        self.window.blit(frame, (self.x, self.y))