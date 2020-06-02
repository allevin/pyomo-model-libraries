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
import csv
import gc
import errno
import inspect
import datetime
import pyutilib.th as unittest
import pyutilib.misc.timing as timing
import pyutilib.misc.import_file as import_file
from performancetests.support import testglobals

from pyomo.core.base.PyomoModel import *

# Nosetests when run sets the verbosity as defined here
# nosetests -q <test>             : NOSE_VERBOSITY = 0  (quiet)
# nosetests    <test>             : NOSE_VERBOSITY = 1  (normal)
# nosetests -v <test>             : NOSE_VERBOSITY = 2  (verbose)
# nosetests --verbosity=xx <test> : NOSE_VERBOSITY = xx (very verbose if xx > 2)
NOSE_OUTPUT_QUIET   = 0
NOSE_OUTPUT_NORMAL  = 1
NOSE_OUTPUT_VERBOSE = 2
OVERRIDE_NORMAL_OUTPUT = True

################################################################################

class PerformanceTestCase(unittest.TestCase):

    def __init__(self, methodName):
        super(PerformanceTestCase, self).__init__(methodName)

        # Nose calls this module in unexpected ways... We therefore need
        # to init the member variables with something, the actual tests
        # will populate with reasonable data for the test runs

        # Find the top level 'performancetests' directory
        thisdir = os.path.dirname(__file__)
        self._performancetestsdir = os.path.abspath(os.path.join(thisdir, os.pardir))
        if os.path.basename(self._performancetestsdir) != 'performancetests':
            exitstr = str(('TEST-ERROR: Cannot Find Main performance tests ') +
                          ('directory named "performancetests" in path %s\n') % thisdir)
            sys.exit(exitstr)

        self._skippingtest = False
        self._skippingreason = ''
        self._modelname = 'Undefined_Model'
        self._testsize = 1
        self._modeldir = 'Undefined_Dir'
        self._csvfilepath = ''
        self._modelwriteoutputfilepath = ''
        self._datafilename = ''
        self._outputformat  = 'lp'
        self._runtimeinfo = {}
        self._runtestcmd = ''
        self._timestamp = ''
        self._createdtestmodelinstance = None
        self._testmodelfilepath = ''
        self._testdatafilepath = ''
        self._testTimer = timing.TicTocTimer()
        self._totalRuntimeTimer = timing.TicTocTimer()

################################################################################
# TOP LEVEL FUNCTIONS CALLED BY THE TESTS

    def initializeTestTimer(self):
        self._testTimer.tic('')
        self._totalRuntimeTimer.tic('')

###

    def createModelInstance(self):
        self._initTestingInfo()

        # Make sure user is not creating another instance
        errmsg = str(('TEST-ERROR: Cannot Create Model Instance - A Model has ') +
                     ('previously been created for this test'))
        self.assertEquals(self._createdtestmodelinstance, None, msg = errmsg)

        # Using pyutilib to import the test model file
        loaded_module = import_file(self._testmodelfilepath)

        # cd to the model directory
        savedcwd = os.getcwd()
        os.chdir(self._modeldir)

        noselog_debug('\nModel Create %s (%d)...\n' % (self._modelname, self._testsize))

        model = loaded_module.create_test_model(size=self._testsize)

        # Now instantiate the model if it is abstract
        if isinstance(model, AbstractModel):
            noselog_debug('MODEL IS ABSTRACT - CREATING INSTANCE\n')
            model = model.create_instance(self._testdatafilepath)
        else:
            noselog_debug('MODEL IS CONCRETE - INSTANCE ALREADY CREATED\n')

        # Perform any post instance processing / setup (if the function exists)
        loaded_module.post_instance_processing(model_instance=model)

        # Restore the saved directory
        os.chdir(savedcwd)

        self._createdtestmodelinstance = model
        return model

