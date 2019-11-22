#
#  ___________________________________________________________________________
#  Pyomo: Python Optimization Modeling Objects
#  Copyright 2017 National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and 
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain 
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

import sys
import os

def _find_packages(path):
    """
    Generate a list of nested packages
    """
    pkg_list = []
    if not os.path.exists(path):
        return []
    if not os.path.exists(path+os.sep+"__init__.py"):
        return []
    else:
        pkg_list.append(path)
    for root, dirs, files in os.walk(path, topdown=True):
        if root in pkg_list and "__init__.py" in files:
            for name in dirs:
                if os.path.exists(root+os.sep+name+os.sep+"__init__.py"):
                    pkg_list.append(root+os.sep+name)
    return [pkg for pkg in map(lambda x:x.replace(os.sep, "."), pkg_list)]

packages = _find_packages('performancetests')

from setuptools import setup

requires = [
    'pyomo',
    ]

if sys.version_info < (2, 7):
    requires.append('argparse')
    requires.append('unittest2')
    requires.append('ordereddict')
    

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as README:
    README=README.read()

setup(name='Pyomo Performance Tests',
  maintainer='Aaron Levine and Miranda Mundt',
  maintainer_email='allevin@sandia.gov and mmundt@sandia.gov',
  license='BSD',
  platforms=["Linux", "Darwin"],
  description='Performance Testing for Pyomo: Python Optimization Modeling Objects',
  long_description=README,
  long_description_content_type='text/markdown',
  packages=packages,
  package_data={'performancetests': ['models/pmedian/*.dat','models/misc/*.dat','models/jump/*','models/dae/*.dat']},
  keywords=['pyomo','performance','testing'],
  install_requires=requires,
  python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
  entry_points="""
    [console_scripts]
    pyomo-performance=performancetests.support.performance_main:main_performance_script
    pyomo-analyze=performancetests.support.performance_analyze:main_analysis_script
  """
#      pyomo-plot=performancetests.support.performance_plot:main_plot_script ##TOBEADDED
    )
    