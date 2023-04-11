from math import sqrt
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import numpy as np


t_span = (0, 300) #antalet sekunder som varvas
start = [1, 0, 0, sqrt(2)] #startens förutsättningar

def f(t, state): #the function takes a vector of the actual state of the particles.
    # It returns the velcoity and acceleration acting on the particle

    #0 x position
    #1 y position
    #2 velocity in x
    #3 velocity in y
    x, y, vx, vy = state

    ax = - x / (x ** 2 + y ** 2) ** (3/2)
    ay = - y / (x ** 2 + y ** 2) ** (3/2)

    return (vx, vy, ax, ay)

    #0 x velocity
    #1 y velocity
    #2 acceleration in x
    #3 acceleration in y

sol = solve_ivp(f, t_span, start, t_eval=np.arange(0, 300 + 0.01, 0.01), method ='LSODA')

x, y, vx, vy = sol.y

# Calculate potential energy
potential_energy = - 1 / np.sqrt(x**2 + y**2)

# Calculate kinetic energy
kinetic_energy = (vx**2 + vy**2) / 2

# Calculate total energy
total_energy = kinetic_energy + potential_energy

# Plot x-y trajectory
plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Trajectory of x-y')

# Plot potential energy
plt.figure(figsize=(8, 6))
plt.plot(sol.t, potential_energy)
plt.xlabel('Time')
plt.ylabel('Potential Energy')
plt.title('Potential Energy vs. Time')

# Plot kinetic energy
plt.figure(figsize=(8, 6))
plt.plot(sol.t, kinetic_energy, label='Kinetic Energy')
plt.xlabel('Time')
plt.ylabel('Kinetic Energy')
plt.title('Kinetic Energy vs. Time')
plt.legend()

# Plot total energy
plt.figure(figsize=(8, 6))
plt.plot(sol.t, total_energy, label='Total Energy')
plt.xlabel('Time')
plt.ylabel('Total Energy')
plt.title('Total Energy vs. Time')
plt.legend()

plt.show()

