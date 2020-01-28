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
    #noselog("SETUP TEST MODULE\n")
    pass

def teardown_module():
    #noselog("TEARDOWN TEST MODULE\n")
    pass

###

@unittest.category('performance', 'short')
class Test_jump_opf_662bus(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('jump_models')
        self.setTestModelName('opf_662bus')
        self.setTestNum('662')
        self.setTestDataFileName("")
        self.setTestTimeout(60)

    def tearDown(self):
        pass

    @unittest.category('nl')
    def test_jump_opf_662bus_nl(self):
        self.runPyomoModelTest('nl')

    @unittest.category('bar')
    def test_jump_opf_662bus_bar(self):
        self.skipThisTest("jump_ofp_662bus_bar is not testable - does not support unary function cos")
        self.runPyomoModelTest('bar')

    @unittest.category('gms')
    def test_jump_opf_662bus_gms(self):
        self.runPyomoModelTest('gms')

###

@unittest.category('performance', 'short')
class Test_jump_opf_662bus_quick(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('jump_models')
        self.setTestModelName('opf_662bus_quick')
        self.setTestNum('662')
        self.setTestDataFileName("")
        self.setTestTimeout(60)

    def tearDown(self):
        pass

    @unittest.category('nl')
    def test_jump_opf_662bus_quick_nl(self):
        self.runPyomoModelTest('nl')

    @unittest.category('bar')
    def test_jump_opf_662bus_quick_bar(self):
        self.skipThisTest("jump_ofp_662bus_quick_bar is not testable - does not support unary function cos")
        self.runPyomoModelTest('bar')

    @unittest.category('gms')
    def test_jump_opf_662bus_quick_gms(self):
        self.runPyomoModelTest('gms')

###

if __name__ == "__main__":
    unittest.main()