###

    def writeModelInstance(self, model, outputFormat):
        self._checkParamType('model', model, ConcreteModel)
        self._checkParamType('outputformat', outputFormat, str)
        self._outputformat = outputFormat

        self._set_CSVFilePath()
        self._set_ModelWriteOutputFilePath()

        errmsg = str(('TEST-ERROR: Cannot Write Model - A Model has ') +
                     ('not been instantiated for this test'))
        self.assertNotEqual(self._createdtestmodelinstance, None, msg = errmsg)

        noselog_debug('Writing Model %s...\n' % self._outputformat)

        model.write('%s' % (self._modelwriteoutputfilepath))

        # Unless we are in a very verbose mode, delete the output
        if not is_nosetest_output_veryverbose():
            self._rm_file(self._modelwriteoutputfilepath)

###

    def capturePerformanceResultTime(self, performance_result_name):
        self._checkParamType('performance_result_name',
                             performance_result_name, str)

        # Print out an indicator of the sub-test progress
        if is_nosetest_output_verbose() or is_nosetest_output_normal():
            noselog('+', OVERRIDE_NORMAL_OUTPUT)

        deltatime = self._testTimer.toc('')
        self._runtimeinfo[performance_result_name] = deltatime
        noselog_debug('%s Time = %s\n' % (performance_result_name, deltatime))

        # Build a report string
        reportstring = '%s_%d (%s) = %f' % (self._modelname,
                                            self._testsize,
                                            performance_result_name,
                                            deltatime) + '\n'
        self._appendRunReportToFinalTestReport(reportstring)

###

    def writeTestTimingResults(self):
        if self._skippingtest == True:
            return 0

        deltatime = self._totalRuntimeTimer.toc('')
        self._runtimeinfo['totalruntime'] = deltatime
        # Build a report string
        reportstring = '%s_%d --%s-- = %f' % (self._modelname,
                                            self._testsize,
                                            'Total Runtime',
                                            deltatime) + '\n\n'
        self._appendRunReportToFinalTestReport(reportstring)
        self._addTotalRunTimeToPackageTIme(deltatime)
        self._save_timing_data_in_csv()

###

    def setTestModelDir(self, dir):
        self._checkParamType('dir', dir, str)
        modeldir = dir
        # If the path does not exist, then try to use our model path
        if not os.path.isdir(modeldir):
            topmodeldir = self.getTopTestingDir() + '/models/'
            secondarymodeldir = '%s%s' % (topmodeldir, dir)
            if not os.path.isdir(secondarymodeldir):
                exitstr = str(('TEST-ERROR: setTestModelDir() - Directory {0} does ') +
                               ('not exist; nor is it under {1}').format(dir, topmodeldir))
                sys.exit(exitstr)
            modeldir = secondarymodeldir
        self._modeldir = modeldir

###

    def setTestModelName(self, modelName):
        self._checkParamType('modelName', modelName, str)
        self._modelname = modelName

###

    def setTestDataFileName(self, dataFileName):
        self._checkParamType('dataFileName', dataFileName, str)
        self._datafilename = dataFileName

###

    def setTestSize(self, testSize):
        self._checkParamType('testSize', testSize, int)
        self._testsize = testSize

###

    def getTopTestingDir(self):
        return self._performancetestsdir

###

    # Skip the Test, This provides some feedback to the user that the test was skipped
    def skipThisTest(self, skipReason):
        self._checkParamType("skipReason", skipReason, str)
        self._skippingtest = True
        self._skippingreason = skipReason
        reportstring = "%s (%d) - Reason: %s" % (self._modelname, self._testsize, self._skippingreason) + "\n"
        self._appendSkipReportToFinalTestReport(reportstring)
        # NOTE: The skipTest call MUST come at the end of this method
        self.skipTest(skipReason)

################################################################################

    def _initTestingInfo(self):
        # Start Garbage Collection
        gc.collect()

        self._timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.initializeTestTimer()

        # Figure out the path to the python test model to run
        self._testmodelfilepath = '%s/%s.py' % (self._modeldir, self._modelname)
        if not os.path.isfile(self._testmodelfilepath):
            exitstr = str(('TEST-ERROR: Cannot find path ') +
                          ('to model file at {0}').format(self._testmodelfilepath))
            sys.exit(exitstr)

        # Figure out the path to the data file (if it is defined)
        if self._datafilename != '':
            self._testdatafilepath = '%s/%s' % (self._modeldir, self._datafilename)
            if not os.path.isfile(self._testdatafilepath):
                exitstr = str(('TEST-ERROR: Cannot find path ') +
                             ('to data file at {0}').format(self._testdatafilepath))
                sys.exit(exitstr)
        else:
            self._testdatafilepath = ''


