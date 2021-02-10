from gurobipy import GRB, Model

demand = [0, 52, 87, 23, 56]
p = 9
h = 1
f = 75

m = Model('4period-lotsizing-closed')

#variables for order/production size
#x1 = m.addVar(vtype=GRB.CONTINUOUS, name='x1')
#x2 = m.addVar(vtype=GRB.CONTINUOUS, name='x2')
#x3 = m.addVar(vtype=GRB.CONTINUOUS, name='x3')
#x4 = m.addVar(vtype=GRB.CONTINUOUS, name='x4')
x = m.addVars(range(1,5), vtype=GRB.CONTINUOUS, name='x')

#variables for fixed set-up
#y1 = m.addVar(vtype=GRB.BINARY, name='y1')
#y2 = m.addVar(vtype=GRB.BINARY, name='y2')
#y3 = m.addVar(vtype=GRB.BINARY, name='y3')
#y4 = m.addVar(vtype=GRB.BINARY, name='y4')
y = m.addVars(range(1,5), vtype=GRB.BINARY, name='y')

#variables for fixed inventory level at the end of the period
#I1 = m.addVar(vtype=GRB.CONTINUOUS, name='I1')
#I2 = m.addVar(vtype=GRB.CONTINUOUS, name='I2')
#I3 = m.addVar(vtype=GRB.CONTINUOUS, name='I3')
#I4 = m.addVar(vtype=GRB.CONTINUOUS, name='I4')
I = m.addVars(range(0,5), vtype=GRB.CONTINUOUS, name='I')

#constraints for stock control and demand satisfaction
#m.addConstr(x1 == demand[1] + I1)
#m.addConstr(I1 + x2 == demand[2] + I2)
#m.addConstr(I2 + x3 == demand[3] + I3)
#m.addConstr(I3 + x4 == demand[4] + I4)
m.addConstrs((I[t-1] + x[t] == demand[t] + I[t]) for t in range(1,5))
m.addConstr(I[0] == 0) #no beginning inventory

#constraints to determine how to handle the fixed cost
#m.addConstr(x1 <= 400 * y1)
#m.addConstr(x2 <= 400 * y2)
#m.addConstr(x3 <= 400 * y3)
#m.addConstr(x4 <= 400 * y4)
m.addConstrs((x[t] <= 400 * y[t]) for t in range(1,5))

m.setObjective(p * x.sum() + f * y.sum() +
               h * I.sum(), GRB.MINIMIZE)

m.optimize()

for v in m.getVars():
    print(v.varName, v.x)

print('The optimal objective function value is', m.objVal)