import pygame
import math
import os
from body import Body
from sys import argv


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
descent_speed = 1e-1
earth_size = 6378100

#Args
planet = argv[1].lower()
if planet == "mars":
    otherbody = Body("Mars", 2.28555e11, 90, 0.0093, 4.5711e11, colour=(180,0,0))
    pixels_per_meter = (1/4*height)/1.5e11
elif planet == "jupiter":
    otherbody = Body("Jupiter", 778e9, 90, 0.048, 778.57e9, body_radius=1e7, colour=(255,178,102))
    pixels_per_meter = (1/6*height)/1.5e11
# elif planet == "venus":
#    otherbody = Body("Venus", 108e9, 160, 0.007, 2*108.6e9, earth_size*0.7, colour=(238, 215, 135))
elif planet == "saturn":
    otherbody = Body("Saturn", 1443e9, 160, 0.0565, 2886e9, 8e6, colour=(247, 203, 59))
    pixels_per_meter = (1/20*height)/1.5e11
else:
    print("Invalid planet \""+planet+"\". Please enjoy Mars")
    otherbody = Body("Mars", 2.28555e11, 90, 0.0093, 4.5711e11, colour=(180,0,0))
    pixels_per_meter = (1/4*height)/1.5e11

def px(meters):
    """converting from meters to pixels
    """
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
pygame.font.init()
screen = pygame.display.set_mode((width, height))
background = pygame.Surface(screen.get_size()).convert()
bg_image = pygame.image.load(os.path.join("data", "stars_bg_4_3.png")).convert()
bg_image = pygame.transform.scale(bg_image, (width, height))
#background.fill(bg_colour)
#background = background.convert()

launch_prepped = False
mainloop = True
simtime = 0
clock = pygame.time.Clock()
phase = 0

#Data
bodies = [Body(), otherbody]

spaceship = Body(name="Spaceship", body_radius=1594525)        # creating an empty object i guess
body_surfaces = [pygame.Surface((px(2*body_scale*body.body_radius), px(2*body_scale*body.body_radius))) for body in bodies]
path_surfaces = [pygame.Surface(pxs(body.major_ax, body.minor_ax)) for body in bodies]
spaceship_surface = pygame.Surface(pxs(spaceship.major_ax, spaceship.minor_ax))
sun_surface = pygame.Surface((50, 50))
myfont = pygame.font.SysFont("Calibri",20)

