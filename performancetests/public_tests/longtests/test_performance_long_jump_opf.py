#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright 2017 National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

#
# Performance Tests for jump_opf
#

from performancetests.support.testsupport import *

###

def setup_module():
    #noselog_debug("SETUP TEST MODULE\n")
    pass

def teardown_module():
    #noselog_debug("TEARDOWN TEST MODULE\n")
    pass

################################################################################

@unittest.category('performance', 'long')
class Test_jump_opf_bus_6620(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir(self.getTopTestingDir() + '/public_tests/models/jump_models')
        self.setTestModelName('model_opf_bus')
        self.setTestSize(6620)
        self.setTestDataFileName("")

    def tearDown(self):
        self.writeTestTimingResults()

    @unittest.category('gms', 'nl')
    def test_jump_opf_bus_6620(self):

        m = self.createModelInstance()
        self.capturePerformanceResultTime("Model Declaration")

        # NOTEL bar is not testable - model_opf_bus does not support unary function cos
        #self.writeModelInstance(m, 'bar')
        #self.capturePerformanceResultTime("Write bar")

        self.writeModelInstance(m, 'gms')
        self.capturePerformanceResultTime("Write gms")

        self.writeModelInstance(m, 'nl')
        self.capturePerformanceResultTime("Write nl")

        # NOTE: lp is not testable - model_opf_bus cannot write legal LP file
        #self.writeModelInstance(m, 'lp')
        #self.capturePerformanceResultTime("Write lp")

###

@unittest.category('performance', 'long')
class Test_jump_opf_bus_quick_6620(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir(self.getTopTestingDir() + '/public_tests/models/jump_models')
        self.setTestModelName('model_opf_bus_quick')
        self.setTestSize(6620)
        self.setTestDataFileName("")

    def tearDown(self):
        self.writeTestTimingResults()

    @unittest.category('gms', 'nl')
    def test_jump_opf_bus_quick_6620(self):

        m = self.createModelInstance()
        self.capturePerformanceResultTime("Model Declaration")

        # NOTEL bar is not testable - model_opf_bus_quick does not support unary function cos
        #self.writeModelInstance(m, 'bar')
        #self.capturePerformanceResultTime("Write bar")

        self.writeModelInstance(m, 'gms')
        self.capturePerformanceResultTime("Write gms")

        self.writeModelInstance(m, 'nl')
        self.capturePerformanceResultTime("Write nl")

        # NOTE: lp is not testable - model_opf_bus_quick cannot write legal LP file
        #self.writeModelInstance(m, 'lp')
        #self.capturePerformanceResultTime("Write lp")
###

if __name__ == "__main__":
    unittest.main()

