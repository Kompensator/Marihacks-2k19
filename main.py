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
global G, sun_mass
G = 6.673e-11
sun_mass = 1.989e30

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

launch_prepped = False
mainloop = True
simtime = 0
clock = pygame.time.Clock()
phase = 0

#Data
bodies = [Body(), Body("Mars", 2.28555e11, 70, 0.0093, 4.5711e11, colour=(180,0,0))]
spaceship = Body(name="Spaceship")        # creating an empty object i guess
body_surfaces = [pygame.Surface((px(2*body_scale*body.body_radius), px(2*body_scale*body.body_radius))) for body in bodies]
path_surfaces = [pygame.Surface(pxs(body.major_ax, body.minor_ax)) for body in bodies]
spaceship_surface = pygame.Surface(pxs(spaceship.major_ax, spaceship.minor_ax))

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

    if(phase == 0):
        pass
    elif(phase == 1):
        pass
    elif(phase == 2):
        if launch_prepped == False:
            # sets the spaceship's position to be equal to earth, but with diff major axis and ecc
            spaceship.r = bodies[0].r
            spaceship.angle = bodies[0].angle
            spaceship.velocity = bodies[0].velocity
            spaceship.a, spaceship.eccentricity = bodies[0].get_transfer_ellipse(bodies[1])
            delta_v = math.sqrt(G*sun_mass*(2/spaceship.r - 1/spaceship.a)) - math.sqrt(G*sun_mass/spaceship.r)
            spaceship.energy = bodies[0].energy
            spaceship.energy += delta_v**2/2
            spaceship.areal_v = ((G*G*sun_mass*sun_mass*(spaceship.eccentricity**2 - 1))/(8*spaceship.energy))**0.5
            spaceship.colour = (183,183,183)
            spaceship.q = spaceship.a*(1 - spaceship.eccentricity**2)
            launch_prepped = True

            spaceship_surface.set_colorkey((0,0,0))
            pygame.draw.circle(spaceship_surface, spaceship.colour, pxs(body_scale*spaceship.body_radius, body_scale*spaceship.body_radius), px(body_scale*spaceship.body_radius))
            spaceship_surface = spaceship_surface.convert()
            # centered_coords = spaceship.update_position(ms*secs_per_msecs)
            px_x, px_y = convert_coords(math.cos(math.radians(spaceship.angle))*spaceship.r, math.sin(math.radians(spaceship.angle))*spaceship.r)
            screen.blit(spaceship_surface, (px_x-px(body_scale*spaceship.body_radius), px_y-px(body_scale*spaceship.body_radius)))
            print (spaceship.r)
        else:
            spaceship_surface.set_colorkey((0,0,0))
            pygame.draw.circle(spaceship_surface, spaceship.colour, pxs(body_scale*spaceship.body_radius, body_scale*spaceship.body_radius), px(body_scale*spaceship.body_radius))
            spaceship_surface = spaceship_surface.convert()
            centered_coords = spaceship.update_position(ms*secs_per_msecs)
            print (spaceship.r)
            px_x, px_y = convert_coords(*centered_coords)
            screen.blit(spaceship_surface, (px_x-px(body_scale*spaceship.body_radius), px_y-px(body_scale*spaceship.body_radius)))

    

    elif(phase == 3):
        pass
    else:
        raise ValueError("Phase out of range!")


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