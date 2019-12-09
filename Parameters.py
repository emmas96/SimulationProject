import math
import os
# Population density: 55 per km^2,
# according to world population and Earth's land area excluding Antarctica
dimension = 100          # Dimension of environment
N = 40000                # Population size

# Movement
d = 0.8                 # Probability of movement
d_exposed = 0.6         # Probability of movement, during incubation time, zombie
d_symptomatic = 0.2     # Probability of movement, when symptomatic, dying

day_time = 960           # 16
night_time = 480          # 8

mean_incubation_time = 1440

beta = 0.6              # Infection rate
gamma = 0.001            # Recovery rate
delta = 0.02            # Death rate
beta_exposed = 0.2
beta_ill = 0.4

# Airport parameters
center = math.floor(dimension/4)
airport_location = [[center, center], [center, 3*center], [3*center, center], [3*center, 3*center]]
stay = 0.97
go = (1-stay)/3
#airport_flow = [[0, 0.33, 0.66, 1], [0.33, 0.33, 0.66, 1], [0.33, 0.66, 0.66, 1], [0.33, 0.66, 1, 1]]
airport_flow = [[stay, stay+1*go, stay+2*go, stay+3*go],
                [1*go, stay+1*go, stay+2*go, stay+3*go],
                [1*go, 2*go, stay+2*go, stay+3*go],
                [1*go, 2*go, 3*go, stay+3*go]]
n_airport = len(airport_location)

# Area boundaries
boundary = dimension/2

# Infect all in grid area or not
infect_all = False

limited_time = True
T = 2000

# Plot parameters
save_path = 'long_run4'
output_path = save_path + '_output.txt'
plot_step = 5          # How often to plot
plot_grid = True
plot_proportions = True

