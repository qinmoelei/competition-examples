#!/usr/bin/env python

# Scoring program for the AutoML challenge
# Isabelle Guyon and Arthur Pesah, ChaLearn, August-November 2014
# Isabelle Guyon: new version June 2016 for AutoSKlearn vs. world
# This fuses the sample code and the scoring program because we need to run both in one.

# ALL INFORMATION, SOFTWARE, DOCUMENTATION, AND DATA ARE PROVIDED "AS-IS". 
# ISABELLE GUYON, CHALEARN, AND/OR OTHER ORGANIZERS OR CODE AUTHORS DISCLAIM
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ANY PARTICULAR PURPOSE, AND THE
# WARRANTY OF NON-INFRINGEMENT OF ANY THIRD PARTY'S INTELLECTUAL PROPERTY RIGHTS. 
# IN NO EVENT SHALL ISABELLE GUYON AND/OR OTHER ORGANIZERS BE LIABLE FOR ANY SPECIAL, 
# INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF SOFTWARE, DOCUMENTS, MATERIALS, 
# PUBLICATIONS, OR INFORMATION MADE AVAILABLE FOR THE CHALLENGE. 

#############################
# ChaLearn AutoML challenge #
#############################

# Usage: python run.py input_dir output_dir

# This sample code can be used either 
# - to submit RESULTS depostited in the res/ subdirectory or 
# - as a template for CODE submission.
#
# The input directory input_dir contains 5 subdirectories named by dataset,
# including:
# 	dataname/dataname_feat.type          -- the feature type "Numerical", "Binary", or "Categorical" (Note: if this file is abscent, get the feature type from the dataname.info file)
# 	dataname/dataname_public.info        -- parameters of the data and task, including metric and time_budget
# 	dataname/dataname_test.data          -- training, validation and test data (solutions/target values are given for training data only)
# 	dataname/dataname_train.data
# 	dataname/dataname_train.solution
# 	dataname/dataname_valid.data
#
# The output directory will receive the predicted values (no subdirectories):
# 	dataname_test_000.predict            -- Provide predictions at regular intervals to make sure you get some results even if the program crashes
# 	dataname_test_001.predict
# 	dataname_test_002.predict
# 	...
# 	dataname_valid_000.predict
# 	dataname_valid_001.predict
# 	dataname_valid_002.predict
# 	...
# 
# Result submission:
# =================
# Search for @RESULT to locate that part of the code.
# ** Always keep this code. **
# If the subdirectory res/ contains result files (predicted values)
# the code just copies them to the output and does not train/test models.
# If no results are found, a model is trained and tested (see code submission).
#
# Code submission:
# ===============
# Search for @CODE to locate that part of the code.
# ** You may keep or modify this template or subtitute your own code. **
# The program saves predictions regularly. This way the program produces
# at least some results if it dies (or is terminated) prematurely. 
# This also allows us to plot learning curves. The last result is used by the
# scoring program.
# We implemented 2 classes:
# 1) DATA LOADING:
#    ------------
# Use/modify 
#                  D = DataManager(basename, input_dir, ...) 
# to load and preprocess data.
#     Missing values --
#       Our default method for replacing missing values is trivial: they are replaced by 0.
#       We also add extra indicator features where missing values occurred. This doubles the number of features.
#     Categorical variables --
#       The location of potential Categorical variable is indicated in D.feat_type.
#       NOTHING special is done about them in this sample code. 
#     Feature selection --
#       We only implemented an ad hoc feature selection filter efficient for the 
#       dorothea dataset to show that performance improves significantly 
#       with that filter. It takes effect only for binary classification problems with sparse
#       matrices as input and unbalanced classes.
# 2) LEARNING MACHINE:
#    ----------------
# Use/modify 
#                 M = MyAutoML(D.info, ...) 
# to create a model.
#     Number of base estimators --
#       Our models are ensembles. Adding more estimators may improve their accuracy.
#       Use M.model.n_estimators = num
#     Training --
#       M.fit(D.data['X_train'], D.data['Y_train'])
#       Fit the parameters and hyper-parameters (all inclusive!)
#       What we implemented hard-codes hyper-parameters, you probably want to
#       optimize them. Also, we made a somewhat arbitrary choice of models in
#       for the various types of data, just to give some baseline results.
#       You probably want to do better model selection and/or add your own models.
#     Testing --
#       Y_valid = M.predict(D.data['X_valid'])
#       Y_test = M.predict(D.data['X_test']) 
#
# ALL INFORMATION, SOFTWARE, DOCUMENTATION, AND DATA ARE PROVIDED "AS-IS". 
# ISABELLE GUYON, CHALEARN, AND/OR OTHER ORGANIZERS OR CODE AUTHORS DISCLAIM
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ANY PARTICULAR PURPOSE, AND THE
# WARRANTY OF NON-INFRIGEMENT OF ANY THIRD PARTY'S INTELLECTUAL PROPERTY RIGHTS. 
# IN NO EVENT SHALL ISABELLE GUYON AND/OR OTHER ORGANIZERS BE LIABLE FOR ANY SPECIAL, 
# INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF SOFTWARE, DOCUMENTS, MATERIALS, 
# PUBLICATIONS, OR INFORMATION MADE AVAILABLE FOR THE CHALLENGE. 
#
# Main contributors: Isabelle Guyon and Arthur Pesah, March-October 2014
# Lukasz Romaszko April 2015
# Originally inspired by code code: Ben Hamner, Kaggle, March 2013
# Modified by Ivan Judson and Christophe Poulain, Microsoft, December 2013
# Last modifications Isabelle Guyon, November 2015

