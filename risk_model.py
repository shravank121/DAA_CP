"""
ALGORITHM 1: NODE FAILURE RISK CALCULATION
Computes risk scores for nodes to predict failures
Time Complexity: O(N) where N is number of nodes
"""

def calculate_node_risk(node):
    """
    Calculate risk score for a single node
    
    Formula: risk = 0.5 * (1 - reliability) + 0.3 * load + 0.2 * failure_history
    
    Args:
        node: Node object
    
    Returns:
        float: Risk score (0-1, higher = more risky)
    """
    if node.status == "failed":
        return 1.0
    
    # Normalize failure_history (cap at 5 failures)
    normalized_history = min(node.failure_history / 5.0, 1.0)
    
    risk = (0.5 * (1 - node.reliability) + 
            0.3 * node.current_load + 
            0.2 * normalized_history)
    
    return min(risk, 1.0)  # Cap at 1.0

def identify_high_risk_nodes(nodes, threshold=0.6):
    """
    Identify all high-risk nodes in the system
    
    Time Complexity: O(N)
    
    Args:
        nodes: List of Node objects
        threshold: Risk threshold for marking nodes as high-risk
    
    Returns:
        list: Node IDs of high-risk nodes
    """
    high_risk_nodes = []
    
    for node in nodes:
        risk = calculate_node_risk(node)
        if risk > threshold:
            high_risk_nodes.append(node.id)
    
    return high_risk_nodes

def get_all_risk_scores(nodes):
    """
    Calculate risk scores for all nodes
    
    Time Complexity: O(N)
    
    Returns:
        dict: Mapping of node_id to risk_score
    """
    return {node.id: calculate_node_risk(node) for node in nodes}
