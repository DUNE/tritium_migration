import matplotlib.pyplot as plt
import numpy as np




with np.load('../diff/fluka_H3_maps8.npz') as data:


    J_bottom_DPipe     = data['J_bottom_DPipe1']
    JE_bottom_DPipe    = data['JE_bottom_DPipe1']

    J_bottom_wall      = data['J_bottom_wall1']
    JE_bottom_wall     = data['JE_bottom_wall1']

    J_side_DPipe     = data['J_side_DPipe1']
    JE_side_DPipe    = data['JE_side_DPipe1']

    J_side_wall      = data['J_side_wall1']
    JE_side_wall     = data['JE_side_wall1']

    H3_bottom_DP_on     = data['H3_bottom_DP1']
    H3_bottom_on     = data['H3_bottom1']
    
with np.load('../diff/fluka_H3_maps8_no_transport.npz') as data:

    H3_bottom_DP_off     = data['H3_bottom_DP1']
    J_bottom_DPipe_off     = data['J_bottom_DPipe1']
    

max_hours = 50*365

print(max_hours)
    
hours_per_year = 365
    
x_values = np.zeros(max_hours)



            

for i in range(max_hours):


    x_values[i] = i/hours_per_year

    
#plt.ylim(0.0, 50000.0)



#plt.plot(x_values,J_bottom_DPipe_off)
#plt.plot(x_values,JE_side_DPipe)

#plt.plot(x_values,J_side_wall)

#plt.plot(H3_bottom_DP_off[:,51])
#plt.plot(H3_bottom_DP_on[:,51])



#plt.semilogy(H3_bottom_wall_on[:,1])    





#plt.ylim(0,100)    
#plt.xlim(50,60)    
#plt.plot(x_values,H3_bottom_Dd_avg)
#plt.plot(H3_bottom_DP[29*365,:])    
#plt.semilogy(H3_bottom_DP[199*365,:])

#plt.plot(H3_air[:])


#plt.title('Tritium in the Dolomite')
#plt.ylabel('H3 concentration (arbitrary units)') 
#plt.xlabel('time (years)')
#plt.xlabel('time (years)')
#
#
#plt.plot(x_values, H3_bottom_dirt_direct)


#plt.plot(H3_bottom[49*365,15,:])
#plt.plot(H3_bottom[49*365,:,4])

#plt.semilogy(H3_bottom_D[20*365,15,:])
#plt.semilogy(H3_bottom_D[30*365,15,:])
#plt.semilogy(H3_bottom_D[40*365,15,:])
#plt.plot(H3_bottom_D[20*365,:,4])
#plt.plot(H3_bottom_D[30*365,:,4])
#plt.plot(H3_bottom_D[40*365,:,4])

#plt.plot(H3_side[9,60,:])
#plt.plot(H3_side[9,:,5])

#plt.plot(H3_side_D[1*365,25,:])
#plt.plot(H3_side_D[30*365,25,:])

#plt.plot(H3_side_D[20*365,:,5])

#plt.plot(H3_slant[9,10,:])
#plt.plot(H3_slant[9,:,5])

#plt.plot(H3_slant_D[9,10,:])
#plt.plot(H3_slant_D[9,:,2])

#plt.plot(H3_top[4*364,10,:])
#plt.plot(H3_top[4*364,:,5])

#plt.plot(H3_top_D[9,10,:])
#plt.plot(H3_top_D[1,:,5])


#plt.semilogy(H3_bottom_DP[49*365,:])

#plt.semilogy(H3_air[:])

#plt.semilogy(H3_bottom_DP[1*365,:])


#plt.semilogy(H3_side_DP[100*365,:])
#plt.semilogy(H3_side_DP[199*365,:])

#plt.semilogy(H3_side_DP[199*365,:])


#plt.semilogy(x_values,H3_side_DP[:,50])
#plt.semilogy(x_values,H3_wall)
#plt.semilogy(x_values,H3_air)
#plt.semilogy(H3_air)

#plt.semilogy(x_values,H3_dol)



#plt.semilogy(H3_side_DP[20*365,:])
#plt.semilogy(H3_side_DP[40*365,:])
#plt.plot(H3_top_DP[10*365,10])


#plt.semilogy(H3_side[20*365,5,:])
#plt.semilogy(H3_side[40*365,5,:])
#plt.plot(H3_top[50*365,5,:])

#plt.plot(H3_top[:,5,5])
#plt.plot(H3_top[:,5,5])
#plt.semilogy(H3_slant_DP[150*365,:])
#plt.plot(H3_side_dirt[20*365,:])
#plt.plot(H3_side_dirt[:,1])
#plt.plot(x_values, H3_d)


plt.show()




