'''
ENS 208 - Fall 2020

Function definitions for cluster-first route-second (CFRS) and route-first
cluster-second (RFCS) algorithms.
'''

from math import ceil
from scipy.cluster.vq import kmeans2, whiten
from TSPalgos import nearest_neighbor

# ============================================================================= 
def CFRS(k, coordinates, d, plt):
    '''
    Constructs a VRP solution using cluster-first route-second (CFRS) heuristic.
    '''
    # CLUSTERING PHASE - Clusters the nodes based on their proximity to each 
    # other via k-means method, which uses Euclidean distance as the proximity 
    # measure).
    x, y = kmeans2(whiten(coordinates), k, iter = 100)  
    plt.scatter(coordinates[:,0], coordinates[:,1], c = y)
    plt.axis('off')
    #plt.show()
    plt.savefig("clusters.png")
    
    depot = 0 # the depot node
    clusters = [{depot} for i in range(k)] # add the depot to all clusters
    
    # Assign the nodes to their respective clusters
    for i, label in enumerate(y):
        if i != depot:
            clusters[label].add(i)    
    print(clusters)
    
    # ROUTING PHASE - Constructs a list of TSP tours based on the clusters
    vrp_solution = [] # a list of TSP tours 
    total_length = 0 # total length of the TSP tours
    
    # Iterate over the clusters, and construct a TSP tour for each cluster
    for cluster in clusters:
        # Construct a TSP tour with your choice of construction method
        tour, tour_length = nearest_neighbor(cluster, depot, d)
        # Add the new tour to vrp_solution
        vrp_solution.append(tour)
        # Add the length of the new TSP tour to total_length
        total_length += tour_length
        
    # Round the result to 2 decimals to avoid floating point representation errors       
    total_length = round(total_length, 2)
    
    # Return the resulting VRP solution and its total length as a tuple
    return vrp_solution, total_length

# =============================================================================
def RFCS(k, nodes, d):
    '''
    Constructs a VRP solution using route-first cluster-second (RFCS) heuristic.
    '''
    depot = 0 # the depot node
    n_max = ceil((len(nodes)-1)/k) # vehicle capacity
    
    # ROUTING PHASE - Constructs a TSP tour over all nodes with your choice of
    # construction method
    tour, tour_length = nearest_neighbor(nodes, depot, d)
    
    # CLUSTERING PHASE - Iterates over the nodes in the TSP tour and splits it
    # into smaller tours each containing at most n_max nodes
    vrp_solution = []
    index = 1
    for i in range(k):
        current_tour = [depot]
        current_nodes = 0
        while current_nodes < n_max and tour[index] != depot:
            current_tour.append(tour[index])
            current_nodes += 1
            index += 1
        current_tour.append(depot)
        vrp_solution.append(current_tour)
        
    # Calculate the total length of the resulting tours
    total_length = 0
    for route in vrp_solution:
        for i in range(len(route)-1):
            total_length += d[route[i]][route[i+1]]
    
    # Round the result to 2 decimals to avoid floating point representation errors       
    total_length = round(total_length, 2)
    
    # Return the resulting VRP solution and its total length as a tuple
    return vrp_solution, total_length
# =============================================================================