# Algorithm Complexity Analysis

## Overview
This document provides detailed time and space complexity analysis for all algorithms implemented in the Predictive Secure File Replication system.

## Algorithm 1: Node Failure Risk Calculation

### Implementation
Located in: `risk_model.py`

### Time Complexity: O(N)
- Iterates through all N nodes exactly once
- For each node, performs constant-time arithmetic operations
- Formula calculation: `risk = 0.5 * (1 - reliability) + 0.3 * load + 0.2 * failure_history`
- Each operation is O(1)

### Space Complexity: O(N)
- Stores risk scores for N nodes in a dictionary
- No additional data structures required

### Pseudocode
```
function calculate_all_risks(nodes):
    risk_scores = {}
    for each node in nodes:                    // O(N)
        risk = 0.5 * (1 - node.reliability)    // O(1)
               + 0.3 * node.load               // O(1)
               + 0.2 * node.failure_history    // O(1)
        risk_scores[node.id] = risk            // O(1)
    return risk_scores
```

---

## Algorithm 2: Greedy Replica Node Selection

### Implementation
Located in: `replication.py`

### Time Complexity: O(N log N)
- Filtering candidates: O(N) - iterate through all nodes
- Scoring each candidate: O(1) per node
- Sorting candidates by score: O(N log N) - dominant operation
- Selecting top K replicas: O(K) where K ≤ N

Overall: O(N) + O(N log N) + O(K) = O(N log N)

### Space Complexity: O(N)
- Stores candidate list with scores: O(N)
- Selected nodes list: O(K) where K ≤ N

### Pseudocode
```
function select_replica_nodes(nodes, file, num_replicas):
    candidates = []
    
    // Filter and score candidates - O(N)
    for each node in nodes:                           // O(N)
        if node.is_alive() and node.has_capacity():   // O(1)
            score = calculate_score(node)             // O(1)
            candidates.append((score, node.id))       // O(1)
    
    // Sort by score - O(N log N)
    candidates.sort(reverse=True)                     // O(N log N)
    
    // Select top K - O(K)
    selected = candidates[0:num_replicas]             // O(K)
    
    return selected
```

---

## Algorithm 3: Minimum Replica Calculation

### Implementation
Located in: `replication.py`

### Time Complexity: O(N log N + R)
- Sorting nodes by failure probability: O(N log N)
- Iterative search for minimum replicas: O(R) where R is result
- In worst case, R = N, so O(N log N + N) = O(N log N)

### Space Complexity: O(N)
- Sorted copy of nodes list: O(N)

### Pseudocode
```
function calculate_minimum_replicas(nodes, target_availability):
    // Sort nodes by failure probability - O(N log N)
    sorted_nodes = sort(nodes, key=failure_probability)  // O(N log N)
    
    num_replicas = 1
    // Iterative search - O(R) where R ≤ N
    while num_replicas <= len(sorted_nodes):             // O(R)
        failure_product = 1.0
        for i in range(num_replicas):                    // O(R)
            failure_product *= sorted_nodes[i].failure_prob
        
        availability = 1 - failure_product
        if availability >= target_availability:
            return num_replicas
        
        num_replicas += 1
    
    return len(sorted_nodes)
```

### Optimization Note
The inner loop makes this O(R²) in the worst case, but R is typically small (3-5 replicas), making it effectively O(N log N) dominated by sorting.

---

## Algorithm 4: Proactive Replica Migration

### Implementation
Located in: `replication.py`

### Time Complexity: O(F × N log N)
- For each high-risk node: O(H) where H = number of high-risk nodes
- For each file on risky node: O(F/H) on average
- For each file, select new node: O(N log N) from Algorithm 2
- Overall: O(H × (F/H) × N log N) = O(F × N log N)

### Space Complexity: O(F + N)
- Migration list: O(F) in worst case
- Temporary data structures: O(N)

### Pseudocode
```
function migrate_replicas(nodes, files, high_risk_nodes):
    migrations = []
    
    // For each high-risk node - O(H)
    for each risky_node in high_risk_nodes:              // O(H)
        
        // For each file on this node - O(F/H) average
        for each file in files:                          // O(F)
            if risky_node in file.replicas:
                
                // Select new node - O(N log N)
                new_node = select_replica_nodes(...)     // O(N log N)
                
                // Perform migration - O(1)
                migrate(file, risky_node, new_node)      // O(1)
                migrations.append(...)                   // O(1)
    
    return migrations
```

