import numpy as np
import math

#################################
####### Functions
################################

##### accumulate tritium in the decay pipe

def fillPOT(array, array_map, POT):

    n = len(array)

    for jj in range(n):
        
        array[jj] = array[jj] + array_map[jj] * POT

    return array


##### accumulate tritium in the walls
##### note I havent converted from stars to tritium yet in the wall or dirt maps

def fillPOT_2D(array, array_map, POT, k):

    H3_Atoms_per_pC = 9.6e6  #atoms per pC
    
    
    nx = array.shape[0]
    ny = array.shape[1]

    for jj in range(nx):

        for kk in range(ny):
        
            array[jj,kk] = array[jj,kk] + array_map[jj,kk] * POT * k / H3_Atoms_per_pC

    return array




###### radial diffusion in a constant substrate, (azmuthally symmetric)

def diff1(array, dr, dt, D):

    n = len(array)
    
    temp = array.copy()
    
    for j in range(1,n-1):

        r = 229.5 + j
        
        temp[j] = array[j] + D * dt  * (( array[j+1] - 2*array[j] + array[j-1])/(dr*dr) +
                                        (1/r)*(array[j+1]-array[j-1])/(2*dr))


    temp[0] = temp[1]   # boundry conditons

    temp[n-1] = temp[n-2]

    array = temp

    return array


###### 1D linear diffusion with a sandwich of two simmilar materials

def diff2(array1, array2, dx, dt, D1, D2):

    n1 = len(array1)
    n2 = len(array2)
    
    temp1 = array1.copy()
    temp2 = array2.copy()

    for j in range(1,n1-1):

        temp1[j] = array1[j] + (D1 * dt /(dx*dx)) * ( array1[j+1] -2*array1[j] + array1[j-1])
        
    D = 0.5*(D1+D2)

    # fast term at boundary

    D = 1.62e-5 #at 12 degrees C

    temp1[n1-1] = array1[n1-1] + (D * dt /(dx*dx)) * ( array2[0] -2*array1[n1-1] + array1[n1-2])

    temp2[0] = array2[0] + (D * dt /(dx*dx)) * ( array2[1] -2*array2[0] + array1[n1-1])


    for j in range(1,n2-1):

        temp2[j] = array2[j] + (D2 * dt /(dx*dx)) * ( array2[j+1] -2*array2[j] + array2[j-1])
    
        
        
    temp1[0] = temp1[1]   # boundry conditons

    temp2[n2-1] = temp2[n2-2]

    array1 = temp1

    array2 = temp2

    return array1, array2




###### linear 2D diffusion with a sandwich of two simmilar materials
    
    
def diff2D(array1, array2, dx, dt, D1, D2):

    n1x = array1.shape[0]
    n1y = array1.shape[1]

    n2x = array2.shape[0]
    n2y = array2.shape[1]

    dy = dx

    #print(n1x, n2x)
    

    laplas1 = (
        (array1[2:,1:-1] -2*array1[1:-1,1:-1] + array1[:-2,1:-1]) / (dx*dx) +
        (array1[1:-1,2:] -2*array1[1:-1,1:-1] + array1[1:-1,:-2]) / (dy*dy)
        )


    array1[1:-1,1:-1] += D1 * dt * laplas1

    D = 0.5*(D1+D2)

    for i in range(1, n1x-1):
    
        array1[i,n1y-1] = array1[i, n1y-1] + (D * dt /(dx*dx)) * ( array2[i,0] -2*array1[i,n1y-1] + array1[i,n1y-2])

    for i in range(1, n2x-1):
        
        array2[i,0] = array2[i,0] + (D * dt /(dx*dx)) * ( array2[i,1] -2*array2[i,0] + array1[i,n1y-1])


    laplas2 = (
        (array2[2:,1:-1] -2*array2[1:-1,1:-1] + array2[:-2,1:-1]) / (dx*dx) +
        (array2[1:-1,2:] -2*array2[1:-1,1:-1] + array2[1:-1,:-2]) / (dy*dy)
        )


    array2[1:-1,1:-1] += D2 * dt * laplas2


    ## boundary conditions

    for i in range(0, n1x-1):
                
        array1[i,0] = array1[i,1]   ## y = 0

    for i in range(0, n2x-1):
        
        array2[i,n2y-1] = array2[i,n2y-2]   ## y = max

    for j in range(0, n1y-1):
                
        array1[0,j] = array1[1,j]    ## x = 0

        array1[n1x-1,j] = array1[n1x-2,j]   ## x = max

    for j in range(0, n2y-1):
                
        array2[0,j] = array2[1,j]  ## x = 0

        array2[n2x-1,j] = array2[n2x-2,j]   ## x = max


    
    return array1, array2



