# Design and Analysis of Algorithms (DAA) Concepts

## Algorithm Design Paradigms Used in This Project

This project demonstrates core DAA concepts through practical implementation in a distributed storage system.

---

## 1. GREEDY ALGORITHMS

### Algorithm 2: Replica Node Selection

**Greedy Strategy:**
- At each step, select the node with the highest score
- Score = reliability + trust_score - load - network_cost
- Never reconsider previous choices

**Greedy Choice Property:**
- Selecting the best available node at each step leads to optimal solution
- Local optimum → Global optimum

**Proof Sketch:**
```
Let S = greedy solution (nodes sorted by score)
Let O = optimal solution

Assume S ≠ O
Let i be first position where S[i] ≠ O[i]
Since S[i] has higher score than O[i], we can replace O[i] with S[i]
This improves or maintains the solution quality
Contradiction: O was optimal
Therefore, S = O (greedy is optimal)
```

**Time Complexity:** O(N log N)
- Scoring: O(N)
- Sorting: O(N log N) ← dominant
- Selection: O(K)

**Space Complexity:** O(N)

---

### Algorithm 4: Proactive Replica Migration

**Greedy Strategy:**
- Identify high-risk nodes (risk > threshold)
- For each file on risky node, greedily select best alternative
- Migrate immediately without considering future states

**Greedy Choice:**
- Always migrate to the currently best available node
- Don't wait for potentially better nodes in future

**Time Complexity:** O(F × N log N)

---

## 2. DYNAMIC PROGRAMMING

### Algorithm 3: Minimum Replica Calculation

**DP Formulation:**

**State Definition:**
- `dp[k]` = availability achieved with k best nodes

**Recurrence Relation:**
```
dp[k] = 1 - ∏(failure_probability[i]) for i = 0 to k-1
```

**Optimal Substructure:**
- Optimal k replicas = Best node + Optimal (k-1) replicas from remaining
- To minimize failure product, always choose nodes with lowest failure probability

**Base Case:**
- `dp[0]` = 0 (no replicas = no availability)
- `dp[1]` = 1 - p[0] (one replica on best node)

**Solution:**
- Find minimum k where `dp[k] ≥ target_availability`

**Time Complexity:** O(N log N)
- Sorting nodes: O(N log N)
- DP iteration: O(N)

**Space Complexity:** O(N)

**Example:**
```
Nodes with failure probabilities: [0.1, 0.15, 0.2, 0.25]
Target availability: 99.9%

dp[1] = 1 - 0.1 = 0.90 (90%)
dp[2] = 1 - (0.1 × 0.15) = 0.985 (98.5%)
dp[3] = 1 - (0.1 × 0.15 × 0.2) = 0.997 (99.7%)
dp[4] = 1 - (0.1 × 0.15 × 0.2 × 0.25) = 0.99925 (99.925%) ✓

Minimum replicas needed: 4
```

---

### Advanced: 0/1 Knapsack for Replica Placement

**Problem:** Select files to store on a node with limited capacity

**DP Table:**
- `dp[i][w]` = maximum importance using first i files with capacity w

**Recurrence:**
```
dp[i][w] = max(
    dp[i-1][w],                           // Don't take file i
    dp[i-1][w-size[i]] + importance[i]    // Take file i
)
```

**Time Complexity:** O(n × W)
**Space Complexity:** O(n × W)

---

## 3. GRAPH ALGORITHMS

### Dijkstra's Algorithm: Shortest Path

**Purpose:** Find optimal routing between nodes in network

**Algorithm:**
1. Initialize distances to infinity
2. Set source distance to 0
3. Use min-heap to always process nearest unvisited node (GREEDY)
4. Update distances to neighbors
5. Repeat until target reached

**Greedy Choice:** Always expand node with minimum distance

**Time Complexity:** O(E log V) with min-heap

**Application in Project:**
- Find nearest nodes for replica placement
- Calculate network latency between nodes
- Optimize data transfer routes

---

### Prim's Algorithm: Minimum Spanning Tree

**Purpose:** Find minimum cost network topology

**Algorithm:**
1. Start with arbitrary node
2. Repeatedly add minimum weight edge connecting tree to non-tree node (GREEDY)
3. Continue until all nodes connected

**Greedy Choice:** Always add minimum weight edge

**Time Complexity:** O(E log V)

**Application in Project:**
- Design efficient replication topology
- Minimize total network cost
- Ensure all nodes are reachable

---

## 4. DIVIDE AND CONQUER

### Load Balancing Algorithm

**Strategy:**
1. **Divide:** Split nodes into two groups
2. **Conquer:** Recursively balance each group
3. **Combine:** Merge balanced groups

**Recurrence Relation:**
```
T(n) = 2T(n/2) + O(n)
```

**By Master Theorem:**
```
a = 2, b = 2, f(n) = O(n)
n^(log_b(a)) = n^1 = n
f(n) = Θ(n^(log_b(a)))
Therefore: T(n) = Θ(n log n)
```

**Time Complexity:** O(n log n)
**Space Complexity:** O(log n) - recursion stack

