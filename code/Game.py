import pygame
from code.Menu import Menu
from code.Player import Player
from code.Background import Background
from code.Enemy import Enemy

class Game:
    def __init__(self):
        # Construtor
        pygame.init()
        self.LARGURA = 800
        self.ALTURA = 500
        self.window = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption("Bunny Jumper")
        self.clock = pygame.time.Clock()
        self.FPS = 60

    def run(self):
        menu = Menu(self.window)
        menu.run()

        player = Player(self.window)
        background = Background(self.window)

        # Inimigos posicionados ao longo da fase
        inimigos = [
            Enemy(self.window, 600),
            Enemy(self.window, 1000),
            Enemy(self.window, 1400),
        ]

        while True:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            player.move()
            background.update(player.direcao)

            for inimigo in inimigos:
                inimigo.update(player.direcao)

            # Remove inimigos que já desapareceram
            inimigos = [i for i in inimigos if i.visivel]

            # Hitbox do player
            player_rect = pygame.Rect(player.x + 20, player.y + 10, 80, 80)

            for inimigo in inimigos:
                if not inimigo.vivo:
                    continue
                # Hitbox do inimigo
                inimigo_rect = pygame.Rect(inimigo.x + 20, inimigo.y + 10, 180, 40)
                if player_rect.colliderect(inimigo_rect):
                    # Pulo na cabeça — player caindo e acima do inimigo
                    if player.vel_y > 0 and player.y + (29 * 3) < inimigo.y + 20:
                        inimigo.morrer()
                        player.vel_y = -8  # Quica após matar
                    else:
                        print("Player tomou dano!")

            background.draw()
            for inimigo in inimigos:
                inimigo.draw()
            player.draw()
            pygame.display.flip()