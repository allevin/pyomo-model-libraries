#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright 2017 National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and 
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain 
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

import os
import sys
import argparse
import pyomo
 

def get_sha(): # Retrieves the SHA for the pyomo directory 
    sha = 'Undefined'
    cwd = os.getcwd()
    pydir = os.path.dirname(pyomo.__file__)
    if os.path.isdir(pydir):
        os.chdir(pydir)
        dir_origin = os.popen('git config --get remote.origin.url').read()
        if 'github.com/Pyomo' in dir_origin:
            tsha = os.popen('git rev-parse --short HEAD').read()
            sha = tsha.replace('\n','')
    os.chdir(cwd)
    string = 'Current Pyomo Repository SHA: ' + sha
    return string

def chng_to_perf(): # Change working directory to Performancetests
    moddir = os.path.dirname(__file__)
    perfdir = os.path.abspath(os.path.join(moddir, os.pardir))
    os.chdir(perfdir)

def main_performance_script(args=None):
    # The main routines for loading fall here
    if args is None:
        args = sys.argv[1:]
        
    parser = argparse.ArgumentParser(description='pyomo-performance [options]')

    parser.add_argument('--version',
                        action='version',
                        version=get_sha())
    parser.add_argument('-c','--cat',
                        action='append',
                        dest='category',
                        help='Specify the category(ies) of performance tests to run in comma-separated list')
    parser.add_argument('-l', '--location',
                        action='store',
                        dest='location',
                        help='Specify location (including name of file, if desired) of test(s)')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        dest='verbose',
                        default=False,
                        help='Verbose output')
#    parser.add_argument('-o', '--output',
#                       action='store',
#                       dest='output',
#                       help='Specify name of output files (INACTIVE)')
#    parser.add_argument('-d', '--directory',
#                       action='store',
#                       dest='directory',
#                       help='Specify location of output files (INACTIVE)')
#    parser.add_argument('-n','--number',
#                        type=int,
#                        action='store',
#                        dest='number',
#                        default=1,
#                        help='Specify the number of runs (INACTIVE)')
#    parser.add_argument('-a','--append',
#                        action='store_true',
#                        dest='append',
#                        default=False,
#                        help='Include a YYMMDD timestamp in the OUTPUT.csv file name (INACTIVE)')

    args = parser.parse_args()
    
    # Options that can be passed to nosetests will be added to a list here
    options=[]
    if args.verbose:
        options.append('-v')
    if args.category:
        cat_str = args.category[0]
        cat_list = cat_str.split(',')
        cat_list_p = []
        for attr in cat_list:
            cat_list_p.append('(' + attr + ')') 
        all_cat = ' and '.join(cat_list_p)
        options.append('"--eval-attr=' + all_cat + '"')
    options=' '.join(options)
        
    # In case the user specified $HOME or ~ in their path, expand it
    loc = ''
    if args.location != None:
        loc = args.location
        if os.path.isdir(loc):
            loc = os.path.expanduser(loc)
    
    # Check if we are currently in the testing repository; if not, switch to testing repository
    dir_origin = os.popen('git config --get remote.origin.url').read()
    if 'github.com/Pyomo/pyomo-model-libraries' not in dir_origin:
        chng_to_perf()
        
        
    os.system('nosetests '+options+' '+loc) 
    return True