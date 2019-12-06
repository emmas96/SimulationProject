# Population density: 55 per km^2,
# according to world population and Earth's land area excluding Antarctica
dimension = 50          # Dimension of environment
N = 2000                # Population size

d = 0.8                 # Probability of movement
d_exposed = d            # Probability of movement, during incubation time, zombie
d_symptomatic = d             # Probability of movement, when symptomatic, dying

day_time = 16           # 16
night_time = 8          # 8

mean_incubation_time = 100

beta = 0.4              # Infection rate
gamma = 0.01            # Recovery rate
delta = 0               # Death rate

# airport parameter
airport_location = [[2, 2], [99, 99], [99, 1]]
airport_flow = [[0, 0.5, 1], [0.5, 0.5, 1], [0.5, 1, 1]]
n_airport = len(airport_location)
cross_wall_coordinate = dimension/2 + 0.5

limited_time = True
T = 1000

save_path = 'base_model_dense_low_inf_test1'
plot_step = 5          # How often to plot

