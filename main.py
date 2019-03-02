import pygame
from body import Body

#Parameters
width = 640
height = 480
bg_colour = (100, 100, 100)
fps = 60
secs_per_msecs = 1000*3600
pixels_per_meter = (2/3*height)/1.5e11

#Conversion from pixels to meters
def pixel(meters):
    return int(meters*pixels_per_meter)
def pixels(centeredx, centeredy):
    return int(centeredx*pixels_per_meter), int(centeredy*pixels_per_meter)
#Coordinate conversions, from (0m, 0m) being the middle of the screen to (0px, 0px) being top-left
def convert_coords(centeredx, centeredy):
    px_cent_x, px_cent_y = pixels(centeredx, centeredy)
    px_abs_x = width/2+px_cent_x
    px_abs_y = height/2-px_cent_y
    return px_abs_x, px_abs_y

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
body_surfaces = [pygame.Surface((pixel(2*body.r), 2*pixel(2*body.r))) for body in bodies]

while mainloop:
    ms = clock.tick(fps)
    playtime += ms/1000
    text = "FPS: {0:.1f}   Playtime: {1:.1f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    #Body movement
    for body, surface in zip(bodies, body_surfaces):
        centered_coords = body.update_position(ms*secs_per_msecs)
        px_x, px_y = convert_coords(*centered_coords)
        pygame.draw.circle(surface, (0, 0, 255), pixels(body.r, body.r), pixel(body.r))
        surface = surface.convert()
        screen.blit(surface, (px_x-pixel(body.r), px_y-pixel(body.r)))

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