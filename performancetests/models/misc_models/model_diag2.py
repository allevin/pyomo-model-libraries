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
    model.x = Var(model.A)

    expr = quicksum(i*model.x[i] for i in model.A)
    model.obj = Objective(expr=expr)

    def c_rule(model, i):
        return (N-i+1)*model.x[i] >= N
    model.c = Constraint(model.A)

    return model

def post_instance_processing(model_instance):
    pass