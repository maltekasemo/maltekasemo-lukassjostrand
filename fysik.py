import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

t_span = np.array([0, 30])

class Planet:
    def __init__(self, x_pos, y_pos, x_velocity, y_velocity):
        self.mass = 1
        self.z = np.array([x_pos, y_pos, x_velocity, y_velocity])
        self.position_vector = np.array([self.z[0], self.z[1]])
        self.velocity_vector = np.array([self.z[2], self.z[3]])
        self.k = 1

    def rorelsemangd(self):
         return self.mass * self.velocity_vector

    def rorelsemangdsmoment(self):
        return np.cross(self.position_vector, self.velocity_vector)

    def kinetisk_energi(self):
        return (self.mass / 2) * (self.z[0]^2 + self.z[1]^2)

    def lagesenergi(self):
        return -self.k / (math.sqrt(self.z[0] ^ 2 + self.z[1] ^ 2))

    def all_energi(self):
        return self.kinetisk_energi() + self.lagesenergi()

    def acceleration(self):
        return self.lagesenergi() / self.mass

planet = Planet(1, 0, 0, 1)


solution = solve_ivp(np.array[planet.velocity_vector, np.array([planet.z[0] / np.linalg.norm(planet.position_vector),
                                               planet.z[0] / np.linalg.norm(planet.position_vector)])], t_span, planet.z)

plt.plot(solution.t, solution[0])
plt.plot(solution.t, solution[1])
plt.savefig("map.png")
