"""
GRAPH ALGORITHMS FOR DISTRIBUTED NETWORK TOPOLOGY

DAA CONCEPTS:
- Graph representation of distributed network
- Shortest path algorithms for optimal routing
- Minimum spanning tree for efficient replication
- Network flow for load balancing
"""

import heapq
from collections import defaultdict

class NetworkGraph:
    """
    Graph representation of distributed storage network
    
    Nodes = Storage nodes
    Edges = Network connections with latency/cost
    """
    
    def __init__(self, nodes):
        """
        Initialize network graph
        
        Args:
            nodes: List of Node objects
        """
        self.nodes = {node.id: node for node in nodes}
        self.edges = defaultdict(dict)  # adjacency list with weights
        self.num_nodes = len(nodes)
    
    def add_edge(self, node1_id, node2_id, latency=1.0):
        """Add bidirectional edge with latency weight"""
        self.edges[node1_id][node2_id] = latency
        self.edges[node2_id][node1_id] = latency
    
    def dijkstra_shortest_path(self, source_id, target_id):
        """
        DIJKSTRA'S ALGORITHM for shortest path
        
        ALGORITHM PARADIGM: Greedy Algorithm
        
        GREEDY CHOICE: Always expand node with minimum distance
        
        Time Complexity: O(E log V) with min-heap
        Space Complexity: O(V)
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
        
        Returns:
            tuple: (distance, path)
        """
        if source_id not in self.nodes or target_id not in self.nodes:
            return float('inf'), []
        
        # Initialize distances
        distances = {node_id: float('inf') for node_id in self.nodes}
        distances[source_id] = 0
        
        # Track paths
        previous = {node_id: None for node_id in self.nodes}
        
        # Min-heap: (distance, node_id)
        heap = [(0, source_id)]
        visited = set()
        
        while heap:
            current_dist, current_id = heapq.heappop(heap)
            
            if current_id in visited:
                continue
            
            visited.add(current_id)
            
            # Found target
            if current_id == target_id:
                break
            
            # Explore neighbors
            for neighbor_id, edge_weight in self.edges[current_id].items():
                if neighbor_id in visited:
                    continue
                
                new_dist = current_dist + edge_weight
                
                # GREEDY CHOICE: Update if shorter path found
                if new_dist < distances[neighbor_id]:
                    distances[neighbor_id] = new_dist
                    previous[neighbor_id] = current_id
                    heapq.heappush(heap, (new_dist, neighbor_id))
        
        if distances[target_id] == float('inf'):
            return float('inf'), []

        # Reconstruct path
        path = []
        current = target_id
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        
        return distances[target_id], path
    
    def prim_mst(self):
        """
        PRIM'S ALGORITHM for Minimum Spanning Tree
        
        ALGORITHM PARADIGM: Greedy Algorithm
        
        PURPOSE: Find minimum cost network to connect all nodes
        USE CASE: Efficient replication topology
        
        GREEDY CHOICE: Always add minimum weight edge connecting tree to non-tree node
        
        Time Complexity: O(E log V)
        Space Complexity: O(V)
        
        Returns:
            list: Edges in MST as (node1, node2, weight) tuples
        """
        if not self.nodes:
            return []
        
        # Start from arbitrary node
        start_node = next(iter(self.nodes.keys()))
        
        # Track nodes in MST
        in_mst = {start_node}
        mst_edges = []
        
        # Min-heap: (weight, node_in_mst, node_not_in_mst)
        heap = []
        for neighbor, weight in self.edges[start_node].items():
            heapq.heappush(heap, (weight, start_node, neighbor))
        
        while heap and len(in_mst) < len(self.nodes):
            weight, from_node, to_node = heapq.heappop(heap)
            
            if to_node in in_mst:
                continue
            
            # GREEDY CHOICE: Add minimum weight edge
            mst_edges.append((from_node, to_node, weight))
            in_mst.add(to_node)
            
            # Add new edges from newly added node
            for neighbor, edge_weight in self.edges[to_node].items():
                if neighbor not in in_mst:
                    heapq.heappush(heap, (edge_weight, to_node, neighbor))
        
        return mst_edges
    
    def find_k_nearest_nodes(self, source_id, k):
        """
        Find K nearest nodes to source using Dijkstra
        
        ALGORITHM: Modified Dijkstra's algorithm
        
        Time Complexity: O(E log V)
        
        Args:
            source_id: Source node ID
            k: Number of nearest nodes to find
        
        Returns:
            list: K nearest node IDs with distances
        """
        if source_id not in self.nodes:
            return []
        
        # Run Dijkstra from source
        distances = {node_id: float('inf') for node_id in self.nodes}
        distances[source_id] = 0
        
        heap = [(0, source_id)]
        visited = set()
        nearest = []
        
        while heap and len(nearest) < k:
            current_dist, current_id = heapq.heappop(heap)
            
            if current_id in visited:
                continue
            
            visited.add(current_id)
            
            if current_id != source_id:
                nearest.append((current_id, current_dist))
            
            # Explore neighbors
            for neighbor_id, edge_weight in self.edges[current_id].items():
                if neighbor_id not in visited:
                    new_dist = current_dist + edge_weight
                    if new_dist < distances[neighbor_id]:
                        distances[neighbor_id] = new_dist
                        heapq.heappush(heap, (new_dist, neighbor_id))
        
        return nearest

