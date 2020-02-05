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
# Performance Tests for diag
#

from performancetests.support.testsupport_new import *

###

def setup_module():
    #noselog_debug("SETUP TEST MODULE\n")
    pass

def teardown_module():
    #noselog_debug("TEARDOWN TEST MODULE\n")
    pass

################################################################################

@unittest.category('performance', 'long')
class Test_diag1_1000000(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('misc_models')
        self.setTestModelName('model_diag1')
        self.setTestSize(1000000)
        self.setTestDataFileName("")

    def tearDown(self):
        self.writeTestTimingResults()

    @unittest.category('bar', 'gms', 'nl', 'lp')
    def test_diag1_1000000(self):

        m = self.createModelInstance()
        self.capturePerformanceResultTime("Model Declaration")

        self.writeModelInstance(m, 'bar')
        self.capturePerformanceResultTime("Write bar")

        self.writeModelInstance(m, 'gms')
        self.capturePerformanceResultTime("Write gms")

        self.writeModelInstance(m, 'nl')
        self.capturePerformanceResultTime("Write nl")

        self.writeModelInstance(m, 'lp')
        self.capturePerformanceResultTime("Write lp")

###

@unittest.category('performance', 'long')
class Test_diag2_1000000(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('misc_models')
        self.setTestModelName('model_diag2')
        self.setTestSize(1000000)
        self.setTestDataFileName("")

    def tearDown(self):
        self.writeTestTimingResults()

    @unittest.category('bar', 'gms', 'nl', 'lp')
    def test_diag2_1000000(self):

        m = self.createModelInstance()
        self.capturePerformanceResultTime("Model Declaration")

        self.writeModelInstance(m, 'bar')
        self.capturePerformanceResultTime("Write bar")

        self.writeModelInstance(m, 'gms')
        self.capturePerformanceResultTime("Write gms")

        self.writeModelInstance(m, 'nl')
        self.capturePerformanceResultTime("Write nl")

        self.writeModelInstance(m, 'lp')
        self.capturePerformanceResultTime("Write lp")

###

if __name__ == "__main__":
    unittest.main()

