
import os, sys
import numpy as np
import pylab as pl
from astropy.io import fits
from pyBBarolo import Ellprof
from pyBBarolo.wrapper import FitMod3D


inpdir = 'data/'
outdir = 'output/'

galaxies = [ 
                f for f in sorted(os.listdir(inpdir)) 
                           if f[:-5] in os.listdir(outdir) ] 

for i, g in enumerate(galaxies):

    cube = fits.open(f'{inpdir}/{g}')    #opening the cube via astropy

    if 'BMAJ' in cube[0].header:

        bmaj = cube[0].header['bmaj']*3600   #getting beam major axis for the rings

        print('{0} = {1}'.format('BMAJ', bmaj))

    rms = np.std(
                cube[0].data[0, :, :] )

    #cut arguments, mostly for robust statistics

    snrcut = np.arange( 
                        4, 2.5, -.5 )         #4, 3.5, 3
    growthcut = np.arange(
                           3, 1.5, -.5 )      #3, 2.5, 2

    #threshold args

    grwth_threshold = np.arange(
                                1, 2.5, .5 ) * rms

    for k in range(len(growthcut)):

        f3d = FitMod3D( 
                        f'{inpdir}/{g}' )
        
        f3d.add_options( 
                free = 'vrot vdisp', outfolder = f"{outdir}/{g[:-5]}/{k}",
                mask = "SEARCH", snrcut = snrcut[k], 
                growthcut = growthcut[k],ftype = 2, 
                wfunc = 1, globalProfile=True,
                flagerrors = True, norm = 'LOCAL',
                redshift = 0.042, restfreq = 1.42040575E9 )

        f3d.run()