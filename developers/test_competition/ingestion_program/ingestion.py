print("I'm the LATEST Ingestion program!")

import os
import sys
import glob
import time

ingestion_program_directory = sys.argv[1]
input_directory = sys.argv[2]
output_directory = sys.argv[3]
hidden_directory = sys.argv[4]
shared_directory = sys.argv[5]
submission_program_directory = sys.argv[6]

print("Ingestion program directory:", ingestion_program_directory)
for thing in glob.glob(os.path.join(ingestion_program_directory, '*')):
	print("ingestion program:", thing)
	
print("Input directory (where the input data should be):", input_directory)
for thing in glob.glob(os.path.join(input_directory, '*')):
	print("input:", thing)
	
print("Hidden directory (where the reference data should be):", hidden_directory)
for thing in glob.glob(os.path.join(hidden_directory, '*')):
	print("hidden:", thing)
	
print("Submission program directory:", submission_program_directory)
for thing in glob.glob(os.path.join(submission_program_directory, '*')):
	print("submission program:", thing)
	
print("Read from shared directory (where the submission writes to):", shared_directory)
nothing = 1
for thing in glob.glob(os.path.join(shared_directory, '*')):
	nothing = 0
	print("shared before:", thing)
if nothing:
	print("shared before: nothing")

time.sleep(5)  # Wait 5 seconds for submission to do something in shared directory

for thing in glob.glob(os.path.join(shared_directory, '*')):
        print("shared later:", thing)
        
print("Write to output directory:", output_directory)
answer_path = os.path.join(output_directory, "answer_from_ingestion.txt")
open(answer_path, 'w+').write('Hello World!')
    
for thing in glob.glob(os.path.join(output_directory, '*')):
	print("output:", thing)
	
# General purpose functions
from os import path
from sys import argv
import data_io

# No machine learning, generates random results for test purposes
from numpy import random


if __name__=="__main__":
	print("****** The ingestion program generates the result  ******\n")
	datanames = data_io.inventory_data(input_directory)
	
	if len(datanames) == 0:
		print("****** No data found ******")

	# Loop over datasets
	for basename in datanames:
		print("****** Processing " + basename.capitalize() + " ******")
		# Here it should process the participant submission (but we don't bother)
                X = data_io.data(path.join(input_directory, basename, basename + '_valid.data'))
                Yvalid = random.rand(X.shape[0])
                X = data_io.data(path.join(input_directory, basename, basename + '_test.data'))
                # This should be where we call the participant submission and use his code:
                Ytest = random.rand(X.shape[0])
                # Write results to files
                data_io.write(path.join(output_directory, basename + '_valid.predict'), Yvalid)
                data_io.write(path.join(output_directory, basename + '_test.predict'), Ytest)
                
    # Lots of debug code...
	data_io.show_io(input_directory, output_directory)	
	data_io.show_version()
                        
	exit(0)
