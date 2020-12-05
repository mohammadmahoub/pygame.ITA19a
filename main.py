import os
import pygame


class Settings(object):
    def __init__(self):
        self.width = 800
        self.height = 600
        self.fps = 60
        self.title = "rabbit"
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.file_path, "images")

    def get_dim(self):
        return (self.width, self.height)


class Football(object):
    def __init__(self, pygame, settings):
        self.settings = settings
        self.pygame = pygame
        self.image = self.pygame.image.load(os.path.join(self.settings.images_path, "football.png")).convert_alpha()
        self.image = self.pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = (settings.width - self.rect.width) // 2
        self.rect.y = (settings.height - self.rect.height) // 2

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.get_dim())
        self.pygame.display.set_caption(self.settings.title)
        self.background = self.pygame.image.load(os.path.join(self.settings.images_path,"background.jpg")).convert()
        self.background_rect = self.background.get_rect()

        self.clock = pygame.time.Clock()
        self.mario = Football(pygame, settings)
        self.done = False

    def run(self):
        while not self.done:
            self.clock.tick(self.settings.fps)
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
            #self.screen.fill((0, 0, 0))
            self.screen.blit(self.background,self.background_rect)
            self.mario.draw(self.screen)
            self.pygame.display.flip()


if __name__ == '__main__':
    settings = Settings()
    pygame.init()
    game = Game(pygame, settings)
    game.run()

    pygame.quit()
