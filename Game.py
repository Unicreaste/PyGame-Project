import pygame
import os

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Pirate robbery')
clock = pygame.time.Clock()

pygame.mixer.music.load('Фон(м).mp3')
pygame.mixer.music.set_volume(3)
pygame.mixer.music.play()

background = pygame.image.load('Фон.png').convert()
background = pygame.transform.smoothscale(background, gameDisplay.get_size())

black = (0, 0, 0)
white = (255, 255, 255)
run = True


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
            pass


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

    def get_event(self, event):
        global run
        if self.rect.collidepoint(event.pos):
            SoundButton(all_sprites)
            ButonX(all_sprites)


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
            self.rect.topleft = (450, 250)
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

    def close(self):
        self.kill()


class ButonX(pygame.sprite.Sprite):
    image = load_image('Bt_X.png', color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = ButonX.image
        self.rect = self.image.get_rect()
        while True:
            self.rect.topleft = (650, 50)
            if len(pygame.sprite.spritecollide(self, all_sprites, False)) == 1:
                break

    def get_event(self, event):
        global run
        if self.rect.collidepoint(event.pos):
            self.kill()
            SoundButton.close(self)


all_sprites = pygame.sprite.Group()

ButonPlay(all_sprites)
ButonSettings(all_sprites)
ButonExit(all_sprites)
Name(all_sprites)

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bt in all_sprites:
                bt.get_event(event)

    # draw the background
    gameDisplay.blit(background, (0, 0))
    all_sprites.draw(gameDisplay)
    pygame.display.flip()
