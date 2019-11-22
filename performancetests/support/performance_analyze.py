#
#  ___________________________________________________________________________
#  Pyomo: Python Optimization Modeling Objects
#  Copyright 2017 National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and 
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain 
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

import sys
import os
import errno
import datetime
import csv
import argparse
import json
import pprint

def main_analysis_script(args=None):
    if args is None:
        args = sys.argv[1:]
        
    # Read in the two file names to be compared
    parser = argparse.ArgumentParser(description='Analyze two Pyomo Performance Test CSV files')
    
    parser.add_argument('-f','--file',
                        action='append',
                        dest='file',
                        help="Specify the two files to compare (-f FILE1,FILE2 or -f FILE1 -f FILE2)")
    
    args = parser.parse_args()
    
    # Exit if files were not specified
    if args.file == None:
        print('USAGE: pyomo-analyze -f FILE1,FILE2 \n       pyomo-analyze -f FILE1 -f FILE2')
        sys.exit('ERROR: Please specify the files to be analyzed.')
    
    files = []
    for item in args.file:
        if '.csv' not in item: #Check if files are both CSVs
            sys.exit('ERROR: Must be CSV files.')
        else:
            files.append(item)
    
    if len(files) == 1: # If files were comma-separated, split into two items
        files = [t for f in files for t in f.split(',')]
      
    
    if os.path.isfile(files[0]) and os.path.isfile(files[1]): # Check that both files exist
        analyze_csv(files)
    else:
        sys.exit('ERROR: Files cannot be found. Please check paths.')
    
    


def analyze_csv(files):
    '''
    This is the data analysis routine.
    These calculations are based on relative difference between the first and second. 
    The formula used is:
        (V2-V1) / |(V1+V2)/2| * 100 = % Difference
    '''
    file1 = files[0]
    file2 = files[1]
    
    # Open the first file and parse it into a dictionary 
    with open(file1, 'r') as csvfile1:
        csvread = csv.reader(csvfile1)
        headers1 = next(csvread, None)
        data1 = {}
        for h in headers1:
            data1[h] = []
        for row in csvread:
            for h,v in zip(headers1,row):
                data1[h].append(v)
      
    # Open the second file and parse it into a dictionary
    with open(file2, 'r') as csvfile2:
        csvread = csv.reader(csvfile2)
        headers2 = next(csvread, None)
        data2 = {}
        for h in headers2:
            data2[h] = []
        for row in csvread:
            for h,v in zip(headers2,row):
                data2[h].append(v)

    # Initialize Analysis dictionary
    results = {}
    
    # Create the headers
    for h in headers1:
        results[h] = []
        
    # Print the timestamps
    time1 = data1['timestamp']
    time1[0] = 'File 1: ' + time1[0]
    time2 = data2['timestamp']
    time2[0] = 'File 2: ' + time2[0]
    results['timestamp'].append(time1[0])
    results['timestamp'].append(time2[0])
    
    # Compare the Python versions
    python1 = data1['python_version']
    python2 = data2['python_version']
    if python1 == python2:
        results['python_version'].append(python1[0])
    else:
        results['python_version'].append(python1[0])
        results['python_version'].append(python2[0])
    
    # Compare the Commit info
    sha1 = data1['commit_info']
    sha2 = data2['commit_info']
    if sha1 == sha2:
        results['commit_info'].append(sha1[0])
    else:
        results['commit_info'].append(sha1[0])
        results['commit_info'].append(sha2[0])
     
    # List of the rest of the headers
    shortheaders = headers1[3:]
    
    # Calculate the relative difference for each remaining data element
    for h in shortheaders:
        results[h].append(get_rel_diff(data1, data2, h))
      
    print('\n************* Analysis Results *************')    
    for key, val in results.items():
        print(key, ":\n      ", val)
    print('**********************************************\n')
    
        
    filepath = _set_CSVFilePath()
    _csv_writer(filepath, results)
    
    
def get_rel_diff(data1, data2, item):
    v1 = data1[item]
    v1 = float(v1[0])
    v2 = data2[item]
    v2 = float(v2[0])
    
    try:
        result = str((v2 - v1)/((v1 + v2)/2) * 100) + ' %'
    except ZeroDivisionError:
        result = 'Undefined'
        
    return result
        
        
#########
# This block contains path changes and output name settings
#########
    
def _chng_to_perf(): # Change working directory to Performancetests
    moddir = os.path.dirname(__file__)
    perfdir = os.path.abspath(os.path.join(moddir, os.pardir))
    os.chdir(perfdir)
    
def _set_CSVFilePath():
    _chng_to_perf()
    timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    runtime_outputdir = '%s/output/analysisdata/' % (os.getcwd())
    _mkdir_p(runtime_outputdir)
    _csvfilepath = '%spyomo_perf_test_analysis_%s.csv' % (runtime_outputdir, timestamp)
    return _csvfilepath

def _mkdir_p(path, mode=777):
    try:
        os.makedirs(path, mode)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            os.system('chmod 777 ' + path)
            pass
        else:
            exitstr = str("Unable to create directory {0}").format(path)
            sys.exit(exitstr)
            
def _csv_writer(file, d):
    with open(file, 'w') as f:
        writer = csv.writer(f)
        for key,val in d.items():
            writer.writerow([key,val])
    
    
    