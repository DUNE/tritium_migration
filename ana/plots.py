import matplotlib.pyplot as plt
import numpy as np




with np.load('../diff/fluka_H3_maps8-nm-slow.npz') as data:

    #H3_bottom    = data['H3_bottom1']
    H3_bottom_D  = data['H3_bottom_D1']
    H3_bottom_Dd = data['H3_bottom_Dd1']
    H3_bottom_D_mix  = data['H3_bottom_D_mix1']

    
    #H3_side    = data['H3_side1']
    #H3_side_D  = data['H3_side_D1']
    #H3_side_Dd = data['H3_side_Dd1']

    #H3_slant    = data['H3_slant1']
    #H3_slant_D  = data['H3_slant_D1']
    #H3_slant_Dd = data['H3_slant_Dd1']

    #H3_top    = data['H3_top1']
    #H3_top_D  = data['H3_top_D1']
    #H3_top_Dd = data['H3_top_Dd1']
    
    #J_bottom_DPipe     = data['J_bottom_DPipe1']

    #J_bottom_wall      = data['J_bottom_wall1']

    #J_side_DPipe     = data['J_side_DPipe1']

    #J_side_wall      = data['J_side_wall1']

    
with np.load('../diff/fluka_H3_maps8-nm-fast.npz') as data:

    H3_bottom_D_fast  = data['H3_bottom_D1']
    


    
H3_bottom_D_avg = np.zeros((H3_bottom_D.shape[0]))
H3_bottom_Dd_avg = np.zeros((H3_bottom_Dd.shape[0]))
H3_bottom_D_mix_avg = np.zeros((H3_bottom_D.shape[0]))

ii = H3_bottom_D.shape[0]
jj = H3_bottom_D.shape[1]
kk = 17

ii = 0
jj = 0
kk = 0


for i in range(ii):   #time

    sum = 0
    sumD = 0
    sumM = 0
    n = 0
    
    for j in range(jj):

        for k in range(kk):

            sum = sum + H3_bottom_D[i,j,k]
            sumD = sumD + H3_bottom_Dd[i,j,k]
            sumM = sumM + H3_bottom_D_mix[i,j,k]

            n = n + 1


    H3_bottom_D_avg[i] = sum/n
    H3_bottom_Dd_avg[i] = sumD/n
    H3_bottom_D_mix_avg[i] = sumM/n
            

max_hours = 50*365

print(max_hours)
    
hours_per_year = 365
    
x_values = np.zeros(max_hours)

            

for i in range(max_hours):


    x_values[i] = i/hours_per_year



norm = lambda y: (y - np.min(y)) / (np.max(y)-np.min(y))
    

#plt.plot(norm(H3_top[1*365,:,1]))
#plt.plot(norm(H3_top[49*365,:,1]))

#plt.plot(norm(H3_top[1*365,1,:]))
#plt.plot(norm(H3_top[49*365,1,:]))


plt.plot(H3_bottom_D[20*365,:,1])
plt.plot(H3_bottom_D_fast[20*365,:,1])

#plt.plot(H3_side_D[20*365,1,:])

#plt.plot(H3_top_D[20*365,:,:].mean(axis=1))
#plt.plot(H3_bottom_D[20*365,:,:].mean(axis=0))

#plt.plot(x_values,H3_bottom_D[:,1,1])
#plt.plot(x_values,H3_bottom_Dd[:,1,1])

#plt.plot(x_values,J_side_wall)


#plt.title('Tritium in bottom dirt @ 20y avg over perp',fontsize=14)
#plt.title('Tritium in bottom dirt @ 20y avg over parallel',fontsize=14)
#plt.title('Tritium in the bottom rock hottest spot',fontsize=14)
#plt.title('Tritium current out of decay pipe (bottom)',fontsize=14)
plt.title('Tritium current out of wall (side)',fontsize=14)
#plt.ylabel('H3 concentration (pCi/cc)',fontsize=14)
plt.ylabel('J(pCi/cm2/sec)',fontsize=14) 
#plt.xlabel('bin number (10 cm bins)',fontsize=14)
plt.xlabel('time (years)',fontsize=14)


plt.tick_params(labelsize=16)

#plt.subplots_adjust(top=0.925)
#plt.subplots_adjust(bottom=0.88)

plt.tight_layout()


    
#plt.ylim(0.0, 50000.0)


#plt.plot(H3_top[20*365,:,1])
#plt.plot(H3_top[20*365,1,:])

#plt.plot(H3_top_D[20*365,:,1])
#plt.plot(H3_top_Dd[20*365,:,1])

#plt.plot(H3_top_D[20*365,1,:])
#plt.plot(H3_top_Dd[20*365,1,:])




#plt.plot(H3_slant[20*365,:,1])
#plt.plot(H3_slant[20*365,25,:])

#plt.plot(H3_slant_D[20*365,:,1])
#plt.plot(H3_slant_Dd[20*365,:,1])

#plt.plot(H3_slant_D[20*365,25,:])
#plt.plot(H3_slant_Dd[20*365,25,:])



#plt.plot(H3_side[20*365,:,1])
#plt.plot(H3_side[20*365,80,:])

#plt.plot(H3_side_D[20*365,:,1])
#plt.plot(H3_side_Dd[20*365,:,1])

#plt.plot(H3_side_D[20*365,80,:])
#plt.plot(H3_side_Dd[20*365,80,:])




#plt.plot(H3_bottom[20*365,10,:])
#plt.plot(H3_bottom[20*365,:,1])

#plt.plot(H3_bottom_D[20*365,10,:])
#plt.plot(H3_bottom_D[20*365,:,1])

#plt.plot(H3_bottom_Dd[20*365,10,:])
#plt.plot(H3_bottom_Dd[20*365,:,1])

#plt.plot(H3_bottom_Dd_avg[20*365,:])

#
#plt.plot(x_values,H3_bottom_Dd_avg)

#plt.plot(x_values,H3_bottom_D_mix_avg)




#plt.ylim(0,100)    
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




