import os
import pygame
import random

# eine Gruppe für alle sprite Objekte
all_object = pygame.sprite.Group()


class Settings(object):
    def __init__(self):
        self.width = 800
        self.height = 600
        self.fps = 60
        self.title = "Bewegte Ball"
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.file_path, "images")

    def get_dim(self):
        return (self.width, self.height)


class Football(pygame.sprite.Sprite):  # Football Objekt vererbt dem sprite-Objekt
    def __init__(self, pygame, settings):
        super(Football, self).__init__()
        self.settings = settings
        self.pygame = pygame
        self.image = self.pygame.image.load(os.path.join(self.settings.images_path, "football.png")).convert_alpha()
        self.image = self.pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = (settings.width - self.rect.width) // 2
        self.rect.y = (settings.height - self.rect.height) // 2

    def update(self):
        self.bewegen()
        self.beschraenken_bewegung()

    def bewegen(self):  # es beweget den ball (betmap) und springt ihn
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

    def random_position(self):
        self.rect.x = random.randrange(0, self.settings.width - self.rect.width)
        self.rect.y = random.randrange(0, self.settings.height - self.rect.height)

    def beschraenken_bewegung(self):  # beschringt die bewgung des ball auf der hintergrund des Bild
        if self.rect.x >= self.settings.width - self.rect.width:
            self.rect.x = self.settings.width - self.rect.width
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= self.settings.height - self.rect.height:
            self.rect.y = self.settings.height - self.rect.height
        if self.rect.y <= 0:
            self.rect.y = 0


class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.get_dim())
        self.pygame.display.set_caption(self.settings.title)
        self.background = self.pygame.image.load(os.path.join(self.settings.images_path, "background.jpg")).convert()
        self.background_rect = self.background.get_rect()
        self.clock = pygame.time.Clock()
        self.football = Football(pygame, settings)
        all_object.add(self.football)
        self.done = False

    def run(self):
        while not self.done:
            self.clock.tick(self.settings.fps)
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.done = True
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self.football.random_position()

            self.screen.blit(self.background, self.background_rect)
            all_object.update()  # es ruft die Methode (update) der sprite Objekte und aktualisiert ihr
            all_object.draw(self.screen)  # es ruft die Methode (draw) der sprite Objekte und stell ihr dar
            self.pygame.display.flip()


if __name__ == '__main__':
    settings = Settings()
    pygame.init()
    game = Game(pygame, settings)
    game.run()

    pygame.quit()
