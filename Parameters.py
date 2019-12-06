import math
# Population density: 55 per km^2,
# according to world population and Earth's land area excluding Antarctica
dimension = 50          # Dimension of environment
N = 2000                # Population size

# Movement
d = 0.8                 # Probability of movement
d_exposed = 1            # Probability of movement, during incubation time, zombie
d_symptomatic = 0             # Probability of movement, when symptomatic, dying

day_time = 16           # 16
night_time = 8          # 8

mean_incubation_time = 24

beta = 0.6              # Infection rate
gamma = 0.01            # Recovery rate
delta = 0.01               # Death rate

# Airport parameters
center = math.floor(dimension/4)
airport_location = [[center, center], [center, 3*center], [3*center, center], [3*center, 3*center]]
airport_flow = [[0, 0.33, 0.66, 1], [0.33, 0.33, 0.66, 1], [0.33, 0.66, 0.66, 1], [0.33, 0.66, 1, 1]]
n_airport = len(airport_location)

# Area boundaries
boundary = dimension/2

limited_time = True
T = 2000

# Plot parameters
save_path = 'test7'
plot_step = 5          # How often to plot
plot_grid = True
plot_proportions = False

