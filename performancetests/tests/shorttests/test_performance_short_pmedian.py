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
# Performance Tests for pmedian
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
class Test_pmedian1_4(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('pmedian_models')
        self.setTestModelName('model_pmedian1')
        self.setTestSize(8)
        self.setTestDataFileName("pmedian.test8.dat")

    def tearDown(self):
        self.writeTestTimingResults()

    @unittest.category('bar', 'gms', 'nl', 'lp')
    def test_pmedian1_4(self):

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
class Test_pmedian2_4(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('pmedian_models')
        self.setTestModelName('model_pmedian2')
        self.setTestSize(4)
        self.setTestDataFileName("pmedian.test4.dat")

    def tearDown(self):
        self.writeTestTimingResults()

    @unittest.category('bar', 'gms', 'nl', 'lp')
    def test_pmedian1_4(self):

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


