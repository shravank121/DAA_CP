"""
Test DAA Algorithm Paradigms
Demonstrates Greedy, DP, Graph Algorithms, Divide & Conquer, Branch & Bound
"""

from nodes import Node
from file_model import File
from replication import (calculate_node_score, select_replica_nodes, 
                         calculate_minimum_replicas)
from graph_algorithms import (NetworkGraph, build_network_topology, 
                              select_replicas_with_topology)
from advanced_algorithms import (knapsack_replica_placement, 
                                divide_and_conquer_load_balance,
                                greedy_vs_optimal_comparison)
import random

def test_greedy_algorithm():
    """
    Test GREEDY ALGORITHM for Replica Selection
    Demonstrates greedy choice property and optimal substructure
    """
    print("\n" + "="*70)
    print("GREEDY ALGORITHM: Replica Node Selection")
    print("="*70)
    
    # Create nodes with varying characteristics
    nodes = [
        Node(0, reliability=0.95, failure_probability=0.05, trust_score=0.90, storage_capacity=100),
        Node(1, reliability=0.70, failure_probability=0.20, trust_score=0.60, storage_capacity=100),
        Node(2, reliability=0.85, failure_probability=0.10, trust_score=0.80, storage_capacity=100),
        Node(3, reliability=0.90, failure_probability=0.08, trust_score=0.85, storage_capacity=100),
        Node(4, reliability=0.80, failure_probability=0.15, trust_score=0.75, storage_capacity=100),
        Node(5, reliability=0.88, failure_probability=0.12, trust_score=0.82, storage_capacity=100),
    ]
    
    # Set loads
    for i, load in enumerate([0.2, 0.9, 0.5, 0.3, 0.6, 0.4]):
        nodes[i].current_load = load
    
    file = File("TestFile", size=5, importance_level=0.9)
    
    print("\nGREEDY STRATEGY: Select nodes with highest score")
    print("Score = reliability + trust_score - load - network_cost\n")
    
    print("Node Scores (sorted by greedy choice):")
    scored_nodes = [(calculate_node_score(n), n.id, n.reliability, n.trust_score, n.current_load) 
                    for n in nodes]
    scored_nodes.sort(reverse=True)
    
    for score, nid, rel, trust, load in scored_nodes:
        print(f"  Node {nid}: score={score:.3f} (rel={rel:.2f}, trust={trust:.2f}, load={load:.2f})")
    
    # Greedy selection
    selected = select_replica_nodes(nodes, file, num_replicas=3)
    print(f"\nGREEDY CHOICE: Select top 3 nodes: {selected}")
    
    print("\nPROOF OF OPTIMALITY:")
    print("  1. Greedy choice: Always pick highest score")
    print("  2. Optimal substructure: Best k nodes = Best node + Best (k-1) from rest")
    print("  3. No reconsideration needed - greedy is optimal")
    
    print(f"\nTime Complexity: O(N log N) - dominated by sorting")
    print(f"Space Complexity: O(N) - candidate list")

def test_dynamic_programming():
    """
    Test DYNAMIC PROGRAMMING for Minimum Replica Calculation
    Demonstrates optimal substructure and overlapping subproblems
    """
    print("\n" + "="*70)
    print("DYNAMIC PROGRAMMING: Minimum Replica Calculation")
    print("="*70)
    
    # Create nodes with known failure probabilities
    nodes = [
        Node(i, reliability=0.90, failure_probability=0.10, trust_score=0.8, storage_capacity=100)
        for i in range(6)
    ]
    
    print("\nPROBLEM: Find minimum replicas for target availability")
    print("APPROACH: Dynamic Programming with greedy optimization\n")
    
    print("DP STATE DEFINITION:")
    print("  dp[k] = availability with k best nodes")
    print("\nRECURRENCE RELATION:")
    print("  dp[k] = 1 - PRODUCT(failure_prob[i]) for i = 0 to k-1")
    print("\nOPTIMAL SUBSTRUCTURE:")
    print("  Optimal k replicas = Best node + Optimal (k-1) replicas\n")
    
    # Test different targets
    targets = [0.90, 0.99, 0.999, 0.9999]
    
    print("Node failure probability: 0.10\n")
    print("DP Table Construction:")
    print("-" * 60)
    
    for target in targets:
        min_replicas = calculate_minimum_replicas(nodes, target_availability=target)
        
        # Show DP computation
        failure_product = 1.0
        for i in range(min_replicas):
            failure_product *= nodes[i].failure_probability
        actual_availability = 1 - failure_product
        
        print(f"\nTarget: {target*100:.2f}%")
        print(f"  DP iterations: {min_replicas}")
        print(f"  Failure product: {failure_product:.6f}")
        print(f"  Availability: {actual_availability*100:.4f}%")
        print(f"  Minimum replicas: {min_replicas}")
    
    print("\n" + "-" * 60)
    print(f"Time Complexity: O(N log N) - sorting + DP iteration")
    print(f"Space Complexity: O(N) - sorted node list")

