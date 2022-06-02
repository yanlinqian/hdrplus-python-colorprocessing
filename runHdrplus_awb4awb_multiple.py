"""Script to run the hdrplus implementation on a single burst.
Copyright (c) 2021 Antoine Monod

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License
as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.
If not, see <http://www.gnu.org/licenses/>.

This file implements an algorithm possibly linked to the patent US9077913B2.
This file is made available for the exclusive aim of serving as scientific tool
to verify the soundness and completeness of the algorithm description.
Compilation, execution and redistribution of this file may violate patents rights in certain countries.
The situation being different for every country and changing over time,
it is your responsibility to determine which patent rights restrictions apply to you
before you compile, use, modify, or redistribute this file.
A patent lawyer is qualified to make this determination.
If and only if they don't conflict with any patent terms,
you can benefit from the following license terms attached to this file.
"""

# imports
import os
import time
import glob
import argparse
from shutil import copyfile, rmtree
# custom package imports
from package.algorithm.hdrplus import hdrplusPipeline
from package.algorithm.genericUtils import getTime
from package.algorithm.params import getParams



options={
		#'outputFolder': './results_test1',
        'outputFolder': 'D:/DATASET/darkawb/iphone8_mergenew',
		#'inputFolder': './test_data/33TJ_20150606_224837_294',
        #'inputFolder': './test_data/DNG_GH5S',
        'inputFolder': 'E:/DARK_AWB/iphone8_c',
		'mode': 'full',
		'referenceIndex': 0,
		'temporalFactor': 75,
		'spatialFactor': 0.1,
 		'ltmGain': -1,
		'gtmContrast': 0.075,
        'awbstatmode': False,
		'verbose': 2,
		'downsize': 4
        }

if __name__ == "__main__":

	# Get the parameters that correspond to the selected mode
	params = getParams(options['mode'])

	# Create output folder if needed
	if not os.path.isdir(options['outputFolder']):
		os.makedirs(options['outputFolder'])

	# Get all dng files  
	rawPthList = glob.glob(os.path.join(options['inputFolder'], "*.dng"))
	rawPthList.sort()
	assert len(rawPthList)%5==0, "image number is not multiple of 5"
	nScene =int(len(rawPthList)/5)
	

	for idScene in range(nScene):
		# For convenience
		currentTime, verbose = time.time(), options['verbose'] > 0
		burstPath = options['inputFolder']
		
		#temporaily create a new folder, copy dng to this folder
		tempPath = os.path.join(options['outputFolder'],os.path.basename(rawPthList[idScene*5])).replace('.dng', '');
		if not os.path.isdir(tempPath):
			os.makedirs(tempPath)
			for i in range(5):
				srcPth=rawPthList[idScene*5+i]
				dstPth=os.path.join(tempPath, os.path.basename(srcPth))
				copyfile(srcPth, dstPth)
		burstPath=tempPath;
		
		# Process the burst
		if verbose:
			print("=" * (20 + len(burstPath)))
			print("Processing burst: {}".format(burstPath))
			print("=" * (20 + len(burstPath)))
			# Run the pipeline on the burst
		hdrplusPipeline(burstPath, params, options)
		
		#delete the temporaily created folder
		if os.path.isdir(tempPath):
			rmtree(tempPath)
		
		if verbose:
			currentTime = getTime(currentTime, ' - Burst processed')
