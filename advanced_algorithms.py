"""
ADVANCED DAA ALGORITHMS FOR DISTRIBUTED STORAGE

This module implements advanced algorithm design paradigms:
1. Dynamic Programming - Optimal replica placement
2. Divide and Conquer - Load balancing
3. Backtracking - Constraint satisfaction
4. Branch and Bound - Cost optimization
"""

def knapsack_replica_placement(nodes, files, total_capacity):
    """
    DYNAMIC PROGRAMMING: 0/1 Knapsack for Replica Placement
    
    PROBLEM: Select which files to replicate on a node with limited capacity
    
    ALGORITHM PARADIGM: Dynamic Programming
    
    FORMULATION:
    - Items: Files with size and importance (value)
    - Capacity: Node storage capacity
    - Goal: Maximize total importance while staying within capacity
    
    RECURRENCE RELATION:
    dp[i][w] = max(dp[i-1][w], dp[i-1][w-size[i]] + importance[i])
    
    Where:
    - dp[i][w] = max importance using first i files with capacity w
    - Base case: dp[0][w] = 0 for all w
    
    Time Complexity: O(n × W) where n = files, W = capacity
    Space Complexity: O(n × W)
    
    Args:
        nodes: List of Node objects
        files: List of File objects
        total_capacity: Storage capacity constraint
    
    Returns:
        dict: Mapping of node_id to list of file_ids to store
    """
    placement = {}
    
    for node in nodes:
        if node.status != "alive":
            continue
        
        n = len(files)
        W = int(min(node.storage_capacity, total_capacity))
        
        # DP table: dp[i][w] = (max_importance, selected_files)
        dp = [[0] * (W + 1) for _ in range(n + 1)]
        
        # Fill DP table
        for i in range(1, n + 1):
            file = files[i - 1]
            file_size = int(file.size)
            file_importance = file.importance
            
            for w in range(W + 1):
                # Don't take file i
                dp[i][w] = dp[i-1][w]
                
                # Take file i if it fits
                if file_size <= w:
                    take_value = dp[i-1][w - file_size] + file_importance
                    if take_value > dp[i][w]:
                        dp[i][w] = take_value
        
        # Backtrack to find selected files
        selected_files = []
        w = W
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected_files.append(files[i-1].id)
                w -= int(files[i-1].size)
        
        placement[node.id] = selected_files
    
    return placement

def divide_and_conquer_load_balance(nodes, files):
    """
    DIVIDE AND CONQUER: Load Balancing Across Nodes
    
    ALGORITHM PARADIGM: Divide and Conquer
    
    STRATEGY:
    1. Divide: Split nodes into two groups
    2. Conquer: Recursively balance each group
    3. Combine: Merge balanced groups
    
    RECURRENCE:
    T(n) = 2T(n/2) + O(n)
    By Master Theorem: T(n) = O(n log n)
    
    Time Complexity: O(n log n)
    Space Complexity: O(log n) - recursion stack
    
    Args:
        nodes: List of Node objects
        files: List of File objects
    
    Returns:
        dict: Balanced file distribution
    """
    def balance_recursive(node_list, file_list):
        """Recursive load balancing"""
        if len(node_list) <= 1:
            # Base case: single node gets all files
            if node_list:
                return {node_list[0].id: [f.id for f in file_list]}
            return {}
        
        # Divide: Split nodes in half
        mid = len(node_list) // 2
        left_nodes = node_list[:mid]
        right_nodes = node_list[mid:]
        
        # Split files based on total load
        total_size = sum(f.size for f in file_list)
        left_capacity = sum(n.storage_capacity for n in left_nodes)
        right_capacity = sum(n.storage_capacity for n in right_nodes)
        
        left_target = total_size * left_capacity / (left_capacity + right_capacity)
        
        # Partition files
        left_files = []
        right_files = []
        current_size = 0
        
        for file in sorted(file_list, key=lambda f: f.size, reverse=True):
            if current_size < left_target:
                left_files.append(file)
                current_size += file.size
            else:
                right_files.append(file)
        
        # Conquer: Recursively balance each half
        left_result = balance_recursive(left_nodes, left_files)
        right_result = balance_recursive(right_nodes, right_files)
        
        # Combine: Merge results
        return {**left_result, **right_result}
    
    return balance_recursive(nodes, files)