###################  Current out of concrete
    

def HTO_Current(C_surf, C_air, T_surf, T_air, h_surf, h_air):

    #####
    #    
    # Ew  bulk evaporation rate  kg/m2/sec
    # beta_p = 6e-9 conective mass transfer coefficient kg/m2/sec/Pa, value for ~stagnant air
    # h_surf   relative humidity at the concrete surface
    # h_air  relative humidity in the air
    # p_sat_surf saturation vapor pressure, Pascals
    # C  concentrations in Bq/m3    
    
    p_sat_surf = psat(T_surf)
    
    p_sat_air = psat(T_air)

    beta_p = 6e-9
    
    Ew = beta_p * (p_sat_surf * h_surf - p_sat_air * h_air)

    #  Bq/m3 * cm3/pCi

    con1 = 0.037 #Bq/pCi 
    
    C_surf = con1 * C_surf  # (Bq/cc)
    C_air = con1 * C_air  # (Bq/cc)

    con2 = 1000000  # 1/cc to 1/m3

    C_surf = con2 * C_surf  # (Bq/m3)
    C_air = con2 * C_air  # (Bq/m3)
    
    rho_w = 1000  # water density kg/m3
    
    alpha_evap = 1.09 #liquid to vaport isotopic fraction for tritium


    C = 1

    if Ew >= 0:
        C = C_surf

    if Ew < 0:
        C = C_air

    evap_part = Ew * (C/(rho_w * alpha_evap))

    #print("evap part = ", evap_part)

    ### diffusion part

    pourosity = 0.23

    C_surf = C_surf / pourosity   # Bq/m3 water

    m3toL = 1000

    C_surf = C_surf / m3toL  #Bq/L

    chi_HTO_conversion = 1.11e17  #Bq/L

    chi_HTO = C_surf / chi_HTO_conversion

    p_star = chi_HTO * p_sat_surf / alpha_evap

    
    Bq_to_moles = 9.31e-16

    C_air = C_air * Bq_to_moles   # moles/m3

    R = 8.314 #K/mol/K

    p_HTO_air = C_air * R * (T_air + 273.3)

    delta_p = h_surf * p_star - h_air * p_HTO_air
    
    kg = 1.11e-6
    kg = 6.00e-6
    kg = 3.00e-7

    dp_part = kg * delta_p

    #print("dp part = ", dp_part)
    
    J_HTO = (evap_part + dp_part)

    #print("......")
    #print(evap_part, dp_part)      
    
    # pCi/cm2/sec

    J_HTO = (1/(con1*con2)) * J_HTO

    evap_part = (1/(con1*con2)) * evap_part

    
    return J_HTO, evap_part

### number of tritium pCi leaving the surface of a wall 

def n_out(C_surf, C_air, T_surf, T_air, h_surf, h_air, surface_area, dt):

    nx = C_surf.shape[0]
    ny = C_surf.shape[1]
    
    nH3 = 0

    evapH3 = 0
    
    for i in range(nx):

        Ji, evapi = HTO_Current(C_surf[i,1], C_air, T_surf, T_air, h_surf, h_air)

        #print(nH3, Ji)

        nH3 = nH3 + dt * surface_area * Ji

        evapH3 = evapH3 + dt * surface_area * evapi


        
    return nH3, evapH3

### number of tritium pCi moving from air into the wall


def n_in(C_surf,nout):

    decay_pipe_length = 1
    
    nx = C_surf.shape[0]
    ny = C_surf.shape[1]

    # 10x10x10 volume bins
    
    for i in range(1,nx-1):

        C_surf[i,1] = C_surf[i,1] - nout/(100*decay_pipe_length)

        if C_surf[i,1] < 0:
            C_surf[i,1] = 0 

        ## reset boundary conditions

        C_surf[i,0] = C_surf[i,1]
            
    return C_surf
        
################# mixing

def mixed(i, array):

    p0 = 0.12
    p1 = -6.469e-5
    p2 = 1.355e-8
    p3 = -5.554e-13

    x = i

    R = 1.0

    if i < 24 * 365:

        #R = p0 + p1*x + p2*x*x + p3*x*x*x

        #R = 0.17

        R = 0.999979774
        
    if i >= 24 * 365:

        #R = 0.35

        R = 0.99988016
        
    if i > 8 * 24 * 365:

        #R = 0.8

        R = 0.99997453

    #temp = array.copy()
        
    return R * array




