#!/usr/bin/env python

# Program substituting itself to the scoring program to test python configuration
# Isabelle Guyon, ChaLearn, September 2014

# ALL INFORMATION, SOFTWARE, DOCUMENTATION, AND DATA ARE PROVIDED "AS-IS". 
# ISABELLE GUYON, CHALEARN, AND/OR OTHER ORGANIZERS OR CODE AUTHORS DISCLAIM
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ANY PARTICULAR PURPOSE, AND THE
# WARRANTY OF NON-INFRINGEMENT OF ANY THIRD PARTY'S INTELLECTUAL PROPERTY RIGHTS. 
# IN NO EVENT SHALL ISABELLE GUYON AND/OR OTHER ORGANIZERS BE LIABLE FOR ANY SPECIAL, 
# INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF SOFTWARE, DOCUMENTS, MATERIALS, 
# PUBLICATIONS, OR INFORMATION MADE AVAILABLE FOR THE CHALLENGE. 

import os
from sys import argv
import data_io 
from glob import glob
from numpy import genfromtxt
import yaml

if (os.name == "nt"):
       filesep = '\\'
else:
       filesep = '/'

if __name__=="__main__":

	input_dir = argv[1]
	output_dir = argv[2]
	
	score_file = open(os.path.join(output_dir, 'scores.txt'), 'wb')
	
	try:
		# Compute "real scores"
		# Get all the solution files from the solution directory
		solution_names = glob(os.path.join(input_dir, 'ref', '*.solution'))

		# Loop over the files from the solution directory and search for predictions with extension .predict having the same basename
		set_num = 1
		for solution_file in solution_names:
			# Extract the dataset name from the file name
			basename = solution_file[-solution_file[::-1].index(filesep):-solution_file[::-1].index('.')-1]
                
			# Get the prediction from the res subdirectory (must end with '.predict')
			predict_file = os.path.join(input_dir, 'res', basename + '.predict')
			if not os.path.isfile(predict_file):
				print('No prediction file for ' + basename)
				score = float('NaN')
			else:
				# Read the solution and prediction values
				solution = genfromtxt(solution_file)
				prediction = genfromtxt(predict_file)
				# Compute score (simple mean square error)
				n=len(solution)
				score = sum([(solution[i]-prediction[i])**2 for i in range(n)])/n 
				print("Set %d" % set_num + " score (" + basename.capitalize() + "): %0.6f" % score)

			# Write scores to the output file
			score_file.write("set%d" % set_num + "_score: %0.6f\n" % score)
			set_num=set_num+1
	except:	
		# Write some arbitrary score to the leaderboard (this code computes NOTHING)	
		print('Something when wrong, perhaps a missing file...')
		print('Writing arbitraty scores for test purposes.')
		score = 3.1415
		score_file.write("set1_score: %0.6f\n" % score)
		score_file.write("set2_score: %0.6f\n" % -score)
		
	# Read the execution time and add it to the scores:
	try:
		metadata = yaml.load(open(os.path.join(input_dir, 'res', 'metadata'), 'r'))
		score_file.write("ExecutionTime: %0.6f\n" % metadata['elapsedTime'])
	except:
		score_file.write("ExecutionTime: 0\n")
		
	score_file.close()

	# Lots of debug stuff
	data_io.show_io(input_dir, output_dir)
	data_io.show_version()
	
	# Example html file
	with open(os.path.join(output_dir, 'scores.html'), 'wb') as html_file:
		html_file.write("<h1>Example HTML file</h1>\nThis shows that we can also have an html file to show extra data.")
		
	exit(0)