while mainloop:
    ms = clock.tick(fps)
    simtime += ms*secs_per_msecs
    text = """FPS: {0:.1f}   
        Days since start: {1:.0f}   
        Scale: {2:.0f} km/px""".format(clock.get_fps(), simtime/3600/24, 1/pixels_per_meter/1000)
    pygame.display.set_caption(text)
    screen.blit(bg_image, (0,0))

    if(phase < 3):
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
        sun_surface.set_colorkey((0,0,0))
        pygame.draw.circle(sun_surface, (252, 212, 64), (25, 25), 25)
        sun_surface = sun_surface.convert()
        screen.blit(sun_surface, (width//2-25, height//2 -25))


    if(phase == 0):
        pass
    elif(phase == 1):
        angle_difference = bodies[0].angle_difference(bodies[1])
        if (abs(angle_difference - angle_delta)) < 1:
            phase = 2
            print ("Launching!")

    elif(phase == 2):
        if launch_prepped == False:
            # sets the spaceship's position to be equal to earth, but with diff major axis and ecc
            spaceship.r = bodies[0].r
            spaceship.initial_angle = bodies[0].angle
            spaceship.angle = 0
            spaceship.velocity = math.sqrt(G*sun_mass*(2/spaceship.r - 1/spaceship.a)) #+ 11500
            spaceship.a, spaceship.eccentricity = bodies[0].get_transfer_ellipse(bodies[1])
            print (spaceship.a, spaceship.eccentricity)
            delta_v = spaceship.velocity - math.sqrt(G*sun_mass/spaceship.r)
            spaceship.energy = bodies[0].energy
            spaceship.energy += delta_v**2/2
            spaceship.areal_v *=  1.085 #((G*G*sun_mass*sun_mass*(spaceship.eccentricity**2 - 1))/(8*spaceship.energy))**0.5
            spaceship.colour = (183,183,183)
            spaceship.q = spaceship.a*(1 - spaceship.eccentricity**2)
            launch_prepped = True

            spaceship_surface.set_colorkey((0,0,0))
            pygame.draw.circle(spaceship_surface, spaceship.colour, pxs(body_scale*spaceship.body_radius, body_scale*spaceship.body_radius), px(body_scale*spaceship.body_radius))
            spaceship_surface = spaceship_surface.convert()
            px_x, px_y = convert_coords(math.cos(math.radians(spaceship.angle + spaceship.initial_angle))*spaceship.r, math.sin(math.radians(spaceship.angle + spaceship.initial_angle))*spaceship.r)
            screen.blit(spaceship_surface, (px_x-px(body_scale*spaceship.body_radius), px_y-px(body_scale*spaceship.body_radius)))
        else:
            spaceship_surface.set_colorkey((0,0,0))
            pygame.draw.circle(spaceship_surface, spaceship.colour, pxs(body_scale*spaceship.body_radius, body_scale*spaceship.body_radius), px(body_scale*spaceship.body_radius))
            spaceship_surface = spaceship_surface.convert()
            centered_coords = spaceship.spaceship_update(ms*secs_per_msecs)
            px_x, px_y = convert_coords(*centered_coords)
            screen.blit(spaceship_surface, (px_x-px(body_scale*spaceship.body_radius), px_y-px(body_scale*spaceship.body_radius)))
        
            other_centered_pos = bodies[1].get_position()
            xdiff = (other_centered_pos[0] - centered_coords[0])
            ydiff = (other_centered_pos[1] - centered_coords[1])
            dist = (xdiff**2+ydiff**2)**0.5
            if (dist <= body_scale*bodies[1].body_radius):
                phase = 3
                bg_image = pygame.image.load(os.path.join("data", "mars_ships_bg_4_3.png"))
                bg_image_scale = width/bg_image.get_width()
                bg_image = pygame.transform.scale(bg_image, (width, height)).convert()
                dy = 0

    elif(phase == 3):
        ship_image = pygame.image.load(os.path.join("data", "ship.png"))
        new_dims = (int(ship_image.get_width()*bg_image_scale), int(ship_image.get_height()*bg_image_scale))
        ship_image = pygame.transform.scale(ship_image, new_dims)
        ship_image.set_colorkey((0,0,0))
        ship_image = ship_image.convert()
        ship_width = ship_image.get_width()
        ship_height = ship_image.get_height()
        dy += descent_speed*ms
        if dy <= ship_height:
            ship_lower = ship_image.subsurface((0, ship_height-dy, ship_width, dy))
            screen.blit(ship_lower, (3*width//5, 0))
        elif dy <= 4*height//5:
            screen.blit(ship_image, (3*width//5, dy-ship_height))
        elif dy <= height:
            screen.blit(ship_image, ((3*width//5, 4*height//5-ship_height)))
        else:
            screen.blit(ship_image, ((3*width//5, 4*height//5-ship_height)))
            astronaut_image = pygame.image.load(os.path.join("data", "astronaut.png"))
            new_dims = (int(astronaut_image.get_width()*bg_image_scale), int(astronaut_image.get_height()*bg_image_scale))
            astronaut_image = pygame.transform.scale(astronaut_image, new_dims)
            astronaut_image.set_colorkey((0,0,0))
            astronaut_image = astronaut_image.convert()
            screen.blit(astronaut_image, (2*width//5, 4*height//5-astronaut_image.get_height())) 

        

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
            if event.key == pygame.K_SPACE:
                if phase == 0:
                    phase = 1
                    angle_delta = bodies[0].get_launch_angle(bodies[1])

# put text on the screen
    if phase == 0:
        text = "Press Space to launch!"
    
    elif phase == 1:
        text = "Waiting for optimal angle = "+str(round(angle_delta))+ " degrees  Current angle = "+str((round(bodies[0].angle_difference(bodies[1]))+360)%360)+" degrees"
    
    elif phase == 2:
        text = "Houston we're on our way!"
    
    else:
        text = "The Eagle has landed!"
    text_surface = myfont.render(text, False, (255,255,255))
    screen.blit(text_surface, (0,0))


    #Display changes
    pygame.display.flip()

#Quit
pygame.quit()