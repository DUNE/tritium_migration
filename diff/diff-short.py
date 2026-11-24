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
from functions import Dpor            # porosity dependence of diffusion coefficient
from functions import Dsat            # saturation dependence of diffusion coefficient
from functions import RhoWater        # temperature dependence of the density of water
from functions import H_HTO           # phase partition factor used to determine saturation
from functions import leaching        # phase partition factor used to determine saturation


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


Ddol = Dpor(Ddol, 0.06, 0.30, 2)

Ddol = Dsat(Ddol, 1, 0.8, 4)


#Ddry = 2 * Ddry


# D old, par old, par new, scaling

Ddry = Dpor(Ddry, 0.23, 0.1, 1.47)

#Ddry = Dpor(Ddry, 0.23, 0.05, 1.47)
#Ddry = Dpor(Ddry, 0.23, 0.15, 1.47)
#Ddry = Dpor(Ddry, 0.23, 0.1, 1.0)
#Ddry = Dpor(Ddry, 0.23, 0.1, 2.0)

Ddry = Dsat(Ddry, 1, 0.72, 3)

#Ddry = Ddry
#Ddry = Dsat(Ddry, 1, 0.5, 3)
#Ddry = Dsat(Ddry, 1, 0.72, 2)
#Ddry = Dsat(Ddry, 1, 0.72, 4)




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

Toff = 0
#Toff = 5
#Toff = -5


Tf_top_DP = 55.5 + Toff   # degrees C
Ti_top_DP = 17.1 + Toff
k_top_DP = 1.33   # 1/year

Tf_side_DP = 55.2 + Toff  # degrees C
Ti_side_DP = 18.4 + Toff
k_side_DP = 1.38   # 1/year

Tf_bottom_DP = 40.1 + Toff  # degrees C
Ti_bottom_DP = 16 + Toff
k_bottom_DP = 1.12   # 1/year

Tf_bottom_wall = 38 + Toff  # degrees C
Ti_bottom_wall = 12.9 + Toff
k_bottom_wall = 0.99   # 1/year

Tf_wall = 16.1 + Toff  # degrees C
Ti_wall = 12.77 + Toff
k_wall = 0.67   # 1/year


################
##### Star Maps
################

with np.load('../DP_stars/fluka_star_maps_DP8.npz') as data:

    #print("Array names:", data.files)


    top_DP_map      = data['top_DP_map1']
    slant_DP_map    = data['slant_DP_map1']
    side_DP_map     = data['side_DP_map1']
    bslant_DP_map   = data['bslant_DP_map1']
    bottom_DP_map   = data['bottom_DP_map1']

    bottom_air      = data['bottom_air1']
    air             = data['air1']


with np.load('../Wall_stars/2DWalls8.npz') as data:

    #print("Array names:", data.files)


    top_map      = data['top_map1']
    slant_map    = data['slant_map1']
    side_map     = data['side_map1']
    bottom_map   = data['bottom_map1']

    top_d_map      = data['top_d_map1']
    slant_d_map    = data['slant_d_map1']
    side_d_map     = data['side_d_map1']
    bottom_d_map   = data['bottom_d_map1']




    

##################################
##### Run length and POTs
#################################



Run = 365 * 30 * 24 + 1

POT = np.empty(Run)

POT = np.load('pot_hour.npy')

max_hours = 365 * 30 * 24

max_days = 365 * 30

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

H3_bottom_D_mix = np.zeros((max_days, n_bottomdx, n_bottomdy))
H3_bottom_D_well = np.zeros((max_days, 2*n_bottomdx, n_bottomdy))

H3_top_Dd = np.zeros((max_days, n_topdx, n_topdy))
H3_slant_Dd = np.zeros((max_days, n_slantdx, n_slantdy))
H3_side_Dd = np.zeros((max_days, n_sidedx, n_sidedy))
H3_bottom_Dd = np.zeros((max_days, n_bottomdx, n_bottomdy))


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

iH3_top_D = np.zeros((n_topdx, n_topdy))
iH3_slant_D = np.zeros((n_slantdx, n_slantdy))
iH3_side_D = np.zeros((n_sidedx, n_sidedy))
iH3_bottom_D = np.zeros((n_bottomdx, n_bottomdy))
iH3_bottom_D_mix = np.zeros((n_bottomdx, n_bottomdy))


