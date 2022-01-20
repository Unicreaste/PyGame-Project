import os
import random
import pygame

pygame.init()

display_width = 1100
display_height = 600
MOVE_SPEED = 7

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Pirate robbery')
clock = pygame.time.Clock()

pygame.mixer.music.load('Фон(м).mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()

background = pygame.image.load('Фон.png').convert()
background = pygame.transform.smoothscale(background, gameDisplay.get_size())

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Ship", "кОРАБЛЬ.png")),
           pygame.image.load(os.path.join("Assets/Ship", "кОРАБЛЬ.png"))]
JUMPING = [pygame.image.load(os.path.join("Assets/Ship", "Gj1.png")),
           pygame.image.load(os.path.join("Assets/Ship", "Gj2.png")),
           pygame.image.load(os.path.join("Assets/Ship", "Gj3.png"))]

SMALL_LANDS = [pygame.image.load(os.path.join("Assets/lands", "Островок.png")),
               pygame.image.load(os.path.join("Assets/lands", "Островок2.png")),
               pygame.image.load(os.path.join("Assets/lands", "Островок3.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

SAN = pygame.image.load(os.path.join("Assets/Other", "San.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Море.png"))


class Ship:
    X_POS = 80
    Y_POS = 290
    JUMP_VEL = 8.5

    def __init__(self):
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.ship_run = True
        self.ship_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.ship_run:
            self.run()
        if self.ship_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.ship_jump:
            self.ship_run = False
            self.ship_jump = True
        elif userInput[pygame.K_DOWN] and not self.ship_jump:
            self.ship_run = False
            self.ship_jump = False
        elif not (self.ship_jump or userInput[pygame.K_DOWN]):
            self.ship_run = True
            self.ship_jump = False

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img[self.step_index // 5]
        if self.ship_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.ship_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class San:
    def __init__(self):
        self.x = random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = SAN
        self.width = self.image.get_width()

    def update(self):
        self.x += game_speed // 200
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, -50))



class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 290


def play():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Ship()
    cloud = Cloud()
    san = San()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill('#58A8CB')
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_LANDS))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        san.draw(SCREEN)
        san.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                play()


loc_x, loc_y = 400, 400
run2 = True


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
        global run2
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
        global run2
        if self.rect.collidepoint(event.pos):
            run2 = False
            menu(death_count=0)


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
        global run2
        if self.rect.collidepoint(event.pos):
            run2 = False


class SoundButton(pygame.sprite.Sprite):
    image = load_image('S_OFF.png', color_key=-1)
    image2 = load_image('S_OFF.png', color_key=-1)
    image3 = load_image('S_ON.png', color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = SoundButton.image
        self.rect = self.image.get_rect()
        while True:
            self.rect.topleft = (1000, 500)
            if len(pygame.sprite.spritecollide(self, all_sprites, False)) == 1:
                break

    def get_event(self, event):
        global run2
        if self.rect.collidepoint(event.pos):
            if pygame.mixer.music.get_volume() > 0:
                pygame.mixer.music.set_volume(0)
                self.image = self.image2
            else:
                pygame.mixer.music.set_volume(10)
                self.image = self.image3


while run2:
    all_sprites = pygame.sprite.Group()
    SoundButton(all_sprites)
    ButonPlay(all_sprites)
    ButonExit(all_sprites)
    Name(all_sprites)
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run2 = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bt in all_sprites:
                bt.get_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                loc_y -= 25
            if event.key == pygame.K_s:
                loc_y += 25
            if event.type == pygame.K_a:
                loc_x -= 25
            if event.key == pygame.K_d:
                loc_x += 25

    gameDisplay.blit(background, (0, 0))
    all_sprites.draw(gameDisplay)
    pygame.display.flip()