def leaching(k, counter_cc, counter_mL, well):

    # k is hours
    

    R = 1.0

    if k < 24 * 365:

        R = 0.999979774
        
    if k >= 24 * 365:

        #R = 0.35

        R = 0.99988016
        
    if k > 8 * 24 * 365:

        #R = 0.8

        R = 0.99997453

    length = 2*1006.0   #cm
    height = 170 
    width = 5   #cm  assuming about a 2 inch screen

    V = length * height * width

    Q = V/R  #cc/year

    Q = Q / (365*24)

    rho_water = 1   # g/cc
    rho_dolomite = 2.5 # g/cc asuming 100% saturation and 20% porosity

    water_weight = 980 * rho_water * Q

    dolomite_weight = 980 * rho_dolomite * V

    w = water_weight / dolomite_weight

    k = -9.4

    L = (1-math.exp(k*w))

    ii = counter_cc.shape[0]
    jj = counter_cc.shape[1]

    Lout = np.zeros((ii, jj))    

    #first loop through and leach out the tritium
    #subtract if from the accumulated tritium
    #track how muc went into the water
    
    for i in range(ii):

        for j in range(jj):
    
            leached = L * counter_cc[i,j]

            Lout[i,j] = leached
            
            counter_cc[i,j] = counter_cc[i,j] - leached
            
            counter_mL[i,j] = counter_mL[i,j] + leached

    #now flow the water along the bottom

    for i in range(2 * ii):

        for j in range(jj):


            if k % 33 == 0:   # water speed is 0.3 cm/hour so it take 33 hours to move 10 cm

                if i == 0:

                    well[i,j] = 0    # bring the new clean water into the system

                if i > 0:

                    well[i,j] = well[i-1, j]  # flow the water to the next bin

        
            #if you are not at the 33 hour break, just accumulate the tritium
            # wrap around since FLUKA is using mirror symmetry around x = 0

            if i < ii:
            
                well[i,j] = well[i,j] + Lout[ii - i - 1,j]   #first water sees mirror image of xmax

            if i >= ii:

                well[i,j] = well[i,j] + Lout[i - ii,j]   #midway through water sees xmin


    return counter_cc, counter_mL, well





######## concrete temperature per year based on parameters taken from numeric model

def temperature(i, Ti, Tf, k):

    ## concert hour to year

    year = i/(365*24)
    
    T = Tf + (Ti-Tf)*math.exp(-k*year)

    if(year > 20):

            T = Tf + (Ti-Tf)*math.exp(-k*(year-21))
    
    return T

#### temperature dependence of saturation pressure

def psat(T):

    p = 610.78 * math.exp((17.27 * T) / (T + 237.3))

    return p

##### temperature dependence of diffusion coefficient with respect to a measured value at 22 degrees C

def Dt(D,T):

    R = 8.314e-3  # kJ/mol/K

    Qd = 21.5 # kJ/mol

    #Qd = 22 # kJ/mol   high
    #Qd = 18 # kJ/mol   low


    T_ref = 295.15

    T2 = T + 273 #K

    arg = (Qd/R) * ((1/T_ref) - (1/T2))
    
    Dnew  = D * math.exp(arg)

    return Dnew


###### temperature dependence of the density of water

def RhoWater(T):

    # temp in celcius, density in kg/m3

    rho = 1000 - 0.04735 * T - 0.004116 * T * T

    return rho

##### phase partition factor used for saturation

def H_HTO(T_surf, C_air, C_surf):

    MH20 = 0.018015 #kg/mol

    R = 8.314  # J/mol-K

    psat_surf = psat(T_surf)

    rho_water = RhoWater(T_surf)
    
    rho_sat = psat_surf * MH20 / (R*(T_surf + 273.3))

    Hsat = rho_sat / rho_water

    sat_factor = 1
    
    if C_air > C_surf * Hsat:

        sat_factor =  C_surf * Hsat / C_air
    
        C_air = C_surf * Hsat

    return sat_factor, C_air
        

def Dpor(D_old, p_old, p_new, m):


    D_new = D_old * ((p_new / p_old) ** m)

    return D_new


def Dsat(D_old, S_old, S_new, n):


    D_new = D_old * ((S_new / S_old) ** n)

    return D_new