iH3_bottom_D_well = np.zeros((2*n_bottomdx, n_bottomdy))


iH3_top_Dd = np.zeros((n_topdx, n_topdy))
iH3_slant_Dd = np.zeros((n_slantdx, n_slantdy))
iH3_side_Dd = np.zeros((n_sidedx, n_sidedy))
iH3_bottom_Dd = np.zeros((n_bottomdx, n_bottomdy))
iH3_bottom_Dd_mix = np.zeros((n_bottomdx, n_bottomdy))


iH3_dol_avg = 0
iH3_dol_direct_avg = 0
iH3_well = 0


####################################
##### Main sampling loop
###################################

iday = 0

ihours = 24*7+1

max = int(max_hours/20)


kc = 0.035
kd = 0.032

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

        ### accumulate tritium for this hour
        iH3_top_DP = fillPOT(iH3_top_DP, top_DP_map, POT[i])
        iH3_slant_DP = fillPOT(iH3_slant_DP, slant_DP_map, POT[i])
        iH3_side_DP = fillPOT(iH3_side_DP, side_DP_map, POT[i])
        iH3_bslant_DP = fillPOT(iH3_bslant_DP, bslant_DP_map, POT[i])
        iH3_bottom_DP = fillPOT(iH3_bottom_DP, bottom_DP_map, POT[i])
                
        iH3_bottom_air = iH3_bottom_air + bottom_air * POT[i]
        iH3_air = iH3_air + air * POT[i]

        iH3_top    = fillPOT_2D(iH3_top, top_map, POT[i], kc)
        iH3_slant  = fillPOT_2D(iH3_slant, slant_map, POT[i], kc)
        iH3_side   = fillPOT_2D(iH3_side, side_map, POT[i], kc)
        iH3_bottom = fillPOT_2D(iH3_bottom, bottom_map, POT[i], kc)

        iH3_top_D    = fillPOT_2D(iH3_top_D, top_d_map, POT[i], kd)
        iH3_slant_D  = fillPOT_2D(iH3_slant_D, slant_d_map, POT[i], kd)
        iH3_side_D   = fillPOT_2D(iH3_side_D, side_d_map, POT[i], kd)
        iH3_bottom_D = fillPOT_2D(iH3_bottom_D, bottom_d_map, POT[i], kd)

        iH3_top_Dd    = fillPOT_2D(iH3_top_Dd, top_d_map, POT[i], kd)
        iH3_slant_Dd  = fillPOT_2D(iH3_slant_Dd, slant_d_map, POT[i], kd)
        iH3_side_Dd   = fillPOT_2D(iH3_side_Dd, side_d_map, POT[i], kd)
        iH3_bottom_Dd = fillPOT_2D(iH3_bottom_Dd, bottom_d_map, POT[i], kd)


        #print(i, iH3_top_DP[1])



    ###########################
    ### Temperatures
    ###########################

    T_top_DP = temperature(i, Ti_top_DP, Tf_top_DP, k_top_DP)
    
    T_wall = temperature(i, Ti_wall, Tf_wall, k_wall)

    T_top_air = 0.5*(T_top_DP + T_wall)

    T_side_DP = temperature(i, Ti_side_DP, Tf_side_DP, k_side_DP)
    
    T_side_air = 0.5*(T_top_DP + T_wall)

    T_bottom_DP = temperature(i, Ti_bottom_DP, Tf_bottom_DP, k_bottom_DP)
    
    T_bottom_wall = temperature(i, Ti_wall, Tf_wall, k_wall)

    T_bottom_air = 0.5*(T_bottom_DP + T_bottom_wall)

    T_slant_DP = T_top_DP

    T_slant_air = T_top_air

    T_bslant_DP = 0.5* (T_side_DP + T_bottom_DP)

    T_bslant_air = 0.5* (T_side_air + T_bottom_air)



    ###########################
    ### Diffusion
    ###########################

    dx = 10 #cm
    dt = 60 * 60 #seconds in an hour

    D_top_DP = Dt(Ddry, T_top_DP)
    D_slant_DP = Dt(Ddry, T_slant_DP)
    D_side_DP = Dt(Ddry, T_side_DP)
    D_bslant_DP = Dt(Ddry, T_bslant_DP)
    D_bottom_DP = Dt(Ddry, T_bottom_DP)

    D_bottom_wall = Dt(Ddry, T_bottom_wall)
    D_wall = Dt(Ddry, T_wall)

    Ddol_t = Dt(Ddol,12.5)

    
    iH3_top_DP    = diff1(iH3_top_DP, dx, dt, D_top_DP)
    iH3_slant_DP  = diff1(iH3_slant_DP, dx, dt, D_slant_DP)
    iH3_side_DP   = diff1(iH3_side_DP, dx, dt, D_side_DP)
    iH3_bottom_DP = diff1(iH3_bottom_DP, dx, dt, D_bottom_DP)
    iH3_bslant_DP = diff1(iH3_bslant_DP, dx, dt, D_bslant_DP)

    iH3_top, iH3_top_D       = diff2D(iH3_top, iH3_top_D, dx, dt, D_wall, Ddirt)
    iH3_slant, iH3_slant_D   = diff2D(iH3_slant, iH3_slant_D, dx, dt, D_wall, Ddirt)
    iH3_side, iH3_side_D     = diff2D(iH3_side, iH3_side_D, dx, dt, D_wall, Ddirt)
    iH3_bottom, iH3_bottom_D = diff2D(iH3_bottom, iH3_bottom_D, dx, dt, D_bottom_wall, Ddol_t)


    ###########################
    ### Air Boundry
    ###########################

    ####################################################
    #####  Impose thermal equilibrium across wall
    #####   AFTER determining bulk concrete parameters
    #####################################################
        

    T_top_DP = T_top_air 

    T_wall = T_top_air

    T_side_DP = T_top_air

    T_bottom_DP = T_bottom_air

    T_bottom_wall = T_bottom_air

    T_slant_DP = T_top_DP

    T_bslant_DP = T_bslant_air
    
    h_surf = 1

    h_air = 1

    #if i > Run:

        #h_surf = 0.25
        #h_air = 0.25

    
    #print(i, iH3_top_DP[n_top_DP-1])
    
    J_top_DP, evap_top_DP       = HTO_Current(iH3_top_DP[n_top_DP-2], iH3_air, T_top_DP,T_top_air, h_surf, h_air)
    J_slant_DP, evap_slant_DP   = HTO_Current(iH3_slant_DP[n_slant_DP-2], iH3_air, T_slant_DP, T_slant_air, h_surf, h_air)
    J_side_DP, evap_side_DP     = HTO_Current(iH3_side_DP[n_side_DP-2], iH3_air, T_side_DP, T_side_air, h_surf, h_air)
    J_bslant_DP, evap_bslant_DP = HTO_Current(iH3_bslant_DP[n_bslant_DP-2], iH3_air, T_bslant_DP, T_bslant_air, h_surf, h_air)
    J_bottom_DP, evap_bottom_DP = HTO_Current(iH3_bottom_DP[n_bottom_DP-2], iH3_bottom_air, T_bottom_DP, T_bottom_air, h_surf, h_air)


    #J_slant_DP = 1
    #J_side_DP = 1
    #J_bslant_DP = 1
    #J_bottom_DP = 1
    #evap_side_DP = 1
    #evap_bottom_DP = 1
    
    
    #print(i)
    #print("iH3_top_DP[last] = ",iH3_top_DP[n_top_DP-2])
    #print("iH3_air = ",iH3_air)
    #print("J_top_DP = ",J_top_DP)
    
    
    nH3_out_top_con    = dt * top_inner_surface * decay_pipe_length * J_top_DP
    nH3_out_slant_con  = dt * slant_inner_surface * decay_pipe_length  * J_slant_DP
    nH3_out_side_con   = dt * side_inner_surface  * decay_pipe_length * J_side_DP
    nH3_out_bslant_con = dt * bslant_inner_surface  * decay_pipe_length * J_bslant_DP
    nH3_out_bottom_con = dt * bottom_inner_surface  * decay_pipe_length * J_bottom_DP

    #nH3_out_top_con = 0
    #nH3_out_slant_con = 0
    #nH3_out_side_con = 0
    #nH3_out_bslant_con = 0
    #nH3_out_bottom_con = 0



        
    
    #print(i,"top DP", iH3_top_DP[n_top_DP-1], iH3_air , J_top_DP, nH3_out_top_con) 

    
    #print(i, "DP", nH3_out_top_con, nH3_out_slant_con, nH3_out_side_con, nH3_out_bslant_con, nH3_out_bottom_con) 
    

    nH3_out_top_wall, eH3_top_wall    = n_out(iH3_top, iH3_air, T_wall, T_top_air, h_surf, h_air, 10 * decay_pipe_length, dt)
    nH3_out_slant_wall, eH3_slant_wall  = n_out(iH3_slant, iH3_air, T_wall, T_slant_air, h_surf, h_air, 10 * decay_pipe_length, dt)
    nH3_out_side_wall, eH3_side_wall   = n_out(iH3_side, iH3_air, T_wall, T_side_air, h_surf, h_air, 10 * decay_pipe_length, dt)
    nH3_out_bottom_wall, eH3_bottom_wall = n_out(iH3_bottom, iH3_bottom_air, T_bottom_wall, T_bottom_air, h_surf, h_air, 10 * decay_pipe_length, dt)

    
    #nH3_out_top_wall = 0
    #nH3_out_slant_wall = 0
    #nH3_out_side_wall = 0
    #nH3_out_bottom_wall = 0

    nH3_into_air = (nH3_out_top_con +
                    nH3_out_slant_con +
                    nH3_out_side_con +
                    nH3_out_bslant_con +
                    nH3_out_top_wall +
                    nH3_out_slant_wall +
                    nH3_out_side_wall)

    
    

    nH3_into_bottom_air = nH3_out_bottom_con + nH3_out_bottom_wall

    
    iH3_air = iH3_air + (nH3_into_air / air_volume)

    if iH3_air < 0:
        iH3_air = 0
    
    iH3_bottom_air = iH3_bottom_air + (nH3_into_bottom_air / bottom_bounded_air_volume)                

    if iH3_bottom_air < 0:
        iH3_bottom_air = 0

    #############################
    #  check saturation
    #############################

    avg_C_DP = 0.25 * (iH3_top_DP[n_top_DP-2] +
                       iH3_slant_DP[n_slant_DP-2] +
                       iH3_side_DP[n_side_DP-2] +
                       iH3_bslant_DP[n_bslant_DP-2]) 

    avg_surf = 0.25 * (T_top_DP + T_slant_DP + T_side_DP + T_bslant_DP)
    
    sat_factor, iH3_air = H_HTO(avg_surf, iH3_air, avg_C_DP)

    sat_factor_b, iH3_bottom_air = H_HTO(T_bottom_DP, iH3_bottom_air, iH3_bottom_DP[n_bottom_DP-2])

    #sat_factor = 1
    #sat_factor_b = 1

    sat_factor = sat_factor * sat_factor_b

    
    #############################
    ## remove tritium from walls
    #############################
    
    iH3_top_DP[n_top_DP-2] = iH3_top_DP[n_top_DP-2] - sat_factor*nH3_out_top_con / (top_inner_surface * 10 * decay_pipe_length)
    iH3_slant_DP[n_slant_DP-2] = iH3_slant_DP[n_slant_DP-2] - sat_factor*nH3_out_slant_con / (slant_inner_surface*10* decay_pipe_length)
    iH3_side_DP[n_side_DP-2] = iH3_side_DP[n_side_DP-2] - sat_factor*nH3_out_side_con / (side_inner_surface*10* decay_pipe_length)
    iH3_bslant_DP[n_bslant_DP-2] = iH3_bslant_DP[n_bslant_DP-2] - sat_factor*nH3_out_bslant_con / (bslant_inner_surface*10* decay_pipe_length)
    iH3_bottom_DP[n_bottom_DP-2]  = iH3_bottom_DP[n_bottom_DP-2]- sat_factor_b*nH3_out_bottom_con / (bottom_inner_surface*10* decay_pipe_length) 

    if iH3_top_DP[n_top_DP-2] < 0:
        iH3_top_DP[n_top_DP-2] = 0

    if iH3_slant_DP[n_slant_DP-2] < 0:
        iH3_slant_DP[n_slant_DP-2] = 0

    if iH3_side_DP[n_slant_DP-2] < 0:
        iH3_side_DP[n_slant_DP-2] = 0

    if iH3_bslant_DP[n_bslant_DP-2] < 0:
        iH3_bslant_DP[n_bslant_DP-2] = 0

    if iH3_bottom_DP[n_bottom_DP-2] < 0:
        iH3_bottom_DP[n_bottom_DP-2] = 0


    #reset boundary conditions

    iH3_top_DP[n_top_DP-1] = iH3_top_DP[n_top_DP-2]
    iH3_slant_DP[n_slant_DP-1] = iH3_slant_DP[n_slant_DP-2]
    iH3_side_DP[n_side_DP-1] = iH3_side_DP[n_side_DP-2]
    iH3_bslant_DP[n_bslant_DP-1] = iH3_bslant_DP[n_bslant_DP-2]
    iH3_bottom_DP[n_bottom_DP-1] = iH3_bottom_DP[n_bottom_DP-2]
    

    #subtracting what came out
        
    iH3_top    = n_in(iH3_top, nH3_out_top_wall)
    iH3_slant  = n_in(iH3_slant, nH3_out_slant_wall)
    iH3_side   = n_in(iH3_side, nH3_out_side_wall)
    iH3_bottom = n_in(iH3_bottom, nH3_out_bottom_wall)

    #    print(i, iH3_top_DP[1], nH3_out_top_con / top_inner_surface)


    

    ##########################################################
    ### air change out on 60th day of the shutdown
    #########################################################



    if i%(24*365) == 0:

        ihours = 0

    if ihours < 24*7:
        
        #iH3_air = 0

        ihours = ihours + 1

    dumb = 0
    
    if i > Run:

        f0 = 0.0
        f25 = 0.999841753
        f50 = 0.999920873
        f75 = 0.999967159
        f90 = 0.999987972
        f100 = 1
        
        iH3_air = f100 * iH3_air
        iH3_bottom_air  =  f100 * iH3_bottom_air
    

    ################################################################
    ### mixing (once per year) basically just for plotting purposes
    ### but also not clear this should be going much faster than the velocity
    ### need to clarify with Chris how these numbers should be used
    #### trying product adding up to yearly number
    #################################################################

    #if i%(24*365) == 0:

        
    #iH3_bottom_D = mixed(i, iH3_bottom_D)
    #iH3_bottom_Dd = mixed(i, iH3_bottom_Dd)

    #iH3_bottom_D, iH3_bottom_D_mix, iH3_bottom_D_well = leaching(i, iH3_bottom_D, iH3_bottom_D_mix, iH3_bottom_D_well)
            
            

    
    
    #########################################################
    ### Record where we are at the end of each day
    #########################################################

    #cond = (0.0407/0.032) * (5.34/6.45)  #convert k factor and stars from dirt numbers to dolomite numbers

    cond = (0.0407/0.032)  #convert K factor from dirt to dolomite numbers

    
    if i%24 == 0:

        H3_bottom_air[iday] = iH3_bottom_air

        H3_air[iday] = iH3_air

        H3_top_DP[iday,:] = iH3_top_DP
        H3_slant_DP[iday,:] = iH3_slant_DP
        H3_side_DP[iday,:] = iH3_side_DP
        H3_bslant_DP[iday,:] = iH3_bslant_DP
        H3_bottom_DP[iday,:] = iH3_bottom_DP

        H3_top[iday,:,:] = iH3_top
        H3_slant[iday,:,:] = iH3_slant
        H3_side[iday,:,:] = iH3_side
        H3_bottom[iday,:,:] = iH3_bottom

        H3_top_D[iday,:,:] = iH3_top_D
        H3_slant_D[iday,:,:] = iH3_slant_D
        H3_side_D[iday,:,:] = iH3_side_D
        H3_bottom_D[iday,:,:] = iH3_bottom_D * cond

        H3_top_Dd[iday,:,:] = iH3_top_Dd
        H3_slant_Dd[iday,:,:] = iH3_slant_Dd
        H3_side_Dd[iday,:,:] = iH3_side_Dd
        H3_bottom_Dd[iday,:,:] = iH3_bottom_Dd * cond

        H3_bottom_D_mix[iday,:,:] = iH3_bottom_D_mix * cond
        H3_bottom_D_well[iday,:,:] = iH3_bottom_D_well * cond

        J_side_DPipe[iday] = J_side_DP
        J_side_wall[iday] = nH3_out_side_wall/side_outer_surface

        JE_side_DPipe[iday] = evap_side_DP
        JE_side_wall[iday] = eH3_side_wall/side_outer_surface

        J_bottom_DPipe[iday] = J_bottom_DP
        J_bottom_wall[iday] = nH3_out_bottom_wall/bottom_outer_surface
        
        JE_bottom_DPipe[iday] = evap_bottom_DP
        JE_bottom_wall[iday] = eH3_bottom_wall/bottom_outer_surface

        
        #print(iday, iH3_top_DP[1], H3_top_DP[iday,1])

        # mix bottom air and side air once per day
        iH3_air = 0.5*(iH3_air + iH3_bottom_air)

        iH3_bottom_air = iH3_air
        
        iday = iday + 1


            
    ##########################################################
    ### Decay all accumulated tritim by 1 hour
    #########################################################

    iH3_top_DP      = iH3_top_DP * math.exp(-1/H3_tau)
    iH3_slant_DP    = iH3_slant_DP * math.exp(-1/H3_tau)
    iH3_side_DP     = iH3_side_DP * math.exp(-1/H3_tau)
    iH3_bottom_DP   = iH3_bottom_DP * math.exp(-1/H3_tau)
    iH3_bslant_DP   = iH3_bslant_DP * math.exp(-1/H3_tau)

    iH3_air         = iH3_air * math.exp(-1/H3_tau)
    iH3_bottom_air  = iH3_bottom_air * math.exp(-1/H3_tau)

    iH3_top         = iH3_top * math.exp(-1/H3_tau)
    iH3_slant       = iH3_slant * math.exp(-1/H3_tau)
    iH3_side        = iH3_side * math.exp(-1/H3_tau)
    iH3_bottom      = iH3_bottom * math.exp(-1/H3_tau)

    iH3_top_D       = iH3_top_D * math.exp(-1/H3_tau)
    iH3_slant_D     = iH3_slant_D * math.exp(-1/H3_tau)
    iH3_side_D      = iH3_side_D * math.exp(-1/H3_tau)
    iH3_bottom_D    = iH3_bottom_D * math.exp(-1/H3_tau)

    iH3_bottom_D_mix = iH3_bottom_D_mix * math.exp(-1/H3_tau)
    iH3_bottom_D_well = iH3_bottom_D_well * math.exp(-1/H3_tau)

    iH3_top_Dd       = iH3_top_Dd * math.exp(-1/H3_tau)
    iH3_slant_Dd     = iH3_slant_Dd * math.exp(-1/H3_tau)
    iH3_side_Dd      = iH3_side_Dd * math.exp(-1/H3_tau)
    iH3_bottom_Dd    = iH3_bottom_Dd * math.exp(-1/H3_tau)

    
    ###########################
    ########## End big loop
    ###########################


    