---

## 5. BRANCH AND BOUND

### Optimal Placement with Constraints

**Strategy:**
1. **Branch:** Explore different placement combinations
2. **Bound:** Prune branches that:
   - Exceed cost constraint
   - Cannot improve best solution
3. **Track:** Maintain best solution found

**Pruning Conditions:**
- Current cost > max_cost → prune
- Best possible availability < current_best → prune

**Time Complexity:** 
- Worst case: O(2^n)
- With pruning: Much better in practice

---

## 6. ALGORITHM ANALYSIS TECHNIQUES

### Asymptotic Analysis

**Big-O Notation:**
- Upper bound on growth rate
- Example: O(N log N) means ≤ c × N log N for large N

**Big-Ω Notation:**
- Lower bound on growth rate
- Example: Ω(N) means ≥ c × N for large N

**Big-Θ Notation:**
- Tight bound (both upper and lower)
- Example: Θ(N log N) means both O(N log N) and Ω(N log N)

### Recurrence Relations

**Master Theorem:**
```
T(n) = aT(n/b) + f(n)

Case 1: f(n) = O(n^c) where c < log_b(a)
        → T(n) = Θ(n^(log_b(a)))

Case 2: f(n) = Θ(n^c) where c = log_b(a)
        → T(n) = Θ(n^c log n)

Case 3: f(n) = Ω(n^c) where c > log_b(a)
        → T(n) = Θ(f(n))
```

---

## 7. OPTIMIZATION TECHNIQUES

### Greedy vs Dynamic Programming

| Aspect | Greedy | Dynamic Programming |
|--------|--------|-------------------|
| Strategy | Make locally optimal choice | Solve subproblems optimally |
| Reconsideration | Never | Yes, through memoization |
| Optimality | Sometimes | Always (if applicable) |
| Time | Usually faster | Usually slower |
| Space | Less | More (memoization) |

**When to use Greedy:**
- Greedy choice property holds
- Optimal substructure exists
- Need fast solution

**When to use DP:**
- Overlapping subproblems
- Optimal substructure
- Need guaranteed optimal solution

---

## 8. COMPLEXITY CLASSES

### Problem Classification

**P (Polynomial Time):**
- Problems solvable in O(n^k) time
- Examples in project:
  - Risk calculation: O(N)
  - Replica selection: O(N log N)
  - Shortest path: O(E log V)

**NP (Nondeterministic Polynomial):**
- Solutions verifiable in polynomial time
- Examples:
  - Optimal placement with all constraints
  - Minimum cost replica distribution

**NP-Complete:**
- Hardest problems in NP
- Related: Multi-objective optimization in distributed systems

---

## 9. ALGORITHM CORRECTNESS

### Proof Techniques

**1. Loop Invariants:**
```
Initialization: True before first iteration
Maintenance: If true before iteration, remains true after
Termination: When loop terminates, invariant gives correctness
```

**2. Induction:**
```
Base case: P(0) or P(1) is true
Inductive step: If P(k) is true, then P(k+1) is true
Conclusion: P(n) is true for all n
```

**3. Contradiction:**
```
Assume algorithm is incorrect
Derive a contradiction
Therefore, algorithm must be correct
```

---

## 10. PRACTICAL APPLICATIONS IN PROJECT

### Algorithm Selection Decision Tree

```
Need to select nodes?
├─ Yes → Use Greedy (Algorithm 2)
│         Fast, optimal for independent choices
│
Need minimum replicas?
├─ Yes → Use DP (Algorithm 3)
│         Optimal substructure, overlapping subproblems
│
Need shortest path?
├─ Yes → Use Dijkstra (Graph Algorithm)
│         Greedy, optimal for non-negative weights
│
Need to balance load?
├─ Yes → Use Divide and Conquer
│         Recursive decomposition, O(n log n)
│
Need optimal with constraints?
└─ Yes → Use Branch and Bound
          Explores space efficiently with pruning
```

---

## Summary Table

| Algorithm | Paradigm | Time | Space | Optimal? |
|-----------|----------|------|-------|----------|
| Risk Calculation | Iteration | O(N) | O(N) | N/A |
| Replica Selection | Greedy | O(N log N) | O(N) | Yes |
| Min Replicas | DP + Greedy | O(N log N) | O(N) | Yes |
| Migration | Greedy | O(F×N log N) | O(F+N) | Yes |
| Shortest Path | Greedy (Dijkstra) | O(E log V) | O(V) | Yes |
| MST | Greedy (Prim) | O(E log V) | O(V) | Yes |
| Load Balance | Divide & Conquer | O(N log N) | O(log N) | Approx |
| Optimal Placement | Branch & Bound | O(2^n) | O(N) | Yes |

---

## Key Takeaways for DAA Course

1. **Algorithm Design:** Choose paradigm based on problem structure
2. **Complexity Analysis:** Always analyze time and space
3. **Correctness:** Prove algorithms work correctly
4. **Optimization:** Trade-offs between time, space, and optimality
5. **Practical Application:** Real-world problems often combine multiple paradigms