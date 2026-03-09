"""
Test script to demonstrate individual algorithms
"""

from nodes import Node
from file_model import File
from risk_model import calculate_node_risk, identify_high_risk_nodes
from replication import calculate_node_score, select_replica_nodes, calculate_minimum_replicas
from availability import calculate_file_availability
import random

def test_algorithm_1_risk_calculation():
    """Test Algorithm 1: Node Failure Risk Calculation"""
    print("\n" + "="*60)
    print("ALGORITHM 1: NODE FAILURE RISK CALCULATION")
    print("="*60)
    
    # Create test nodes with different characteristics
    nodes = [
        Node(0, reliability=0.95, failure_probability=0.05, trust_score=0.9, storage_capacity=100),
        Node(1, reliability=0.70, failure_probability=0.20, trust_score=0.6, storage_capacity=100),
        Node(2, reliability=0.85, failure_probability=0.10, trust_score=0.8, storage_capacity=100),
    ]
    
    # Add some load
    nodes[0].current_load = 0.3
    nodes[1].current_load = 0.8
    nodes[2].current_load = 0.5
    
    # Add failure history
    nodes[1].failure_history = 2
    
    print("\nNode Characteristics:")
    for node in nodes:
        risk = calculate_node_risk(node)
        print(f"Node {node.id}:")
        print(f"  Reliability: {node.reliability:.2f}")
        print(f"  Load: {node.current_load:.2f}")
        print(f"  Failure History: {node.failure_history}")
        print(f"  RISK SCORE: {risk:.3f}")
    
    # Identify high-risk nodes
    high_risk = identify_high_risk_nodes(nodes, threshold=0.4)
    print(f"\nHigh-risk nodes (threshold=0.4): {high_risk}")
    print("Time Complexity: O(N)")

def test_algorithm_2_replica_selection():
    """Test Algorithm 2: Greedy Replica Node Selection"""
    print("\n" + "="*60)
    print("ALGORITHM 2: GREEDY REPLICA NODE SELECTION")
    print("="*60)
    
    # Create test nodes
    nodes = [
        Node(0, reliability=0.95, failure_probability=0.05, trust_score=0.9, storage_capacity=100),
        Node(1, reliability=0.70, failure_probability=0.20, trust_score=0.6, storage_capacity=100),
        Node(2, reliability=0.85, failure_probability=0.10, trust_score=0.8, storage_capacity=100),
        Node(3, reliability=0.90, failure_probability=0.08, trust_score=0.85, storage_capacity=100),
        Node(4, reliability=0.80, failure_probability=0.15, trust_score=0.75, storage_capacity=100),
    ]
    
    # Set different loads
    nodes[0].current_load = 0.2
    nodes[1].current_load = 0.9
    nodes[2].current_load = 0.5
    nodes[3].current_load = 0.3
    nodes[4].current_load = 0.6
    
    # Create a test file
    file = File("TestFile", size=5, importance_level=0.9)
    
    print("\nNode Scores:")
    for node in nodes:
        score = calculate_node_score(node)
        print(f"Node {node.id}: score={score:.3f} (reliability={node.reliability:.2f}, "
              f"trust={node.trust_score:.2f}, load={node.current_load:.2f})")
    
    # Select best 3 nodes
    selected = select_replica_nodes(nodes, file, num_replicas=3)
    print(f"\nSelected nodes for 3 replicas: {selected}")
    print("Time Complexity: O(N log N)")

def test_algorithm_3_minimum_replicas():
    """Test Algorithm 3: Minimum Replica Calculation"""
    print("\n" + "="*60)
    print("ALGORITHM 3: MINIMUM REPLICA CALCULATION")
    print("="*60)
    
    # Create test nodes
    nodes = [
        Node(i, reliability=0.90, failure_probability=0.10, trust_score=0.8, storage_capacity=100)
        for i in range(10)
    ]
    
    # Test different availability targets
    targets = [0.99, 0.999, 0.9999]
    
    print("\nMinimum replicas needed for different availability targets:")
    print(f"Node failure probability: 0.10")
    
    for target in targets:
        min_replicas = calculate_minimum_replicas(nodes, target_availability=target)
        
        # Calculate actual availability
        failure_product = 1.0
        for i in range(min_replicas):
            failure_product *= nodes[i].failure_probability
        actual_availability = 1 - failure_product
        
        print(f"\nTarget: {target*100:.2f}%")
        print(f"  Minimum replicas: {min_replicas}")
        print(f"  Actual availability: {actual_availability*100:.4f}%")

def test_algorithm_6_availability():
    """Test Algorithm 6: System Availability Calculation"""
    print("\n" + "="*60)
    print("ALGORITHM 6: SYSTEM AVAILABILITY CALCULATION")
    print("="*60)
    
    # Create test nodes
    nodes = [
        Node(0, reliability=0.95, failure_probability=0.05, trust_score=0.9, storage_capacity=100),
        Node(1, reliability=0.90, failure_probability=0.10, trust_score=0.85, storage_capacity=100),
        Node(2, reliability=0.85, failure_probability=0.15, trust_score=0.80, storage_capacity=100),
        Node(3, reliability=0.80, failure_probability=0.20, trust_score=0.75, storage_capacity=100),
    ]
    
    # Create test file with replicas
    file = File("TestFile", size=5, importance_level=0.9)
    file.replicas = [0, 1, 2]
    
    print("\nFile replicas on nodes: [0, 1, 2]")
    print("Node failure probabilities:")
    for i in [0, 1, 2]:
        print(f"  Node {i}: {nodes[i].failure_probability:.2f}")
    
    availability = calculate_file_availability(file, nodes)
    print(f"\nFile availability: {availability*100:.4f}%")
    
    # Show calculation
    failure_product = nodes[0].failure_probability * nodes[1].failure_probability * nodes[2].failure_probability
    print(f"\nCalculation:")
    print(f"  Failure product: {nodes[0].failure_probability} × {nodes[1].failure_probability} × {nodes[2].failure_probability} = {failure_product:.6f}")
    print(f"  Availability: 1 - {failure_product:.6f} = {availability:.6f}")

def main():
    """Run all algorithm tests"""
    random.seed(42)
    
    print("\n" + "="*60)
    print("ALGORITHM DEMONSTRATION AND TESTING")
    print("Design and Analysis of Algorithms - Course Project")
    print("="*60)
    
    test_algorithm_1_risk_calculation()
    test_algorithm_2_replica_selection()
    test_algorithm_3_minimum_replicas()
    test_algorithm_6_availability()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
