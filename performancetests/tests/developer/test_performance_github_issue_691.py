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
# Performance Test Case: Github Issue 691
# Link to issue: https://github.com/Pyomo/pyomo/issues/691
# Originally reported by osarwar (Owais from CMU, through Qi Chen)
# Slight changes to match testing naming convention
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
    
@unittest.category('performance', 'developer')
class Test_osarwar_github_issue(PerformanceTestCase):
    
    def setUp(self):
        self.setTestModelDir('devel_models')
        self.setTestModelName('osarwar_github_issue_691')
        self.setTestNum('1000')
        self.setTestDataFileName("")
        self.setTestTimeout(60)
        
    def tearDown(self):
        pass
    
    @unittest.category('lp')
    def test_osarwar_github_issue_691_lp(self):
        self.runPyomoModelTest('lp')
        
    @unittest.category('nl')
    def test_osarwar_github_issue_691_nl(self):
        self.runPyomoModelTest('nl')
        
    @unittest.category('bar')
    def test_osarwar_github_issue_691_bar(self):
        self.runPyomoModelTest('bar')
        
    @unittest.category('gms')
    def test_osarwar_github_issue_691_gms(self):
        self.runPyomoModelTest('gms')
        
###
        
if __name__ == "__main__":
    unittest.main()