import pygame
import math
from body import Body

#Parameters
width = 800
height = 600
bg_colour = (100, 100, 100)
fps = 60
secs_per_msecs = 3.6e5
pixels_per_meter = (1/4*height)/1.5e11
body_scale = 2000
trace_width = 5

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
    return int(px_abs_x), int(px_abs_y)

#Initialization
pygame.init()
screen = pygame.display.set_mode((width, height))
background = pygame.Surface(screen.get_size())
background.fill(bg_colour)
background = background.convert()

mainloop = True
simtime = 0
clock = pygame.time.Clock()
phase = 0

#Data
bodies = [Body(), Body("Mars", 2.28555e11, 70, 0.0093, 4.5711e11, colour=(180,0,0))]
body_surfaces = [pygame.Surface((px(2*body_scale*body.body_radius), px(2*body_scale*body.body_radius))) for body in bodies]
path_surfaces = [pygame.Surface(pxs(body.major_ax, body.minor_ax)) for body in bodies]

while mainloop:
    ms = clock.tick(fps)
    simtime += ms*secs_per_msecs
    text = """FPS: {0:.1f}   
        Days since start: {1:.0f}   
        Scale: {2:.0f} km/px""".format(clock.get_fps(), simtime/3600/24, 1/pixels_per_meter/1000)
    pygame.display.set_caption(text)
    screen.blit(background, (0,0))

    #Movement
    for body, bsurface, psurface in zip(bodies, body_surfaces, path_surfaces):
        centered_coords = body.update_position(ms*secs_per_msecs)
        px_x, px_y = convert_coords(*centered_coords)

        #Paths
        psurface.set_colorkey((0,0,0))
        pygame.draw.ellipse(psurface, (0, 0, 255), (0, 0, px(body.major_ax), px(body.minor_ax)), 2)
        psurface.convert()
        screen.blit(psurface, convert_coords(-body.c-body.a, body.b))

        #Bodies
        bsurface.set_colorkey((0,0,0))
        pygame.draw.circle(bsurface, body.colour, pxs(body_scale*body.body_radius, body_scale*body.body_radius), px(body_scale*body.body_radius))
        bsurface = bsurface.convert()
        screen.blit(bsurface, (px_x-px(body_scale*body.body_radius), px_y-px(body_scale*body.body_radius)))

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