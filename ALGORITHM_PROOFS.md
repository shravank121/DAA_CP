# Algorithm Correctness Proofs and Analysis

## Design and Analysis of Algorithms - Formal Proofs

This document provides formal correctness proofs and complexity analysis for all algorithms in the project.

---

## Algorithm 1: Node Failure Risk Calculation

### Algorithm Description
```
function calculate_risk(node):
    risk = 0.5 × (1 - node.reliability)
         + 0.3 × node.load
         + 0.2 × node.failure_history
    return risk
```

### Correctness Proof

**Claim:** The algorithm correctly computes a risk score in range [0, 1].

**Proof:**
1. Each component is bounded:
   - `(1 - reliability)` ∈ [0, 1] since reliability ∈ [0, 1]
   - `load` ∈ [0, 1] by definition
   - `failure_history` normalized to [0, 1]

2. Weighted sum with coefficients summing to 1.0:
   - 0.5 + 0.3 + 0.2 = 1.0

3. Therefore: risk ∈ [0, 1] ✓

### Complexity Analysis

**Time Complexity:** O(N)
- Single pass through N nodes
- Constant time arithmetic per node: O(1)
- Total: N × O(1) = O(N)

**Space Complexity:** O(N)
- Store risk score for each node
- No additional data structures

**Proof:**
```
T(N) = Σ(i=1 to N) c
     = c × N
     = O(N)
```

---

## Algorithm 2: Greedy Replica Node Selection

### Algorithm Description
```
function select_replicas(nodes, k):
    candidates = []
    for each node in nodes:
        score = calculate_score(node)
        candidates.append((score, node))
    
    candidates.sort(reverse=True)
    return candidates[0:k]
```

### Greedy Choice Property

**Claim:** Selecting the node with highest score at each step is safe.

**Proof by Exchange Argument:**

Let S = {s₁, s₂, ..., sₖ} be greedy solution (sorted by score)  
Let O = {o₁, o₂, ..., oₖ} be optimal solution

Assume S ≠ O. Let i be first position where sᵢ ≠ oᵢ.

Since nodes are sorted by score: score(sᵢ) ≥ score(oᵢ)

Create O' = O \ {oᵢ} ∪ {sᵢ} (replace oᵢ with sᵢ)

Total score of O' ≥ Total score of O (since score(sᵢ) ≥ score(oᵢ))

But O was optimal, contradiction!

Therefore, S = O (greedy is optimal) ✓

### Optimal Substructure

**Claim:** Optimal k nodes = Best node + Optimal (k-1) nodes from remaining

**Proof:**
Suppose optimal k nodes don't include the best node.  
Replace any node with the best node → score increases.  
Contradiction with optimality.  
Therefore, optimal solution includes best node. ✓

### Complexity Analysis

**Time Complexity:** O(N log N)

**Proof:**
```
T(N) = T_filter + T_score + T_sort + T_select
     = O(N) + O(N) + O(N log N) + O(k)
     = O(N log N)  [sorting dominates]
```

**Space Complexity:** O(N)
- Candidate list: O(N)
- Selected list: O(k) where k ≤ N

---

## Algorithm 3: Minimum Replica Calculation (Dynamic Programming)

### Algorithm Description
```
function min_replicas(nodes, target):
    sorted_nodes = sort(nodes by failure_prob)
    
    k = 1
    failure_product = 1.0
    
    while k ≤ len(nodes):
        failure_product *= sorted_nodes[k-1].failure_prob
        availability = 1 - failure_product
        
        if availability ≥ target:
            return k
        
        k += 1
    
    return len(nodes)
```

### Dynamic Programming Formulation

**State Definition:**
- `dp[k]` = availability with k best nodes

**Recurrence Relation:**
```
dp[0] = 0
dp[k] = 1 - ∏(i=0 to k-1) failure_prob[sorted_nodes[i]]
```

**Optimal Substructure:**

**Lemma:** To minimize failure product, select nodes with minimum failure probabilities.

**Proof:**
Let p₁ ≤ p₂ ≤ ... ≤ pₙ be sorted failure probabilities.

For any k nodes, failure product = ∏ pᵢ

To minimize product, select k smallest values: p₁, p₂, ..., pₖ

Any other selection includes some pⱼ where j > k, and pⱼ > pᵢ for some i ≤ k.

Replacing pⱼ with pᵢ decreases product.

Therefore, optimal selection uses k smallest probabilities. ✓

### Correctness Proof

**Claim:** Algorithm returns minimum k such that availability ≥ target.

**Proof by Induction:**

**Base case (k=1):**
- dp[1] = 1 - p₁ where p₁ is minimum failure probability
- If dp[1] ≥ target, return 1 (correct)
- Otherwise, continue (correct)

**Inductive hypothesis:** Assume correct for k-1.

**Inductive step:** For k:
- dp[k] = 1 - (p₁ × p₂ × ... × pₖ)
- This is maximum availability with k nodes (by optimal substructure)
- If dp[k] ≥ target, k is minimum (by induction hypothesis)
- If dp[k] < target, need more nodes (correct)

Therefore, algorithm is correct. ✓

