import math

global G, sun_mass
G = 6.673e-11
sun_mass = 1.989e30

class body(object):
    def __init__ (self, name, r, angle, eccentriticy, major_ax, color):    
        self.name = name
        self.r = r
        self.angle = angle
        self.eccentricity = eccentriticy
        self.major_ax = major_ax
        self.a = major_ax/2
        self.velocity = (G*sun_mass*(2/self.r - 1/(self.a)))**0.5
        self.energy = (self.velocity**2)/2 - G*sun_mass/self.r
        self.areal_v = (G*G*sun_mass*sun_mass*(self.eccentricity**2 - 1))/(8*self.energy)
        self.q = self.a*(1 - self.eccentricity**2)

        print("Body "+ name+ " created")

    def update_position(self, delta_t):
        self.angle += (2*self.areal_v/self.r**2)*delta_t
        self.r = self.q/(1 + self.eccentricity*math.cos(math.radians(self.angle)))
        self.velocity = (G*sun_mass*(2/self.r - 1/(self.a)))**0.5
        return math.cos(math.radians(self.angle))*self.r, math.sin(math.radians(self.angle))*self.r





if __name__ == "__name__":
    earth = body("Earth", 1.5e11, 0, 0.0167, 3e11, (255,255,255))
    delta_t = 3600
    for i in range(1000000):
        x, y = earth.update_position(delta_t)
        print ("x = "+str(x))
        print ("y = "+str(y))
        print (earth.velocity)
    
else:
    pass
