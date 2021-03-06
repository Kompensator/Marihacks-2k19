import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
import sys

class point():
    """returns an object that is a two dimensional 'vector'
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

class body():
    """return a body that has a location (2d vector), mass, velocity, name
    """
    def __init__(self, location:  float, mass, velocity, name = ''):
        self.location = location
        self.mass = mass
        self.velocity = velocity
        self.name = name

def calculate_single_body_acceleration(bodies, body_index, n, laser_power, burn_time):
    """ return the acceleration on a body in bodies caused by other bodies
    using F = G*m1*m2/r^2
    """
    g_constant = 6.6740831 *10 **(-11)
    acceleration = point(0,0)    #initializing a zero acceleration vector
    target_body = bodies[body_index]
    for index, other_body in enumerate(bodies):    #gives a list like [(1,sun),(2,earth),....]
        if index == 0 and index != body_index:     # this hack turns off physics between all bodies except sun
            r = math.sqrt((target_body.location.x - other_body.location.x)**2 + (target_body.location.y - other_body.location.y)**2)
            try:
                temp_acc = (g_constant * other_body.mass)/r**3    #this value multiplied by the distance in 1 dimension will give the acceleration
            except ZeroDivisionError:
                print ("ZeroDivisionError occured and caught in computing acceleration: r = 0")

            acceleration.x = temp_acc*(other_body.location.x - target_body.location.x)
            acceleration.y = temp_acc*(other_body.location.y - target_body.location.y)
        else:
            pass
    if target_body.name == "asteroid":
        ax, ay = laser_force(bodies, n, laser_power, burn_time)
        acceleration.x += ax
        acceleration.y += ay
    return acceleration

def laser_force(bodies, n, laser_power, burn_time):
    for body in bodies:
        if body.name == "asteroid":
            laser_power = float(laser_power)
            burn_time = float(burn_time)

            laser_force = math.sqrt(1.596e-3*(laser_power-1358.41))   # in N
            number_of_time_intervals = burn_time//14400
            if n < number_of_time_intervals:   # the less than equal sign is fixed
                x_coordinate = body.location.x
                y_coordinate = body.location.y
                if x_coordinate != 0:
                    theta = math.atan(y_coordinate/x_coordinate)
                elif x_coordinate == 0 and y_coordinate > 0:
                    theta = np.pi/2      #zero division is fixed
                else:
                    theta = -1*np.pi/2

                acc_x = (math.sin(theta)*laser_force)/body.mass
                acc_y = (-math.cos(theta)*laser_force)/body.mass
                return acc_x, acc_y
            elif n == number_of_time_intervals:
                print ("Burn finished!")   #optional
                return 0 , 0
            else:
                return 0 ,0
        else:
            pass


def calculate_velocity(bodies, n, laser_power, burn_time, dt = 14400):    # dt is equivalent to 4hrs, so 6 updates per day
    """compute all the velocity after dt and change the velocity attributes in the bodies
    """
    for body_index, target_body in enumerate(bodies):
        acceleration = calculate_single_body_acceleration(bodies, body_index, n, laser_power, burn_time)
        target_body.velocity.x += acceleration.x * dt
        target_body.velocity.y += acceleration.y * dt

def calculate_position(bodies, dt = 14400):   # dt = 4 hours, 6 ticks/day
    for body in bodies:
        body.location.x += body.velocity.x * dt
        body.location.y += body.velocity.y *dt
        print (body.location.x, body.location.y)

def compute_gravity_step(bodies, n, laser_power, burn_time, dt = 14400):
    calculate_velocity(bodies, n, laser_power, burn_time, dt = dt)
    calculate_position(bodies, dt = dt)


sun = {"location":point(0,0), "mass":2e30, "velocity":point(0,0)}
mercury = {"location":point(0,5.7e10), "mass":3.285e23, "velocity":point(47000,0)}
venus = {"location":point(0,1.1e11), "mass":4.8e24, "velocity":point(35000,0)}
earth = {"location":point(-9.124e10,-7.830e10), "mass":6e24, "velocity":point(-2.629e4,2.417e4)}
mars = {"location":point(0,2.2e11), "mass":2.4e24, "velocity":point(24000,0)}
jupiter = {"location":point(0,7.7e11), "mass":1e28, "velocity":point(13000,0)}
saturn = {"location":point(0,1.4e12), "mass":5.7e26, "velocity":point(9000,0)}
uranus = {"location":point(0,2.8e12), "mass":8.7e25, "velocity":point(6835,0)}
neptune = {"location":point(0,4.5e12), "mass":1e26, "velocity":point(5477,0)}
pluto = {"location":point(0,3.7e12), "mass":1.3e22, "velocity":point(4748,0)}
asteroid = {"location":point(-7.133e10,-1.159e11),"mass":27e9,"velocity":point(-2.812e4,1.409e4)}

bodies = [
        body( location = sun["location"], mass = sun["mass"], velocity = sun["velocity"], name = "sun"),
        body( location = earth["location"], mass = earth["mass"], velocity = earth["velocity"], name = "earth"),
        body( location = asteroid["location"], mass = asteroid["mass"], velocity = asteroid["velocity"], name = "asteroid")]
        #body( location = mars["location"], mass = mars["mass"], velocity = mars["velocity"], name = "mars"),
        #body( location = venus["location"], mass = venus["mass"], velocity = venus["velocity"], name = "venus"),
        #body( location = jupiter["location"], mass = jupiter["mass"], velocity = jupiter["velocity"], name = "jupiter"),
        #body( location = mercury["location"], mass = mercury["mass"], velocity = mercury["velocity"], name = "mercury")]
fig, ax = plt.subplots()
xdata, ydata = [], []   # this is for current position data
x_hist, y_hist = [], []  # this is for historical position data
ln, = plt.plot([], [], 'ro', markersize = 6, animated=True)      # 'ro' = red circle 'bo' = blue circle ...
ln1, = plt.plot([],[], "bo", markersize = 0.01, animated = True)   #markersize = how big the circle is
earth, = plt.plot([],[], "go", markersize = 6, animated=True)
# ln is the current position, ln1 is the past position
ttl = ax.text(0, 0, '', transform = ax.transAxes,fontsize = 10)
sun, = plt.plot([],[],'yo', markersize = 10, animated =True)

def init():
    ax.set_xlim(-5e11, 5e11)     # these 2 define the scale of the graph
    ax.set_ylim(-5e11, 5e11)
    ttl.set_text('')
    return ln, ttl

def update(frame):
    if frame == 0:
        global laser_power
        global burn_time
        laser_power = input("Laser Power (W) > ")    # inputs the power and burn time from user on the first iteration
        burn_time = input('Burn time (s) > ')
    xdata, ydata = [], []
    xdata2, ydata2 = [],[]
    sunx, suny = [],[]
    compute_gravity_step(bodies,frame, laser_power, burn_time)   # each frame is one dt
    for body in bodies:
        if body.name == "asteroid":
            xdata.append(body.location.x)
            ydata.append(body.location.y)
        elif body.name == "earth":
            xdata2.append(body.location.x)
            ydata2.append(body.location.y)
        elif body.name == "sun":
            sunx.append(body.location.x)
            suny.append(body.location.y)

    ln.set_data(xdata, ydata)
    earth.set_data(xdata2, ydata2)
    sun.set_data(sunx,suny)
    for body in bodies:
        x_hist.append(body.location.x)
        y_hist.append(body.location.y)
    ln1.set_data(x_hist, y_hist)
    a_e_distance = math.sqrt((bodies[1].location.x-bodies[2].location.x)**2 + (bodies[1].location.y - bodies[2].location.y)**2)

    if a_e_distance < 1.5e9:
        print("Collision: asteroid in Hill sphere")
        sys.exit(0)
    elif frame == 4380:     # program stops at this tick
        print("Collision averted!")
        """print ("x asteroid: ", bodies[2].location.x)
        print ("y asteroid: ", bodies[2].location.y)
        print ("vx asteroid: ", bodies[2].velocity.x)
        print ("vy asteroid: ", bodies[2].velocity.y)
        print ("x earth: ", bodies[1].location.x)
        print ("y earth: ", bodies[1].location.y)
        print ("vx earth: ", bodies[1].velocity.x)
        print ("vy earth: ", bodies[1].velocity.y)"""
        sys.exit(0)
    ttl.set_text(str("Time elapsed: "+ str(frame*4)+" hours" +"   Burn Time: " + str(int(burn_time)//3600)+' hours'))
    return ln, ln1, earth, ttl, sun

ani = FuncAnimation(fig, update, interval = 1, init_func=init, blit=True)

plt.show()
