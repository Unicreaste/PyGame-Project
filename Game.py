import pygame
import os

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Pirate robbery')
clock = pygame.time.Clock()

background = pygame.image.load('Фон.png').convert()
background = pygame.transform.smoothscale(background, gameDisplay.get_size())

black = (0, 0, 0)
white = (255, 255, 255)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


crashed = False


class ButonPlay(pygame.sprite.Sprite):
    image = load_image('Button_Play.png', color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = ButonPlay.image
        self.rect = self.image.get_rect()
        while True:
            self.rect.topleft = (50, 150)
            if len(pygame.sprite.spritecollide(self, all_sprites, False)) == 1:
                break


class ButonSettings(pygame.sprite.Sprite):
    image = load_image('Button_Settings.png', color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = ButonSettings.image
        self.rect = self.image.get_rect()
        while True:
            self.rect.topleft = (50, 250)
            if len(pygame.sprite.spritecollide(self, all_sprites, False)) == 1:
                break

class ButonExit(pygame.sprite.Sprite):
    image = load_image('Button_Exit.png', color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = ButonExit.image
        self.rect = self.image.get_rect()
        while True:
            self.rect.topleft = (50, 350)
            if len(pygame.sprite.spritecollide(self, all_sprites, False)) == 1:
                break


all_sprites = pygame.sprite.Group()

ButonPlay(all_sprites)
ButonSettings(all_sprites)
ButonExit(all_sprites)

run = True
while run:
    clock.tick(60)

    # handle the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # draw the background
    gameDisplay.blit(background, (0, 0))
    all_sprites.draw(gameDisplay)
    pygame.display.flip()
