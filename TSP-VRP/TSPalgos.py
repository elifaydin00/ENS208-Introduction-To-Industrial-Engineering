'''
ENS 208 - Introduction to IE

Function definitions for nearest neighbor, savings, and 2-opt algorithms.
'''

from pqdict import pqdict

# =============================================================================
def nearest_neighbor(nodes, origin, d):
    '''
    Constructs a TSP solution using the nearest neighbor algorithm, NNH, 
    for a given set of nodes, the associated pairwise distance matrix-d, 
    and the origin.
    '''
    # Tour should start at the origin
    tour = [origin]
    
    # Initialize the tour length
    tour_length = 0
    
    # If the origin is not in nodes, add it to nodes
    if origin not in nodes:
        nodes.append(origin)
    
    # Nearest neighbor search until all nodes are visited
    while len(tour) < len(nodes):
        dist, next_node = min((d[tour[-1]][i], i) for i in nodes if i not in tour)
        tour_length += dist
        tour.append(next_node)
        print('Added', next_node, 'to the tour!')
    
    # Tour should end at the origin
    tour_length += d[tour[-1]][origin]
    tour.append(origin)
    
    # Round the result to 2 decimals to avoid floating point representation errors
    tour_length = round(tour_length, 2)

    # Return the resulting tour and its length as a tuple
    return tour, tour_length

# =============================================================================
def savings(nodes, origin, d):
    '''
    Constructs a TSP solution using the savings method for a given set/list of 
    nodes, their pairwise distances-d, and the origin.
    '''
    # Set of customer nodes (i.e. nodes other than the origin)
    customers = {i for i in nodes if i != origin}
    
    # Initialize out-and-back tours from the origin to every other node
    tours = {(i,i): [origin, i, origin] for i in customers}
    
    # Compute savings
    savings = {(i, j): round(d[i][origin] + d[origin][j] - d[i][j], 2) 
               for i in customers for j in customers if j != i}
        
    # Define a priority queue dictionary to get a pair of nodes (i,j) which yields
    # the maximum savings
    pq = pqdict(savings, reverse = True)
    
    # Merge subtours until obtaining a TSP tour
    while len(tours) > 1:
        i,j = pq.pop()
        print((i, j))
        # Outer loop
        break_outer = False
        for t1 in tours:
            for t2 in tours.keys()-{t1}:
                if t1[1] == i and t2[0] == j:
                    print('Merging', tours[t1], 'and', tours[t2])
                    tours[(t1[0], t2[1])] = tours[t1][:-1] + tours[t2][1:]
                    del tours[t1], tours[t2]
                    print(tours)
                    break_outer = True
                    break
            if break_outer:
                break
        else:
            print('No merging opportunities can be found for', (i,j)) 
    
    # Final tours dictionary (involves a single tour, which is the TSP tour)
    print(tours)
    
    # Compute tour length
    tour_length = 0
    for tour in tours.values():
        for i in range(len(tour)-1):
            tour_length += d[tour[i]][tour[i+1]]
            
    # Round the result to 2 decimals to avoid floating point representation errors
    tour_length = round(tour_length, 2)

    # Return the resulting tour and its length as a tuple
    return tour, tour_length

# =============================================================================
def two_opt(tour, tour_length, d):
    '''
    Improves a given TSP solution using the 2-opt algorithm. Note: This function
    applies 2opt correctly only when the distance matrix is symmetric. In case
    of asymmetric distances, one needs to update the cost difference calculation
    incurred by swapping.
    '''
    current_tour, current_tour_length = tour, tour_length
    best_tour, best_tour_length = current_tour, current_tour_length
    solution_improved = True
    
    while solution_improved:
        print()
        print('Attempting to improve the tour', current_tour, 
              'with length', current_tour_length)
        solution_improved = False
        
        for i in range(1, len(current_tour)-2):
            for j in range(i+1, len(current_tour)-1):
                difference = round((d[current_tour[i-1]][current_tour[j]]
                                  + d[current_tour[i]][current_tour[j+1]]
                                  - d[current_tour[i-1]][current_tour[i]]
                                  - d[current_tour[j]][current_tour[j+1]]), 2)
                
                print('Cost difference due to swapping', current_tour[i], 'and',
                      current_tour[j], 'is:', difference)
                
                if current_tour_length + difference < best_tour_length:
                    print('Found an improving move! Updating the best tour...')
                    
                    best_tour = current_tour[:i] + list(reversed(current_tour[i:j+1])) + current_tour[j+1:]
                    best_tour_length = round(current_tour_length + difference, 2)
                    
                    print('Improved tour is:', best_tour, 'with length',
                          best_tour_length)
                    
                    solution_improved = True
                    
        current_tour, current_tour_length = best_tour, best_tour_length
    
    # Return the resulting tour and its length as a tuple
    return best_tour, best_tour_length  

# =============================================================================