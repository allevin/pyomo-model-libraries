#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright 2017 National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

# Global variables used for the testing system
# This function will set them, and make them available
def accessTestGlobals():
    global NOSE_VERBOSITY
    global packagerunreportlist
    global packageskippedreportlist
    global packagetotalruntime
    global pyomo_sha

    NOSE_VERBOSITY = 0
    packagerunreportlist = []
    packageskippedreportlist = []
    packagetotalruntime = 0
    pyomo_sha = "Undefined"

