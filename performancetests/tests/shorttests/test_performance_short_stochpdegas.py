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
# Performance Tests for stochpdegas
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

@unittest.category('performance', 'short')
class Test_stochpdegas(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('dae_models')
        self.setTestModelName('run_stochpdegas1_automatic')
        self.setTestNum('0')
        self.setTestDataFileName("")
        self.setTestTimeout(60)

    def tearDown(self):
        pass

    @unittest.category('nl')
    def test_stochpdegas_nl(self):
        self.runPyomoModelTest('nl', scriptmode = True)

    @unittest.category('bar')
    def test_stochpdegas_bar(self):
        self.runPyomoModelTest('bar', scriptmode = True)

    @unittest.category('gms')
    def test_stochpdegas_gms(self):
        self.runPyomoModelTest('gms', scriptmode = True)

###

if __name__ == "__main__":
    unittest.main()