def branch_and_bound_optimal_placement(nodes, files, max_cost):
    """
    BRANCH AND BOUND: Optimal Replica Placement with Cost Constraint
    
    ALGORITHM PARADIGM: Branch and Bound
    
    PROBLEM: Find optimal replica placement minimizing cost while maximizing availability
    
    STRATEGY:
    1. Branch: Explore different placement combinations
    2. Bound: Prune branches that exceed cost or can't improve solution
    3. Track best solution found
    
    Time Complexity: O(2^n) worst case, but pruning reduces practical complexity
    Space Complexity: O(n) - recursion depth
    
    Args:
        nodes: List of Node objects
        files: List of File objects
        max_cost: Maximum allowed cost
    
    Returns:
        tuple: (best_placement, best_availability, cost)
    """
    best_solution = {
        'placement': {},
        'availability': 0,
        'cost': 0
    }
    
    def calculate_placement_availability(placement, file):
        """Calculate availability for a file given placement"""
        if file.id not in [fid for fids in placement.values() for fid in fids]:
            return 0
        
        failure_product = 1.0
        for node_id, file_ids in placement.items():
            if file.id in file_ids:
                node = next(n for n in nodes if n.id == node_id)
                failure_product *= node.failure_probability
        
        return 1 - failure_product
    
    def branch_and_bound_recursive(file_idx, current_placement, current_cost):
        """Recursive branch and bound exploration"""
        nonlocal best_solution
        
        # Base case: all files placed
        if file_idx >= len(files):
            # Calculate total availability
            total_avail = sum(
                calculate_placement_availability(current_placement, f) 
                for f in files
            ) / len(files)
            
            # Update best solution if better
            if total_avail > best_solution['availability']:
                best_solution = {
                    'placement': {nid: list(fids) for nid, fids in current_placement.items()},
                    'availability': total_avail,
                    'cost': current_cost
                }
            return
        
        file = files[file_idx]
        
        # Branch: Try placing file on each node
        for node in nodes:
            if node.status != "alive" or not node.has_capacity(file.size):
                continue
            
            # Calculate cost of this placement
            placement_cost = (1 - node.reliability)
            new_cost = current_cost + placement_cost
            
            # Bound: Prune if cost exceeds maximum
            if new_cost > max_cost:
                continue
            
            # Add file to this node
            if node.id not in current_placement:
                current_placement[node.id] = []
            current_placement[node.id].append(file.id)
            node.current_load += file.size / node.storage_capacity
            
            # Recurse
            branch_and_bound_recursive(file_idx + 1, current_placement, new_cost)
            
            # Backtrack
            current_placement[node.id].remove(file.id)
            node.current_load -= file.size / node.storage_capacity
            node.current_load = max(0.0, node.current_load)
            if not current_placement[node.id]:
                del current_placement[node.id]
    
    # Start branch and bound
    branch_and_bound_recursive(0, {}, 0)
    
    return best_solution['placement'], best_solution['availability'], best_solution['cost']

def greedy_vs_optimal_comparison(nodes, files):
    """
    Compare Greedy vs Optimal (DP) solutions
    
    Demonstrates trade-off between:
    - Greedy: Fast but approximate
    - DP: Slower but optimal
    
    Returns:
        dict: Comparison results
    """
    import time
    from replication import select_replica_nodes
    
    # Greedy approach
    start_time = time.time()
    greedy_placement = {}
    for file in files:
        selected = select_replica_nodes(nodes, file, 3)
        greedy_placement[file.id] = selected
    greedy_time = time.time() - start_time
    
    # DP approach (knapsack)
    start_time = time.time()
    dp_placement = knapsack_replica_placement(nodes, files, 1000)
    dp_time = time.time() - start_time
    
    return {
        'greedy': {
            'placement': greedy_placement,
            'time': greedy_time
        },
        'dp': {
            'placement': dp_placement,
            'time': dp_time
        }
    }