# =========================== BEGIN USER OPTIONS ==============================

# Debug level:
############## 
# 0: run the code normally, using the time budget of the tasks
# 1: run the code normally, but limits the time to max_time
# 2: run everything, but do not train, generate random outputs in max_time
# 3: stop before the loop on datasets
# 4: just list the directories and program version
debug_mode = 0

# Time budget
#############
# Maximum time of training in seconds PER DATASET (there are 5 datasets). 
# The code should keep track of time spent and NOT exceed the time limit 
# in the dataset "info" file, stored in D.info['time_budget'], see code below.
# Beat AutoSKLearn: this overwrites time in the info file
max_time = 300 
# Use float('Inf') if you want this to have no effect

# Memory limit
##############
memlimit = 50000

# Maximum number of cycles, number of samples, and estimators
#############################################################
# Your training algorithm may be fast, so you may want to limit anyways the 
# number of points on your learning curve (this is on a log scale, so each 
# point uses twice as many time than the previous one.)
# The original code was modified to do only a small "time probing" followed
# by one single cycle. We can now also give a maximum number of estimators 
# (base learners).
max_cycle = 1 
max_estimators = float('Inf')
max_samples = 50000

# ZIP your results and code
###########################
# You can create a code submission archive, ready to submit, with zipme = True.
# This is meant to be used on your LOCAL server.
import datetime
zipme = False # use this flag to enable zipping of your code submission
the_date = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
submission_filename = '../automl_sample_submission_' + the_date

# I/O defaults
##############
# If true, the previous res/ directory is not overwritten, it changes name
save_previous_results = False
overwrite_output = True # save space
######## NEW AutoSKLEARN challenge
# Default I/O directories:      
root_dir = "/Users/isabelleguyon/Documents/Projects/Codalab/AutoMLcompetition/AutoSKlearn_bundle/ZautoSKLearn_scoring_jul18/"
default_input_dir = root_dir + "sample_hp" 
default_output_dir = root_dir + "score"  

# Constant used for a missing score
missing_score = -0.999999

# Version number
scoring_version = 0.9

######## END NEW AutoSKLEARN challenge

# =============================================================================
# =========================== END USER OPTIONS ================================
# =============================================================================

# Version of the sample code
# Change in 1.1: time is measured by time.time(), not time.clock(): we keep track of wall time
# Changes in version 2: examples of models from Lukasz; GPU code
# Changes in version 3: put back all Lukasz's stuff in model. Handle sparse numeric data.
# Added susampling to data manager to support large datasets. Added run_on_gpu in MyAutoML
# Version 3.1 Random forest is used for regression. Removed chunking in model predictions
# Version 3.2: minor correction: makes sure TP filter not run for regression.
# Version 3.3: do not write results of first cycle
version = 3.3 

