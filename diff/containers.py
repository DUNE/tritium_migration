
import numpy as np
import math



################################
###### Containers / Histograms
################################



#### Bins

def make_maps():

    top_DP_map = np.array([])
    
def make_bins():

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

def make_containers():


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

    H3_top_Dd = np.zeros((max_days, n_topdx, n_topdy))
    H3_slant_Dd = np.zeros((max_days, n_slantdx, n_slantdy))
    H3_side_Dd = np.zeros((max_days, n_sidedx, n_sidedy))
    H3_bottom_Dd = np.zeros((max_days, n_bottomdx, n_bottomdy))

    H3_bottom_Dd_mix = np.zeros((max_days, n_bottomdx, n_bottomdy))

    H3_bottom_D_removed = np.zeros((max_days, n_bottomdx, n_bottomdy))
    H3_bottom_Dd_removed = np.zeros((max_days, n_bottomdx, n_bottomdy))


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

    iH3_top_Dd = np.zeros((n_topdx, n_topdy))
    iH3_slant_Dd = np.zeros((n_slantdx, n_slantdy))
    iH3_side_Dd = np.zeros((n_sidedx, n_sidedy))
    iH3_bottom_Dd = np.zeros((n_bottomdx, n_bottomdy))
    iH3_bottom_Dd_mix = np.zeros((n_bottomdx, n_bottomdy))



