print("I'm a NEW submission!")

import os
import sys
import glob
from distutils.dir_util import copy_tree

program_directory = sys.argv[1]
input_directory = sys.argv[2]
output_directory = sys.argv[3]
hidden_directory = sys.argv[4]
shared_directory = sys.argv[5]
submission_directory = sys.argv[6]
ingestion_directory = sys.argv[7]


print("Sharing the code submitted...")  
copy_tree (program_directory, shared_directory)

print("Write some stuff to shared file...") 
for i in range(10):
    name = "{}_{}".format("newfile", i)
    open(os.path.join(shared_directory, name), 'w+').write('test!')
    
print("Writing answer to...", output_directory)

answer_path = os.path.join(output_directory, "answer.txt")
open(answer_path, 'w+').write('Hello World!')
    
print("Program directory:", program_directory)
for thing in glob.glob(os.path.join(program_directory, '*')):
	print("program:", thing)
	
print("Input directory:", input_directory)
for thing in glob.glob(os.path.join(input_directory, '*')):
	print("input:", thing)
	
print("Output directory:", output_directory)
for thing in glob.glob(os.path.join(output_directory, '*')):
	print("output:", thing)
	
print("Hidden directory:", hidden_directory)
for thing in glob.glob(os.path.join(hidden_directory, '*')):
	print("hidden:", thing)
	
print("Shared directory:", shared_directory)
for thing in glob.glob(os.path.join(shared_directory, '*')):
	print("shared:", thing)
	
print("Submission directory:", submission_directory)
for thing in glob.glob(os.path.join(submission_directory, '*')):
	print("submission:", thing)
	
print("Ingestion directory:", ingestion_directory)
for thing in glob.glob(os.path.join(ingestion_directory, '*')):
	print("ingestion:", thing)
    
