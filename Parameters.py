# Population density: 55 per km^2,
# according to world population and Earth's land area excluding Antarctica
dimension = 50          # Dimension of environment
N = 2000                # Population size

d = 0.8                 # Probability of movement
d_zombie = 1            # Probability of movement, during incubation time, zombie
d_dying = 0.4           # Probability of movement, when symptomatic, dying

mean_incubation_time = 3

beta = 0.6              # Infection rate
gamma = 0.01            # Recovery rate
delta = 0.01            # Death rate