def test_graph_algorithms():
    """
    Test GRAPH ALGORITHMS: Dijkstra and Prim
    Demonstrates greedy algorithms on graphs
    """
    print("\n" + "="*70)
    print("GRAPH ALGORITHMS: Dijkstra's Shortest Path & Prim's MST")
    print("="*70)
    
    # Create small network
    nodes = [Node(i, reliability=0.9, failure_probability=0.1, 
                  trust_score=0.8, storage_capacity=100) for i in range(5)]
    
    # Build network graph
    graph = NetworkGraph(nodes)
    
    # Add edges with latencies
    edges = [
        (0, 1, 2.0), (0, 2, 4.0),
        (1, 2, 1.0), (1, 3, 7.0),
        (2, 3, 3.0), (2, 4, 5.0),
        (3, 4, 2.0)
    ]
    
    for n1, n2, latency in edges:
        graph.add_edge(n1, n2, latency)
    
    print("\nNetwork Topology:")
    print("  Nodes: 0, 1, 2, 3, 4")
    print("  Edges (with latency):")
    for n1, n2, lat in edges:
        print(f"    {n1} -- {n2}: {lat}ms")
    
    # Test Dijkstra's algorithm
    print("\n" + "-" * 60)
    print("DIJKSTRA'S ALGORITHM: Shortest Path from Node 0 to Node 4")
    print("-" * 60)
    
    distance, path = graph.dijkstra_shortest_path(0, 4)
    
    print(f"\nGREEDY STRATEGY: Always expand node with minimum distance")
    print(f"\nShortest path: {' -> '.join(map(str, path))}")
    print(f"Total distance: {distance}ms")
    
    print(f"\nTime Complexity: O(E log V) with min-heap")
    print(f"Space Complexity: O(V)")
    
    # Test Prim's algorithm
    print("\n" + "-" * 60)
    print("PRIM'S ALGORITHM: Minimum Spanning Tree")
    print("-" * 60)
    
    mst_edges = graph.prim_mst()
    
    print(f"\nGREEDY STRATEGY: Always add minimum weight edge to tree")
    print(f"\nMST Edges:")
    total_weight = 0
    for n1, n2, weight in mst_edges:
        print(f"  {n1} -- {n2}: {weight}ms")
        total_weight += weight
    
    print(f"\nTotal MST weight: {total_weight}ms")
    print(f"Time Complexity: O(E log V)")
    print(f"Space Complexity: O(V)")

def test_divide_and_conquer():
    """
    Test DIVIDE AND CONQUER for Load Balancing
    Demonstrates recursive decomposition
    """
    print("\n" + "="*70)
    print("DIVIDE AND CONQUER: Load Balancing")
    print("="*70)
    
    # Create nodes
    nodes = [Node(i, reliability=0.9, failure_probability=0.1,
                  trust_score=0.8, storage_capacity=100) for i in range(8)]
    
    # Create files
    files = [File(f"File_{i}", size=random.uniform(5, 15), 
                  importance_level=random.uniform(0.5, 1.0)) for i in range(16)]
    
    print("\nPROBLEM: Distribute 16 files across 8 nodes")
    print("\nSTRATEGY:")
    print("  1. DIVIDE: Split nodes into two groups")
    print("  2. CONQUER: Recursively balance each group")
    print("  3. COMBINE: Merge balanced groups")
    
    print("\nRECURRENCE RELATION:")
    print("  T(n) = 2T(n/2) + O(n)")
    print("\nMASTER THEOREM:")
    print("  a=2, b=2, f(n)=O(n)")
    print("  n^(log_b(a)) = n^1 = n")
    print("  f(n) = Theta(n) -> Case 2")
    print("  Therefore: T(n) = Theta(n log n)")
    
    # Perform load balancing
    balanced = divide_and_conquer_load_balance(nodes, files)
    
    print("\nBalanced Distribution:")
    for node_id, file_ids in sorted(balanced.items()):
        node = nodes[node_id]
        total_size = sum(f.size for f in files if f.id in file_ids)
        print(f"  Node {node_id}: {len(file_ids)} files, {total_size:.1f}GB")
    
    print(f"\nTime Complexity: O(n log n)")
    print(f"Space Complexity: O(log n) - recursion stack")

