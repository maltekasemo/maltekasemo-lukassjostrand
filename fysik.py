import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import numpy as np
from math import sqrt

t_span = (0, 30) #the number of seconds we iterate over
starting_velocities = [1 / 2, 1, sqrt(2), 2]

def run():
    for start_vel in starting_velocities:  # using all the velocities given in the PDF
        start = [1, 0, 0, start_vel]  # setting the initial state of movement
        sol = solve_ivp(f, t_span, start, t_eval=np.arange(0, t_span[1], 0.001), method='LSODA')  # integrating

        x, y, vx, vy = sol.y  # extracting the wanted parts of the answer returned

        potential_energy, kinetic_energy, total_energy = get_energies(x, y, vx, vy)
        angular_momentum = (x * vy - y * vx)

        create_graphs(x, y, start_vel, sol, potential_energy, kinetic_energy, total_energy, angular_momentum)

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

def get_energies(x, y, vx, vy):
    potential_energy = - 1 / np.sqrt(x ** 2 + y ** 2)
    kinetic_energy = (vx ** 2 + vy ** 2) / 2
    total_energy = potential_energy + kinetic_energy

    return potential_energy, kinetic_energy, total_energy

def create_graphs(x, y, start_vel, sol, potential_energy, kinetic_energy, total_energy, angular_momentum):
    plot_trajectory(x, y, start_vel)
    plot_energies(sol, potential_energy, kinetic_energy, total_energy, start_vel)
    plot_angular_momentum(sol, angular_momentum, start_vel)

def plot_trajectory(x,y,start_vel):
    plt.plot(x, y)
    plt.xlabel('x-coordinate (m)')
    plt.ylabel('y-coordinate (m)')
    plt.title(f'Trajectory of x-y | vy0 = {round(start_vel, 3)} m/s')
    plt.savefig(f'trajectory_{start_vel}.png')
    plt.clf() #clearing the figure

def plot_energies(sol, potential_energy, kinetic_energy, total_energy, start_vel):
    plt.plot(sol.t, potential_energy, label='Potential Energy')
    plt.plot(sol.t, kinetic_energy, label='Kinetic Energy')
    plt.plot(sol.t, total_energy, label='Total Energy')
    plt.xlabel('Time (s)')
    plt.ylabel('Energies (J)')
    plt.title(f'Change in energies | vy0 = {round(start_vel, 3)} m/s')
    plt.legend()
    plt.savefig(f'energy_{start_vel}.png')
    plt.clf()  # clearing the figure

def plot_angular_momentum(sol, angular_momentum, start_vel):
    plt.plot(sol.t, angular_momentum.round(1), label='Angular Momentum')
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Momentum (kg/m^2)')
    plt.title(f'Angular momentum | vy0 = {round(start_vel, 3)} m/s')
    plt.savefig(f'momentum_{start_vel}.png')
    plt.clf()  # clearing the figure



