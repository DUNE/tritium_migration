import matplotlib.pyplot as plt
import ROOT
import math
import numpy as np
from scipy.ndimage import gaussian_filter


c1 = ROOT.TCanvas()

# 1. Open the file in read mode
fluka_file = ROOT.TFile.Open("../dpipe_4mAu26_histos/dpipe_4mAu26_clay_2026_hs8.root", "READ")

fstars = fluka_file.Get("usrbin")

# test histograms

hb = ROOT.TH2F("hb","bottom",1000,0,1000,2000,-1000,1000)



### geometry  for section 8

## concrete

bottom_x_min = 0.0    
bottom_x_max = 1006
bottom_y_min = -802.3
bottom_y_max = -650

nbcx = int((bottom_x_max - bottom_x_min)/10) + 1
nbcy = int((bottom_y_max - bottom_y_min)/10) 

side_x_min = 752.0
side_x_max = 1006.0
side_y_min = -802.3
side_y_max = 375.0

nscx = int((side_x_max - side_x_min)/10)
nscy = int((side_y_max - side_y_min)/10)

slant_xp_min = 758.0
slant_xp_max = 976.0
slant_yp_min = -305.0
slant_yp_max = 298.0

nslcxp = int((slant_xp_max - slant_xp_min)/10) + 1
nslcyp = int((slant_yp_max - slant_yp_min)/10) + 1

top_x_min = 0.0
top_x_max = 492.0
top_y_min = 747.0
top_y_max = 889.0

ntcx = int((top_x_max - top_x_min)/10)
ntcy = int((top_y_max - top_y_min)/10)

## dirt

bottom_d_x_min = 0.0
bottom_d_x_max = 1006.0
bottom_d_y_min = -802.3 - 500.0
bottom_d_y_max = -802.3

nbdx = int((bottom_d_x_max - bottom_d_x_min)/10) + 1
nbdy = int((bottom_d_y_max - bottom_d_y_min)/10)

side_d_x_min = 1006.0
side_d_x_max = 1006.0 + 500.0
side_d_y_min = -802.3
side_d_y_max = 375.0

nsdx = int((side_d_x_max - side_d_x_min)/10)
nsdy = int((side_d_y_max - side_d_y_min)/10)

slant_d_xp_min = 976.0
slant_d_xp_max = 976.0 + 500.0
slant_d_yp_min = -305.0
slant_d_yp_max = 298.0

nsldxp = int((slant_d_xp_max - slant_d_xp_min)/10) + 1
nsldyp = int((slant_d_yp_max - slant_d_yp_min)/10) + 1 

top_d_x_min = 0.0
top_d_x_max = 492.0
top_d_y_min = 889.0
top_d_y_max = 889.0 + 500.0

ntdx = int((top_d_x_max - top_d_x_min)/10)
ntdy = int((top_d_y_max - top_d_y_min)/10)


### star maps

bottom_map = np.zeros((nbcx, nbcy))
side_map = np.zeros((nscy, nscx))
slant_map = np.zeros((nslcyp, nslcxp))
top_map = np.zeros((ntcx, ntcy))

bottom_d_map = np.zeros((nbdx, nbdy))
side_d_map = np.zeros((nsdy, nsdx))
slant_d_map = np.zeros((nsldyp, nsldxp))
top_d_map = np.zeros((ntdx, ntdy))

star_min = 1e-30

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

                    if stars == 0:
                        stars = star_min
                    
                    map[x_bin,  mapy - 1 - y_bin] = stars

                            #hb.Fill(x_bin+x_min,y_bin+y_min,fstars.GetBinContent(i,j))
            
    return map            

def fill_top_map(x_min, x_max, y_min, y_max, map):

    mapx = map.shape[0]
    mapy = map.shape[1]

    print(mapx, mapy)
    
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

                    if stars == 0:
                        stars = star_min

                    
                    map[x_bin,  y_bin] = stars
                    
                    #print(x , y, x_bin, y_bin, stars)
                    
                            #hb.Fill(x_bin+x_min,y_bin+y_min,fstars.GetBinContent(i,j))
            
    return map            


def fill_side_map(x_min, x_max, y_min, y_max, map):

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

                    if stars == 0:
                        stars = star_min

                    map[y_bin,  x_bin] = stars
                    
                    #print(x , y, y_bin, x_bin)
                    
                            #hb.Fill(x_bin+x_min,y_bin+y_min,fstars.GetBinContent(i,j))
            
    return map            





