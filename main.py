import pygame
from body import Body

#Parameters
width = 640
height = 480
bg_colour = (100, 100, 100)
fps = 30
secs_per_msecs = 1000*3600
pixels_per_meter = (2/3*height)/1.5e11

#Coordinate conversions, from (0, 0) being the middle of the screen to (0, 0) being top-left
def convert_coords(centeredx, centeredy):
    px_x = width/2+centeredx*pixels_per_meter
    px_y = height/2-centeredy*pixels_per_meter
    return absx, absy

#Initialization
pygame.init()
screen = pygame.display.set_mode((width, height))
background = pygame.Surface(screen.get_size())
background.fill(bg_colour)
background = background.convert()
screen.blit(background, (0,0))

mainloop = True
playtime = 0
clock = pygame.time.Clock()

#Data
bodies = [Body()]

while mainloop:
    ms = clock.tick(30)
    playtime += ms/1000
    text = "FPS: {0:.1f}   Playtime: {1:.1f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    #Body movement
    for body in bodies:
        centered_coords = body.update_position(ms*secs_per_msecs)
        px_coords = convert_coords(*centered_coords)


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