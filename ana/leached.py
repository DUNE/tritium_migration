import matplotlib.pyplot as plt
import numpy as np




with np.load('../diff/fluka_H3_maps8-well.npz') as data:
    
    #    H3_bottom  = data['H3_bottom1']

    H3_bottom_D  = data['H3_bottom_D1']
    H3_bottom_Dd = data['H3_bottom_Dd1']
    H3_bottom_D_mix  = data['H3_bottom_D_mix1']
    H3_bottom_D_well  = data['H3_bottom_D_well1']

#with np.load('../diff/fluka_H3_maps8_not_leached.npz') as data:

    #H3_bottom_D_no_mix  = data['H3_bottom_D1']
    #H3_bottom_no_mix  = data['H3_bottom1']

    
H3_bottom_D_avg = np.zeros((H3_bottom_D.shape[0]))
H3_bottom_Dd_avg = np.zeros((H3_bottom_Dd.shape[0]))
H3_bottom_D_mix_avg = np.zeros((H3_bottom_D.shape[0]))
H3_bottom_D_no_mix_avg = np.zeros((H3_bottom_D.shape[0]))
H3_bottom_D_well_avg = np.zeros((H3_bottom_D_well.shape[0]))

ii = H3_bottom_D.shape[0]
jj = H3_bottom_D.shape[1]
kk = 17

#ii = 0
#jj = 0
#kk = 0


for i in range(ii):   #time

    sum = 0
    sumD = 0
    sumM = 0
    sumNM = 0
    sumW = 0
    
    n = 0
    nW = 0
    
    for j in range(jj):

        for k in range(kk):

            sum = sum + H3_bottom_D[i,j,k]
            sumD = sumD + H3_bottom_Dd[i,j,k]
            sumM = sumM + H3_bottom_D_mix[i,j,k]
            #sumNM = sumNM + H3_bottom_D_no_mix[i,j,k]

            n = n + 1



    for k in range(kk):

        sumW = sumW + H3_bottom_D_well[i,2*jj-1,k]

        nW = nW + 1
            

    H3_bottom_D_avg[i] = sum/n
    H3_bottom_Dd_avg[i] = sumD/n
    H3_bottom_D_mix_avg[i] = sumM/n
    H3_bottom_D_well_avg[i] = sumW/nW
    #H3_bottom_D_no_mix_avg[i] = sumNM/n
            

max_hours = 30*365

print(max_hours)
    
hours_per_year = 365
    
x_values = np.zeros(max_hours)

            

for i in range(max_hours):


    x_values[i] = i/hours_per_year

#plt.plot(x_values,H3_bottom_D_no_mix_avg)
#plt.plot(x_values,H3_bottom_Dd_avg)
#plt.plot(x_values,H3_bottom_D_avg)
#plt.plot(x_values,H3_bottom_D_mix_avg)
plt.plot(x_values,H3_bottom_D_well_avg)



max_id = np.argmax(H3_bottom_D_mix_avg)
max_y = H3_bottom_D_mix_avg[max_id]
print(max_y)


#plt.plot(H3_bottom_no_mix[20*365,:,:].mean(axis=0))
#plt.plot(H3_bottom[20*365,:,:].mean(axis=0))



#plt.title('Tritium in the rock',fontsize=14)
#plt.title('Tritium in bottom wall @ 20y avg over parallel',fontsize=14)
#plt.title('Tritium in the bottom rock hottest spot',fontsize=14)
#plt.title('Tritium current out of decay pipe (bottom)',fontsize=14)
#plt.title('Tritium current out of wall (side)',fontsize=14)
#plt.ylabel('H3 concentration (pCi/cc)',fontsize=14)
#plt.ylabel('J(pCi/cm2/sec)',fontsize=14) 
#plt.xlabel('bin number (10 cm bins)',fontsize=14)
#plt.xlabel('time (years)',fontsize=14)

#plt.ylim(0,5.0)    
#plt.xlim(10,15)    

plt.tick_params(labelsize=16)


plt.tight_layout()


#plt.plot(H3_bottom_D[20*365,10,:])
#plt.plot(H3_bottom_D[20*365,:,1])

#plt.plot(H3_bottom_Dd[20*365,10,:])
#plt.plot(H3_bottom_Dd[20*365,:,1])

#plt.plot(H3_bottom_Dd_avg[20*365,:])

#
#plt.plot(x_values,H3_bottom_Dd_avg)

#plt.plot(x_values,H3_bottom_D_mix_avg)




#
#plt.xlim(50,60)    
#plt.semilogy(H3_bottom_DP[20*365,:])
#plt.plot(H3_bottom_DP[29*365,:])    
#plt.semilogy(H3_bottom_DP[199*365,:])

#plt.plot(H3_air[:])


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




