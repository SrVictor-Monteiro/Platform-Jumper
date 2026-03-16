import pygame
import random

class Enemy:
    def __init__(self, window, x):
        # Construtor
        self.window = window
        self.x = x
        self.y = 370
        self.vel_y = 0
        self.gravidade = 0.5
        self.no_chao = True
        self.velocidade = 2
        self.direcao = -1
        self.vivo = True
        self.visivel = True
        self.estado = "walk"
        self.frame_atual = 0
        self.contador_frames = 0
        self.velocidade_animacao = 8
        self.escala = 2
        self.timer_morte = 0

        # Temporizadores aleatórios de comportamento
        self.timer_pulo = random.randint(60, 180)
        self.timer_direcao = random.randint(60, 180)

        # Spritesheets
        self.sprites = {
            "idle": self._carregar("assets/images/enemies/Idle.png", 8, 81, 31),
            "walk": self._carregar("assets/images/enemies/Walk.png", 8, 118, 33),
            "jump": self._carregar("assets/images/enemies/Jump.png", 13, 122, 62),
            "hurt": self._carregar("assets/images/enemies/Hurt.png", 6, 114, 35),
            "dead": self._carregar("assets/images/enemies/Dead.png", 3, 102, 27),
        }

    def _carregar(self, caminho, num_frames, larg, alt):
        # Divide o spritesheet em frames individuais
        sheet = pygame.image.load(caminho).convert_alpha()
        frames = []
        for i in range(num_frames):
            frame = sheet.subsurface((i * larg, 0, larg, alt))
            frame = pygame.transform.scale(frame, (larg * self.escala, alt * self.escala))
            frames.append(frame)
        return frames

    def _animar(self):
        # Avança o frame da animação
        self.contador_frames += 1
        if self.contador_frames >= self.velocidade_animacao:
            self.contador_frames = 0
            if self.estado == "dead":
                # Para no último frame da morte
                if self.frame_atual < len(self.sprites["dead"]) - 1:
                    self.frame_atual += 1
            else:
                self.frame_atual = (self.frame_atual + 1) % len(self.sprites[self.estado])

    def update(self, camera_direcao):
        # Acompanha o movimento do mundo (parallax)
        self.x -= camera_direcao * 3.5

        if not self.vivo:
            self.timer_morte -= 1
            if self.timer_morte <= 0:
                self.visivel = False
            self._animar()
            return

        # Pulo aleatório
        self.timer_pulo -= 1
        if self.timer_pulo <= 0 and self.no_chao:
            self.vel_y = -10
            self.no_chao = False
            self.estado = "jump"
            self.frame_atual = 0
            self.timer_pulo = random.randint(60, 180)

        # Mudança de direção aleatória
        self.timer_direcao -= 1
        if self.timer_direcao <= 0:
            self.direcao *= -1
            self.timer_direcao = random.randint(60, 180)

        # Movimento horizontal
        self.x += self.velocidade * self.direcao

        # Gravidade
        self.vel_y += self.gravidade
        self.y += self.vel_y

        # Colisão com o chão
        CHAO = 370
        if self.y >= CHAO:
            self.y = CHAO
            self.vel_y = 0
            self.no_chao = True
            if self.estado == "jump":
                self.estado = "walk"
                self.frame_atual = 0

        self._animar()

    def morrer(self):
        # Inicia animação de morte e timer para desaparecer
        self.vivo = False
        self.estado = "dead"
        self.frame_atual = 0
        self.contador_frames = 0
        self.timer_morte = 60

    def draw(self):
        if not self.visivel:
            return
        frame = self.sprites[self.estado][self.frame_atual]
        # Espelha o sprite conforme a direção
        if self.direcao == 1:
            frame = pygame.transform.flip(frame, True, False)
        self.window.blit(frame, (self.x, self.y))