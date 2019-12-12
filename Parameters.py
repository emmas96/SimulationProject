import math
import os
# Population density: 55 per km^2,
# according to world population and Earth's land area excluding Antarctica
dimension = 50          # Dimension of environment
N = 10000                # Population size

# Movement
d = 0.9                 # Probability of movement
d_exposed = d         # Probability of movement, during incubation time, zombie
d_symptomatic = 0.2     # Probability of movement, when symptomatic, dying

travellers = True
traveller_ratio = 0.9
panic_threshold = 1

day_time = 16           # 16
night_time = 8          # 8

mean_incubation_time = 48

beta = 0.6              # Infection rate
gamma = 0.01            # Recovery rate
delta = 0               # Death rate
beta_exposed = 0.15
beta_ill = 0.3

# Airport parameters
center = math.floor(dimension/4)
airport_location = [[center, center], [center, 3*center], [3*center, center], [3*center, 3*center]]
stay = 0.5
go = (1-stay)/3
#airport_flow = [[0, 0.33, 0.66, 1], [0.33, 0.33, 0.66, 1], [0.33, 0.66, 0.66, 1], [0.33, 0.66, 1, 1]]
airport_flow = [[stay, stay+1*go, stay+2*go, stay+3*go],
                [1*go, stay+1*go, stay+2*go, stay+3*go],
                [1*go, 2*go, stay+2*go, stay+3*go],
                [1*go, 2*go, 3*go, stay+3*go]]
n_airport = len(airport_location)
not_start_at_airport = True

# Area boundaries
boundary = dimension/2

# Infect all in grid area or not
infect_all = False

limited_time = True
T = 720

# Plot parameters
save_path = 'travellers'
output_path = save_path + '_output.txt'
plot_step = 1          # How often to plot
plot_grid = False
plot_proportions = False

