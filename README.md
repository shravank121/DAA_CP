# Predictive Secure File Replication in Distributed Systems

## Design and Analysis of Algorithms (DAA) Course Project

### Focus: Algorithm Design Paradigms and Complexity Analysis

This project demonstrates core DAA concepts through a distributed storage system simulation. The system uses multiple algorithm design paradigms (Greedy, Dynamic Programming, Graph Algorithms, Divide & Conquer) to predict node failures and proactively migrate replicas for high availability.

### Key DAA Concepts Implemented:
- **Greedy Algorithms** with proof of optimality
- **Dynamic Programming** with optimal substructure
- **Graph Algorithms** (Dijkstra, Prim's MST)
- **Divide and Conquer** with Master Theorem analysis
- **Branch and Bound** for constrained optimization
- **Complexity Analysis** (Big-O, recurrence relations)

## System Architecture

### Node Model
Each node in the distributed cluster has:
- `node_id`: Unique identifier
- `reliability`: Probability node stays alive (0-1)
- `failure_probability`: Probability of failure per time step
- `trust_score`: Trust level (0-1)
- `storage_capacity`: Maximum storage in GB
- `current_load`: Current storage usage (0-1)
- `status`: "alive" or "failed"
- `stored_files`: List of file IDs

### File Model
Each file has:
- `file_id`: Unique identifier
- `size`: File size in GB
- `importance`: Importance level
- `replicas`: List of node IDs storing replicas

## Core Algorithms with DAA Paradigms

### Algorithm 1: Node Failure Risk Calculation
**Paradigm:** Iterative Algorithm  
**Time Complexity:** O(N)  
**Space Complexity:** O(N)

Computes risk score for each node:
```
risk(node) = 0.5 × (1 - reliability) + 0.3 × load + 0.2 × failure_history
```

### Algorithm 2: Greedy Replica Node Selection
**Paradigm:** Greedy Algorithm  
**Time Complexity:** O(N log N)  
**Space Complexity:** O(N)

**Greedy Choice Property:** Always select node with highest score  
**Optimal Substructure:** Best k nodes = Best node + Best (k-1) from remaining

Scoring function:
```
score(node) = reliability + trust_score - load - network_cost
```

**Proof of Optimality:** Selecting highest-scored nodes at each step leads to globally optimal solution for independent replica placement.

### Algorithm 3: Minimum Replica Calculation (Dynamic Programming)
**Paradigm:** Dynamic Programming + Greedy  
**Time Complexity:** O(N log N)  
**Space Complexity:** O(N)

**DP State:** `dp[k]` = availability with k best nodes  
**Recurrence:** `dp[k] = 1 - ∏(failure_prob[i])` for i = 0 to k-1  
**Optimal Substructure:** Minimum k replicas uses k nodes with lowest failure probability

Determines minimum replicas for target availability:
```
Availability = 1 - Π(failure_probability of replica nodes)
```

### Algorithm 4: Proactive Replica Migration (Greedy)
**Paradigm:** Greedy Algorithm  
**Time Complexity:** O(F × N log N)  
**Space Complexity:** O(F + N)

**Greedy Strategy:** For each high-risk node, immediately migrate to best available node without reconsidering future states.

### Algorithm 5: Failure Simulation
**Paradigm:** Probabilistic Algorithm  
**Time Complexity:** O(N)  
**Space Complexity:** O(N)

Simulates node failures using Monte Carlo method.

### Algorithm 6: System Availability Calculation
**Paradigm:** Iterative Algorithm  
**Time Complexity:** O(F × R) where R = avg replicas  
**Space Complexity:** O(F)

Calculates availability using probability theory.

## Advanced DAA Algorithms

### Dijkstra's Shortest Path (Graph Algorithm)
**Paradigm:** Greedy on Graphs  
**Time Complexity:** O(E log V)  
**Application:** Find optimal routing between nodes

### Prim's Minimum Spanning Tree (Graph Algorithm)
**Paradigm:** Greedy on Graphs  
**Time Complexity:** O(E log V)  
**Application:** Design efficient replication topology

### Divide and Conquer Load Balancing
**Paradigm:** Divide and Conquer  
**Recurrence:** T(n) = 2T(n/2) + O(n)  
**Time Complexity:** O(n log n) by Master Theorem  
**Application:** Distribute files across nodes

### 0/1 Knapsack (Dynamic Programming)
**Paradigm:** Dynamic Programming  
**Time Complexity:** O(n × W)  
**Application:** Optimal file selection with capacity constraints

## Project Structure

```
project/
├── nodes.py                    # Node class definition
├── file_model.py              # File class definition
├── risk_model.py              # Algorithm 1: Risk calculation
├── replication.py             # Algorithms 2, 3, 4: Greedy & DP
├── graph_algorithms.py        # Dijkstra, Prim's MST
├── advanced_algorithms.py     # Knapsack DP, Divide & Conquer, Branch & Bound
├── failure_simulation.py      # Algorithm 5: Failure simulation
├── availability.py            # Algorithm 6: Availability calculation
├── simulator.py               # Main simulation engine
├── main.py                    # Entry point
├── test_algorithms.py         # Basic algorithm tests
├── test_daa_concepts.py       # DAA paradigm demonstrations
├── README.md                  # Project overview
├── DAA_CONCEPTS.md           # Detailed DAA explanations
├── COMPLEXITY_ANALYSIS.md     # Algorithm complexity proofs
├── QUICKSTART.md             # Quick start guide
└── PRESENTATION_OUTLINE.md    # Presentation structure
```

## Installation and Usage

### Basic Simulation
No external dependencies required for core algorithms.

```bash
# Run main simulation
python main.py

# Test individual algorithms
python test_algorithms.py

# Demonstrate DAA concepts
python test_daa_concepts.py
```

### Optional Visualization
For graph visualization (optional):
```bash
pip install networkx matplotlib
python visualization.py
```

## Usage

Run the simulation:
```bash
python main.py
```

The simulator will:
1. Initialize nodes and files
2. Perform initial replica placement
3. Run simulation steps:
   - Calculate node risk scores
   - Detect high-risk nodes
   - Migrate replicas proactively
   - Simulate node failures
   - Maintain minimum replicas
   - Calculate system availability

## Configuration

Edit `main.py` to adjust parameters:
- `NUM_NODES`: Number of nodes in cluster (default: 15)
- `NUM_FILES`: Number of files to store (default: 8)
- `RISK_THRESHOLD`: Risk threshold for migration (default: 0.6)
- `SIMULATION_STEPS`: Number of time steps (default: 10)
- `MIN_REPLICAS`: Minimum replicas per file (default: 3)

## Sample Output

```
=== Time Step 1 ===
High-risk nodes detected: [3, 7]
  Node 3 risk = 0.652
  Node 7 risk = 0.701
Migrated File_2: Node 3 → Node 9
Node 7 FAILED
Removed 2 replicas from failed nodes
Created replica of File_4 on Node 12
System availability: 99.87%
```

## Algorithm Complexity Summary

| Algorithm | Paradigm | Time | Space | Optimal? |
|-----------|----------|------|-------|----------|
| Risk Calculation | Iteration | O(N) | O(N) | N/A |
| Replica Selection | Greedy | O(N log N) | O(N) | Yes |
| Min Replicas | DP + Greedy | O(N log N) | O(N) | Yes |
| Replica Migration | Greedy | O(F×N log N) | O(F+N) | Yes |
| Failure Simulation | Probabilistic | O(N) | O(N) | N/A |
| Availability Calc | Iteration | O(F×R) | O(F) | N/A |
| Dijkstra's Path | Greedy (Graph) | O(E log V) | O(V) | Yes |
| Prim's MST | Greedy (Graph) | O(E log V) | O(V) | Yes |
| Load Balance | Divide & Conquer | O(N log N) | O(log N) | Approx |
| Knapsack | Dynamic Prog | O(N×W) | O(N×W) | Yes |

Where:
- N = number of nodes
- F = number of files
- R = average replicas per file

## Future Enhancements

- Network graph visualization using networkx and matplotlib
- Dynamic load balancing
- Cost optimization for replica placement
- Byzantine fault tolerance
- Geographic distribution simulation

## DAA Learning Outcomes

This project demonstrates mastery of:

1. **Algorithm Design Paradigms**
   - Greedy algorithms with correctness proofs
   - Dynamic programming with recurrence relations
   - Graph algorithms for network problems
   - Divide and conquer with Master Theorem

2. **Complexity Analysis**
   - Asymptotic notation (Big-O, Ω, Θ)
   - Recurrence relation solving
   - Time-space trade-offs
   - Best/average/worst case analysis

3. **Optimization Techniques**
   - Greedy choice property
   - Optimal substructure
   - Memoization and tabulation
   - Pruning strategies

4. **Practical Application**
   - Real-world distributed systems problem
   - Multiple algorithm paradigms in one system
   - Performance vs optimality trade-offs
   - Scalability considerations

## References

- Cormen, T. H., et al. "Introduction to Algorithms" (CLRS)
- Kleinberg, J., & Tardos, É. "Algorithm Design"
- Distributed Systems: Principles and Paradigms