### Complexity Analysis

**Time Complexity:** O(N log N)

**Proof:**
```
T(N) = T_sort + T_iterate
     = O(N log N) + O(N)
     = O(N log N)
```

**Space Complexity:** O(N)
- Sorted node list: O(N)
- Variables: O(1)

---

## Algorithm 4: Proactive Replica Migration

### Algorithm Description
```
function migrate_replicas(nodes, files, high_risk_nodes):
    migrations = []
    
    for risky_node in high_risk_nodes:
        for file in files:
            if risky_node in file.replicas:
                new_node = select_best_node(nodes, file)
                migrate(file, risky_node, new_node)
                migrations.append((file, risky_node, new_node))
    
    return migrations
```

### Greedy Strategy

**Greedy Choice:** For each file on risky node, immediately select best available node.

**Claim:** Greedy migration maintains or improves system availability.

**Proof:**
Let A_before = availability before migration  
Let A_after = availability after migration

For file f with replicas on nodes {n₁, n₂, ..., nₖ}:

A_before(f) = 1 - ∏ p(nᵢ)

After migrating from risky node nᵣ to safe node nₛ:

A_after(f) = 1 - ∏ p(nᵢ) where nᵣ replaced by nₛ

Since nₛ is selected greedily: p(nₛ) ≤ p(nᵣ)

Therefore: ∏ p(nᵢ) after ≤ ∏ p(nᵢ) before

Thus: A_after(f) ≥ A_before(f) ✓

### Complexity Analysis

**Time Complexity:** O(F × N log N)

**Proof:**
```
Let H = number of high-risk nodes
Let F = number of files
Let R = average replicas per file

T(F, N, H) = Σ(h in H) Σ(f in F) T_select(N)
           = H × (F/H) × O(N log N)  [on average]
           = F × O(N log N)
           = O(F × N log N)
```

**Space Complexity:** O(F + N)
- Migration list: O(F) worst case
- Node data: O(N)

---

## Graph Algorithm: Dijkstra's Shortest Path

### Algorithm Description
```
function dijkstra(graph, source, target):
    distances = {v: ∞ for v in vertices}
    distances[source] = 0
    heap = [(0, source)]
    visited = {}
    
    while heap:
        dist, u = heap.pop_min()
        if u == target:
            return dist
        
        if u in visited:
            continue
        visited.add(u)
        
        for v in neighbors(u):
            new_dist = dist + weight(u, v)
            if new_dist < distances[v]:
                distances[v] = new_dist
                heap.push((new_dist, v))
    
    return ∞
```

### Correctness Proof

**Claim:** Dijkstra's algorithm finds shortest path in graphs with non-negative weights.

**Proof by Induction:**

**Invariant:** When node u is removed from heap, distances[u] is shortest path distance.

**Base case:** source node has distance 0 (correct).

**Inductive step:**
Assume invariant holds for all visited nodes.

When u is removed from heap:
- u has minimum distance among unvisited nodes
- Any shorter path to u would go through unvisited node v
- But distances[v] ≥ distances[u] (u was minimum)
- With non-negative weights: path through v ≥ distances[u]
- Therefore, distances[u] is optimal ✓

### Complexity Analysis

**Time Complexity:** O(E log V)

**Proof:**
```
- Each vertex added to heap once: O(V)
- Each edge relaxed once: O(E)
- Heap operations: O(log V)
- Total: O(V log V + E log V) = O(E log V)
```

**Space Complexity:** O(V)
- Distance array: O(V)
- Heap: O(V)
- Visited set: O(V)

---

## Graph Algorithm: Prim's Minimum Spanning Tree

### Algorithm Description
```
function prim_mst(graph):
    mst = []
    visited = {start_node}
    heap = [(weight, start, neighbor) for neighbor in adj[start]]
    
    while heap and len(visited) < V:
        weight, u, v = heap.pop_min()
        
        if v in visited:
            continue
        
        mst.append((u, v, weight))
        visited.add(v)
        
        for w in neighbors(v):
            if w not in visited:
                heap.push((edge_weight(v, w), v, w))
    
    return mst
```

### Correctness Proof (Cut Property)

**Cut Property:** For any cut (S, V-S), minimum weight edge crossing cut is in MST.

**Proof by Contradiction:**

Assume minimum edge e = (u, v) crossing cut is not in MST.

Let T be MST. Adding e to T creates cycle.

Cycle must cross cut at some other edge e' = (x, y).

Since e is minimum crossing cut: weight(e) ≤ weight(e')

Create T' = T - {e'} + {e}

