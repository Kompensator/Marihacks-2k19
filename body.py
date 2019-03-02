import math

global G, sun_mass
G = 6.673e-11
sun_mass = 1.989e30

class Body(object):
    """ Docstring for Body class
    default values for earth
    update_position needs dt to run
    """
    def __init__ (self, name = "Earth", r = 1e11, angle=0, eccentriticy=0.0167, major_ax=3e11, color=(255,255,255)):    
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
        if self.angle > 360:
            self.fix_angle()
        return math.cos(math.radians(self.angle))*self.r, math.sin(math.radians(self.angle))*self.r

    def fix_angle(self):
        self.angle = self.angle%360

    def angle_difference(self, other_body):
        difference = other_body.angle - self.angle
        return difference





if __name__ == "__name__":

    
else:
    pass