# General purpose functions
import time
overall_start = time.time()         # <== Mark starting time
import os
from sys import argv, path
import numpy as np
import gc
import yaml                         # NEW AutoSKLEARN challenge

def pynish_me_aka_evaluate_model(D, M):
    try:
        X_train = D.data['X_train']
        y_train = D.data['Y_train']
        X_valid = D.data['X_valid']
        X_test = D.data['X_test']

        M = M.fit(X_train, y_train)

        if D.info['task'] == 'regression':
            y_valid_pred = M.predict(X_valid)
            y_test_pred = M.predict(X_test)
        else:
            if D.info['task'] == 'binary.classification':
                y_valid_pred = M.predict_proba(X_valid)[:,1]
                y_test_pred = M.predict_proba(X_test)[:,1]
            else:
                y_valid_pred = M.predict_proba(X_valid)
                y_test_pred = M.predict_proba(X_test)

        return y_valid_pred, y_test_pred
    # Will be catched by the pynisher
    except MemoryError as e:
        raise e
    except Exception as e:
        return e

# Our directories
# Note: On cadalab, there is an extra sub-directory called "program"
# Keave this stuff "as is"
running_on_codalab = False
run_dir = os.path.abspath(".")
codalab_run_dir = os.path.join(run_dir, "program")

if os.path.isdir(codalab_run_dir):
    run_dir = codalab_run_dir
    running_on_codalab = True
else:
    running_on_codalab = False

lib_dir = os.path.join(run_dir, "lib")
res_dir = os.path.join(run_dir, "res")
data_dir = os.path.join(run_dir, "data") # NEW AutoSKLEARN challenge
ref_dir = os.path.join(run_dir, "ref") # NEW AutoSKLEARN challenge
score_dir = os.path.join(run_dir, "score")

# Our libraries
path.append(run_dir)
path.append(lib_dir)
import data_io  # general purpose input/output functions
from data_manager import DataManager  # load/save data and get info about them
from libscores import *  # Library of scores we implemented NEW AutoSKLEARN challenge

import _logging
logger = _logging.get_logger()

if running_on_codalab:
    logger.info("Running on Codalab!")

# Add Beat Auto-sklearn libraries
path.insert(0, os.path.join(lib_dir, "xgboost", "python-package"))
path.insert(0, lib_dir)

if "PYTHONPATH" not in os.environ:
    os.environ["PYTHONPATH"] = ""
os.environ["PYTHONPATH"] = lib_dir + os.pathsep + os.environ["PYTHONPATH"] + os.pathsep + os.path.join(lib_dir,"xgboost","python-package")

# Now do Beat Auto-sklearn imports
import json
import ConfigSpace
from autosklearn.util.pipeline import get_configuration_space, get_model
from autosklearn.constants import *
from autosklearn.pipeline.classification import SimpleClassificationPipeline
from autosklearn.pipeline.regression import SimpleRegressionPipeline
import pynisher
from xgboost.core import XGBoostError

if debug_mode >= 4 or running_on_codalab: # Show library version and directory structure
    data_io.show_version()
    data_io.show_dir(run_dir)

# =========================== BEGIN PROGRAM ================================

