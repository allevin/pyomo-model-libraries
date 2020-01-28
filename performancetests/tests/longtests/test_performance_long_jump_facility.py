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
    #noselog("SETUP TEST MODULE\n")
    pass

def teardown_module():
    #noselog("TEARDOWN TEST MODULE\n")
    pass

###

@unittest.category('performance', 'long')
class Test_jump_facility25(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('jump_models')
        self.setTestModelName('facility25')
        self.setTestNum('25')
        self.setTestDataFileName("")
        self.setTestTimeout(60)

    def tearDown(self):
        pass

    @unittest.category('lp')
    def testjump_facility25_lp(self):
        self.runPyomoModelTest('lp')

    @unittest.category('nl')
    def testjump_facility25_nl(self):
        self.runPyomoModelTest('nl')

    @unittest.category('bar')
    def test_jump_facility25_bar(self):
        self.runPyomoModelTest('bar')

    @unittest.category('gms')
    def test_jump_facility25_gms(self):
        self.runPyomoModelTest('gms')

###

@unittest.category('performance', 'long')
class Test_jump_facility25_quick(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('jump_models')
        self.setTestModelName('facility25_quick')
        self.setTestNum('25')
        self.setTestDataFileName("")
        self.setTestTimeout(60)

    def tearDown(self):
        pass

    @unittest.category('lp')
    def test_jump_facility25_quick_lp(self):
        self.runPyomoModelTest('lp')

    @unittest.category('nl')
    def test_jump_facility25_quick_nl(self):
        self.runPyomoModelTest('nl')

    @unittest.category('bar')
    def test_jump_facility25_quick_bar(self):
        self.runPyomoModelTest('bar')

    @unittest.category('gms')
    def test_jump_facility25_quick_gms(self):
        self.runPyomoModelTest('gms')

###

if __name__ == "__main__":
    unittest.main()