#####

    # Save the Pyomo run timings into a csv file
    def _save_timing_data_in_csv(self):
        python_v = (str(sys.version_info.major) + '.' +
                    str(sys.version_info.minor) + '.' +
                    str(sys.version_info.micro))
        self._runtimeinfo['timestamp'] = self._timestamp
        self._runtimeinfo['python_version'] = python_v
        self._runtimeinfo['commit_info'] = testglobals.pyomo_sha
        csv_columns = self._runtimeinfo.keys()

        if self._csvfilepath == '':
            return

        with open(self._csvfilepath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            writer.writerow(self._runtimeinfo)

#####

    def _rm_file(self, path):
        if os.path.isfile(path):
            os.remove(path)

    def _mkdir_p(self, path, mode=777):
        try:
            os.makedirs(path, mode)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                exitstr = str('Unable to create directory {0}').format(path)
                noselog(exitstr, OVERRIDE_NORMAL_OUTPUT)
                sys.exit(exitstr)

#####

    def _set_CSVFilePath(self):
        runtime_outputdir = '%s/output/runtime/' % (self._performancetestsdir)
        self._mkdir_p(runtime_outputdir)
        self._csvfilepath = '%spyomo_%s_%d.csv' % (runtime_outputdir,
                                                   self._modelname,
                                                   self._testsize)

    def _set_ModelWriteOutputFilePath(self):
        modeldata_outputdir = '%s/output/rundata/' % (self._performancetestsdir)
        self._mkdir_p(modeldata_outputdir)
        self._modelwriteoutputfilepath = '%spyomo_%s_%d.%s' % (modeldata_outputdir,
                                                               self._modelname,
                                                               self._testsize,
                                                               self._outputformat)

#####

    def _appendRunReportToFinalTestReport(self, reportstring):
        testglobals.packagerunreportlist.append(reportstring)

    def _appendSkipReportToFinalTestReport(self, reportstring):
        testglobals.packageskippedreportlist.append(reportstring)

    def _addTotalRunTimeToPackageTIme(self, RunTime):
        testglobals.packagetotalruntime += RunTime

####

    def _checkParamType(self, varname, vardata, datatype):
        caller = inspect.stack()[1][3]
        if not isinstance(vardata, datatype) :
            exitstr = str(('TEST-ERROR: Function {0}() param {1} = {2} is a ') +
                          ('not a {3}; it is a {4}')).format(caller, varname,
                                                             vardata, datatype,
                                                             type(vardata))
            sys.exit(exitstr)

################################################################################
# Global support routines

def is_nosetest_output_veryverbose():
    return (testglobals.NOSE_VERBOSITY > NOSE_OUTPUT_VERBOSE)

def is_nosetest_output_verbose():
    return (testglobals.NOSE_VERBOSITY >= NOSE_OUTPUT_VERBOSE)

def is_nosetest_output_normal():
    return (testglobals.NOSE_VERBOSITY == NOSE_OUTPUT_NORMAL)

def is_nosetest_output_quiet():
    return (testglobals.NOSE_VERBOSITY == NOSE_OUTPUT_QUIET)

###

def noselog(logmsg, override_normal_mode = False):
    # Check to see if we are in quiet mode
    if is_nosetest_output_quiet():
        return

    # Check to see if we are supposed to output the log
    if is_nosetest_output_verbose() or override_normal_mode:
        # Nose allows writes to stderr to show up on the screenWrite to std err
        if isinstance(logmsg, str):
            sys.stderr.write(logmsg)
        if isinstance(logmsg, list):
            for logstr in logmsg:
                sys.stderr.write(logstr)
###

def noselog_debug(logmsg):
    if is_nosetest_output_veryverbose():
        logmsg = 'DEBUG: ' + logmsg
        noselog(logmsg, override_normal_mode = True)


def initTestModule():
    noselog_debug("initTestModule()\n")

def finalizeTestModuleResults():
    noselog_debug("finalizeTestModuleResults()\n")
