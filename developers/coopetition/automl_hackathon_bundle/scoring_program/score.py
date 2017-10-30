#!/usr/bin/env python

# Scoring program for the AutoML challenge
# Isabelle Guyon and Arthur Pesah, ChaLearn, August-November 2014
# Lukasz Romaszko -- coopetitions June 2015

# ALL INFORMATION, SOFTWARE, DOCUMENTATION, AND DATA ARE PROVIDED "AS-IS". 
# ISABELLE GUYON, CHALEARN, AND/OR OTHER ORGANIZERS OR CODE AUTHORS DISCLAIM
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ANY PARTICULAR PURPOSE, AND THE
# WARRANTY OF NON-INFRINGEMENT OF ANY THIRD PARTY'S INTELLECTUAL PROPERTY RIGHTS. 
# IN NO EVENT SHALL ISABELLE GUYON AND/OR OTHER ORGANIZERS BE LIABLE FOR ANY SPECIAL, 
# INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF SOFTWARE, DOCUMENTS, MATERIALS, 
# PUBLICATIONS, OR INFORMATION MADE AVAILABLE FOR THE CHALLENGE. 

# Some libraries and options
import os
import pandas


from sys import argv
import yaml
import time
from libscores import * # Library of scores we implemented

# Default I/O directories:      
root_dir = "/Users/isabelleguyon/Documents/Projects/Codalab/AutoMLcompetition/StartingKit/"
default_input_dir = root_dir + "scoring_input0" 
default_output_dir = root_dir + "scoring_output0"  

# Debug flag 0: no debug, 1: show all scores, 2: also show version amd listing of dir
debug_mode = 1

# Constant used for a missing score
missing_score = -0.999999

# Version number
scoring_version = 0.8
    
    
def isEmpty(log_file): #is a log file empty?
    it = 0
    for line in open(log_file):
        it += 1
        if it == 2:
            if len(line.strip())==0:
                return True
            if line[0]=='N': #'N'o data
                return True
            else:
                return False
    return True
                
# =============================== MAIN ========================================
    
