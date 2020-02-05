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
# Performance Tests for clnlbeam
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
class Test_jump_clnlbeam_5000(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('jump_models')
        self.setTestModelName('model_clnlbeam')
        self.setTestSize(5000)
        self.setTestDataFileName("clnlbeam-5000.dat")

    def tearDown(self):
        self.writeTestTimingResults()

    @unittest.category('bar', 'gms', 'nl', 'lp')
    def test_jump_clnbeam_5000(self):

        m = self.createModelInstance()
        self.capturePerformanceResultTime("Model Declaration")

        # NOTEL bar is not testable - model_clnbeam does not support unary function sin
        #self.writeModelInstance(m, 'bar')
        #self.capturePerformanceResultTime("Write bar")

        self.writeModelInstance(m, 'gms')
        self.capturePerformanceResultTime("Write gms")

        self.writeModelInstance(m, 'nl')
        self.capturePerformanceResultTime("Write nl")

###

if __name__ == "__main__":
    unittest.main()


