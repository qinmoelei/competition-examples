# Functions performing various input/output operations for the ChaLearn AutoML challenge

# Main contributors: Arthur Pesah and Isabelle Guyon, August-October 2014

# ALL INFORMATION, SOFTWARE, DOCUMENTATION, AND DATA ARE PROVIDED "AS-IS". 
# ISABELLE GUYON, CHALEARN, AND/OR OTHER ORGANIZERS OR CODE AUTHORS DISCLAIM
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ANY PARTICULAR PURPOSE, AND THE
# WARRANTY OF NON-INFRIGEMENT OF ANY THIRD PARTY'S INTELLECTUAL PROPERTY RIGHTS. 
# IN NO EVENT SHALL ISABELLE GUYON AND/OR OTHER ORGANIZERS BE LIABLE FOR ANY SPECIAL, 
# INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF SOFTWARE, DOCUMENTS, MATERIALS, 
# PUBLICATIONS, OR INFORMATION MADE AVAILABLE FOR THE CHALLENGE. 

from __future__ import print_function
from sys import getsizeof, stderr
from itertools import chain
from collections import deque
try:
    from reprlib import repr
except ImportError:
    pass

import numpy as np
import os
import shutil
from scipy.sparse import * # used in data_binary_sparse 
from zipfile import ZipFile, ZIP_DEFLATED
from contextlib import closing
import data_converter
from sys import stderr
from sys import version
from glob import glob as ls
from os import getcwd as pwd
from pip import get_installed_distributions as lib
import yaml
from shutil import copy2
import csv
import psutil
import platform
import _logging

logger = _logging.get_logger()

# ================ Small auxiliary functions =================

if (os.name == "nt"):
       filesep = '\\'
else:
       filesep = '/'

def mkdir(d):
    ''' Create a new directory'''
    if not os.path.exists(d):
        os.makedirs(d)
        
def mvdir(source, dest):
    ''' Move a directory'''
    if os.path.exists(source):
        os.rename(source, dest)

def rmdir(d):
    ''' Remove an existingdirectory'''
    if os.path.exists(d):
        shutil.rmtree(d)
        
# ================ Output prediction results and prepare code submission =================
        
def write(filename, predictions):
    ''' Write prediction scores in prescribed format'''
    with open(filename, "w") as output_file:
        for row in predictions:
            if type(row) is not np.ndarray and type(row) is not list:
                row = [row]
            for val in row:
                output_file.write('{0:g} '.format(float(val)))
            output_file.write('\n')

def zipdir(archivename, basedir):
    '''Zip directory, from J.F. Sebastian http://stackoverflow.com/'''
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                if fn[-4:]!='.zip':
                    absfn = os.path.join(root, fn)
                    zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                    z.write(absfn, zfn)
                    
# ================ Inventory input data and create data structure =================
   
def inventory_data(input_dir):
    ''' Inventory the datasets in the input directory and return them in alphabetical order'''
    # Assume first that there is a hierarchy dataname/dataname_train.data
    training_names = inventory_data_dir(input_dir)
    ntr=len(training_names)
    if ntr==0:
        # Try to see if there is a flat directory structure
        training_names = inventory_data_nodir(input_dir)
    ntr=len(training_names)
    if ntr==0:
        logger.warning('WARNING: Inventory data - No data file found')
        training_names = []
    training_names.sort()
    return training_names
        
def inventory_data_nodir(input_dir):
    ''' Inventory data, assuming flat directory structure'''
    training_names = ls(os.path.join(input_dir, '*_train.data'))
    for i in range(0,len(training_names)):
        name = training_names[i]
        training_names[i] = name[-name[::-1].index(filesep):-name[::-1].index('_')-1]
        check_dataset(input_dir, training_names[i])
    return training_names
    
def inventory_data_dir(input_dir):
    ''' Inventory data, assuming flat directory structure, assuming a directory hierarchy'''
    training_names = ls(input_dir + '/*/*_train.data') # This supports subdirectory structures obtained by concatenating bundles
    for i in range(0,len(training_names)):
        name = training_names[i]
        training_names[i] = name[-name[::-1].index(filesep):-name[::-1].index('_')-1]
        check_dataset(os.path.join(input_dir, training_names[i]), training_names[i])
    return training_names
    
def check_dataset(dirname, name):
    ''' Check the test and valid files are in the directory, as well as the solution'''
    valid_file = os.path.join(dirname, name + '_valid.data')
    if not os.path.isfile(valid_file):
        logger.critical('No validation file for ' + name)
        exit(1)  
    test_file = os.path.join(dirname, name + '_test.data')
    if not os.path.isfile(test_file):
        logger.critical('No test file for ' + name)
        exit(1)
    # Check the training labels are there
    training_solution = os.path.join(dirname, name + '_train.solution')
    if not os.path.isfile(training_solution):
        logger.critical('No training labels for ' + name)
        exit(1)
    return True


