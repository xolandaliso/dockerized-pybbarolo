import os, sys
import shutil
import numpy as np
import pylab as pl
from astropy.io import fits
from pyBBarolo.wrapper import FitMod3D



def process_data(input_folder, output_folder):

    # check for input folder 

    if not os.path.exists(input_folder):
        print('data dir not found, exiting')
        sys.exit(1)

    # ensure output folder exists, create one incase it does not

    if not os.path.exists(output_folder):
        print(f'output folder not passed, creating one called : {output_folder}')
        os.makedirs(output_folder)


    # list files in the input folder

    files = [ x for x 
                in os.listdir(input_folder) if '.fits' or '.FITS' in x ]

    if len(files) == 0:
        print('no data cubes found in the input dir, exit')
        sys.exit(1)
    
    # model each data 

    for i, g in enumerate(files):

        cube = fits.open(f'{input_folder}/{g}')    #opening the cube via astropy

        if 'BMAJ' in cube[0].header:

            bmaj = cube[0].header['bmaj']*3600   #getting beam major axis for the rings

            print('{0} = {1}'.format('BMAJ', bmaj))

        rms = np.std(cube[0].data[0, :, :])

        #cut arguments, mostly for robust statistics

        snrcut = np.arange( 
                            4, 2.5, -.5 )         #4, 3.5, 3
        growthcut = np.arange(
                            3, 1.5, -.5 )      #3, 2.5, 2

        #threshold args

        grwth_threshold = np.arange(
                                    1, 2.5, .5 ) * rms

        for k in range( len(growthcut) ):

            f3d = FitMod3D( 
                            f'{input_folder}/{g}' )
            
            f3d.add_options(
                            free = 'vrot vdisp', \
                            outfolder = f"{outdir}/{g[:-5]}/{k}", \
                            mask = "SEARCH", snrcut = snrcut[k], \
                            growthcut = growthcut[k], ftype = 2,\
                            wfunc = 1, globalProfile=True, \
                            flagerrors = True, norm = 'LOCAL',\
                            redshift = 0.0, restfreq = 1.42040575E9 )

            f3d.run()


if __name__ == "__main__":

    # check if the number of arguments is correct

    if len(sys.argv) < 2:
        print("Usage: python pybbarolo.py <input_folder> [<output_folder>]")
        sys.exit(1)

    # extract input folder path from command-line arguments

    input_folder = sys.argv[1]

    # use the second argument as output folder if provided, else set a default

    output_folder = sys.argv[2] if len(sys.argv) >= 3 else "output_data"

    # call the processing function with the provided arguments

    process_data(input_folder, output_folder)