import pygame
from body import Body

#Parameters
width = 800
height = 600
bg_colour = (100, 100, 100)
fps = 60
secs_per_msecs = 3.6e5
pixels_per_meter = (1/3*height)/1.5e11
body_scale = 1000

#Conversion from pixels to meters
def px(meters):
    return int(meters*pixels_per_meter)
def pxs(centeredx, centeredy):
    return px(centeredx), px(centeredy)
#Coordinate conversions, from (0m, 0m) being the middle of the screen to (0px, 0px) being top-left
def convert_coords(centeredx, centeredy):
    px_cent_x, px_cent_y = pxs(centeredx, centeredy)
    px_abs_x = width/2+px_cent_x
    px_abs_y = height/2-px_cent_y
    return px_abs_x, px_abs_y

#Initialization
pygame.init()
screen = pygame.display.set_mode((width, height))
background = pygame.Surface(screen.get_size())
background.fill(bg_colour)
background = background.convert()

mainloop = True
simtime = 0
clock = pygame.time.Clock()

#Data
bodies = [Body()]
body_surfaces = [pygame.Surface((px(2*body_scale*body.body_radius), px(2*body_scale*body.body_radius))) for body in bodies]

while mainloop:
    ms = clock.tick(fps)
    simtime += ms*secs_per_msecs
    text = """FPS: {0:.1f}   
        Milliseconds since start: {1:.5f}   
        Scale: {2:.0f} km/px""".format(clock.get_fps(), simtime*1000, 1/pixels_per_meter/1000)
    pygame.display.set_caption(text)
    screen.blit(background, (0,0))

    #Body movement
    for body, surface in zip(bodies, body_surfaces):
        centered_coords = body.update_position(ms*secs_per_msecs)
        px_x, px_y = convert_coords(*centered_coords)
        surface.set_colorkey((0,0,0))
        pygame.draw.circle(surface, body.colour, pxs(body_scale*body.body_radius, body_scale*body.body_radius), px(body_scale*body.body_radius))
        surface = surface.convert()
        screen.blit(surface, (px_x-px(body.body_radius), px_y-px(body.body_radius)))

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