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
class Test_bilinear1_100000(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('misc_models')
        self.setTestModelName('bilinear1_100000')
        self.setTestNum('100000')
        self.setTestDataFileName("")
        self.setTestTimeout(60)

    def tearDown(self):
        pass

    @unittest.category('lp')
    def test_bilinear1_100000_lp(self):
        self.runPyomoModelTest('lp')

    @unittest.category('nl')
    def test_bilinear1_100000_nl(self):
        self.runPyomoModelTest('nl')

    @unittest.category('bar')
    def test_bilinear1_100000_bar(self):
        self.runPyomoModelTest('bar')

    @unittest.category('gms')
    def test_bilinear1_100000_gms(self):
        self.runPyomoModelTest('gms')

###

#@unittest.category('performance', 'long')
#class Test_bilinear2_100000(PerformanceTestCase):
#
#    def setUp(self):
#        self.setTestModelDir('misc_models')
#        self.setTestModelName('bilinear2_100000')
#        self.setTestNum('100000')
#        self.setTestDataFileName("")
#        self.setTestTimeout(60)
#
#    def tearDown(self):
#        pass
#
#    @unittest.category('lp')
#    def test_bilinear2_100000_lp(self):
#        self.runPyomoModelTest('lp')
#
#    @unittest.category('nl')
#    def test_bilinear2_100000_nl(self):
#        self.runPyomoModelTest('nl')
#
#    @unittest.category('bar')
#    def test_bilinear2_100000_bar(self):
#        self.runPyomoModelTest('bar')
#
#    @unittest.category('gms')
#    def test_bilinear2_100000_gms(self):
#        self.runPyomoModelTest('gms')

###

if __name__ == "__main__":
    unittest.main()


