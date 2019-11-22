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
import re
import csv
import gc
import errno
import pyomo
import inspect
import datetime
import pyutilib.subprocess
import pyutilib.th as unittest
from performancetests.support import testglobals
from multiprocessing import Process

################################################################################

class PerformanceTestCase(unittest.TestCase):

    def __init__(self, methodName):
        super(PerformanceTestCase, self).__init__(methodName)

        # Nose calls this module in unexpected ways... We therefore need
        # to init the member variables with something, the actual tests
        # will populate with reasonable data for the test runs

        # Find the top level "performancetests" directory
        thisdir = os.path.dirname(__file__)
        self._performancetestsdir = os.path.abspath(os.path.join(thisdir, os.pardir))
        if os.path.basename(self._performancetestsdir) != "performancetests":
            exitstr = str("TEST-ERROR: Cannot Find Main performance tests directory named 'performancetests' in path %s") % thisdir
            sys.exit(exitstr)

        self._verbose = True
        self._timeout = 60
        self._skippingtest = False
        self._skippingreason = ""
        self._modelname = ''
        self._num = '1'
        self._rundir = os.getcwd()
        self._modeldir = os.getcwd()
        self._outfilepath = os.getcwd()
        self._csvfilepath = os.getcwd()
        self._modeldatafilepath = os.getcwd()
        self._datafilename = None
        self._format  = 'lp'
        self._runtimeinfo = {}
        self._runtestcmd = ""
        self._timestamp = ""

        self.setTestVerbose(True)
        self.setTestTimeout(60)

###

    # Perform a Performance Test run of a Model via Pyomo
    def runPyomoModelTest(self, format, scriptmode=False):
        self._checkParamType("format", format, str)
        self._format = format
        self._set_OutputFilePath()
        self._set_CSVFilePath()
        self._set_ModelDataFilePath()
        rtn = self._run_testing_model(runasscript=scriptmode)
        if rtn == -2:
            errstr = str('Run of Pyomo Model {0} has TIMED-OUT in {1} seconds, rtn = {2}').format(self._modelname, self._timeout, rtn)
        else:
            errstr = str('Run of Pyomo Model {0} failed, rtn = {1}').format(self._modelname, rtn)
        self.assertGreaterEqual(rtn, 0, msg = errstr)

###

    # Skip the Test, This provides some feedback to the user that the test was skipped
    def skipThisTest(self, reason):
        self._checkParamType("reason", reason, str)
        self._skippingtest = True
        self._skippingreason = reason
        reportstring = "Model %s_%s (%s) - Test Skipped: %s" % (self._modelname, self._num, self._format, self._skippingreason) + "\n"
        self._appendSkipReportToFinalTestReport(reportstring)
        # NOTE: The skipTest MUST come at the end of this method
        self.skipTest(reason)

###

    def setTestTimeout(self, time):
        self._checkParamType("time", time, int)
        self._timeout = time

    def setTestVerbose(self, verbose):
        self._checkParamType("verbose", verbose, bool)
        self._verbose = verbose

    def setTestModelDir(self, dir):
        self._checkParamType("dir", dir, str)
        modeldir = dir
        # If the path does not exist, then try to use our model path
        if not os.path.isdir(modeldir):
            topmodeldir = self.getTopTestingDir() + '/models/'
            secondarymodeldir = '%s%s' % (topmodeldir, dir)
            if not os.path.isdir(secondarymodeldir):
                exitstr = str("TEST-ERROR: setTestModelDir() - Directory {0} does not exist; nor is it under {1}").format(dir, topmodeldir)
                sys.exit(exitstr)
            modeldir = secondarymodeldir
        self._modeldir = modeldir
        self._rundir = modeldir

    def setTestModelName(self, name):
        self._checkParamType("name", name, str)
        self._modelname = name

    def setTestDataFileName(self, name):
        self._checkParamType("name", name, str)
        self._datafilename = name

    def setTestNum(self, num):
        self._checkParamType("num", num, str)
        self._num = num

    def getTopTestingDir(self):
        return self._performancetestsdir

