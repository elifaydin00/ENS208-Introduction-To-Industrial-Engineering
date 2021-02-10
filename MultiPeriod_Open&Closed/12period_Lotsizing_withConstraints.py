from gurobipy import GRB, Model

demand = [0, 10, 62, 12, 130, 154, 129, 88, 52, 124, 160, 238, 41]
p = 5
h = 0.4
f = 54

m = Model('12-period-lotsizing')

x = m.addVars(range(1,13), vtype=GRB.CONTINUOUS, name='x')
y = m.addVars(range(1,13), vtype=GRB.BINARY, name='y')
I = m.addVars(range(0,13), vtype=GRB.CONTINUOUS, name='I')

#constraints for stock control and demand satisfaction
m.addConstrs((I[t-1] + x[t] == demand[t] + I[t]) for t in range(1,13))
m.addConstr(I[0] == 0) #no beginning inventory

#constraints to determine how to handle the fixed cost
m.addConstrs((x[t] <= 1200 * y[t]) for t in range(1,13))

#m.addConstrs(x[t] <= 160 for t in range(1,13))
#m.addConstrs(I[t] <= 80 for t in range(1,13))
# m.addConstr(y.sum() <= 6)
#m.addConstr(sum(y[t] for t in range(1,13)) <= 6)
# m.addConstrs(x[t] <= 240 for t in range(1,13))
# m.addConstrs(I[t] <= 120 for t in range(1,13))


m.setObjective(p * x.sum() + f * y.sum() +
               h * I.sum(), GRB.MINIMIZE)

m.optimize()


for v in m.getVars():
    print(v.varName, v.x)

print('The optimal objective function value is', m.objVal)