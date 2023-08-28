from pyBBarolo.wrapper import FitMod3D
from pyBBarolo import Ellprof
import numpy as np
import pylab as pl
import os
from astropy.io import fits

inpdir = 'cluster_dilated_cubelets/'
outdir = 'cluster_dilated_output_free_vdisp/'

#x0, y0, inc, phi = np.loadtxt('ring_parameters.txt', skiprows = 1, unpack = True) 

galaxies = [f for f in sorted(os.listdir(inpdir)) if f[:-5] in os.listdir(outdir)] 

print(galaxies)

for i, g in enumerate(galaxies):

    cube = fits.open(f'{inpdir}/{g}')    #opening the cube via astropy

    if 'BMAJ' in cube[0].header:

        bmaj = cube[0].header['bmaj']*3600   #getting beam major axis for the rings

        print('{0} = {1}'.format('BMAJ', bmaj))

    rms = np.std(cube[0].data[0, :, :])

    #print('RMS = %.7f' %rms)

    #cut arguments, mostly for robust statistics

    snrcut = np.arange(4, 2.5, -.5)         #4, 3.5, 3
    growthcut = np.arange(3, 1.5, -.5)      #3, 2.5, 2

    #threshold args

    grwth_threshold = np.arange(1, 2.5, .5)*rms

    for k in range(len(growthcut)):

        f3d = FitMod3D(f'{inpdir}/{g}')#, nradii = 5, radsep = bmaj/2)# vrot = (10, 250, 500))#  x0 = x0[i], y0 = y0[i], inc = inc[i], pa = phi[0]) #automatically

        #--you removed two arguments, snrcut and growthcut--#
        #--fix pa, inc and vsys ---> {done! results not so much different ;)}
        #--check the chi-square to quantify ----> {we can actually compare the radial surface brightness profiles for the cube and model}
        #--find a way to fit different number of radii for each galaxy ---> {let the model work it out!!}

        f3d.add_options(free = 'vrot vdisp', outfolder = f"{outdir}/{g[:-5]}/{k}",
                    mask = "SEARCH", snrcut = snrcut[k], growthcut = growthcut[k], ftype = 2, wfunc = 1, globalProfile=True,
                    flagerrors = True, norm = 'LOCAL', redshift = 0.042, restfreq = 1.42040575E9)

        f3d.run()

        print('\n___________dynamical modelling done______________\n')

        
        '''
        el = Ellprof(f'{inpdir}/{g}')

        el.init(radii = np.loadtxt(f'{outdir}/{g[:-5]}/{k}/rings_final1.txt')[:, 1], xpos = np.loadtxt(f'{outdir}/{g[:-5]}/{k}/rings_final1.txt')[:, 9], 
        ypos = np.loadtxt(f'{outdir}/{g[:-5]}/{k}/rings_final1.txt')[:, 10],
        inc = np.loadtxt(f'{outdir}//{g[:-5]}/{k}/rings_final1.txt')[:, 4], phi = np.loadtxt(f'{outdir}/{g[:-5]}/{k}/rings_final1.txt')[:, 5])

        el.set_options(mask = 'SEARCH')

        rings = el.compute()

        os.mkdir(f"{outdir}/{g[:-5]}/{k}/ellprof")

        el.writeto(f"{outdir}/{g[:-5]}/{k}/ellprof/ellprof_cube.txt")

        print('\n_________surface profile created____________\n')

        cube_ellprof = np.loadtxt(f"{outdir}/{g[:-5]}/{k}/ellprof/ellprof_cube.txt")

        r, surf_dens = cube_ellprof[:, 0], cube_ellprof[:, -1]

        model_ellprof = np.loadtxt(f"{outdir}/{g[:-5]}/{k}/densprof.txt")[:, -1]

        fig1 = pl.figure(1)

        fr1 = fig1.add_axes((.1, .3, .8, .6))
        pl.plot(r, surf_dens, 'r.')
        pl.plot(r, model_ellprof, color = 'grey', ls = '', marker = '.')
        pl.ylabel(r'$\Sigma_{\rm HI}$ (M$_{\odot}$ pc$^{-2})$')
        fr1.set_xticklabels([])


        fr2 = fig1.add_axes((.1, .1, .8, .2))        
        pl.plot(r, surf_dens - model_ellprof, 'k.')
        pl.axhline(0, r[0], r[-1], color = 'r')
        pl.xlabel('radius (arcsec)')
        pl.ylabel(r'$\Sigma_{\rm res}$')
        pl.savefig(f"{outdir}/{g[:-5]}/{k}/ellprof/comp.pdf", format = 'pdf')
        pl.close()

        '''