################################################################################

    # Run a model as a test problem
    def _run_testing_model(self, runasscript):
        if self._skippingtest == True:
            return 0


        def run_subprocess_test():
            # Run the test as a sub-process with the pyutilib.subprocess killing
            # the job based on a slightly larger timeout.
            res = pyutilib.subprocess.run(self._runtestcmd,
                                          outfile=self._outfilepath,
                                          verbose=self._verbose,
                                          timelimit=self._timeout + 0.5)
            return res[0]


        def init_subprocess_testing_system():
            # Start Garbage Collection
            gc.collect()

            self._timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Figure out the path to the python test model to run
            testmodelfilepath = '%s/%s.py' % (self._modeldir, self._modelname)
            if not os.path.isfile(testmodelfilepath):
                sys.exit(str("TEST-ERROR: Cannot find path to model file at {0}").format(testmodelfilepath))

            # Figure out the path to the data file (if it is defined)
            if self._datafilename != "":
                datafilepath = '%s/%s' % (self._modeldir, self._datafilename)
                if not os.path.isfile(datafilepath):
                    sys.exit(str("TEST-ERROR: Cannot find path to data file at {0}").format(datafilepath))
            else:
                datafilepath = ""

            # Build the command line to be run
            if runasscript == False:
                self._runtestcmd = 'pyomo convert --report-timing --output=%s %s %s' % (self._modeldatafilepath,
                                                                                        testmodelfilepath,
                                                                                        datafilepath)
            else:
                self._runtestcmd = 'python %s %s' % (testmodelfilepath, self._modeldatafilepath)

            if self._verbose:
                print("Command: %s" % self._runtestcmd)


        def perform_subprocess_testing():
            # cd to the model directory
            savedcwd = os.getcwd()
            os.chdir(self._rundir)

            # Launch a subprocess with timeout.
            p1 = Process(target=run_subprocess_test, name='Run_Subprocess_Test_Function')
            p1.start()
            p1.join(timeout=self._timeout)
            p1.terminate()
            res = p1.exitcode

            os.chdir(savedcwd)

            if p1.exitcode == None:
                print("Performance testing FAILED because testing TIMEOUT was generated! : subprocess rtn = %s" % str(res))
                print("")
                print("Pyomo Logfile: ")
                self._dump_file_to_stdout(self._outfilepath)
                print("")
                return -2

            # Check for a failure of the run, and log the output file
            if res != 0:
                print("Performance testing FAILED because an ERROR was generated! : subprocess rtn %s" % str(res))
                print("")
                print("Pyomo Logfile: ")
                self._dump_file_to_stdout(self._outfilepath)
                print("")
                return -1

            return res

        def perform_subprocess_post_processing():
            totalruntime = 0
            # Run was successful, so extract the timing data
            self._runtimeinfo = self._extract_timing_data()
            self._save_timing_data_in_csv(self._runtimeinfo, self._timestamp)

            # Get the total runtime from the dict to be returned
            totalruntime = self._runtimeinfo['totalruntime']

            # Delete the unwanted output files
            self._rm_file(self._modeldatafilepath)
            self._rm_file(self._outfilepath)

            # Build a report string
            typestr = "Script" if runasscript else "Model "
            reportstring = "%s %s_%s (%s) - Total Runtime = %f" % (typestr,
                                                                   self._modelname,
                                                                   self._num,
                                                                   self._format,
                                                                   totalruntime) + "\n"
            self._appendRunReportToFinalTestReport(reportstring)

            # Tell the user the Model Runtime in the unit tests
            if self._is_nosetest_output_veryverbose() == True:
                noselog("\n")
                noselog(reportstring)

            self._sumTotalRunTimes(totalruntime)
            return totalruntime

        def f():
            init_subprocess_testing_system()
            res = perform_subprocess_testing()
            if res != 0:
                return res
            return perform_subprocess_post_processing()

        # Run f() above, and return its results
        return f()

#####

    # Extract Pyomo model run timings from output file
    def _extract_timing_data(self):
        seconds = {}

        with open(self._outfilepath, 'r') as OUTPUT:
            if self._verbose:
                sys.stdout.write("*" * 15 )
                sys.stdout.write("  EXTRACTED TIMING  ")
                sys.stdout.write("*" * 15 + "\n")

            # Init the timing data
            seconds['totalruntime'] = 0
            seconds['construct'] = 0
            seconds['write_problem'] = 0
            seconds['read_logfile'] = 0
            seconds['read_solution'] = 0
            seconds['solver'] = 0
            seconds['presolve'] = 0
            seconds['postsolve'] = 0
            seconds['transformations'] = 0

            for line in OUTPUT:
                if self._verbose:
                    sys.stdout.write(line)
                tokens = re.split('[ \t]+', line.strip())
                if len(tokens) < 2:
                    pass
                # Look for the tokens to fill the seconds dict var
                elif tokens[1] == 'seconds' and tokens[2] == 'required':
                    if tokens[3:5] == ['to', 'construct']:
                        seconds['construct'] = float(tokens[0])
                    elif tokens[3:6] == ['to', 'write', 'file']:
                        seconds['write_problem'] = float(tokens[0])
                    elif tokens[3:6] == ['to', 'read', 'logfile']:
                        seconds['read_logfile'] = float(tokens[0])
                    elif tokens[3:6] == ['to', 'read', 'solution']:
                        seconds['read_solution'] = float(tokens[0])
                    elif tokens[3:5] == ['for', 'solver']:
                        seconds['solver'] = float(tokens[0])
                    elif tokens[3:5] == ['for', 'presolve']:
                        seconds['presolve'] = float(tokens[0])
                    elif tokens[3:5] == ['for', 'postsolve']:
                        seconds['postsolve'] = float(tokens[0])
                    elif tokens[3:6] == ['for', 'problem', 'transformations']:
                        seconds['transformations'] = float(tokens[0])

            # Sume up all the numbers and add to the seconds dict var
            sum = 0
            for key in seconds.keys():
                sum += seconds[key]
            seconds['totalruntime'] = sum

            if self._verbose:
                sys.stdout.write("*" * 50 + "\n")
                sys.stdout.write(str("{0}\n").format(seconds))
                sys.stdout.write("*" * 50 + "\n")
        return seconds

