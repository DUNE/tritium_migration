import matplotlib.pyplot as plt
import numpy as np
import math
import time

from functions import fillPOT         # go from protons to Tritium in the decay pipe
from functions import fillPOT_2D      # go from protons to Tritium in the walls/dirt/rock
from functions import diff1           # 1D radial diffusion
from functions import diff2           # 1D linear diffusion in two volumes
from functions import diff2D          # 2D linear diffussion 
from functions import HTO_Current     # tritium current into and out of the air gap 
from functions import n_out           # number of pCi leaving the DP and walls
from functions import n_in            # number of pCi of tritium entering the outer walls
from functions import mixed           # mixing in the form of the concentration model
from functions import temperature     # DP and wall temps as a function of time
from functions import psat            # temp dependence of saturation pressure
from functions import Dt              # temp dependence of diffusion coefficient
from functions import RhoWater        # temperature dependence of the density of water
from functions import H_HTO           # phase partition factor used to determine saturation


start_time = time.perf_counter()

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


rho_vapor = 0.0173
rho_liquid = 1000

Ddry_cm2 = 2.4e-6  #cm2/sec

Ddry = Ddry_cm2

Ddirt = 9.5e-7  #cm2/sec

Ddol = 1.5e-7 #cm2/sec

Ddol = 6.09 * 2.73 * Ddol   # correct for 80%-> 100% saturation and 6% porosity to 20% porosity

Ddry = 1.2e-7  #corrected for 10% porosity and 72% saturation




#########################################
##### Decay pipe geometries and binnings
#########################################

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


################
##### Star Maps
################

with np.load('../test/fluka_star_maps_DP.npz') as data:

    #print("Array names:", data.files)


    top_DP_map      = data['top_DP_map1']
    slant_DP_map    = data['slant_DP_map1']
    side_DP_map     = data['side_DP_map1']
    bslant_DP_map   = data['bslant_DP_map1']
    bottom_DP_map   = data['bottom_DP_map1']

    bottom_air      = data['bottom_air1']
    air             = data['air1']


with np.load('../test/2D-old.npz') as data:

    #print("Array names:", data.files)


    top_map      = data['top_map1']
    slant_map    = data['slant_map1']
    side_map     = data['side_map1']


    top_d_map      = data['top_d_map1']
    slant_d_map    = data['slant_d_map1']
    side_d_map     = data['side_d_map1']

with np.load('../Wall_stars/2D_bottom8.npz') as data:

    bottom_map   = data['bottom_map1']
    bottom_d_map   = data['bottom_d_map1']
    bottom_avg_map   = data['bottom_avg_map1']
    bottom_d_avg_map   = data['bottom_d_avg_map1']



#print(bottom_d_map.shape[0], bottom_d_map.shape[1])
    
bottom_dt_map = np.zeros((bottom_d_map.shape[0], 26))


for i in range(bottom_d_map.shape[0]):

    for j in range(25):
    
        bottom_dt_map[i,j] = bottom_d_map[i,j]

    bottom_dt_map[i,25] = 0



    
##################################
##### Run length and POTs
#################################



Run = 365 * 30 * 24 + 1

POT = np.empty(Run)

POT = np.load('pot_hour.npy')

max_hours = 365 * 50 * 24

max_days = 365 * 50

################################
###### Containers / Histograms
################################

#### Bins

n_top_DP = len(top_DP_map)
n_slant_DP = len(slant_DP_map)
n_side_DP = len(side_DP_map)
n_bottom_DP = len(bottom_DP_map)
n_bslant_DP = len(bslant_DP_map)

n_topx = top_map.shape[0]
n_topy = top_map.shape[1]

n_slantx = slant_map.shape[0]
n_slanty = slant_map.shape[1]

n_sidex = side_map.shape[0]
n_sidey = side_map.shape[1]

n_bottomx = bottom_map.shape[0]
n_bottomy = bottom_map.shape[1]

n_topdx = top_d_map.shape[0]
n_topdy = top_d_map.shape[1]

n_slantdx = slant_d_map.shape[0]
n_slantdy = slant_d_map.shape[1]

n_sidedx = side_d_map.shape[0]
n_sidedy = side_d_map.shape[1]

n_bottomdx = bottom_d_map.shape[0]
n_bottomdy = bottom_d_map.shape[1]

n_bottomdtx = bottom_dt_map.shape[0]
n_bottomdty = bottom_dt_map.shape[1]

#### Info per sample period


H3_top_DP = np.zeros((max_days, n_top_DP))
H3_slant_DP = np.zeros((max_days, n_slant_DP))
H3_side_DP = np.zeros((max_days, n_side_DP))
H3_bslant_DP = np.zeros((max_days, n_bslant_DP))
H3_bottom_DP = np.zeros((max_days, n_bottom_DP))

