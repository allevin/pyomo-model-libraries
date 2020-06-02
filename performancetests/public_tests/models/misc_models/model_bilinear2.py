#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright 2017 National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

from pyomo.environ import *

def create_test_model(size):
    N = size

    model = ConcreteModel()

    model.A = RangeSet(N)
    model.x = Var(model.A, bounds=(1,2))

    with nonlinear_expression() as expr:
        for i in model.A:
            if not (i+1) in model.A:
                continue
            expr += i*(model.x[i]*model.x[i+1]+1)
    model.obj = Objective(expr=expr)

    return model

def post_instance_processing(model_instance):
    pass