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
# Performance Tests for jump_facility
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
class Test_jump_facility_25(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('jump_models')
        self.setTestModelName('model_facility')
        self.setTestSize(25)
        self.setTestDataFileName("data-facility-25.dat")

    def tearDown(self):
        self.writeTestTimingResults()

    @unittest.category('bar', 'gms', 'nl', 'lp')
    def test_jump_facility_25(self):

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
class Test_jump_facility_quick_25(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('jump_models')
        self.setTestModelName('model_facility_quick')
        self.setTestSize(25)
        self.setTestDataFileName("data-facility-25.dat")

    def tearDown(self):
        self.writeTestTimingResults()

    @unittest.category('bar', 'gms', 'nl', 'lp')
    def test_jump_facility_quick_25(self):

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

