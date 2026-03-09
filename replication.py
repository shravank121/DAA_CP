"""
ALGORITHM 2: GREEDY REPLICA NODE SELECTION (GREEDY ALGORITHM)
ALGORITHM 3: MINIMUM REPLICA CALCULATION (DYNAMIC PROGRAMMING)
ALGORITHM 4: PROACTIVE REPLICA MIGRATION (GREEDY ALGORITHM)

DAA CONCEPTS USED:
- Greedy Algorithm: Local optimal choices lead to global optimum
- Dynamic Programming: Optimal substructure for replica calculation
- Optimization: Maximizing availability while minimizing cost
"""

def calculate_node_score(node, network_cost=0.1):
    """
    Calculate suitability score for replica placement
    
    GREEDY CHOICE PROPERTY:
    - Selecting node with highest score at each step
    - Score combines multiple factors: reliability, trust, load
    
    Formula: score = reliability + trust_score - load - network_cost
    
    PROOF OF GREEDY CHOICE:
    - Higher reliability → Lower failure probability
    - Higher trust → More secure storage
    - Lower load → More available capacity
    - Lower network cost → Faster access
    
    Args:
        node: Node object
        network_cost: Cost of network communication (default 0.1)
    
    Returns:
        float: Node score (higher = better candidate)
    """
    if node.status == "failed":
        return -1.0
    
    score = (node.reliability + 
             node.trust_score - 
             node.current_load - 
             network_cost)
    
    return score

def select_replica_nodes(nodes, file, num_replicas, exclude_nodes=None):
    """
    ALGORITHM 2: GREEDY ALGORITHM for Replica Node Selection
    
    ALGORITHM PARADIGM: Greedy Algorithm
    
    GREEDY STRATEGY:
    1. Score all candidate nodes based on multiple criteria
    2. Sort nodes by score (best first)
    3. Select top K nodes greedily
    
    OPTIMAL SUBSTRUCTURE:
    - Best K nodes = Best node + Best (K-1) nodes from remaining
    
    GREEDY CHOICE PROPERTY:
    - Selecting highest-scored node at each step is safe
    - Local optimum leads to global optimum for independent replicas
    
    PROOF SKETCH:
    - Let S = greedy solution, O = optimal solution
    - If S ≠ O, we can replace lowest node in O with highest in S
    - This improves or maintains total score
    - Contradiction: O was optimal
    - Therefore, S = O (greedy is optimal)
    
    Time Complexity: O(N log N) - dominated by sorting
    Space Complexity: O(N) - for candidate list
    
    Args:
        nodes: List of all Node objects
        file: File object to replicate
        num_replicas: Number of replicas to create
        exclude_nodes: Set of node IDs to exclude
    
    Returns:
        list: Selected node IDs for replica placement
    """
    if exclude_nodes is None:
        exclude_nodes = set()
    
    # Step 1: Filter candidate nodes - O(N)
    candidates = []
    for node in nodes:
        if (node.status == "alive" and 
            node.id not in exclude_nodes and 
            node.has_capacity(file.size)):
            score = calculate_node_score(node)
            candidates.append((score, node.id))
    
    # Step 2: Sort by score (descending) - O(N log N)
    # GREEDY CHOICE: Always pick highest score
    candidates.sort(reverse=True, key=lambda x: x[0])
    
    # Step 3: Select top num_replicas nodes - O(K)
    selected = [node_id for score, node_id in candidates[:num_replicas]]
    
    return selected

def calculate_minimum_replicas(nodes, target_availability=0.999):
    """
    ALGORITHM 3: DYNAMIC PROGRAMMING for Minimum Replica Calculation
    
    ALGORITHM PARADIGM: Dynamic Programming with Greedy Optimization
    
    PROBLEM FORMULATION:
    - Given: N nodes with failure probabilities p₁, p₂, ..., pₙ
    - Find: Minimum K such that Availability ≥ target
    - Availability = 1 - ∏(pᵢ) for i in selected replicas
    
    OPTIMAL SUBSTRUCTURE:
    - If we need K replicas, we should choose K nodes with lowest failure probability
    - Optimal K replicas = Node with min p + Optimal (K-1) replicas
    
    GREEDY CHOICE:
    - Always select node with lowest failure probability
    - This minimizes the failure product
    
    RECURRENCE RELATION:
    - Let A(k) = availability with k best nodes
    - A(k) = 1 - ∏(p[i]) for i = 0 to k-1 (sorted by p)
    - Find minimum k where A(k) ≥ target
    
    PROOF OF CORRECTNESS:
    - To minimize ∏(pᵢ), select nodes with smallest pᵢ values
    - This is greedy optimal for product minimization
    - Therefore, minimum K is found by iterating sorted nodes
    
    Time Complexity: O(N log N) - sorting dominates
    Space Complexity: O(N) - sorted node list
    
    Args:
        nodes: List of Node objects
        target_availability: Required availability level (default 0.999)
    
    Returns:
        int: Minimum number of replicas needed
    """
    # Step 1: Sort nodes by failure probability (ascending) - O(N log N)
    # GREEDY CHOICE: Select nodes with lowest failure probability
    sorted_nodes = sorted([n for n in nodes if n.status == "alive"], 
                         key=lambda x: x.failure_probability)
    
    if not sorted_nodes:
        return 0
    
    # Step 2: Dynamic Programming - build up solution iteratively
    # dp[k] = availability with k best nodes
    num_replicas = 1
    failure_product = 1.0
    
    while num_replicas <= len(sorted_nodes):
        # Update failure product incrementally - O(1) per iteration
        failure_product *= sorted_nodes[num_replicas - 1].failure_probability
        
        # Calculate availability - DP state
        availability = 1 - failure_product
        
        # Check if target reached
        if availability >= target_availability:
            return num_replicas
        
        num_replicas += 1
    
    return len(sorted_nodes)  # Use all available nodes

def migrate_replicas_from_risky_nodes(nodes, files, high_risk_node_ids):
    """
    ALGORITHM 4: Proactive replica migration from high-risk nodes
    
    Time Complexity: O(F × N) where F = files, N = nodes
    
    Args:
        nodes: List of Node objects
        files: List of File objects
        high_risk_node_ids: List of high-risk node IDs
    
    Returns:
        list: Migration events (tuples of file_id, from_node, to_node)
    """
    migrations = []
    node_dict = {node.id: node for node in nodes}
    
    # For each high-risk node
    for risky_node_id in high_risk_node_ids:
        if risky_node_id not in node_dict:
            continue
        
        risky_node = node_dict[risky_node_id]
        
        # Find all files on this node
        for file in files:
            if risky_node_id in file.replicas:
                # Select a new node for this replica
                exclude = set(file.replicas)
                new_nodes = select_replica_nodes(nodes, file, 1, exclude)
                
                if new_nodes:
                    new_node_id = new_nodes[0]
                    new_node = node_dict[new_node_id]
                    
                    # Perform migration
                    if new_node.add_file(file.id, file.size):
                        file.add_replica(new_node_id)
                        
                        # Remove from risky node if we have enough replicas
                        if file.get_replica_count() > 2:
                            risky_node.remove_file(file.id, file.size)
                            file.remove_replica(risky_node_id)
                        
                        migrations.append((file.id, risky_node_id, new_node_id))
    
    return migrations