def build_network_topology(nodes, connectivity=0.5):
    """
    Build network graph with random topology
    
    Args:
        nodes: List of Node objects
        connectivity: Probability of edge between nodes (0-1)
    
    Returns:
        NetworkGraph: Constructed network graph
    """
    import random
    
    graph = NetworkGraph(nodes)
    
    # Create edges based on connectivity
    for i, node1 in enumerate(nodes):
        for node2 in nodes[i+1:]:
            if random.random() < connectivity:
                # Random latency between 1-10 ms
                latency = random.uniform(1.0, 10.0)
                graph.add_edge(node1.id, node2.id, latency)
    
    return graph

def select_replicas_with_topology(nodes, file, num_replicas, graph):
    """
    Select replica nodes considering network topology
    
    ALGORITHM: Greedy selection with distance constraint
    
    STRATEGY:
    - Select diverse nodes (not too close together)
    - Minimize maximum distance between replicas
    - Balance reliability and network cost
    
    Args:
        nodes: List of Node objects
        file: File object
        num_replicas: Number of replicas needed
        graph: NetworkGraph object
    
    Returns:
        list: Selected node IDs
    """
    from replication import calculate_node_score
    
    # Score all nodes
    candidates = []
    for node in nodes:
        if node.status == "alive" and node.has_capacity(file.size):
            score = calculate_node_score(node)
            candidates.append((score, node.id))
    
    candidates.sort(reverse=True)
    
    if not candidates:
        return []
    
    # Greedy selection with diversity
    selected = [candidates[0][1]]  # Start with best node
    
    while len(selected) < num_replicas and len(selected) < len(candidates):
        best_candidate = None
        best_score = -float('inf')
        
        # Find candidate that maximizes: node_score + min_distance_to_selected
        for score, node_id in candidates:
            if node_id in selected:
                continue
            
            # Calculate minimum distance to already selected nodes
            min_dist = float('inf')
            for selected_id in selected:
                dist, _ = graph.dijkstra_shortest_path(node_id, selected_id)
                min_dist = min(min_dist, dist)
            
            # Prefer reachable candidates; disconnected candidates are deprioritized.
            if min_dist == float('inf'):
                combined_score = -float('inf')
            else:
                # Combined score: balance quality and diversity
                combined_score = score + 0.1 * min_dist
            
            if combined_score > best_score:
                best_score = combined_score
                best_candidate = node_id
        
        if best_candidate:
            selected.append(best_candidate)
        else:
            break
    
    return selected
