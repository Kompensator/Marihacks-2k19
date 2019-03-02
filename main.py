import pygame

#Parameters
screen_size = (640, 480)
bg_colour = (0,0,0)
fps = 30

#Initialization
pygame.init()
screen = pygame.display.set_mode(screen_size)
background = pygame.Surface(screen.get_size())
background.fill(bg_colour)
background = background.convert()
screen.blit(background, (0,0))

mainloop = True
playtime = 0
clock = pygame.time.Clock()

while mainloop:
    ms = clock.tick(30)
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    #Event handling
    for event in pygame.event.get():
        #Quit button
        if event.type == pygame.QUIT: 
            mainloop = False
        #Keypresses
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False

    #Display changes
    pygame.display.flip()

#Quit
pygame.quit()