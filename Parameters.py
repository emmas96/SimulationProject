# Population density: 55 per km^2,
# according to world population and Earth's land area excluding Antarctica
dimension = 100          # Dimension of environment
N = 1000                # Population size

d = 0.8                 # Probability of movement
d_zombie = d            # Probability of movement, during incubation time, zombie
d_dying = 0             # Probability of movement, when symptomatic, dying

day_time = 16           # 16
night_time = 0          # 8

mean_incubation_time = 100

beta = 0.6              # Infection rate
gamma = 0.01            # Recovery rate
delta = 0               # Death rate

# airport parameter
n_airport = 0
airport_location = [[2, 2], [99, 99], [99, 1]]
airport_flow = [[0, 0.5, 1], [0.5, 0.5, 1], [0.5, 1, 1]]