if __name__=="__main__":

    #### INPUT/OUTPUT: Get input and output directory names
    if len(argv)==1: # Use the default input and output directories if no arguments are provided
        input_dir = default_input_dir
        output_dir = default_output_dir
    else:
        input_dir = argv[1]
        output_dir = argv[2] 
    # Create the output directory, if it does not already exist and open output files  
    mkdir(output_dir) 
    score_file = open(os.path.join(output_dir, 'scores.txt'), 'wb')
    html_file = open(os.path.join(output_dir, 'scores.html'), 'wb')
    
    # Get all the solution files from the solution directory
    solution_names = sorted(ls(os.path.join(input_dir, 'ref', '*.solution')))
    scoreAVG = 0
    # Loop over files in solution directory and search for predictions with extension .predict having the same basename
    set_num = 1
    for solution_file in solution_names:
        # Extract the dataset name from the file name
        basename = solution_file[-solution_file[::-1].index(filesep):-solution_file[::-1].index('.')-1]
        # Load the info file and get the task and metric
        info_file = ls(os.path.join(input_dir, 'ref', basename[0:2] + '*_public.info'))[0]
        info = get_info (info_file)    
        score_name = info['task'][0:-15] + info['metric'][0:-7].upper() 
        try:
            # Get the last prediction from the res subdirectory (must end with '.predict')
            predict_file = ls(os.path.join(input_dir, 'res', basename + '*.predict'))[-1]
            if (predict_file == []): raise IOError('Missing prediction file {}'.format(basename))
            predict_name = predict_file[-predict_file[::-1].index(filesep):-predict_file[::-1].index('.')-1]
            # Read the solution and prediction values into numpy arrays
            solution = read_array(solution_file)
            prediction = read_array(predict_file)
            if(solution.shape!=prediction.shape): raise ValueError("Bad prediction shape {}".format(prediction.shape))

            try:
                # Compute the score prescribed by the info file (for regression scores, no normalization)            
                if info['metric']=='r2_metric' or info['metric']=='a_metric': 
                    # Remove NaN and Inf for regression
                    solution = sanitize_array (solution); prediction = sanitize_array (prediction)  
                    score = eval(info['metric'] + '(solution, prediction, "' + info['task'] + '")')
                else:
                    # Compute version that is normalized (for classification scores). This does nothing if all values are already in [0, 1]
                    [csolution, cprediction] = normalize_array (solution, prediction)
                    score = eval(info['metric'] + '(csolution, cprediction, "' + info['task'] + '")')
                print("======= Set %d" % set_num + " (" + predict_name.capitalize() + "): score(" + score_name + ")=%0.12f =======" % score)                
                html_file.write("======= Set %d" % set_num + " (" + predict_name.capitalize() + "): score(" + score_name + ")=%0.12f =======\n" % score)
            except:
                raise Exception('Error in calculation of the specific score of the task')
                
            if debug_mode>0: 
                scores = compute_all_scores(solution, prediction)
                write_scores(html_file, scores)
                    
        except Exception as inst:
            score = missing_score
            
            print("======= Set %d" % set_num + " (" + basename.capitalize() + "): score(" + score_name + ")=ERROR =======")
            html_file.write("======= Set %d" % set_num + " (" + basename.capitalize() + "): score(" + score_name + ")=ERROR =======\n")            
            print inst
            
        # Write score corresponding to selected task and metric to the output file
        score_file.write("set%d" % set_num + "_score: %0.12f\n" % score)
        scoreAVG += score
        
        set_num=set_num+1            
    # End loop for solution_file in solution_names

    # Read the execution time and add it to the scores:
    try:
        metadata = yaml.load(open(os.path.join(input_dir, 'res', 'metadata'), 'r'))
        score_file.write("Duration: %0.6f\n" % metadata['elapsedTime'])
    except:
        score_file.write("Duration: 0\n")
    scoreAVG /= 5.0
    score_file.write("avg_score: %0.12f\n" % scoreAVG )
        
        
        
        
        
        
    ############ COOPETITION START
    diff = 0
    try:
        user = os.path.join(input_dir, 'coopetition', 'current_user.txt')
        for line in open(user):
            __ME = line.strip()
            assert len(__ME)>0
            break
        
        scores_file = os.path.join(input_dir, 'scores', 'metadata')
        if os.path.isfile(scores_file):
            for line in open(scores_file):
                print(line)
        else:
            print("-------- No scores metadata")
            
        log_file = os.path.join(input_dir, 'coopetition', 'coopetition_phase_1.txt')
        if os.path.isfile(log_file):
            for line in open(log_file):
                print(line)
        else:
            print("-------- No log file")    
            
        log_file = os.path.join(input_dir, 'coopetition', 'coopetition_downloads.txt')
        Ndown = 0  
        if os.path.isfile(log_file):
            if not isEmpty(log_file):
                log_file = os.path.join(input_dir, 'coopetition', 'coopetition_downloads.txt')
                downs_all = pandas.read_csv(log_file, index_col=False)        
                downs_my = downs_all[downs_all['submission_owner'] == __ME]
                downs_my = downs_my[downs_my['downloaded_by'] != __ME]
                downs_my = downs_my.drop_duplicates(['submission_owner','downloaded_by'])
                print downs_my
                Ndown = len(downs_my) 
        else:
            print("-------- No downloads file")   
            
        log_file = os.path.join(input_dir, 'coopetition', 'coopetition_scores_phase_1.txt')
        Nsub = -1
        if os.path.isfile(log_file):    
            if not isEmpty(log_file): # there is some data
                scores_all = pandas.read_csv(log_file, index_col=False)        
                print scores_all
                Nsub = len(scores_all[scores_all['User'] == __ME]) + 1
                if Nsub > 1: # had any entry earlier (apart from the current one)
                    VAL = scores_all[scores_all['User'] == __ME]["AVG"].values
                    print VAL
                    maxi = -5
                    for v in VAL:
                        f = float(v.split()[0])
                        if f > maxi:
                            maxi = f
                    print "maxi", maxi
                    diff = scoreAVG - maxi
                
                print "Nsub", Nsub   
            else:
                Nsub = 1  
        else:
            print("-------- No scores file")      
        
       
        score_file.write("Nsub: %d\n" % Nsub)    
        score_file.write("Diff: %0.6f\n" % diff)  
        score_file.write("Ndown: %d\n" % Ndown)      
    except:    
        print "ERROR in COOPETITION!"
        ############ COOPETITION END   
        
        
        
        
        
    html_file.close()
    score_file.close()

    # Lots of debug stuff
    if debug_mode>1:
        swrite('\n*** SCORING PROGRAM: PLATFORM SPECIFICATIONS ***\n\n')
        show_platform()
        show_io(input_dir, output_dir)
        show_version(scoring_version)
        
    time.sleep(3)    
    time.sleep(3)    	
    #exit(0)



