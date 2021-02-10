from gurobipy import GRB, Model

# Create a new model
m = Model("monthly-carpenter")

# Create variables
#xc1 = m.addVar(vtype=GRB.INTEGER, name="xc1")
#xc2 = m.addVar(vtype=GRB.INTEGER, name="xc2")
#xc3 = m.addVar(vtype=GRB.INTEGER, name="xc3")
#xc4 = m.addVar(vtype=GRB.INTEGER, name="xc4")
xc = m.addVars(range(1,5),vtype=GRB.INTEGER, name='chair')

#Ic1 = m.addVar(vtype=GRB.INTEGER, name="Ic1")
#Ic2 = m.addVar(vtype=GRB.INTEGER, name="Ic2")
#Ic3 = m.addVar(vtype=GRB.INTEGER, name="Ic3")
#Ic4 = m.addVar(vtype=GRB.INTEGER, name="Ic4")
Ic = m.addVars(range(0,5), vtype=GRB.INTEGER, name='chair_stock')

#xt1 = m.addVar(vtype=GRB.INTEGER, name="xt1")
#xt2 = m.addVar(vtype=GRB.INTEGER, name="xt2")
#xt3 = m.addVar(vtype=GRB.INTEGER, name="xt3")
#xt4 = m.addVar(vtype=GRB.INTEGER, name="xt4")
xt = m.addVars(range(1,5),vtype=GRB.INTEGER, name='table')

#It1 = m.addVar(vtype=GRB.INTEGER, name="It1")
#It2 = m.addVar(vtype=GRB.INTEGER, name="It2")
#It3 = m.addVar(vtype=GRB.INTEGER, name="It3")
#It4 = m.addVar(vtype=GRB.INTEGER, name="It4")
It = m.addVars(range(0,5),vtype=GRB.INTEGER, name='table_stock')

# Add constraint
#m.addConstr(xc[1] + 2.5 * xt[1] <= 50, "rawmat1")
#m.addConstr(xc[2] + 2.5 * xt[2] <= 50, "rawmat2")
#m.addConstr(xc[3] + 2.5 * xt[3] <= 50, "rawmat3")
#m.addConstr(xc[4] + 2.5 * xt[4] <= 50, "rawmat4")
m.addConstrs((xc[i] + 2.5 * xt[i] <= 50 for i in range(1,5)), name='rawmat')

# Add constraint
#m.addConstr(2 * xc[1] + xt[1]  <= 40, "workhour1")
#m.addConstr(2 * xc[2] + xt[2]  <= 40, "workhour2")
#m.addConstr(2 * xc[3] + xt[3]  <= 40, "workhour3")
#m.addConstr(2 * xc[4] + xt[4]  <= 40, "workhour4")

m.addConstrs((2 * xc[i] + xt[i] <= 40 for i in range(1,5)), name='workhour')

# stock kontrol for chair
#m.addConstr(8 + xc1 == 16 + Ic1)
#m.addConstr(Ic1 + xc2 == 20 + Ic2)
#m.addConstr(Ic2 + xc3 == 15 + Ic3)
#m.addConstr(Ic3 + xc4 == 10 + Ic4)
chair_demand = [0, 16, 20, 15, 13]

m.addConstr(Ic[0] == 8) #beginning inventory
m.addConstrs((Ic[i-1] + xc[i] == chair_demand[i] + Ic[i] for i in range(1,5)),
             name='chair_control')


# stock kontrol for table
#m.addConstr(5 + xt1 == 12 + It1)
#m.addConstr(It1 + xt2 == 8 + It2)
#m.addConstr(It2 + xt3 == 18 + It3)
#m.addConstr(It3 + xt4 == 10 + It4)
table_demand = [0, 12, 8, 18, 15]
m.addConstr(It[0] == 5) #beginning inventory
m.addConstrs((It[i-1] + xt[i] == table_demand[i] + It[i] for i in range(1,5)),
             name='table_control')


# Set objective
#m.setObjective(10 * xc[1] + 15 * xt[1] +
#               10 * xc[2] + 15 * xt[2] +
#               10 * xc[3] + 15 * xt[3] +
#               10 * xc[4] + 15 * xt[4], GRB.MAXIMIZE)
m.setObjective(10 * xc.sum() + 15 * xt.sum(), GRB.MAXIMIZE)

m.optimize()

for v in m.getVars():
    print(v.varName, v.x)

print('The optimal objective function value is', m.objVal)
