class SetCover():
    # initializes the object with the dataset, parses the data
    def __init__(self, inputFile):
        with open(inputFile) as f:
            lines = f.split("\n")
            firstLine = lines[0].split()
            # m is the number of rows, which correspond to elements 
            self.m = firstLine[0]
            # n is the number of columns, which correspond to sets
            self.n = firstLine[1]
            # sets is a list where sets[i] corresponds to the weight of the i-th set
            sets = []
            # elements is a list of lists where elements[i] is the set of sets that contain element i
            elements = []
            temp = []
            for i in range(1, len(lines)):
                line = lines[i].split()
                if len(sets) < self.n:
                    for weight in line:
                        sets.append(weight)
                elif len(line) == 1 and len(elements) != 0:
                    elements.append(temp)
                    temp = []
                else:
                    for setNumber in line:
                        temp.append(setNumber)
            elements.append(temp)
            self.sets = sets
            self.elements = elements
    
    # the Integer Linear Program version of Set Cover, solved exactly using the CP-SAT ILP Solver
    def solveILP(self):
        from ortools.sat.python import cp_model
        model = cp_model.CpModel()
        elements = self.elements
        sets = self.sets
        # indicator variables for whether or not the i-th set is included in the solution
        set_vars = [model.NewBoolVar(f'indicator for set {i}') for i in range(self.n)]
        # constraint that each vertex needs to be covered
        for element in elements:
            setCoverConstraint = 0
            for elementSet in element:
                setCoverConstraint += set_vars[elementSet]
            model.Add(setCoverConstraint >= 1)
        # minimization of the total weight
        total_weight = 0
        for i in range(len(sets)):
            total_weight += (sets[i] * set_vars[i])
        model.Minimize(total_weight)

        # solve the constraint program and print the results
        solver = cp_model.CpSolver()
        if solver.Solve(model) == cp_model.OPTIMAL:
            answer = 0
            for j in range(len(sets)):
                answer += solver.Value(set_vars[j])    
            print(f'the optimal set cover weight is {answer}')
            print(solver.ResponseStats())

    # the Linear Programming + Randomized Rounding Scheme version of Set Cover, approximated by using the GLOP solver and rounding scheme
    def solveLP_Rounding(self):
        from ortools.linear_solver import pywraplp
        import random
        solver = pywraplp.Solver('set_cover_LP_solver', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
        elements = self.elements
        sets = self.sets
        # indicator variables for whether or not the i-th set is included in the solution
        set_vars = [solver.NumVar(0, 1, f'indicator for set {i}') for i in range(self.n)]
        # constraint that each vertex needs to be covered
        for element in elements:
            setCoverConstraint = 0
            for elementSet in element:
                setCoverConstraint += set_vars[elementSet]
            solver.Add(setCoverConstraint >= 1)
        # minimization of the total weight using linear programming
        total_weight = 0
        for i in range(len(sets)):
            total_weight += (sets[i] * set_vars[i])
        solver.Minimize(total_weight)
        
        # solve the constraint program
        if solver.Solve() == Solver.OPTIMAL:
            set_answers = [set_vars[i].solution_value() for i in range(len(set_vars))]
        
        # randomzied rounding scheme: add the set to the solution with probability corresponding to the value of the variable
        answer = 0
        for setElem in range(len(sets)):
            if random.random() < set_answers[setElem]:
                answer += sets[setElem]

        # print the results
        print(f'the optimal set cover weight is {answer}')
        print(solver.ResponseStats())

        

                

