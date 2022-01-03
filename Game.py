import pygame

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

background = pygame.image.load('Фон.png').convert()
background = pygame.transform.smoothscale(background, gameDisplay.get_size())

black = (0, 0, 0)
white = (255, 255, 255)

crashed = False



x = round(display_width * 0.001)
y = round(display_height * 0.01)

run = True
while run:
    clock.tick(60)

    # handle the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update the game states and positions of objects
    keys = pygame.key.get_pressed()
    x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
    y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5
    x = x % gameDisplay.get_width()
    y = y % gameDisplay.get_height()

    # draw the background
    gameDisplay.blit(background, (0, 0))

    # draw the entire scene

    # update the display
    pygame.display.flip()