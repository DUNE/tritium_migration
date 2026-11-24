import matplotlib.pyplot as plt
import ROOT
import math
import numpy as np
from scipy.ndimage import gaussian_filter


c1 = ROOT.TCanvas()

# 1. Open the file in read mode


fluka_file = ROOT.TFile.Open("../dpipe_4mAu26_histos/dpipe_4mAu26_clay_2026_hs8.root", "READ")

fstars = fluka_file.Get("usrbin")


### geometry

## concrete

bottom_x_min = 0.0
bottom_x_max = 1006.0
bottom_y_min = -802.3
bottom_y_max = -650.0

nbcx = int((bottom_x_max - bottom_x_min)/10)
nbcy = int((bottom_y_max - bottom_y_min)/10)

#print(nbcx, nbcy)

nbcx = nbcx + 1

## dirt

bottom_d_x_min = 0.0
bottom_d_x_max = 1006.0
bottom_d_y_min = -1302.0
bottom_d_y_max = -802.3

nbdx = int((bottom_d_x_max - bottom_d_x_min)/10)
nbdy = int((bottom_d_y_max - bottom_d_y_min)/10)

nbdx = nbdx + 1


### star maps

bottom_map = np.zeros((nbcx, nbcy))

bottom_d_map = np.zeros((nbdx, nbdy))




def fill_bottom_map(x_min, x_max, y_min, y_max, map):

    mapx = map.shape[0]
    mapy = map.shape[1]

    for i in range(1,fstars.GetNbinsX() + 1):

        x = fstars.GetXaxis().GetBinCenter(i)

        if x>= x_min and x < x_max :

            for j in range(1,fstars.GetNbinsY() + 1):

                y = fstars.GetYaxis().GetBinCenter(j)

                if y >= y_min and y < y_max :

                    #print(x , y)
                    
                    x_zero = x - 5 - x_min
                    y_zero = y - 5 - y_min

                    x_bin = int(x_zero/10)
                    y_bin = int(y_zero/10)
                    
                    stars = fstars.GetBinContent(i,j)

                    #print(x_bin, y_bin, stars)
                    
                    if stars == 0:
                        stars = 1e-29
                    
                    map[x_bin,  mapy - 1 - y_bin] = stars

                            #hb.Fill(x_bin+x_min,y_bin+y_min,fstars.GetBinContent(i,j))
            
    return map            





bottom_map = fill_bottom_map(bottom_x_min, bottom_x_max, bottom_y_min, bottom_y_max, bottom_map)

bottom_d_map = fill_bottom_map(bottom_d_x_min, bottom_d_x_max, bottom_d_y_min, bottom_d_y_max, bottom_d_map)

for i in range(nbdx):
    bottom_d_map[i,nbdy-1] = 1e-29

 

bms = gaussian_filter(bottom_map,sigma=1.0)

bmds = gaussian_filter(bottom_d_map,sigma=1.0)


def shift(new, old):

    nx = old.shape[0]
    ny = old.shape[1]

    for i in range(nx):
        for j in range(ny):

            new[i+1,j+1] = old[i,j]

    return new


def shift_dirt(new, old):

    nx = old.shape[0]
    ny = old.shape[1]

    #print(ny, new.shape[1])
    
    for i in range(nx):
        for j in range(ny):

            new[i+1,j] = old[i,j]

    return new

            
bottom_map2 = np.zeros((nbcx+2, nbcy+1))

bottom_d_map2 = np.zeros((nbdx+2, nbdy+1))

bottom_avg_map2 = np.zeros((nbcy+1))

bottom_d_avg_map2 = np.zeros((nbdy+1))



bottom_map2 = shift(bottom_map2, bms)

bottom_d_map2 = shift_dirt(bottom_d_map2, bmds)


### average over x



for i in range(nbcy+1):

    sum = 0

    for j in range(1,nbcx+1):
    
        sum = sum + bottom_map2[j,i]

    bottom_avg_map2[i] = sum/nbcx


for i in range(nbdy):

    sum = 0

    for j in range(1,nbdx+1):
    
        sum = sum + bottom_d_map2[j,i]

    bottom_d_avg_map2[i] = sum/nbdx



    
np.savez('2D_bottom8.npz',
         bottom_map1   = bottom_map2,
         bottom_d_map1 = bottom_d_map2,
         bottom_avg_map1   = bottom_avg_map2,
         bottom_d_avg_map1 = bottom_d_avg_map2)

 











