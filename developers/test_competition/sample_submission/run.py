#!/usr/bin/env python

# Create a random submission
# Isabelle Guyon, ChaLearn, July 2014

# ALL INFORMATION, SOFTWARE, DOCUMENTATION, AND DATA ARE PROVIDED "AS-IS". 
# ISABELLE GUYON, CHALEARN, AND/OR OTHER ORGANIZERS OR CODE AUTHORS DISCLAIM
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ANY PARTICULAR PURPOSE, AND THE
# WARRANTY OF NON-INFRINGEMENT OF ANY THIRD PARTY'S INTELLECTUAL PROPERTY RIGHTS. 
# IN NO EVENT SHALL ISABELLE GUYON AND/OR OTHER ORGANIZERS BE LIABLE FOR ANY SPECIAL, 
# INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF SOFTWARE, DOCUMENTS, MATERIALS, 
# PUBLICATIONS, OR INFORMATION MADE AVAILABLE FOR THE CHALLENGE. 

# General purpose functions
from os import path
from sys import argv
import data_io

# No machine learning, generates random results for test purposes
from numpy import random


if __name__=="__main__":
	print("****** Sample submitted code ******\n")
	# Inventory the datasets (new style, datasets in subdirectories)
	input_dir = argv[1]
	datanames = data_io.inventory_data(input_dir)
	
	# The output directory will contain the scores, create it if it does not exist
	output_dir = argv[2]
	data_io.mkdir(output_dir)
	
	if len(datanames) == 0:
		print("****** No data found ******")

	# Loop over datasets
	for basename in datanames:
		print("****** Processing " + basename.capitalize() + " ******")
		# Fake predictions on validation and test data
                X = data_io.data(path.join(input_dir, basename, basename + '_valid.data'))
                Yvalid = random.rand(X.shape[0])
                X = data_io.data(path.join(input_dir, basename, basename + '_test.data'))
                Ytest = random.rand(X.shape[0])
                # Write results to files
                data_io.write(path.join(output_dir, basename + '_valid.predict'), Yvalid)
                data_io.write(path.join(output_dir, basename + '_test.predict'), Ytest)
                
    # Lots of debug code...
	data_io.show_io(input_dir, output_dir)	
	data_io.show_version()
                        
	exit(0)




