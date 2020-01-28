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
### #######################################################################

@unittest.category('performance', 'short')
class Test_bilinear1_100(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('misc_models')
        self.setTestModelName('model_bilinear1_100')
        self.setTestNum('100')
        self.setTestDataFileName("")

    def tearDown(self):
        pass

    @unittest.category('bar', 'gms', 'nl', 'lp')
    def test_bilinear1_100_bar(self):

        m = self.CreateModelInstance()
        self.capture_performance_result_time("Model Declaration")

        self.WriteModelInstance(m, 'bar')
        self.capture_performance_result_time("Write bar")

        self.WriteModelInstance(m, 'gms')
        self.capture_performance_result_time("Write gms")

        self.WriteModelInstance(m, 'nl')
        self.capture_performance_result_time("Write nl")

        self.WriteModelInstance(m, 'lp')
        self.capture_performance_result_time("Write lp")

###

@unittest.category('performance', 'short')
class Test_bilinear2_100(PerformanceTestCase):

    def setUp(self):
        self.setTestModelDir('misc_models')
        self.setTestModelName('model_bilinear2_100')
        self.setTestNum('100')
        self.setTestDataFileName("")

    def tearDown(self):
        pass

    @unittest.category('bar', 'gms', 'nl', 'lp')
    def test_bilinear2_100_bar(self):

        m = self.CreateModelInstance()
        self.capture_performance_result_time("Model Declaration")

        self.WriteModelInstance(m, 'bar')
        self.capture_performance_result_time("Write bar")

        self.WriteModelInstance(m, 'gms')
        self.capture_performance_result_time("Write gms")

        self.WriteModelInstance(m, 'nl')
        self.capture_performance_result_time("Write nl")

        self.WriteModelInstance(m, 'lp')
        self.capture_performance_result_time("Write lp")

###

if __name__ == "__main__":
    unittest.main()