#print(H3_top[1,10])
    

np.savez('fluka_H3_maps8-kg3e7.npz',
         #H3_top_DP1             = H3_top_DP,
         #H3_slant_DP1           = H3_slant_DP,
         #H3_side_DP1            = H3_side_DP,
         #H3_bslant_DP1          = H3_bslant_DP,
         #H3_bottom_DP1          = H3_bottom_DP,
         #H3_bottom_air1         = H3_bottom_air,
         #H3_air1                = H3_air,
         #H3_top1                = H3_top,
         #H3_slant1              = H3_slant,
         #H3_side1               = H3_side,
         #H3_bottom1             = H3_bottom,
         #H3_top_D1              = H3_top_D,
         #H3_slant_D1            = H3_slant_D,
         #H3_side_D1             = H3_side_D,
         H3_bottom_D1           = H3_bottom_D,
         H3_bottom_D_mix1       = H3_bottom_D_mix,
         H3_bottom_D_well1       = H3_bottom_D_well,
         #H3_top_Dd1             = H3_top_Dd,
         #H3_slant_Dd1           = H3_slant_Dd,
         #H3_side_Dd1            = H3_side_Dd,
         H3_bottom_Dd1          = H3_bottom_Dd
         #J_side_DPipe1          = J_side_DPipe,
         #J_side_wall1           = J_side_wall,
         #JE_side_DPipe1         = JE_side_DPipe,
         #JE_side_wall1          = JE_side_wall,
         #J_bottom_DPipe1        = J_bottom_DPipe,
         #J_bottom_wall1         = J_bottom_wall,
         #JE_bottom_DPipe1       = JE_bottom_DPipe,
         #JE_bottom_wall1        = JE_bottom_wall)
         )

end_time = time.perf_counter()

elapsed_time = end_time - start_time
elapsed_minutes = elapsed_time / 60

print(f"Execution time: {elapsed_minutes:.2f} minutes")
