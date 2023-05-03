import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import numpy as np
from math import sqrt

t_span = (0, 30) #the number of seconds we iterate over

def f(t, state): #the function takes a vector of the actual state of the particles.
    # It returns the velocity and acceleration acting on the particle

    #0 x position
    #1 y positiont
    #2 velocity in x
    #3 velocity in y
    x, y, vx, vy = state

    r = np.sqrt(x ** 2 + y ** 2) #calculating the distance from the energy source
    ax = -x / r ** 3 #acceleration in x direction
    ay = -y / r ** 3 #acceleration in y direction

    return (vx, vy, ax, ay)

    #0 x velocity
    #1 y velocity
    #2 acceleration in x
    #3 acceleration in y

for start_vel in [1/2, 1, sqrt(2), 2]: #using all the velocities given in the PDF
    start = [1, 0, 0, start_vel] #setting the initial state of movement
    sol = solve_ivp(f, t_span, start, t_eval=np.arange(0, t_span[1], 0.001), method='LSODA') #integrating

    x, y, vx, vy = sol.y #extracting the wanted parts of the answer returned

    # Calculate potential energy
    potential_energy = - 1 / np.sqrt(x**2 + y**2)

    # Calculate kinetic energy
    kinetic_energy = (vx**2 + vy**2) / 2

    # Calculate total energy
    total_energy = potential_energy + kinetic_energy

    # Plot x-y trajectory
    plt.figure(figsize=(8, 6))
    plt.plot(x, y)
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title(f'Trajectory of x-y | vy0 = {start_vel}')
    plt.savefig(f'trajectory_{start_vel}.png')
    plt.clf() #clearing the figure

    # Plot the different energies in relationship to each other
    plt.plot(sol.t, potential_energy, label='Potential Energy')
    plt.plot(sol.t, kinetic_energy, label='Kinetic Energy')
    plt.plot(sol.t, total_energy, label='Total Energy')
    plt.xlabel('Time (s')
    plt.ylabel('Energies (J)')
    plt.title(f'Change in energies | vy0 = {start_vel}')
    plt.savefig(f'energy_{start_vel}.png')
