
import numpy as np
import math


###########
#  External Constants
##########

#### Tritium lifetime

H3_halflife = 12.33 #years

Ln2 = 0.693  # natural log of 2

H3_lifetime = H3_halflife / Ln2  # years

H3_tau = H3_lifetime * 365  # lifetime in days

H3_tau = H3_tau * 24 # lifetime in hours

#### Diffusion and mass transport constants

####### concrete parameters


Ddry_cm2 = 2.4e-6  #cm2/sec

Ddry = Ddry_cm2

Ddirt = 9.5e-7  #cm2/sec

Ddol = 1.5e-7 #cm2/sec

Ddol = 6.09 * 2.73 * Ddol   # correct for 80%-> 100% saturation and 6% porosity to 20% porosity

Ddry = 1.2e-7  #corrected for 10% porosity and 72% saturation



rho_vapor = 0.0173
rho_liquid = 1000


#########################################
##### Decay pipe geometries and binnings
#########################################


### Based on coordinates from Paola's file
### All would get multiplied by decay pipe length to make an actual surface area or volume

##Section 8 for 4m geometry

top_inner_surface = 267.5   #cm

top_outer_surface = 325.1   #cm

slant_inner_surface = 505.5

slant_outer_surface = 603.6

side_inner_surface = 673.5

side_outer_surface = 970.1

bottom_inner_surface = 406

bottom_outer_surface = 772

bslant_inner_surface = 309.7



air_volume = 288918 #cm2

decay_pipe_length = 19400 #cm

decay_pipe_length = 1 #cm

air_volume = decay_pipe_length * air_volume  #cc

bottom_bounded_air_volume = decay_pipe_length * 406 * 25


#######################
### Temperatures
#######################

Tf_top_DP = 55.5   # degrees C
Ti_top_DP = 17.1
k_top_DP = 1.33   # 1/year

Tf_side_DP = 55.2   # degrees C
Ti_side_DP = 18.4
k_side_DP = 1.38   # 1/year

Tf_bottom_DP = 40.1   # degrees C
Ti_bottom_DP = 16
k_bottom_DP = 1.12   # 1/year

Tf_bottom_wall = 38   # degrees C
Ti_bottom_wall = 12.9
k_bottom_wall = 0.99   # 1/year

Tf_wall = 16.1   # degrees C
Ti_wall = 12.77
k_wall = 0.67   # 1/year



##################################
##### Run length and POTs
#################################



Run = 365 * 30 * 24 + 1

POT = np.empty(Run)

POT = np.load('pot_hour.npy')

max_hours = 365 * 100 * 24

max_days = 365 * 100

