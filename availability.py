"""
ALGORITHM 6: SYSTEM AVAILABILITY CALCULATION
Calculates availability metrics for files and the system
"""

def calculate_file_availability(file, nodes):
    """
    Calculate availability for a single file
    
    Formula: Availability = 1 - Π(failure_probability of replica nodes)
    
    Args:
        file: File object
        nodes: List of Node objects
    
    Returns:
        float: Availability score (0-1)
    """
    if not file.replicas:
        return 0.0
    
    node_dict = {node.id: node for node in nodes}
    
    # Calculate product of failure probabilities
    failure_product = 1.0
    for node_id in file.replicas:
        if node_id in node_dict:
            node = node_dict[node_id]
            if node.status == "alive":
                failure_product *= node.failure_probability
            else:
                # Failed node has 100% failure probability
                failure_product *= 1.0
    
    availability = 1 - failure_product
    return availability

def calculate_system_availability(files, nodes):
    """
    Calculate overall system availability
    
    Returns average availability across all files
    
    Args:
        files: List of File objects
        nodes: List of Node objects
    
    Returns:
        float: Average system availability (0-1)
    """
    if not files:
        return 0.0
    
    total_availability = 0.0
    for file in files:
        total_availability += calculate_file_availability(file, nodes)
    
    return total_availability / len(files)

def get_availability_report(files, nodes):
    """
    Generate detailed availability report
    
    Returns:
        dict: Mapping of file_id to availability score
    """
    report = {}
    for file in files:
        report[file.id] = calculate_file_availability(file, nodes)
    
    return report
