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
import inspect
import nose
import pyomo
from performancetests.support import testglobals
from performancetests.support import testsupport
from performancetests.support.testsupport import *

def setup_package():
    testglobals.accessTestGlobals()
    testglobals.NOSE_VERBOSITY = get_package_nosetest_verbosity()
    noselog_debug('NOSE_VERBOSENESS = %s\n' % str(testglobals.NOSE_VERBOSITY))

    noselog_debug('SETUP NOSE PACKAGE\n')
    testglobals.packagerunreportlist = []
    testglobals.packageskippedreportlist = []
    testglobals.packagetotalruntime = 0
    testglobals.pyomo_sha = _get_pyomo_sha()
    noselog_debug('PYOMO SHA = %s\n\n' % str(testglobals.pyomo_sha))

def teardown_package():
    noselog_debug('TEARDOWN NOSE PACKAGE\n')
    if is_nosetest_output_verbose() or is_nosetest_output_normal():
        noselog('\n', OVERRIDE_NORMAL_OUTPUT)
        if len(testglobals.packageskippedreportlist) > 0:
            noselog('Skipped Tests:\n', OVERRIDE_NORMAL_OUTPUT)
            noselog(testglobals.packageskippedreportlist)

        noselog('\nPerformance Testing Report:\n', OVERRIDE_NORMAL_OUTPUT)
        noselog(testglobals.packagerunreportlist, OVERRIDE_NORMAL_OUTPUT)

        report = str(('\nTotal Runtime for all tests ') +
                      ('= %f seconds\n') % testglobals.packagetotalruntime)
        noselog(report, OVERRIDE_NORMAL_OUTPUT)
    pass

################################################################################

def get_package_nosetest_verbosity():
    """ Return the verbosity setting of the currently running nosetest
        0 - Quite (-q)
        1 - Normal
        2 - Verbose (-v)
        3+ - Debugging levels of Nosetest
    """
    runner = _get_package_nosetest_texttestrunner_class()
    if runner != None:
        return runner.verbosity
    else:
        return 0;

###

def _get_package_nosetest_texttestresult_class():
    """ Return the nosetests texttestresult running tests
    """
    runner = _get_package_nosetest_texttestrunner_class()
    if runner != None:
        return runner.resultclass
    else:
        return None;

###

def _get_package_nosetest_texttestrunner_class():
    """ Return the nosetests testrunner class we do this by searching
        upwards in the frames for the nose.core.TextTestRunner.
    """
    frame = inspect.currentframe()
    while frame:
        self = frame.f_locals.get('self')
        #noselog_debug(str('frame = {0}\n').format(self))
        if isinstance(self, nose.core.TextTestRunner):
            #noselog_debug(str('TextTestRunner attr = {0}\n').format(dir(self)))
            return self
        frame = frame.f_back
    return None

####

def _get_pyomo_sha(): # Retrieves the SHA for the pyomo directory
    sha = 'Undefined'
    pydir = os.path.dirname(pyomo.__file__)
    if os.path.isdir(pydir):
        os.chdir(pydir)
        dir_origin = os.popen('git config --get remote.origin.url').read()
        if 'github.com/Pyomo' in dir_origin:
            tsha = os.popen('git rev-parse --short HEAD').read()
            sha = tsha.replace('\n','')
    return sha


