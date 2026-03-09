"""
ALGORITHM 5: FAILURE SIMULATION
Simulates node failures based on failure probabilities
"""

import random

def simulate_node_failures(nodes):
    """
    Simulate node failures for one time step
    
    For each alive node, fail it with probability = failure_probability
    
    Time Complexity: O(N)
    
    Args:
        nodes: List of Node objects
    
    Returns:
        list: IDs of nodes that failed in this step
    """
    failed_nodes = []
    
    for node in nodes:
        if node.status == "alive":
            # Random failure based on failure probability
            if random.random() < node.failure_probability:
                node.mark_failed()
                failed_nodes.append(node.id)
    
    return failed_nodes

def cleanup_failed_node_replicas(nodes, files):
    """
    Remove replicas from failed nodes
    
    Args:
        nodes: List of Node objects
        files: List of File objects
    
    Returns:
        int: Number of replicas removed
    """
    node_dict = {node.id: node for node in nodes}
    removed_count = 0
    
    for file in files:
        # Check each replica location
        replicas_to_remove = []
        for node_id in file.replicas:
            if node_id in node_dict and node_dict[node_id].status == "failed":
                replicas_to_remove.append(node_id)
        
        # Remove failed replicas
        for node_id in replicas_to_remove:
            file.remove_replica(node_id)
            removed_count += 1
    
    return removed_count