if __name__=="__main__" and debug_mode<4:	
      
    #### Check whether everything went well (no time exceeded)
    execution_success = True
    
    #### INPUT/OUTPUT: Get input and output directory names
    if len(argv)==1: # Use the default input and output directories if no arguments are provided
        input_dir = default_input_dir
        output_dir = default_output_dir
    else:
        input_dir = argv[1]
        output_dir = argv[2] 
        
    # Lots of debug stuff NEW AutoSKLEARN challenge
    if debug_mode>-1:
        logger.info('*** SCORING PROGRAM: PLATFORM SPECIFICATIONS ***')
        show_platform()
        show_io(input_dir, output_dir)
        show_version(scoring_version)
        
    ######### SCORING NOW (NEW AutoSKLEARN challenge)
    # Fill out default score in case the code crashes!
    # Create the output directory, if it does not already exist and open output files  
    mkdir(output_dir) 
    score_file = open(os.path.join(output_dir, 'scores.txt'), 'wb')
    html_file = open(os.path.join(output_dir, 'scores.html'), 'wb')

    # Get all the solution files from the solution directory
    solution_names = sorted(ls(os.path.join(ref_dir, '*.solution')))

    # Loop over files in solution directory and search for predictions with extension .predict having the same basename
    set_num = 1
    for solution_file in solution_names:
        # Extract the dataset name from the file name
        basename = solution_file[-solution_file[::-1].index(filesep):-solution_file[::-1].index('.')-1]
        score = missing_score             
        score_file.write("set%d" % set_num + "_score: %0.12f\n" % score)
        set_num=set_num+1            
    html_file.close()
    score_file.close() 
        
    # Read the hyper-parameters NEW AutoSKLEARN challenge
    hp_filename = os.path.join(input_dir, "res", 'hp.json')

    if not os.path.isfile(hp_filename):
        logger.critical("%s does not exist. Did you upload the original .zip "
                        "file?" % hp_filename)
        exit(1)

    try:
        with open(hp_filename) as fh:
            configuration = json.load(fh)
    except Exception as inst:
        execution_success = False
        logger.critical("Could not read JSON: %s. Did you upload the "
                        "original .zip file?" % hp_filename)
        logger.critical(inst)
        exit(1)

    for key in configuration:
        configuration[key] = str(configuration[key])

        try:
            configuration[key] = float(configuration[key])

            if np.abs(np.round(configuration[key], 0) -
                      configuration[key]) < 0.00001:
                configuration[key] = np.round(configuration[key], 0).astype(int)

        except Exception:
            pass

    # Move old results and create a new output directory 
    if not(running_on_codalab) and save_previous_results:
        data_io.mvdir(res_dir, res_dir+'_'+the_date) 
    data_io.mkdir(res_dir) 
    
    #### INVENTORY DATA (and sort dataset names alphabetically)
    datanames = data_io.inventory_data(data_dir)
    # Overwrite the "natural" order
    
    #### DEBUG MODE: Show dataset list and STOP
    if debug_mode>=3:
        data_io.show_io(data_dir, res_dir)
        logger.info('****** Sample code version ' + str(version) + '******')
        logger.info('========== DATASETS ==========')
        data_io.write_list(datanames)      
        datanames = [] # Do not proceed with learning and testing
        

    # =================== NEW AutoSKLEARN challenge REMOVED @RESULT SUBMISSION (KEEP THIS) ==================

    # ================ @CODE SUBMISSION (SUBTITUTE YOUR CODE) ================= 
    time_left_over = 0
    for basename in datanames: # Loop over datasets

        filename_valid = basename + '_valid.predict'
        filename_test = basename + '_test.predict'
        try:
            os.remove(filename_valid)
        except:
            pass
        try:
            os.remove(filename_test)
        except:
            pass

        logger.info("************************************************")
        logger.info("******** Processing dataset " + basename.capitalize() + "********")
        logger.info("************************************************")
        
        # ======== Creating a data object with data, informations about it
        logger.info("========= Reading and converting data ==========")
        D = DataManager(basename, data_dir, max_samples=max_samples)
        logger.info(str(D))
        logger.info("[+] Size of uploaded data  %5.2f bytes" %
               data_io.total_size(D))
        overall_time_budget = min(max_time, D.info['time_budget'])
        
        # ======== Create auto-sklearn model
        new_info_object = {}
        new_info_object['is_sparse'] = D.info['is_sparse']
        new_info_object['task'] = STRING_TO_TASK_TYPES[D.info['task']]
        new_info_object['metric'] = STRING_TO_METRIC[D.info['metric']]

        configuration_space = get_configuration_space(new_info_object)
        try:
            config = ConfigSpace.Configuration(configuration_space, configuration)
        except Exception as inst:
            execution_success = False
            logger.critical(inst)
            continue

        logger.info("Running the following configuration:")
        logger.info(str(config))

        if 'classifier:__choice__' in configuration:
            M = SimpleClassificationPipeline(config, 1)
        elif 'regressor:__choice__' in configuration:
            M = SimpleRegressionPipeline(config, 1)
        else:
            execution_success = False
            logger.critical('Invalid hyperparameter configuration, does neither '
                            'contain hyperparameter classifier:__choice__ nor '
                            'regressor:__choice__!')
            continue

        evaluate_model = pynisher.enforce_limits(
            mem_in_mb=memlimit, wall_time_in_s=overall_time_budget)(
        pynish_me_aka_evaluate_model)
        rval = evaluate_model(D, M)
        if rval is not None:
            if isinstance(rval, ValueError) and rval.message == "KernelPCA " \
                                                                "removed all features!":
                logger.error("KernelPCA removed all features. Please try a "
                             "different configuration.")
                execution_success = False
                continue
            elif isinstance(rval, XGBoostError):
                logger.error("Internal XGBoost error. Please try a different "
                             "configuration.")
                execution_success = False
                continue
            elif isinstance(rval, Exception):
                logger.error("Unexpected exception. Please report to the "
                             "competition organizers:")
                logger.error(rval.__class__.__name__)
                logger.error(rval.message)
                execution_success = False
                continue
            else:
                Y_valid, Y_test = rval
        else:
            if issubclass(evaluate_model.exit_status,
                          pynisher.TimeoutException):
                logger.error("You've reached the timeout of %d seconds. "
                             "Model fitting was terminated.",
                             overall_time_budget)
            elif issubclass(evaluate_model.exit_status,
                            pynisher.MemorylimitException):
                logger.error("You've reached the memory limit of %dMB. "
                             "Model fitting was terminated.", memlimit)
            else:
                logger.error("No result returned for unknown reasons.")
            execution_success = False
            continue

        data_io.write(os.path.join(res_dir, filename_valid), Y_valid)
        data_io.write(os.path.join(res_dir, filename_test), Y_test)

        # Clean up
        del D
        del M
        gc.collect()
    	
    overall_time_spent = time.time() - overall_start
    if execution_success:
        logger.info("[+] Done")
    else:
        logger.error("[-] Done, but some tasks failed")
    logger.info(("[-] Overall time spent %5.2f sec " % overall_time_spent) + \
                (" :: Overall time budget %5.2f sec" % overall_time_budget))
              
    ######### SCORING NOW (NEW AutoSKLEARN challenge)
    # Create the output directory, if it does not already exist and open output files  
    mkdir(output_dir) 
    score_file = open(os.path.join(output_dir, 'scores.txt'), 'wb')
    html_file = open(os.path.join(output_dir, 'scores.html'), 'wb')

    # Get all the solution files from the solution directory
    solution_names = sorted(ls(os.path.join(ref_dir, '*.solution')))

    # Loop over files in solution directory and search for predictions with extension .predict having the same basename
    set_num = 1
    for solution_file in solution_names:
        # Extract the dataset name from the file name
        basename = solution_file[-solution_file[::-1].index(filesep):-solution_file[::-1].index('.')-1]
        # Load the info file and get the task and metric
        info_file = ls(os.path.join(ref_dir, basename[0:3] + '*_public.info'))[0]
        info = get_info (info_file)    
        score_name = info['task'][0:-15] + info['metric'][0:-7].upper() 
        try:
            # Get the last prediction from the res subdirectory (must end with '.predict')
            predict_file = ls(os.path.join(res_dir,  basename + '*.predict'))[-1]
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
                logger.info("======= Set %d" % set_num + " (" + predict_name.capitalize() + "): score(" + score_name + ")=%0.12f =======" % score)
                html_file.write("======= Set %d" % set_num + " (" + predict_name.capitalize() + "): score(" + score_name + ")=%0.12f =======\n" % score)
            except:
                raise Exception('Error in calculation of the specific score of the task')
                
            if debug_mode>0: 
                scores = compute_all_scores(solution, prediction)
                write_scores(html_file, scores)
                    
        except Exception as inst:
            score = missing_score
            logger.error("======= Set %d" % set_num + " (" +
                         basename.capitalize() + "): score(" + score_name + ")=ERROR =======")
            html_file.write("======= Set %d" % set_num + " (" + basename.capitalize() + "): score(" + score_name + ")=ERROR =======\n")
            logger.error(inst)
            
        # Write score corresponding to selected task and metric to the output file
        score_file.write("set%d" % set_num + "_score: %0.12f\n" % score)
        set_num=set_num+1            
    # End loop for solution_file in solution_names

	# NEW AutoSKLEARN challenge No execution duration

    html_file.close()
    score_file.close()

    exit(0)
    #if running_on_codalab:
    #    if execution_success:
    #        exit(0)
    #    else:
    #        exit(1)
