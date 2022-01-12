import pygame
import os
import webbrowser

pygame.init()

display_width = 800
display_height = 600
MOVE_SPEED = 7

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Pirate robbery')
clock = pygame.time.Clock()

pygame.mixer.music.load('Фон(м).mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

background = pygame.image.load('Корабль.png').convert()
background = pygame.transform.smoothscale(background, gameDisplay.get_size())

run = True

loc_x, loc_y = 400, 400
pers_im = pygame.image.load('data/Player.png')


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


class Name(pygame.sprite.Sprite):
    image = load_image('Name.png', color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Name.image
        self.rect = self.image.get_rect()
        while True:
            self.rect.topleft = (350, 30)
            if len(pygame.sprite.spritecollide(self, all_sprites, False)) == 1:
                break

    def get_event(self, event):
        global run
        if self.rect.collidepoint(event.pos):
            pass


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

    def get_event(self, event):
        global run
        if self.rect.collidepoint(event.pos):
            runs()


class ButonExit(pygame.sprite.Sprite):
    image = load_image('Button_Exit.png', color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = ButonExit.image
        self.rect = self.image.get_rect()
        while True:
            self.rect.topleft = (50, 250)
            if len(pygame.sprite.spritecollide(self, all_sprites, False)) == 1:
                break

    def get_event(self, event):
        global run
        if self.rect.collidepoint(event.pos):
            run = False


class SoundButton(pygame.sprite.Sprite):
    image = load_image('S_ON.png', color_key=-1)
    image2 = load_image('S_OFF.png', color_key=-1)
    image3 = load_image('S_ON.png', color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = SoundButton.image
        self.rect = self.image.get_rect()
        while True:
            self.rect.topleft = (700, 500)
            if len(pygame.sprite.spritecollide(self, all_sprites, False)) == 1:
                break

    def get_event(self, event):
        global run
        if self.rect.collidepoint(event.pos):
            if pygame.mixer.music.get_volume() > 0:
                pygame.mixer.music.set_volume(0)
                self.image = self.image2
            else:
                pygame.mixer.music.set_volume(10)
                self.image = self.image3


all_sprites = pygame.sprite.Group()
ButonPlay(all_sprites)
ButonExit(all_sprites)
Name(all_sprites)
SoundButton(all_sprites)

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bt in all_sprites:
                bt.get_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                loc_y -= 25
            if event.key == pygame.K_s:
                loc_y += 25
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                loc_x -= 25
            if event.key == pygame.K_d:
                loc_x += 25

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(pers_im, (loc_x, loc_y))
    all_sprites.draw(gameDisplay)
    pygame.display.flip()
