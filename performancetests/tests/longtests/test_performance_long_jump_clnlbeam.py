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

from performancetests.support.testsupport import *

###

def setup_module():
    #noselog("SETUP TEST MODULE\n")
    pass

def teardown_module():
    #noselog("TEARDOWN TEST MODULE\n")
    pass

###

@unittest.category('performance', 'long')
class Test_clnlbeam_50000(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('jump_models')
        self.setTestModelName('clnlbeam')
        self.setTestNum('50000')
        self.setTestDataFileName("clnlbeam-50000.dat")
        self.setTestTimeout(60)

    def tearDown(self):
        pass

    @unittest.category('nl')
    def test_clnlbeam_50000_nl(self):
        self.runPyomoModelTest('nl')

    @unittest.category('bar')
    def test_clnlbeam_50000_bar(self):
        self.skipThisTest("jump_clnlbeam_50000_bar is not testable - does not support unary function sin")
        self.runPyomoModelTest('bar')

    @unittest.category('gms')
    def test_clnlbeam_50000_gms(self):
        self.runPyomoModelTest('gms')

###

if __name__ == "__main__":
    unittest.main()