H3_air = np.zeros(max_days)
H3_bottom_air = np.zeros(max_days)

H3_top = np.zeros((max_days, n_topx, n_topy))
H3_bottom = np.zeros((max_days, n_bottomx, n_bottomy))
H3_side = np.zeros((max_days, n_sidex, n_sidey))
H3_slant = np.zeros((max_days, n_slantx, n_slanty))

H3_top_D = np.zeros((max_days, n_topdx, n_topdy))
H3_slant_D = np.zeros((max_days, n_slantdx, n_slantdy))
H3_side_D = np.zeros((max_days, n_sidedx, n_sidedy))
H3_bottom_D = np.zeros((max_days, n_bottomdx, n_bottomdy))

H3_bottom_Dt = np.zeros((max_days, n_bottomdtx, n_bottomdty))

H3_bottom_D_mix = np.zeros((max_days, n_bottomdx, n_bottomdy))

H3_top_Dd = np.zeros((max_days, n_topdx, n_topdy))
H3_slant_Dd = np.zeros((max_days, n_slantdx, n_slantdy))
H3_side_Dd = np.zeros((max_days, n_sidedx, n_sidedy))
H3_bottom_Dd = np.zeros((max_days, n_bottomdx, n_bottomdy))

H3_bottom_Dd_mix = np.zeros((max_days, n_bottomdx, n_bottomdy))

H3_bottom_D_removed = np.zeros((max_days, n_bottomdx, n_bottomdy))
H3_bottom_Dd_removed = np.zeros((max_days, n_bottomdx, n_bottomdy))

# add 1D averages to compare 2D and 1D diffusion
H3_bottom_avg = np.zeros((max_days, n_bottomy))

H3_bottom_D_avg = np.zeros((max_days, n_bottomdy))

H3_bottom_Dd_avg = np.zeros((max_days, n_bottomdy))



J_side_DPipe = np.zeros((max_days))
J_side_wall = np.zeros((max_days))

JE_side_DPipe = np.zeros((max_days))
JE_side_wall = np.zeros((max_days))


J_bottom_DPipe = np.zeros((max_days))
J_bottom_wall = np.zeros((max_days))

JE_bottom_DPipe = np.zeros((max_days))
JE_bottom_wall = np.zeros((max_days))


#### Counters

iH3_top_DP = np.zeros(n_top_DP)
iH3_slant_DP = np.zeros(n_slant_DP)
iH3_side_DP = np.zeros(n_side_DP)
iH3_bslant_DP = np.zeros(n_bslant_DP)
iH3_bottom_DP = np.zeros(n_bottom_DP)


iH3_bottom_air = 0
iH3_air = 0

iH3_top = np.zeros((n_topx, n_topy))
iH3_slant = np.zeros((n_slantx, n_slanty))
iH3_side = np.zeros((n_sidex, n_sidey))
iH3_bottom = np.zeros((n_bottomx, n_bottomy))

iH3_bottom_t = np.zeros((n_bottomx, n_bottomy))

iH3_bottom_avg = np.zeros((n_bottomy))

iH3_top_D = np.zeros((n_topdx, n_topdy))
iH3_slant_D = np.zeros((n_slantdx, n_slantdy))
iH3_side_D = np.zeros((n_sidedx, n_sidedy))
iH3_bottom_D = np.zeros((n_bottomdx, n_bottomdy))
iH3_bottom_D_mix = np.zeros((n_bottomdx, n_bottomdy))

iH3_bottom_Dt = np.zeros((n_bottomdtx, n_bottomdty))

iH3_bottom_D_avg = np.zeros((n_bottomdy))

iH3_top_Dd = np.zeros((n_topdx, n_topdy))
iH3_slant_Dd = np.zeros((n_slantdx, n_slantdy))
iH3_side_Dd = np.zeros((n_sidedx, n_sidedy))
iH3_bottom_Dd = np.zeros((n_bottomdx, n_bottomdy))
iH3_bottom_Dd_mix = np.zeros((n_bottomdx, n_bottomdy))

iH3_bottom_Dd_avg = np.zeros((n_bottomdy))



####################################
##### Main sampling loop
###################################

iday = 0

ihours = 24*7+1

max = int(max_hours/20)


kc = 0.035
kd = 0.032
kdol = 0.0407 * (5.34/6.45)

#max_hours = 100



