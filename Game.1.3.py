import os
import pygame
import random

all_sprites = pygame.sprite.Group()
all_rocks = pygame.sprite.Group()
all_players = pygame.sprite.Group()


class Settings(object):
    def __init__(self):
        self.width = 1200
        self.height = 800
        self.fps = 60
        self.title = "Mario"
        self.punkte = 0
        self.TIME_EVENT = pygame.USEREVENT + 1
        self.SPEED_UP = 0;
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.images_path = os.path.join(self.file_path, "images")

    def get_dim(self):
        return (self.width, self.height)


class Mario(pygame.sprite.Sprite):
    def __init__(self, pygame, settings):
        super(Mario, self).__init__()
        self.settings = settings
        self.pygame = pygame
        self.image = self.pygame.image.load(os.path.join(self.settings.images_path, "mario.png")).convert_alpha()
        self.image = self.pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = (settings.width - self.rect.width) // 2
        self.rect.y = (settings.height - self.rect.height) // 2

    def istPositionFrei(self, x, y):
        mario = Mario(pygame, settings)
        mario.rect.x = x
        mario.rect.y = y
        return not pygame.sprite.spritecollideany(mario, all_rocks)

    def jump(self):
        while (True):
            x = random.randrange(0, self.settings.width - self.rect.width)
            y = random.randrange(0, self.settings.height - self.rect.height)
            if (self.istPositionFrei(x, y)):
                self.rect.x = x
                self.rect.y = y
                break

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
        if keys[pygame.K_RIGHT]:
            self.rect.x += 3
        if keys[pygame.K_DOWN]:
            self.rect.y += 3
        if keys[pygame.K_UP]:
            self.rect.y -= 3


class Punktstand(pygame.sprite.Sprite):
    def __init__(self, pygame, settings):
        super(Punktstand, self).__init__()
        self.settings = settings
        self.pygame = pygame
        self.font = pygame.font.SysFont(None, 40)
        self.image = self.font.render(f'punkte: {self.settings.punkte}', True, (255, 0, 0))
        self.image = self.pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def update(self):
        self.image = self.font.render(f'punkte: {self.settings.punkte}', True, (255, 0, 0))


class Rock(pygame.sprite.Sprite):
    def __init__(self, pygame, settings):
        super(Rock, self).__init__()
        self.settings = settings
        self.pygame = pygame
        self.image = self.pygame.image.load(os.path.join(self.settings.images_path, "rock.png")).convert_alpha()
        size = random.randrange(20, 60)
        self.image = self.pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, settings.width - self.rect.width)
        self.rect.y = random.randrange(-10, 20)
        self.geschwindigkeit = random.randrange(1, 2)

    def generate_rock(self):
        while (True):
            rock = Rock(pygame, settings)
            if (not pygame.sprite.spritecollideany(rock, all_rocks)):
                all_rocks.add(rock)
                all_sprites.add(all_rocks)
                break
            rock.kill()

    def update(self):
        self.rect.y += self.geschwindigkeit + self.settings.SPEED_UP
        if (self.rect.y + self.rect.height >= self.settings.height):
            self.settings.punkte += 1
            print(f'{self.settings.punkte}')
            self.kill()
            self.generate_rock()


class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.get_dim())
        self.pygame.display.set_caption(self.settings.title)
        self.clock = pygame.time.Clock()
        self.mario = Mario(pygame, settings)
        # self.punkte = Punktstand(pygame,settings)
        pygame.time.set_timer(self.settings.TIME_EVENT, 3000)
        all_players.add(self.mario)
        all_rocks.add(Rock(pygame, settings))
        all_sprites.add(Punktstand(pygame, settings))
        all_sprites.add(all_rocks, all_players)
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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.mario.jump()
                if event.type == self.settings.TIME_EVENT:
                    for rock in range(random.randrange(1, 3)):
                        all_rocks.add(Rock(pygame, settings))
                        all_sprites.add(all_rocks)
                        self.settings.SPEED_UP += 1

            self.screen.fill((100, 100, 100))
            if (pygame.sprite.spritecollideany(self.mario, all_rocks)):
                self.done = True

            all_sprites.update()
            # self.mario.draw(self.screen)
            all_sprites.draw(self.screen)
            self.pygame.display.flip()


if __name__ == '__main__':
    settings = Settings()
    pygame.init()
    game = Game(pygame, settings)
    game.run()

    pygame.quit()