def data(filename, nbr_features=None):
    ''' The 2nd parameter makes possible a using of the 3 functions of data reading (data, data_sparse, data_binary_sparse) without changing parameters'''
    return np.array(data_converter.file_to_array(filename), dtype=float)
            
def data_sparse (filename, nbr_features):
    ''' This function takes as argument a file representing a sparse matrix
    sparse_matrix[i][j] = "a:b" means matrix[i][a] = basename and load it with the loadsvm load_svmlight_file
    '''
    return data_converter.file_to_libsvm (filename = filename, data_binary = False  , n_features = nbr_features)



def data_binary_sparse (filename , nbr_features):
    ''' This fuction takes as argument a file representing a sparse binary matrix 
    sparse_binary_matrix[i][j] = "a"and transforms it temporarily into file svmlibs format( <index2>:<value2>)
    to load it with the loadsvm load_svmlight_file
    '''
    return data_converter.file_to_libsvm (filename = filename, data_binary = True  , n_features = nbr_features)


 
# ================ Copy results from input to output ==========================
 
def copy_results(datanames, result_dir, output_dir, verbose):
    ''' This function copies all the [dataname.predict] results from result_dir to output_dir'''
    missing_files = []
    for basename in datanames:
        try:
            missing = False
            test_files = ls(result_dir + "/" + basename + "*_test*.predict")
            if len(test_files)==0: 
                logger.warning("[-] Missing 'test' result files for " + basename) 
                missing = True
            valid_files = ls(result_dir + "/" + basename + "*_valid*.predict")
            if len(valid_files)==0: 
                logger.warning("[-] Missing 'valid' result files for " + basename) 
                missing = True
            if missing == False:
                for f in test_files: copy2(f, output_dir)
                for f in valid_files: copy2(f, output_dir)
                logger.warning("[+] " + basename.capitalize() + " copied")
            else: 
                missing_files.append(basename)           
        except:
            logger.error("[-] Missing result files")
            return datanames
    return missing_files

# ================ Display directory structure and code version (for debug purposes) =================
      
def show_dir(run_dir):
    logger.info('=== Listing run dir ===')
    map(logger.info, ls(run_dir))
    map(logger.info, ls(run_dir + '/*'))
    map(logger.info, ls(run_dir + '/*/*'))
    map(logger.info, ls(run_dir + '/*/*/*'))
    map(logger.info, ls(run_dir + '/*/*/*/*'))
      
def show_io(input_dir, output_dir):
    logger.info('=== DIRECTORIES ===')
    # Show this directory
    logger.info("-- Current directory " + pwd() + ":")
    map(logger.info, ls('.'))
    map(logger.info, ls('./*'))
    map(logger.info, ls('./*/*'))
    
    # List input and output directories
    logger.info("-- Input directory " + input_dir)
    map(logger.info, ls(input_dir))
    map(logger.info, ls(input_dir + '/*'))
    map(logger.info, ls(input_dir + '/*/*'))
    map(logger.info, ls(input_dir + '/*/*/*'))

    logger.info("-- Output directory  " + output_dir)
    map(logger.info, ls(output_dir))
    map(logger.info, ls(output_dir + '/*'))
        
    # write meta data to sdterr
    logger.info('=== METADATA ===')
    logger.info("-- Current directory " + pwd() + ":")
    try:
        metadata = yaml.load(open('metadata', 'r'))
        for key,value in metadata.items():
            logger.info(key + ': ' + str(value))
    except:
        logger.info("none");
    logger.info("-- Input directory " + input_dir + ":")
    try:
        metadata = yaml.load(open(os.path.join(input_dir, 'metadata'), 'r'))
        for key,value in metadata.items():
            logger.info(key + ': ' + str(value))
    except:
        logger.info("none")
    
def show_version():
    # Python version and library versions
    logger.info('=== VERSIONS ===')
    # Python version
    logger.info("Python version: " + version)
    # Give information on the version installed
    logger.info("Versions of libraries installed:")
    for line in sorted(["%s==%s" % (i.key, i.version) for i in lib()]):
        logger.info(line)
 
 # Compute the total memory size of an object in bytes

def total_size(o, handlers={}):
    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        logger.info('%s, %s, %s', s, type(o), repr(o))

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)

    # write the results in a csv file
def platform_score ( basename , mem_used ,n_estimators , time_spent , time_budget ):
# write the results and platform information in a csv file (performance.csv)
    with open('performance.csv', 'a') as fp:
        a = csv.writer(fp, delimiter=',')
        #['Data name','Nb estimators','System', 'Machine' , 'Platform' ,'memory used (Mb)' , 'number of CPU' ,' time spent (sec)' , 'time budget (sec)'],
        data = [
        [basename,n_estimators,platform.system(), platform.machine(),platform.platform() , float("{0:.2f}".format(mem_used/1048576.0)) , str(psutil.cpu_count()) , float("{0:.2f}".format(time_spent)) ,    time_budget ]
        ]
        a.writerows(data)

