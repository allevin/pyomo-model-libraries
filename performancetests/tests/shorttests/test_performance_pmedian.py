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
class Test_pmedian1_4(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('pmedian_models')
        self.setTestModelName('pmedian1')
        self.setTestNum('4')
        self.setTestDataFileName("pmedian.test4.dat")

        self.setTestTimeout(60)

    def tearDown(self):
        pass

    @unittest.category('lp')
    def test_pmedian1_4_lp(self):
        self.runPyomoModelTest('lp')

    @unittest.category('nl')
    def test_pmedian1_4_nl(self):
        self.runPyomoModelTest('nl')

    @unittest.category('bar')
    def test_pmedian1_4_bar(self):
        self.runPyomoModelTest('bar')

    @unittest.category('gms')
    def test_pmedian1_4_gms(self):
        self.runPyomoModelTest('gms')

###

@unittest.category('performance', 'short')
class Test_pmedian2_4(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('pmedian_models')
        self.setTestModelName('pmedian2')
        self.setTestNum('4')
        self.setTestDataFileName("pmedian.test4.dat")

        self.setTestTimeout(60)

    def tearDown(self):
        pass

    @unittest.category('lp')
    def test_pmedian2_4_lp(self):
        self.runPyomoModelTest('lp')

    @unittest.category('nl')
    def test_pmedian2_4_nl(self):
        self.runPyomoModelTest('nl')

    @unittest.category('bar')
    def test_pmedian2_4_bar(self):
        self.runPyomoModelTest('bar')

    @unittest.category('gms')
    def test_pmedian2_4_gms(self):
        self.runPyomoModelTest('gms')

###

if __name__ == "__main__":
    unittest.main()