for i in range(max_hours):
#for i in range(2*24*365):

    if i%(24*365) == 0:
        print( int( i/(24*365) ) )   #years
        #print(iday, iH3_top_DP[1], H3_top_DP[iday,1])

    ###################################
    ##### get protons, deposite tritium
    ####################################
    
    if i < Run:

        iH3_bottom = fillPOT_2D(iH3_bottom, bottom_map, POT[i], kc)

        iH3_bottom_t = fillPOT_2D(iH3_bottom_t, bottom_map, POT[i], kc)

        iH3_bottom_D = fillPOT_2D(iH3_bottom_D, bottom_d_map, POT[i], kdol)

        iH3_bottom_Dt = fillPOT_2D(iH3_bottom_Dt, bottom_dt_map, POT[i], kdol)
        
        iH3_bottom_Dd = fillPOT_2D(iH3_bottom_Dd, bottom_d_map, POT[i], kdol)

        iH3_bottom_avg = fillPOT(iH3_bottom_avg, bottom_avg_map, POT[i])
        iH3_bottom_D_avg = fillPOT(iH3_bottom_D_avg, bottom_d_avg_map, POT[i])
        iH3_bottom_Dd_avg = fillPOT(iH3_bottom_Dd_avg, bottom_d_avg_map, POT[i])


        H3_Atoms_per_pC = 9.6e6  #atoms per pC


        #iH3_bottom_avg = (kc / H3_Atoms_per_pC) *  iH3_bottom_avg
        #iH3_bottom_D_avg = (kdol / H3_Atoms_per_pC) *  iH3_bottom_D_avg
        #iH3_bottom_Dd_avg = (kdol / H3_Atoms_per_pC) *  iH3_bottom_Dd_avg
        
        

        #print(i, iH3_top_DP[1])



    ###########################
    ### Temperatures
    ###########################

    
    T_bottom_wall = temperature(i, Ti_wall, Tf_wall, k_wall)


        

    ###########################
    ### Diffusion
    ###########################

    dx = 10 #cm
    dt = 60 * 60 #seconds in an hour

    D_bottom_wall = Dt(Ddry, T_bottom_wall)

    D_bottom_dol = Dt(Ddry,T_bottom_wall)

    Ddol_t = Dt(Ddol,12.5)

    
    iH3_bottom, iH3_bottom_D = diff2D(iH3_bottom, iH3_bottom_D, dx, dt, D_bottom_wall, Ddol_t)

    iH3_bottom_t, iH3_bottom_Dt = diff2D(iH3_bottom_t, iH3_bottom_Dt, dx, dt, D_bottom_wall, Ddol_t)



    
    iH3_bottom_avg, iH3_bottom_D_avg = diff2(iH3_bottom_avg, iH3_bottom_D_avg, dx, dt, D_bottom_wall, Ddol_t)


    
    #########################################################
    ### Record where we are at the end of each day
    #########################################################

    
    if i%24 == 0:

        H3_bottom[iday,:,:] = iH3_bottom
        H3_bottom_D[iday,:,:] = iH3_bottom_D

        H3_bottom_Dd[iday,:,:] = iH3_bottom_Dd

        H3_bottom_Dt[iday,:,:] = iH3_bottom_Dt

        H3_bottom_avg[iday,:] = (kc / H3_Atoms_per_pC) * iH3_bottom_avg
        H3_bottom_D_avg[iday,:] = (kdol / H3_Atoms_per_pC) * iH3_bottom_D_avg
        H3_bottom_Dd_avg[iday,:] = (kdol / H3_Atoms_per_pC) * iH3_bottom_Dd_avg
        
        
        iday = iday + 1


            
    ##########################################################
    ### Decay all accumulated tritim by 1 hour
    #########################################################

    iH3_bottom      = iH3_bottom * math.exp(-1/H3_tau)

    iH3_bottom_D    = iH3_bottom_D * math.exp(-1/H3_tau)

    iH3_bottom_t      = iH3_bottom_t * math.exp(-1/H3_tau)

    iH3_bottom_Dt    = iH3_bottom_Dt * math.exp(-1/H3_tau)

    iH3_bottom_Dd    = iH3_bottom_Dd * math.exp(-1/H3_tau)

    iH3_bottom_avg      = iH3_bottom_avg * math.exp(-1/H3_tau)

    iH3_bottom_D_avg    = iH3_bottom_D_avg * math.exp(-1/H3_tau)

    iH3_bottom_Dd_avg    = iH3_bottom_Dd_avg * math.exp(-1/H3_tau)



    
    ###########################
    ########## End big loop
    ###########################


    

#print(H3_top[1,10])
    

np.savez('fluka_H3_maps8_bottom_only.npz',
         H3_bottom1             = H3_bottom,
         H3_bottom_D1           = H3_bottom_D,
         H3_bottom_Dt1          = H3_bottom_Dt,
         H3_bottom_Dd1          = H3_bottom_Dd,
         H3_bottom_avg1         = H3_bottom_avg,
         H3_bottom_D_avg1       = H3_bottom_D_avg,
         H3_bottom_Dd_avg1      = H3_bottom_Dd_avg)



end_time = time.perf_counter()

elapsed_time = end_time - start_time
elapsed_minutes = elapsed_time / 60

print(f"Execution time: {elapsed_minutes:.2f} minutes")