#####

    # Save the Pyomo run timings into a csv file
    def _save_timing_data_in_csv(self, runtimeinfo, timestamp):

        csv_columns = ['timestamp','python_version','commit_info','totalruntime','construct','write_problem','read_logfile','read_solution','solver','presolve','postsolve','transformations']
        runtimeinfo['timestamp'] = timestamp
        runtimeinfo['commit_info'] = testglobals.pyomo_sha

        python_v = str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)
        runtimeinfo['python_version'] = python_v

        with open(self._csvfilepath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerow(runtimeinfo)

#####

    def _dump_file_to_stdout(self, fname):
        if not os.path.exists(fname):
            return
        with open(fname, 'r') as INPUT:
            for line in INPUT:
                sys.stdout.write(line)

    def _mkdir_p(self, path, mode=777):
        try:
            os.makedirs(path, mode)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                exitstr = str("Unable to create directory {0}").format(path)
                noselog(exitstr)
                sys.exit(exitstr)

    def _rm_file(self, path):
        if os.path.isfile(path):
            os.remove(path)


#####
    def _set_OutputFilePath(self):
        rundata_outputdir = '%s/output/rundata/' % (self._performancetestsdir)
        self._mkdir_p(rundata_outputdir)
        self._outfilepath = '%spyomo_%s_%s_%s.out' % (rundata_outputdir,
                                                      self._modelname,
                                                      self._num, self._format)

    def _set_CSVFilePath(self):
        runtime_outputdir = '%s/output/runtime/' % (self._performancetestsdir)
        self._mkdir_p(runtime_outputdir)
        self._csvfilepath = '%spyomo_%s_%s_%s.csv' % (runtime_outputdir,
                                                      self._modelname,
                                                      self._num, self._format)

    def _set_ModelDataFilePath(self):
        modeldata_outputdir = '%s/output/rundata/' % (self._performancetestsdir)
        self._mkdir_p(modeldata_outputdir)
        self._modeldatafilepath = '%spyomo_%s_%s.%s' % (modeldata_outputdir,
                                                        self._modelname,
                                                        self._num, self._format)

#####

    # Nosetests when run sets the verbosity as defined here
    # nosetests -q <test>             : NOSE_VERBOSITY = 0  (quiet)
    # nosetests    <test>             : NOSE_VERBOSITY = 1  (normal)
    # nosetests -v <test>             : NOSE_VERBOSITY = 2  (verbose)
    # nosetests --verbosity=xx <test> : NOSE_VERBOSITY = xx (very verbose if xx > 2)

    def _is_nosetest_output_veryverbose(self):
        return (testglobals.NOSE_VERBOSITY > 2)

    def _is_nosetest_output_verbose(self):
        return (testglobals.NOSE_VERBOSITY >= 2)

    def _is_nosetest_output_normal(self):
        return (testglobals.NOSE_VERBOSITY == 1)

    def _is_nosetest_output_quiet(self):
        return (testglobals.NOSE_VERBOSITY == 0)

#####

    def _appendRunReportToFinalTestReport(self, reportstring):
        testglobals.packagerunreportlist.append(reportstring)

    def _appendSkipReportToFinalTestReport(self, reportstring):
        testglobals.packageskippedreportlist.append(reportstring)

####

    def _sumTotalRunTimes(self, runtime):
        testglobals.packagetotalruntime += runtime

####

    def _checkParamType(self, varname, vardata, datatype):
        caller = inspect.stack()[1][3]
        if not isinstance(vardata, datatype) :
            exitstr = str("TEST-ERROR: {0}() param {1} = {2} is a not a {3}; it is a {4}").format(caller, varname, vardata, datatype, type(vardata))
            sys.exit(exitstr)

################################################################################

def noselog(logmsg):
    # Nose allows writes to stderr to show up on the screenWrite to std err
    if isinstance(logmsg, str):
        sys.stderr.write(logmsg)
    if isinstance(logmsg, list):
        for logstr in logmsg:
            sys.stderr.write(logstr)

