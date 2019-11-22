# Pyomo Performance Tests Overview

Pyomo is a Python-based open-source software package that supports a diverse set of optimization capabilities for formulating and analyzing optimization models. Pyomo can be used to define symbolic problems, create concrete problem instances, and solve these instances with standard solvers.

This repository contains the reworked benchmark tests (aka, performance tests) to be run using `nose 1.3.7` for Pyomo, based on Bill Hart's original tests.

## Placement of Repository

Your local copy of `Pyomo/pyomo-model-libraries` repository should be parallel to the `Pyomo/pyomo` repository.

## Setup
To initialize the included console scripts, run:
```
$ python setup.py develop
```
These tests assume that `pyomo` has been setup using the same command. The tests can still be run if `pyomo` was installed using different means - output files, however, will be missing useful Github commit information.

## Running the Tests

### Manually
These tests can be invoked using the following command from the `pyomo-model-libraries` directory:
```
$ nosetests performancetests/tests/<subset>
```

The available subsets are `longtests` and `shorttests`.

Also, both `longtests` and `shorttests` can be run together:
```
$ nosetests performancetests/tests
```
You can also use categories to initialize the tests:
```
$ nosetests "--eval-attr=short and (not nl)" performancetests/tests
```
### Console Script
These tests can also be invoked from any directory using the following console script command:
```
$ pyomo-performance [-h] [--version] [-c CATEGORY] [-l LOCATION] [-v]
```
The optional arguments are as follows:
```
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -c CATEGORY, --cat CATEGORY
                        Specify the category(ies) of performance tests to run
                        in comma-separated list
  -l LOCATION, --location LOCATION
                        Specify location (including name of file, if desired)
                        of test(s)
  -v, --verbose         Verbose output

```
By default, the console script will run all tests in the `performancetests/tests` directory, but this can be filtered using categories like `short`, `long`, `nl`, `'not bar'`, etc.

### Output
Results from the test will print to the terminal in this fashion:
```
Performance Testing Report:
Pyomo Model bilinear1_100_100 (bar) - Total Runtime = 0.490000
Pyomo Model bilinear1_100_100 (gms) - Total Runtime = 0.470000
```

Output files in `.csv` format will be created in the `performancetests/output/runtime` directory for each successfully run test. Rundata as `.out` files will be created in the `performancetests/output/rundata` directory.

## Comparing Output Files

### Console Script
This package includes a console script that will compare the data within two performance test `csv` files.
This script can be invoked using the following command:
```
$ pyomo-analyze [-h] [-f FILE1] [-f FILE2]
```
The two files can either be listed by two calls to the `-f` option or a single call in a comma-separated list:
```
# These commands are the same:

$ pyomo-analyze -f path/to/file1 -f path/to/file2
$ pyomo-analyze -f path/to/file1,path/to/file2
```

The results will be printed to the console as well as in `.csv` format in the `performancetests/output/analysisdata` directory.

### Difference Calculation
The results of the analysis routine compares the same element of each file, i.e., timestamp to timestamp, solver to solver, etc.

For `timestamp`, `python_version`, and `commit_info`, differences will be called out explicitly, if they exist.

For the remaining elements, the relative percentage difference is calculated, with `v1` as the FILE1 value and `v2` as the FILE2 value, by:
```
(v2-v1) / ((v1+v2)/2) * 100
```
If `v1` and `v2` are both 0, the result will be listed as `Undefined`.

The output will look like this:
```
************* Analysis Results *************
timestamp :
       [['File 1: 2019-11-22 13:37:44', 'File 2: 2019-11-22 13:37:49']]
python_version :
       ['3.7.4']
commit_info :
       ['84f2f728b']
totalruntime :
       ['-9.182861518736637 %']
construct :
       ['-7.951586703904198 %']
write_problem :
       ['-10.162846371077565 %']
read_logfile :
       ['Undefined']
read_solution :
       ['Undefined']
solver :
       ['Undefined']
presolve :
       ['Undefined']
postsolve :
       ['Undefined']
transformations :
       ['Undefined']
**********************************************
```