weight(T') ≤ weight(T)

But T was MST, so weight(T') = weight(T)

Therefore, T' is also MST containing e. ✓

**Prim's Correctness:**

Prim's algorithm always selects minimum weight edge crossing current cut.

By cut property, this edge is in some MST.

Therefore, Prim's algorithm constructs an MST. ✓

### Complexity Analysis

**Time Complexity:** O(E log V)

**Proof:**
```
- Each vertex added to MST once: O(V)
- Each edge considered once: O(E)
- Heap operations: O(log V)
- Total: O(E log V)
```

---

## Divide and Conquer: Load Balancing

### Algorithm Description
```
function balance(nodes, files):
    if len(nodes) == 1:
        return {nodes[0]: files}
    
    mid = len(nodes) // 2
    left_nodes = nodes[:mid]
    right_nodes = nodes[mid:]
    
    # Partition files
    left_files, right_files = partition(files, left_nodes, right_nodes)
    
    # Recursively balance
    left_result = balance(left_nodes, left_files)
    right_result = balance(right_nodes, right_files)
    
    return merge(left_result, right_result)
```

### Recurrence Relation

```
T(n) = 2T(n/2) + O(n)
```

Where:
- 2T(n/2): Two recursive calls on half the nodes
- O(n): Partitioning files

### Master Theorem Application

**Form:** T(n) = aT(n/b) + f(n)

**Parameters:**
- a = 2 (two subproblems)
- b = 2 (half size each)
- f(n) = O(n) (partitioning cost)

**Analysis:**
```
n^(log_b(a)) = n^(log_2(2)) = n^1 = n

f(n) = O(n) = Θ(n^(log_b(a)))

By Master Theorem Case 2:
T(n) = Θ(n^(log_b(a)) × log n)
     = Θ(n log n)
```

### Correctness Proof

**Claim:** Algorithm balances load proportionally to capacity.

**Proof by Induction:**

**Base case (n=1):** Single node gets all files (trivially balanced).

**Inductive hypothesis:** Assume correct for n/2 nodes.

**Inductive step:** For n nodes:
- Partition files proportionally to left/right capacity
- Recursively balance each half (correct by IH)
- Merge results (preserves balance)

Therefore, algorithm is correct. ✓

---

## Dynamic Programming: 0/1 Knapsack

### Algorithm Description
```
function knapsack(items, capacity):
    dp = array[n+1][W+1] initialized to 0
    
    for i from 1 to n:
        for w from 0 to W:
            if size[i] <= w:
                dp[i][w] = max(
                    dp[i-1][w],
                    dp[i-1][w-size[i]] + value[i]
                )
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp[n][W]
```

### Optimal Substructure

**Claim:** Optimal solution for n items contains optimal solution for n-1 items.

**Proof:**

Let OPT(i, w) = optimal value using first i items with capacity w.

**Case 1:** Item i not in optimal solution
- OPT(i, w) = OPT(i-1, w)

**Case 2:** Item i in optimal solution
- OPT(i, w) = value[i] + OPT(i-1, w-size[i])

If OPT(i-1, w-size[i]) was not optimal, we could improve OPT(i, w).

Contradiction. Therefore, optimal substructure holds. ✓

### Recurrence Relation

```
OPT(i, w) = max(
    OPT(i-1, w),                      // Don't take item i
    OPT(i-1, w-size[i]) + value[i]    // Take item i
)

Base cases:
OPT(0, w) = 0 for all w
OPT(i, 0) = 0 for all i
```

### Correctness Proof

**Claim:** DP algorithm computes optimal solution.

**Proof by Induction:**

**Base case:** OPT(0, w) = 0 (no items, no value) ✓

**Inductive hypothesis:** Assume dp[i-1][w] is correct for all w.

**Inductive step:** For dp[i][w]:
- By optimal substructure, optimal solution is max of two cases
- Case 1: dp[i-1][w] (correct by IH)
- Case 2: dp[i-1][w-size[i]] + value[i] (correct by IH)
- Taking maximum gives optimal solution ✓

### Complexity Analysis

**Time Complexity:** O(n × W)

**Proof:**
```
T(n, W) = Σ(i=1 to n) Σ(w=0 to W) O(1)
        = n × W × O(1)
        = O(n × W)
```

**Space Complexity:** O(n × W)
- DP table: (n+1) × (W+1)

**Optimization:** Can reduce to O(W) using rolling array.

---

## Summary of Correctness Proofs

| Algorithm | Proof Technique | Key Property |
|-----------|----------------|--------------|
| Risk Calculation | Direct proof | Bounded computation |
| Greedy Selection | Exchange argument | Greedy choice property |
| Min Replicas (DP) | Induction | Optimal substructure |
| Migration | Greedy analysis | Availability improvement |
| Dijkstra | Induction | Greedy choice on graphs |
| Prim's MST | Cut property | Minimum edge property |
| Load Balance | Induction | Recursive correctness |
| Knapsack | Induction | Optimal substructure |

---

## Complexity Class Summary

All algorithms in this project are in class P (polynomial time):

- O(N): Linear algorithms (risk calculation, failure simulation)
- O(N log N): Sorting-based algorithms (greedy selection, DP)
- O(E log V): Graph algorithms (Dijkstra, Prim)
- O(n × W): Pseudo-polynomial (Knapsack)

No NP-complete problems are solved exactly (all solutions are polynomial).

---

## References

1. Cormen, T. H., et al. "Introduction to Algorithms" (CLRS), 3rd Edition
2. Kleinberg, J., & Tardos, É. "Algorithm Design", 2005
3. Dasgupta, S., et al. "Algorithms", 2006