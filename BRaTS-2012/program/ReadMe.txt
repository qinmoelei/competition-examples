Building an evaluation program that works with CodaLab

This example uses python.

BratsEvaluate.py - is an example that iterates through the files in input/ref and looks for a corresponding file in input/res. If it finds corresponding files it runs RegistrationMetrics.exe on the two files to compute metrics about their differences.
RegistrationMetrics.exe - a windows executable that will compare segmented images and provide metrics about the differences in the segmented images.
setup.py - this is a file that enables py2exe to build a windows executable of the evaluate.py script.
metadata - this is a file that lists the contents of the program.zip bundle for the CodaLab system.

Once these pieces are assembled they are packages as program.zip which CodaLab can then use to evaluate the submissions for a competition.