---

## Algorithm 5: Failure Simulation

### Implementation
Located in: `failure_simulation.py`

### Time Complexity: O(N)
- Iterate through all N nodes: O(N)
- For each node, generate random number and compare: O(1)
- Mark node as failed: O(1)

### Space Complexity: O(N)
- List of failed node IDs: O(N) in worst case

### Pseudocode
```
function simulate_failures(nodes):
    failed_nodes = []
    
    for each node in nodes:                    // O(N)
        if node.is_alive():                    // O(1)
            if random() < node.failure_prob:   // O(1)
                node.mark_failed()             // O(1)
                failed_nodes.append(node.id)   // O(1)
    
    return failed_nodes
```

---

## Algorithm 6: System Availability Calculation

### Implementation
Located in: `availability.py`

### Time Complexity: O(F × R)
- For each file: O(F)
- For each replica of the file: O(R) where R = average replicas per file
- Calculate failure product: O(R)
- Overall: O(F × R)

### Space Complexity: O(F)
- Availability report dictionary: O(F)
- Node lookup dictionary: O(N)

### Pseudocode
```
function calculate_system_availability(files, nodes):
    node_dict = create_lookup(nodes)           // O(N)
    total_availability = 0
    
    // For each file - O(F)
    for each file in files:                    // O(F)
        failure_product = 1.0
        
        // For each replica - O(R)
        for each node_id in file.replicas:     // O(R)
            node = node_dict[node_id]          // O(1)
            failure_product *= node.failure_prob  // O(1)
        
        availability = 1 - failure_product     // O(1)
        total_availability += availability     // O(1)
    
    return total_availability / len(files)     // O(1)
```

---

## Overall Simulation Complexity

### Per Time Step
The simulation executes the following operations per time step:

1. Risk calculation: O(N)
2. Identify high-risk nodes: O(N)
3. Replica migration: O(F × N log N)
4. Failure simulation: O(N)
5. Cleanup failed replicas: O(F × R)
6. Maintain replicas: O(F × N log N)
7. Availability calculation: O(F × R)

**Total per step: O(F × N log N)**

### Full Simulation
For T time steps:
**Total complexity: O(T × F × N log N)**

### Space Complexity
- Nodes: O(N)
- Files: O(F)
- Replica mappings: O(F × R)
- Temporary structures: O(N + F)

**Total space: O(N + F × R)**

---

## Complexity Summary Table

| Algorithm | Time Complexity | Space Complexity | Dominant Operation |
|-----------|----------------|------------------|-------------------|
| Risk Calculation | O(N) | O(N) | Linear scan |
| Replica Selection | O(N log N) | O(N) | Sorting |
| Minimum Replicas | O(N log N) | O(N) | Sorting |
| Replica Migration | O(F × N log N) | O(F + N) | Nested selection |
| Failure Simulation | O(N) | O(N) | Linear scan |
| Availability Calc | O(F × R) | O(F) | Nested iteration |
| **Per Time Step** | **O(F × N log N)** | **O(N + F × R)** | **Replica operations** |

---

## Optimization Opportunities

### 1. Replica Selection Caching
- Cache sorted node scores between time steps
- Only recompute when node states change significantly
- Reduces O(N log N) to O(N) in stable periods

### 2. Incremental Risk Updates
- Only recalculate risk for nodes with changed state
- Maintain risk score cache
- Reduces O(N) to O(k) where k = changed nodes

### 3. Spatial Indexing
- Use spatial data structures for node selection
- K-d trees or quadtrees for geographic distribution
- Reduces selection from O(N log N) to O(log N)

### 4. Lazy Migration
- Batch migrations across multiple time steps
- Reduce migration overhead
- Trade-off: slightly lower availability for better performance

---

## Scalability Analysis

### Small Scale (N=10, F=5)
- Per step: ~50 operations
- Very fast, real-time capable

### Medium Scale (N=100, F=50)
- Per step: ~50,000 operations
- Still efficient, sub-second execution

### Large Scale (N=1000, F=500)
- Per step: ~5,000,000 operations
- May require optimization
- Consider parallel processing

### Very Large Scale (N=10000, F=5000)
- Per step: ~500,000,000 operations
- Requires distributed simulation
- Implement caching and incremental updates