def fill_map_prime(xp_min, xp_max, yp_min, yp_max, map):

    for i in range(1,fstars.GetNbinsX() + 1):

        x = fstars.GetXaxis().GetBinCenter(i)

        x = x - 5  ## bin wall
        
        for j in range(1,fstars.GetNbinsY() + 1):

            y = fstars.GetYaxis().GetBinCenter(j)

            y = y - 5   ## bin wall
            
            xp = 0.707*x+0.707*y

            yp = -0.707*x + 0.707*y
        
            if ( xp >= xp_min and
                 xp <  xp_max and
                 yp >= yp_min and
                 yp <  yp_max ) :


                #print(x , y, xp, yp)

                x_zero = xp - xp_min
                y_zero = yp - yp_min

                x_bin = int(x_zero/10)
                y_bin = int(y_zero/10)

                stars = fstars.GetBinContent(i,j)

                if stars == 0:
                    stars = star_min

                                            
                map[y_bin, x_bin] = stars

                #print(x , y, y_bin, x_bin)
                
                        #hb.Fill(x,y,fstars.GetBinContent(i,j))
    return map            





bottom_map = fill_bottom_map(bottom_x_min, bottom_x_max, bottom_y_min, bottom_y_max, bottom_map)

bottom_d_map = fill_bottom_map(bottom_d_x_min, bottom_d_x_max, bottom_d_y_min, bottom_d_y_max, bottom_d_map)

side_map = fill_side_map(side_x_min, side_x_max, side_y_min, side_y_max, side_map)
side_d_map = fill_side_map(side_d_x_min, side_d_x_max, side_d_y_min, side_d_y_max, side_d_map)

top_map = fill_top_map(top_x_min, top_x_max, top_y_min, top_y_max, top_map)
top_d_map = fill_top_map(top_d_x_min, top_d_x_max, top_d_y_min, top_d_y_max, top_d_map)

slant_map = fill_map_prime(slant_xp_min, slant_xp_max, slant_yp_min, slant_yp_max, slant_map)
slant_d_map = fill_map_prime(slant_d_xp_min, slant_d_xp_max, slant_d_yp_min, slant_d_yp_max, slant_d_map)



tms = gaussian_filter(top_map,sigma=1.0)
slms = gaussian_filter(slant_map,sigma=2.5)
sms = gaussian_filter(side_map,sigma=2.0)
bms = gaussian_filter(bottom_map,sigma=2.0)


tmds = gaussian_filter(top_d_map,sigma=1.0)
slmds = gaussian_filter(slant_d_map,sigma=2.5)
smds = gaussian_filter(side_d_map,sigma=2.0)
bmds = gaussian_filter(bottom_d_map,sigma=2.0)


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
side_map2 = np.zeros((nscy+2, nscx+1))
slant_map2 = np.zeros((nslcyp+2, nslcxp+1))
top_map2 = np.zeros((ntcx+2, ntcy+1))

bottom_d_map2 = np.zeros((nbdx+2, nbdy+1))
side_d_map2 = np.zeros((nsdy+2, nsdx+1))
slant_d_map2 = np.zeros((slant_d_map.shape[0]+2, slant_d_map.shape[1]+1))
top_d_map2 = np.zeros((ntdx+2, ntdy+1))

bottom_map2 = shift(bottom_map2, bms)
side_map2 = shift(side_map2, sms)
slant_map2 = shift(slant_map2, slms)
top_map2 = shift(top_map2, tms)


bottom_d_map2 = shift_dirt(bottom_d_map2, bmds)
side_d_map2 = shift_dirt(side_d_map2, smds)
slant_d_map2 = shift_dirt(slant_d_map2, slmds)
top_d_map2 = shift_dirt(top_d_map2, tmds)




#hb.Draw()

np.savez('2Dwalls8.npz',
         bottom_map1   = bottom_map2,
         side_map1     = side_map2,
         slant_map1    = slant_map2,
         top_map1      = top_map2,
         bottom_d_map1 = bottom_d_map2,
         side_d_map1   = side_d_map2,
         slant_d_map1  = slant_d_map2,
         top_d_map1    = top_d_map2)
 











