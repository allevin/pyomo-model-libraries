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
# Performance Tests for bilinear
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

@unittest.category('performance', 'short')
class Test_bilinear1_100(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('misc_models')
        self.setTestModelName('model_bilinear1')
        self.setTestSize(100)
        self.setTestDataFileName("")

    def tearDown(self):
        self.writeTestTimingResults()

    @unittest.category('bar', 'gms', 'nl', 'lp')
    def test_bilinear1_100(self):

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

@unittest.category('performance', 'short')
class Test_bilinear2_100(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('misc_models')
        self.setTestModelName('model_bilinear2')
        self.setTestSize(100)
        self.setTestDataFileName("")

    def tearDown(self):
        self.writeTestTimingResults()

    @unittest.category('bar', 'gms', 'nl', 'lp')
    def test_bilinear2_100(self):

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


