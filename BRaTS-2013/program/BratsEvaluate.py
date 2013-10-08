#!/usr/bin/env python2.7
"""
    get a pair of files from the res and ref directories
    and pass them to Regristration metrics. write result to the out directory
"""
import os, sys, optparse, re
import subprocess
import inspect


def findTruth(submitted_file, truth_dir):
    ''' given a submitted file find the corresponding truth file'''
    m = re.search(r"(\d+)\.mha$", submitted_file)
    if m is not None:
        number_string = m.groups(0)[0]
        dirList=os.listdir(truth_dir)
        for truth_file in dirList:
            if truth_file.rfind(number_string+'.mha') < 0:
                continue
            else:
                return truth_file
    return None
            

#only needed to append the label to the file name
def compressedLabel(labels):
    '''remove white space from label string'''
    label_list = labels.split()
    return ''.join(label_list)   

      
def main():
    ''' inputs are ;
       an input directory containing a ref and res subfolders
       an output directory
    '''
    parser = optparse.OptionParser()
    
    options, args = parser.parse_args()
    if len(args) != 2:
        parser.error("incorrect number of arguments")

    submit_dir = os.path.join(args[0], 'res') 
    truth_dir = os.path.join(args[0], 'ref')
    out_dir = args[1]
    
    #Region 1 in VS is the complete tumor (labels 1+2+3+4)
    #Region 2 is the core tumor (labels 3+4)
    #Region 3 is the enhancing tumor (label 4)

    labels = ['1 2 3 4', '3 4', '4']

    if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        output_file_name = os.path.join(out_dir, 'scores.txt')              
        out_handle = open(output_file_name, 'a')

        submit_list=os.listdir(submit_dir)
        for submitted_file in submit_list:
            truth = findTruth(submitted_file, truth_dir)
            if truth is None:
                print 'no truth file found for' + submitted_file
            else:
                submit_file = os.path.join(submit_dir, submitted_file)
                truth_file = os.path.join(truth_dir, truth)
                exe_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
                exe_file = os.path.join(exe_path,'RegistrationMetrics.exe')
                for label in labels:
                    subprocess.call(['RegistrationMetrics.exe', submit_file, truth_file, label], stdout=out_handle)

        out_handle.close()
                
main()
