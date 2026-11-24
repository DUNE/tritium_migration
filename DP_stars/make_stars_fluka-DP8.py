import matplotlib.pyplot as plt
import numpy as np
import math

###########
#  External Constants
##########


#########################################
##### Geometries and binnings
#########################################

### Geometries from Paola
### and these are the ones I used when defining the functions
### used to fit stars versus radius, x, y, or x prime

DP_top_inner = 230 #cm
DP_top_outer = 680 #cm

DP_top_r = DP_top_outer - DP_top_inner

DP_slant_inner = 230 #cm
DP_slant_outer = 680 #cm

DP_slant_r = DP_slant_outer - DP_slant_inner

DP_side_inner = 230 #cm
DP_side_outer = 745 #cm

DP_side_r = DP_side_outer - DP_side_inner

DP_bslant_inner = 230 #cm
DP_bslant_outer = 745 #cm

DP_bslant_r = DP_bslant_outer - DP_slant_inner

DP_bottom_inner = 230 #cm
DP_bottom_outer = 745 #cm

DP_bottom_r = DP_bottom_outer - DP_bottom_inner


#### 10 cm bins

nbins_top_DP = int(DP_top_r/10)
nbins_slant_DP = int(DP_slant_r/10)
nbins_side_DP = int(DP_side_r/10)
nbins_bslant_DP = int(DP_bslant_r/10)
nbins_bottom_DP = int(DP_bottom_r/10)


##### Add boundry condition bins
##### both sides of decay pipe
##### Inside of outer wall
##### Outside of dirt

nbins_top_DP = nbins_top_DP + 2
nbins_slant_DP = nbins_slant_DP + 2
nbins_side_DP = nbins_side_DP + 2
nbins_bslant_DP = nbins_bslant_DP + 2
nbins_bottom_DP = nbins_bottom_DP + 2



#################################################
#################################################
##### Star Maps
#################################################
#################################################


########################
#####   Inner decay pipe
########################

#####   Top

top_DP_map = np.empty(nbins_top_DP)

p0 = 1.65
p1 = -0.14
p2 = 0.00036
p3 = -4.8e-7
p4 = 2.4e-10

for i in range(nbins_top_DP):

    x = (DP_top_inner - 0.5) + i*10

    ln_stars = p0 + p1*x + p2*x*x + p3*x*x*x + p4*x*x*x*x

    stars = math.exp(ln_stars)

    top_DP_map[i] = stars #stars/cc/proton
    
top_DP_map[0] = 0
top_DP_map[nbins_top_DP-1] = 0

#####   Slant

slant_DP_map = np.empty(nbins_slant_DP)

p0 = -1.43
p1 = -0.11
p2 = 0.00024
p3 = -2.94e-7
p4 =  1.32e-10

for i in range(nbins_slant_DP):

    x = (DP_slant_inner - 0.5) + i*10

    ln_stars = p0 + p1*x + p2*x*x + p3*x*x*x + p4*x*x*x*x

    stars = math.exp(ln_stars)

    slant_DP_map[i] = stars
    
slant_DP_map[0] = 0
slant_DP_map[nbins_slant_DP-1] = 0

###### side

side_DP_map = np.empty(nbins_side_DP)


p0 = 5.53
p1 = -0.18
p2 = 0.00051
p3 = -7.14e-7
p4 = 3.74e-10

for i in range(nbins_side_DP):

    x = (DP_side_inner - 0.5) + i*10

    ln_stars = p0 + p1*x + p2*x*x + p3*x*x*x + p4*x*x*x*x
        
    stars = math.exp(ln_stars)

    side_DP_map[i] = stars  #stars/cc/proton
    
side_DP_map[0] = 0
side_DP_map[nbins_side_DP-1] = 0


######### bottom slant


bslant_DP_map = np.empty(nbins_bslant_DP)


p0 = -7.28
p1 = 302.39
p2 = 543.23
p3 = -21.55
p4 = 0.064
p5 = -0.00027
p6 = 3.46e-7
p7 = -1.60e-10

for i in range(nbins_bslant_DP):

    x = (DP_bslant_inner - 0.5) + i*10

    ln_stars = ( p0*math.exp(-0.5*(x-p1)*(x-p1)/p2) +
                 p3 + p4*x + p5*x*x + p6*x*x*x + p7*x*x*x*x )
        
    stars = math.exp(ln_stars)

    bslant_DP_map[i] = stars  #stars/cc/proton
    
bslant_DP_map[0] = 0
bslant_DP_map[nbins_bslant_DP-1] = 0


###### bottom

bottom_DP_map = np.empty(nbins_bottom_DP)


p0 = 15.26
p1 = -0.3042
p2 = 0.001098
p3 = -2.1e-6
p4 = 1.96e-9
p5 = -7.111e-13

for i in range(nbins_bottom_DP):

    x = (DP_bottom_inner - 0.5) + i*10

    ln_stars = p0 + p1*x + p2*x*x + p3*x*x*x + p4*x*x*x*x + p5*x*x*x*x*x
        
    stars = math.exp(ln_stars)

    bottom_DP_map[i] = stars  #stars/cc/proton
    
bottom_DP_map[0] = 0
bottom_DP_map[nbins_bottom_DP-1] = 0




#################
##### Air
#################

air = 1.737e-16

bottom_air = 2.15e-16



####################################
########  Concert to tritium in pCi
####################################

H3_Atoms_per_pC = 9.6e6  #atoms per pC

Kair = 0.035

Kcon = 0.035


####  Air

air = air * Kair / H3_Atoms_per_pC   #pCi/cc/proton

bottom_air = bottom_air * Kair / H3_Atoms_per_pC   #pCi/cc/proton 

#### Concrete

top_DP_map = top_DP_map * Kcon / H3_Atoms_per_pC   #pCi/cc/proton

slant_DP_map = slant_DP_map * Kcon / H3_Atoms_per_pC   #pCi/cc/proton

side_DP_map = side_DP_map * Kcon / H3_Atoms_per_pC   #pCi/cc/proton

bslant_DP_map = bslant_DP_map * Kcon / H3_Atoms_per_pC   #pCi/cc/proton

bottom_DP_map = bottom_DP_map * Kcon / H3_Atoms_per_pC   #pCi/cc/proton 


np.savez('fluka_star_maps_DP8.npz',
         top_DP_map1      = top_DP_map,
         slant_DP_map1    = slant_DP_map,
         side_DP_map1     = side_DP_map,
         bslant_DP_map1   = bslant_DP_map,
         bottom_DP_map1   = bottom_DP_map, 
         air1             = air,
         bottom_air1      = bottom_air)

