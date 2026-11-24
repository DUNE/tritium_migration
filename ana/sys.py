import matplotlib.pyplot as plt
import numpy as np




with np.load('../diff/fluka_H3_maps8-nm-fast.npz') as data:

    #H3_bottom    = data['H3_bottom1']
    H3_bottom_D_nom  = data['H3_bottom_D1']
    H3_bottom_Dd_nom = data['H3_bottom_Dd1']


with np.load('../diff/fluka_H3_maps8-kg3e7.npz') as data:

    H3_bottom_D_low  = data['H3_bottom_D1']
    H3_bottom_Dd_low = data['H3_bottom_Dd1']


with np.load('../diff/fluka_H3_maps8-kg6e6.npz') as data:

    H3_bottom_D_high  = data['H3_bottom_D1']
    H3_bottom_Dd_high = data['H3_bottom_Dd1']

nom  = H3_bottom_D_nom - H3_bottom_Dd_nom
low  = H3_bottom_D_low - H3_bottom_Dd_low
high = H3_bottom_D_high - H3_bottom_Dd_high
    
nom_avg = np.zeros((H3_bottom_D_nom.shape[0]))
low_avg = np.zeros((H3_bottom_D_nom.shape[0]))
high_avg = np.zeros((H3_bottom_D_nom.shape[0]))

dir_avg = np.zeros((H3_bottom_D_nom.shape[0]))
tot_avg = np.zeros((H3_bottom_D_nom.shape[0]))
    
ii = H3_bottom_D_nom.shape[0]
jj = H3_bottom_D_nom.shape[1]
kk = 17

#ii = 0
#jj = 0
#kk = 0


for i in range(ii):   #time

    sumN = 0
    sumL = 0
    sumH = 0
    sumD = 0
    n = 0
    
    for j in range(jj):

        for k in range(kk):

            sumN = sumN + nom[i,j,k]
            sumL = sumL + low[i,j,k]
            sumH = sumH + high[i,j,k]
            sumD = sumD + H3_bottom_Dd_nom[i,j,k]

            n = n + 1


    nom_avg[i] = sumN/n
    low_avg[i] = sumL/n
    high_avg[i] = sumH/n
    dir_avg[i] = sumD/n
            

tot_avg = dir_avg + nom_avg
    
max_hours = 30*365

print(max_hours)
    
hours_per_year = 365
    
x_values = np.zeros(max_hours)

            

for i in range(max_hours):


    x_values[i] = i/hours_per_year



max_id = np.argmax(nom_avg)

max_nom =nom_avg[max_id]
max_low =low_avg[max_id]
max_high =high_avg[max_id]

max_20 =nom_avg[20*365]
dir_20 = dir_avg[20*365]
tot_20 = tot_avg[20*365]


plus = (max_high - max_nom) / max_nom
minus = (max_low - max_nom) / max_nom

print(f"{plus:.3g}",f"{minus:.3g}")

print(f"{max_nom:.3g}",f"{max_20:.3g}")

ratio = tot_20/dir_20

print(ratio)




#plt.plot(x_values,nom_avg)
#plt.plot(x_values,low_avg)
#plt.plot(x_values,high_avg)

#plt.plot(x_values,(high_avg-nom_avg)/nom_avg)

plt.plot(x_values,tot_avg)
plt.plot(x_values,dir_avg)

#plt.title('Fractional difference in C for factor of 2 in D',fontsize=14)
#plt.ylabel('(C(2D) - C(D)) / C(D) ',fontsize=14)


plt.title('Tritium concentration in Dolomite diff + direct, no mixing',fontsize=14)
plt.ylabel('Concentration (pCi/cc) ',fontsize=14)

plt.xlabel('time (years)',fontsize=14)
plt.tick_params(labelsize=16)
plt.tight_layout()

#plt.xlim(20, 30)
#plt.ylim(0.03, 0.05)

plt.show()