def test_knapsack_dp():
    """
    Test 0/1 KNAPSACK Dynamic Programming
    Demonstrates classic DP problem
    """
    print("\n" + "="*70)
    print("DYNAMIC PROGRAMMING: 0/1 Knapsack for File Placement")
    print("="*70)
    
    # Create node with limited capacity
    nodes = [Node(0, reliability=0.9, failure_probability=0.1,
                  trust_score=0.8, storage_capacity=50)]
    
    # Create files with size and importance
    files = [
        File("File_A", size=10, importance_level=60),
        File("File_B", size=20, importance_level=100),
        File("File_C", size=30, importance_level=120),
        File("File_D", size=15, importance_level=80),
        File("File_E", size=25, importance_level=110),
    ]
    
    print("\nPROBLEM: Select files to maximize importance within capacity")
    print(f"Node capacity: {nodes[0].storage_capacity}GB\n")
    
    print("Files:")
    for f in files:
        print(f"  {f.id}: size={f.size}GB, importance={f.importance}")
    
    print("\nDP FORMULATION:")
    print("  dp[i][w] = max importance using first i files with capacity w")
    print("\nRECURRENCE:")
    print("  dp[i][w] = max(")
    print("      dp[i-1][w],                    // Don't take file i")
    print("      dp[i-1][w-size[i]] + value[i]  // Take file i")
    print("  )")
    
    # Solve knapsack
    placement = knapsack_replica_placement(nodes, files, 50)
    
    print(f"\nOPTIMAL SELECTION:")
    selected_files = placement[0]
    total_size = sum(f.size for f in files if f.id in selected_files)
    total_importance = sum(f.importance for f in files if f.id in selected_files)
    
    for fid in selected_files:
        f = next(file for file in files if file.id == fid)
        print(f"  {f.id}: size={f.size}GB, importance={f.importance}")
    
    print(f"\nTotal size: {total_size}GB / {nodes[0].storage_capacity}GB")
    print(f"Total importance: {total_importance}")
    
    print(f"\nTime Complexity: O(n * W) where W = capacity")
    print(f"Space Complexity: O(n * W)")

def test_algorithm_comparison():
    """
    Compare different algorithm paradigms
    """
    print("\n" + "="*70)
    print("ALGORITHM PARADIGM COMPARISON")
    print("="*70)
    
    print("\n" + "-" * 70)
    print("| Paradigm          | Time         | Space    | Optimal? | Use Case |")
    print("-" * 70)
    print("| Greedy            | O(N log N)   | O(N)     | Yes*     | Fast selection |")
    print("| Dynamic Prog      | O(N*W)       | O(N*W)   | Yes      | Optimization |")
    print("| Divide & Conquer  | O(N log N)   | O(log N) | Approx   | Decomposition |")
    print("| Graph (Dijkstra)  | O(E log V)   | O(V)     | Yes      | Shortest path |")
    print("| Graph (Prim)      | O(E log V)   | O(V)     | Yes      | MST |")
    print("| Branch & Bound    | O(2^n)**     | O(N)     | Yes      | Constrained opt |")
    print("-" * 70)
    print("* Greedy optimal when greedy choice property holds")
    print("** Exponential worst case, but pruning helps in practice")
    
    print("\n\nKEY INSIGHTS:")
    print("  1. Greedy: Fast but requires proof of optimality")
    print("  2. DP: Guaranteed optimal but higher complexity")
    print("  3. Divide & Conquer: Good for recursive decomposition")
    print("  4. Graph algorithms: Essential for network problems")
    print("  5. Branch & Bound: Handles complex constraints")

def main():
    """Run all DAA concept tests"""
    random.seed(42)
    
    print("\n" + "="*70)
    print("DESIGN AND ANALYSIS OF ALGORITHMS (DAA)")
    print("Algorithm Paradigm Demonstrations")
    print("="*70)
    
    test_greedy_algorithm()
    test_dynamic_programming()
    test_graph_algorithms()
    test_divide_and_conquer()
    test_knapsack_dp()
    test_algorithm_comparison()
    
    print("\n" + "="*70)
    print("ALL DAA CONCEPT TESTS COMPLETE")
    print("="*70)
    print("\nKey Takeaways:")
    print("  [OK] Greedy algorithms make locally optimal choices")
    print("  [OK] Dynamic programming solves overlapping subproblems")
    print("  [OK] Graph algorithms handle network topology")
    print("  [OK] Divide and conquer recursively decomposes problems")
    print("  [OK] Each paradigm has specific use cases and trade-offs")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
