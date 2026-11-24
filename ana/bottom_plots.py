import matplotlib.pyplot as plt
import numpy as np




with np.load('../diff/fluka_H3_maps8_bottom_only.npz') as data:


    H3_bottom = data['H3_bottom1']

    H3_bottom_D = data['H3_bottom_D1']

    H3_bottom_Dd = data['H3_bottom_Dd1']

    H3_bottom_Dt = data['H3_bottom_Dt1']


    H3_bottom_avg = data['H3_bottom_avg1']

    H3_bottom_D_avg = data['H3_bottom_D_avg1']

    H3_bottom_Dd_avg = data['H3_bottom_Dd_avg1']


    


max_hours = 30*365

print(max_hours)
    
hours_per_year = 365
    
x_values = np.zeros(max_hours)

H3_bottom_avg2 = np.zeros((H3_bottom.shape[0], H3_bottom.shape[2]))

H3_bottom_D_avg2 = np.zeros((H3_bottom_D.shape[0], H3_bottom_D.shape[2]))

H3_bottom_Dd_avg2 = np.zeros((H3_bottom_Dd.shape[0], H3_bottom_Dd.shape[2]))
                            

for i in range(H3_bottom.shape[0]):   #time
    
    for j in range(H3_bottom.shape[2]):   #y

        sum = 0

        for k in range(H3_bottom.shape[1]):   # average over x

            sum = sum + H3_bottom[i,k,j]

        H3_bottom_avg2[i,j] = sum/H3_bottom.shape[1]
            

for i in range(max_hours):


    x_values[i] = i/hours_per_year

    
#plt.ylim(0.0, 50000.0)



#plt.plot(H3_bottom[20*365,10,:])
#plt.plot(H3_bottom[20*365,:,1])

#plt.plot(H3_bottom_D[20*365,10,:])
#plt.plot(H3_bottom_D[50*365,:,1])

#plt.plot(H3_bottom_Dd[20*365,10,:])
#plt.plot(H3_bottom_Dd[20*365,:,1])

#plt.plot(H3_bottom_Dd_avg[20*365,:])


#plt.plot(H3_bottom_avg[49*365,:])
#plt.plot(H3_bottom_avg2[49*365,:])

plt.plot(H3_bottom_D[49*365,10,:])
plt.plot(H3_bottom_Dt[49*365,10,:])



#plt.ylim(0,100)    
#plt.xlim(50,60)    
#plt.semilogy(H3_bottom_DP[20*365,:])
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




