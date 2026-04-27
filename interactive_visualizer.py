"""
Interactive Visualizer for DAA Algorithms
Shows step-by-step execution of Greedy, Dynamic Programming, and Graph Algorithms
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
import numpy as np
from simulator import DistributedStorageSimulator
import random
from collections import defaultdict

class InteractiveVisualizer:
    def __init__(self, num_nodes=10, num_files=5):
        """
        Initialize the interactive visualizer
        
        Args:
            num_nodes: Number of nodes in the cluster
            num_files: Number of files to store
        """
        self.simulator = DistributedStorageSimulator(num_nodes, num_files, 0.6)
        self.num_nodes = num_nodes
        self.num_files = num_files
        
        # Algorithm step tracking
        self.current_step = 0
        self.algorithm_steps = []
        self.current_algorithm = None
        
        # Set up the figure
        self.fig = plt.figure(figsize=(18, 12))
        self.fig.suptitle('Interactive DAA Algorithms Visualizer', fontsize=16, fontweight='bold')
        
        # Create subplots
        gs = self.fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        self.ax_main = self.fig.add_subplot(gs[:2, :2])  # Main visualization
        self.ax_algorithm = self.fig.add_subplot(gs[0, 2])  # Algorithm details
        self.ax_complexity = self.fig.add_subplot(gs[1, 2])  # Complexity analysis
        self.ax_code = self.fig.add_subplot(gs[2, :])  # Code explanation
        
        self._setup_plots()
        
    def _setup_plots(self):
        """Set up initial plot configurations"""
        self.ax_main.set_title('Algorithm Execution Visualization')
        self.ax_main.axis('off')
        
        self.ax_algorithm.set_title('Algorithm Steps')
        self.ax_algorithm.axis('off')
        
        self.ax_complexity.set_title('Complexity Analysis')
        self.ax_complexity.axis('off')
        
        self.ax_code.set_title('Code & Explanation')
        self.ax_code.axis('off')
    
    def visualize_greedy_replica_selection(self):
        """Visualize Greedy Algorithm for Replica Selection"""
        self.current_algorithm = "Greedy Replica Selection"
        
        # Initialize
        self.simulator.initial_replica_placement(min_replicas=1)
        
        # Get a file to demonstrate
        file = self.simulator.files[0]
        
        # Calculate scores for all nodes
        from replication import select_replica_nodes
        candidates = select_replica_nodes(self.simulator.nodes, file, len(self.simulator.nodes))
        
        # Create algorithm steps
        self.algorithm_steps = []
        for i, (score, node_id) in enumerate(candidates[:5]):  # Show top 5
            node = self.simulator.nodes[node_id]
            step = {
                'step': i + 1,
                'node_id': node_id,
                'score': score,
                'reliability': node.reliability,
                'trust_score': node.trust_score,
                'load': node.current_load,
                'selected': i < 3  # Select top 3
            }
            self.algorithm_steps.append(step)
        
        self._animate_greedy_algorithm()
    
    def _animate_greedy_algorithm(self):
        """Animate the greedy algorithm execution"""
        self.fig.clear()
        
        # Recreate subplots
        gs = self.fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        self.ax_main = self.fig.add_subplot(gs[:2, :2])
        self.ax_algorithm = self.fig.add_subplot(gs[0, 2])
        self.ax_complexity = self.fig.add_subplot(gs[1, 2])
        self.ax_code = self.fig.add_subplot(gs[2, :])
        
        # Draw network with greedy selection
        self._draw_greedy_network()
        
        # Draw algorithm steps
        self._draw_greedy_steps()
        
        # Draw complexity analysis
        self._draw_greedy_complexity()
        
        # Draw code explanation
        self._draw_greedy_code()
        
        plt.tight_layout()
        plt.show()
    
    def _draw_greedy_network(self):
        """Draw network showing greedy selection process"""
        self.ax_main.clear()
        self.ax_main.set_title('Greedy Replica Selection - Node Scoring')
        self.ax_main.axis('off')
        
        # Create network layout
        G = nx.Graph()
        for node in self.simulator.nodes:
            G.add_node(node.id)
        
        # Add edges between alive nodes
        for i, node1 in enumerate(self.simulator.nodes):
            for node2 in self.simulator.nodes[i+1:]:
                if node1.status == "alive" and node2.status == "alive":
                    G.add_edge(node1.id, node2.id)
        
        pos = nx.spring_layout(G, seed=42)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.2, ax=self.ax_main)
        
        # Draw nodes with colors based on greedy selection
        node_colors = []
        node_sizes = []
        node_labels = {}
        
        for node in self.simulator.nodes:
            # Find if this node is in our algorithm steps
            step_info = next((s for s in self.algorithm_steps if s['node_id'] == node.id), None)
            
            if step_info:
                if step_info['selected']:
                    node_colors.append('gold')  # Selected
                    node_sizes.append(800)
                    node_labels[node.id] = f"N{node.id}\nScore: {step_info['score']:.3f}\n✓"
                else:
                    node_colors.append('lightblue')  # Considered but not selected
                    node_sizes.append(600)
                    node_labels[node.id] = f"N{node.id}\nScore: {step_info['score']:.3f}"
            else:
                node_colors.append('lightgray')  # Not considered
                node_sizes.append(400)
                node_labels[node.id] = f"N{node.id}"
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=node_sizes, alpha=0.8, ax=self.ax_main)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, node_labels, font_size=8, ax=self.ax_main)
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gold', 
                      markersize=10, label='Selected Nodes'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', 
                      markersize=10, label='Considered Nodes'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgray', 
                      markersize=10, label='Not Considered')
        ]
        self.ax_main.legend(handles=legend_elements, loc='upper right')
    
    def _draw_greedy_steps(self):
        """Draw greedy algorithm step-by-step execution"""
        self.ax_algorithm.clear()
        self.ax_algorithm.set_title('Greedy Algorithm Steps')
        self.ax_algorithm.axis('off')
        
        step_text = "Greedy Selection Process:\n" + "="*40 + "\n"
        
        for i, step in enumerate(self.algorithm_steps):
            status = "✓ SELECTED" if step['selected'] else "○ Considered"
            step_text += f"Step {step['step']}: Node {step['node_id']}\n"
            step_text += f"  Score: {step['score']:.3f} {status}\n"
            step_text += f"  Reliability: {step['reliability']:.3f}\n"
            step_text += f"  Trust: {step['trust_score']:.3f}\n"
            step_text += f"  Load: {step['load']:.3f}\n"
            step_text += "-"*30 + "\n"
        
        self.ax_algorithm.text(0.05, 0.95, step_text, transform=self.ax_algorithm.transAxes,
                              verticalalignment='top', fontfamily='monospace', fontsize=9,
                              bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    def _draw_greedy_complexity(self):
        """Draw complexity analysis for greedy algorithm"""
        self.ax_complexity.clear()
        self.ax_complexity.set_title('Complexity Analysis')
        self.ax_complexity.axis('off')
        
        complexity_text = """
Greedy Algorithm Complexity:

Time Complexity: O(N log N)
- Sorting N nodes by score: O(N log N)
- Selecting top K nodes: O(K)
- Overall: O(N log N)

Space Complexity: O(N)
- Score array: O(N)
- Sorted list: O(N)
- Result storage: O(K)

Greedy Choice Property:
✓ Locally optimal choice leads to
  globally optimal solution

Optimal Substructure:
✓ Best K nodes = Best node + 
  Best (K-1) from remaining

Proof of Optimality:
By induction on K:
- Base K=1: Trivially optimal
- Inductive step: Assume optimal for K-1
- Adding best remaining node maintains optimality
        """
        
        self.ax_complexity.text(0.05, 0.95, complexity_text, transform=self.ax_complexity.transAxes,
                               verticalalignment='top', fontfamily='monospace', fontsize=8,
                               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    def _draw_greedy_code(self):
        """Draw code explanation for greedy algorithm"""
        self.ax_code.clear()
        self.ax_code.set_title('Greedy Algorithm Implementation')
        self.ax_code.axis('off')
        
        code_text = """
# Greedy Replica Selection Algorithm
def select_replica_nodes(nodes, file, k):
    '''
    Greedy Algorithm: Select k best nodes for replicas
    
    Greedy Choice: Always select node with highest score
    Score = reliability + trust - load - network_cost
    '''
    
    # Step 1: Calculate scores for all nodes
    candidates = []
    for node in nodes:
        if node.status == "alive" and node.can_store_file(file):
            score = (node.reliability + 
                    node.trust_score - 
                    node.current_load - 
                    network_cost(node, file))
            candidates.append((score, node.id))
    
    # Step 2: Sort by score (descending) - GREEDY CHOICE
    candidates.sort(reverse=True, key=lambda x: x[0])
    
    # Step 3: Select top k nodes - OPTIMAL SUBSTRUCTURE
    selected_nodes = [node_id for score, node_id in candidates[:k]]
    
    return selected_nodes

# Why this works:
# 1. Greedy Choice Property: Selecting highest-scored node is always optimal
# 2. Optimal Substructure: After selecting best node, problem reduces to selecting k-1 from remaining
# 3. Exchange Argument: Any optimal solution can be transformed to greedy solution without reducing quality
        """
        
        self.ax_code.text(0.02, 0.98, code_text, transform=self.ax_code.transAxes,
                         verticalalignment='top', fontfamily='monospace', fontsize=8,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    def visualize_dynamic_programming(self):
        """Visualize Dynamic Programming for Minimum Replicas"""
        self.current_algorithm = "Dynamic Programming - Minimum Replicas"
        
        # Calculate minimum replicas needed for different availability targets
        from replication import calculate_minimum_replicas
        
        # Create availability targets and calculate minimum replicas
        availability_targets = [0.90, 0.95, 0.99, 0.999]
        dp_results = []
        
        for target in availability_targets:
            min_replicas, availability = calculate_minimum_replicas(
                self.simulator.nodes, target
            )
            dp_results.append({
                'target': target,
                'min_replicas': min_replicas,
                'actual_availability': availability
            })
        
        self._animate_dp_algorithm(dp_results)
    
    def _animate_dp_algorithm(self, dp_results):
        """Animate the DP algorithm"""
        self.fig.clear()
        
        # Recreate subplots
        gs = self.fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        self.ax_main = self.fig.add_subplot(gs[:2, :2])
        self.ax_algorithm = self.fig.add_subplot(gs[0, 2])
        self.ax_complexity = self.fig.add_subplot(gs[1, 2])
        self.ax_code = self.fig.add_subplot(gs[2, :])
        
        # Draw DP table
        self._draw_dp_table(dp_results)
        
        # Draw DP steps
        self._draw_dp_steps(dp_results)
        
        # Draw DP complexity
        self._draw_dp_complexity()
        
        # Draw DP code
        self._draw_dp_code()
        
        plt.tight_layout()
        plt.show()
    
    def _draw_dp_table(self, dp_results):
        """Draw DP table visualization"""
        self.ax_main.clear()
        self.ax_main.set_title('Dynamic Programming: Minimum Replicas Calculation')
        self.ax_main.axis('off')
        
        # Create a visual table
        table_data = []
        for result in dp_results:
            table_data.append([
                f"{result['target']*100:.1f}%",
                f"{result['min_replicas']}",
                f"{result['actual_availability']*100:.3f}%"
            ])
        
        # Draw table
        col_labels = ['Target Availability', 'Min Replicas', 'Actual Availability']
        row_labels = [f"Case {i+1}" for i in range(len(dp_results))]
        
        table = self.ax_main.table(cellText=table_data,
                                 colLabels=col_labels,
                                 rowLabels=row_labels,
                                 cellLoc='center',
                                 loc='center',
                                 bbox=[0.2, 0.3, 0.6, 0.4])
        
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Color code the table
        for i in range(len(dp_results)):
            for j in range(3):
                cell = table[(i+1, j)]
                if dp_results[i]['actual_availability'] >= dp_results[i]['target']:
                    cell.set_facecolor('lightgreen')
                else:
                    cell.set_facecolor('lightyellow')
        
        # Add DP formula
        formula_text = """
DP Recurrence Relation:
Availability(k) = 1 - Π(failure_prob[i]) for i = 0 to k-1

Where failure_prob is sorted in ascending order
        """
        
        self.ax_main.text(0.5, 0.1, formula_text, transform=self.ax_main.transAxes,
                         horizontalalignment='center', fontsize=10,
                         bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    def _draw_dp_steps(self, dp_results):
        """Draw DP step-by-step explanation"""
        self.ax_algorithm.clear()
        self.ax_algorithm.set_title('DP Algorithm Steps')
        self.ax_algorithm.axis('off')
        
        steps_text = "Dynamic Programming Process:\n" + "="*40 + "\n"
        
        for i, result in enumerate(dp_results):
            steps_text += f"Case {i+1}: Target {result['target']*100:.1f}%\n"
            steps_text += f"  Step 1: Sort nodes by failure probability\n"
            steps_text += f"  Step 2: Calculate availability for k=1,2,3...\n"
            steps_text += f"  Step 3: Find minimum k meeting target\n"
            steps_text += f"  Result: k={result['min_replicas']} replicas\n"
            steps_text += f"  Actual: {result['actual_availability']*100:.3f}%\n"
            steps_text += "-"*30 + "\n"
        
        self.ax_algorithm.text(0.05, 0.95, steps_text, transform=self.ax_algorithm.transAxes,
                              verticalalignment='top', fontfamily='monospace', fontsize=9,
                              bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    def _draw_dp_complexity(self):
        """Draw DP complexity analysis"""
        self.ax_complexity.clear()
        self.ax_complexity.set_title('DP Complexity Analysis')
        self.ax_complexity.axis('off')
        
        complexity_text = """
DP Algorithm Complexity:

Time Complexity: O(N log N)
- Sorting nodes by failure prob: O(N log N)
- DP table calculation: O(N × K) where K ≤ N
- Overall: O(N log N)

Space Complexity: O(N)
- DP array: O(N)
- Sorted nodes: O(N)

Optimal Substructure:
✓ Minimum k for target A depends on
  minimum k-1 for target A'

Overlapping Subproblems:
✓ Same availability calculations
  reused across different targets
        """
        
        self.ax_complexity.text(0.05, 0.95, complexity_text, transform=self.ax_complexity.transAxes,
                               verticalalignment='top', fontfamily='monospace', fontsize=8,
                               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    def _draw_dp_code(self):
        """Draw DP code explanation"""
        self.ax_code.clear()
        self.ax_code.set_title('Dynamic Programming Implementation')
        self.ax_code.axis('off')
        
        code_text = """
# Dynamic Programming: Minimum Replicas
def calculate_minimum_replicas(nodes, target_availability):
    '''
    DP: Find minimum replicas for target availability
    
    DP State: dp[k] = availability with k best nodes
    Recurrence: dp[k] = 1 - Π(failure_prob[i]) for i = 0 to k-1
    '''
    
    # Step 1: Sort nodes by failure probability (ascending)
    sorted_nodes = sorted(nodes, key=lambda n: n.failure_probability)
    
    # Step 2: Build DP table
    dp = [0.0] * (len(sorted_nodes) + 1)
    dp[0] = 0.0  # 0 replicas = 0 availability
    
    for k in range(1, len(sorted_nodes) + 1):
        # Calculate availability with k best nodes
        failure_prob_product = 1.0
        for i in range(k):
            failure_prob_product *= sorted_nodes[i].failure_probability
        
        dp[k] = 1.0 - failure_prob_product
        
        # Step 3: Check if target met
        if dp[k] >= target_availability:
            return k, dp[k]
    
    return len(sorted_nodes), dp[-1]

# Why DP works:
# 1. Optimal Substructure: Optimal solution for k depends on k-1
# 2. Overlapping Subproblems: Same failure_prob calculations reused
# 3. Memoization: DP table stores intermediate results
        """
        
        self.ax_code.text(0.02, 0.98, code_text, transform=self.ax_code.transAxes,
                         verticalalignment='top', fontfamily='monospace', fontsize=8,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    def visualize_graph_algorithm(self):
        """Visualize Graph Algorithm (Dijkstra's Shortest Path)"""
        self.current_algorithm = "Graph Algorithm - Dijkstra's Shortest Path"
        
        # Create a network topology
        from graph_algorithms import dijkstra_shortest_path
        
        # Create a simple graph for demonstration
        graph = self._create_sample_graph()
        
        # Find shortest path from node 0 to node 9
        path, distance = dijkstra_shortest_path(graph, 0, 9)
        
        self._animate_graph_algorithm(graph, path, distance)
    
    def _create_sample_graph(self):
        """Create a sample graph for demonstration"""
        # Create a graph with weighted edges
        graph = {}
        num_nodes = 10
        
        for i in range(num_nodes):
            graph[i] = {}
        
        # Add edges with weights (representing network costs)
        edges = [
            (0, 1, 2), (0, 2, 5), (1, 2, 1), (1, 3, 3),
            (2, 3, 2), (2, 4, 4), (3, 4, 1), (3, 5, 5),
            (4, 5, 3), (4, 6, 2), (5, 6, 4), (5, 7, 1),
            (6, 7, 3), (6, 8, 2), (7, 8, 1), (7, 9, 4),
            (8, 9, 2)
        ]
        
        for u, v, w in edges:
            graph[u][v] = w
            graph[v][u] = w
        
        return graph
    
    def _animate_graph_algorithm(self, graph, path, distance):
        """Animate the graph algorithm"""
        self.fig.clear()
        
        # Recreate subplots
        gs = self.fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        self.ax_main = self.fig.add_subplot(gs[:2, :2])
        self.ax_algorithm = self.fig.add_subplot(gs[0, 2])
        self.ax_complexity = self.fig.add_subplot(gs[1, 2])
        self.ax_code = self.fig.add_subplot(gs[2, :])
        
        # Draw graph with shortest path
        self._draw_graph_with_path(graph, path)
        
        # Draw algorithm steps
        self._draw_dijkstra_steps(graph, path, distance)
        
        # Draw complexity
        self._draw_dijkstra_complexity()
        
        # Draw code
        self._draw_dijkstra_code()
        
        plt.tight_layout()
        plt.show()
    
    def _draw_graph_with_path(self, graph, path):
        """Draw graph with shortest path highlighted"""
        self.ax_main.clear()
        self.ax_main.set_title("Dijkstra's Algorithm - Shortest Path")
        self.ax_main.axis('off')
        
        # Create networkx graph
        G = nx.Graph()
        
        # Add edges
        for u in graph:
            for v, w in graph[u].items():
                if u < v:  # Avoid duplicate edges
                    G.add_edge(u, v, weight=w)
        
        # Layout
        pos = nx.spring_layout(G, seed=42)
        
        # Draw all edges in gray
        nx.draw_networkx_edges(G, pos, alpha=0.3, width=1, ax=self.ax_main)
        
        # Highlight shortest path
        if len(path) > 1:
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, 
                                 edge_color='red', width=3, alpha=0.8, ax=self.ax_main)
        
        # Draw nodes
        node_colors = []
        for node in G.nodes():
            if node in path:
                node_colors.append('gold')  # Path nodes
            elif node == path[0]:
                node_colors.append('green')  # Start node
            elif node == path[-1]:
                node_colors.append('red')    # End node
            else:
                node_colors.append('lightblue')  # Other nodes
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=500, alpha=0.8, ax=self.ax_main)
        
        # Draw labels
        labels = {node: f"N{node}" for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=10, ax=self.ax_main)
        
        # Draw edge weights
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, ax=self.ax_main)
        
        # Add path information
        path_text = f"Shortest Path: {' → '.join(map(str, path))}\nTotal Distance: {distance}"
        self.ax_main.text(0.5, 0.05, path_text, transform=self.ax_main.transAxes,
                         horizontalalignment='center', fontsize=10,
                         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    def _draw_dijkstra_steps(self, graph, path, distance):
        """Draw Dijkstra algorithm steps"""
        self.ax_algorithm.clear()
        self.ax_algorithm.set_title('Dijkstra Algorithm Steps')
        self.ax_algorithm.axis('off')
        
        steps_text = """
Dijkstra's Algorithm Execution:

Initialization:
- Distance to source = 0
- Distance to all others = ∞
- All nodes unvisited

Main Loop:
1. Select unvisited node with minimum distance
2. Mark as visited
3. Update distances to neighbors
4. Repeat until destination visited

Greedy Choice:
✓ Always pick closest unvisited node
✓ Leads to optimal shortest path

Result:
- Shortest path found
- All shortest distances known
        """
        
        self.ax_algorithm.text(0.05, 0.95, steps_text, transform=self.ax_algorithm.transAxes,
                              verticalalignment='top', fontfamily='monospace', fontsize=9,
                              bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    def _draw_dijkstra_complexity(self):
        """Draw Dijkstra complexity analysis"""
        self.ax_complexity.clear()
        self.ax_complexity.set_title('Dijkstra Complexity Analysis')
        self.ax_complexity.axis('off')
        
        complexity_text = """
Dijkstra's Algorithm Complexity:

Time Complexity: O(E log V)
- Using priority queue (min-heap)
- E = number of edges
- V = number of vertices
- Each edge processed once: O(E log V)

Space Complexity: O(V)
- Distance array: O(V)
- Priority queue: O(V)
- Visited set: O(V)

Greedy Property:
✓ Optimal substructure
✓ Always picks shortest unvisited path
✓ No negative edge weights allowed
        """
        
        self.ax_complexity.text(0.05, 0.95, complexity_text, transform=self.ax_complexity.transAxes,
                               verticalalignment='top', fontfamily='monospace', fontsize=8,
                               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    def _draw_dijkstra_code(self):
        """Draw Dijkstra code explanation"""
        self.ax_code.clear()
        self.ax_code.set_title("Dijkstra's Algorithm Implementation")
        self.ax_code.axis('off')
        
        code_text = """
# Dijkstra's Shortest Path Algorithm
def dijkstra_shortest_path(graph, start, end):
    '''
    Greedy Graph Algorithm: Find shortest path
    
    Strategy: Always expand the closest unvisited node
    Guarantees optimality for non-negative edge weights
    '''
    
    import heapq
    
    # Initialize distances
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Priority queue: (distance, node)
    pq = [(0, start)]
    visited = set()
    previous = {}
    
    while pq:
        # Get closest unvisited node - GREEDY CHOICE
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
            
        visited.add(current)
        
        # Check if reached destination
        if current == end:
            break
        
        # Update neighbor distances
        for neighbor, weight in graph[current].items():
            if neighbor not in visited:
                new_dist = current_dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
    
    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous.get(current)
    path.reverse()
    
    return path, distances[end]

# Why Dijkstra works:
# 1. Greedy Choice Property: Closest unvisited node is optimal
# 2. Optimal Substructure: Shortest path to node depends on shortest path to predecessor
# 3. No Negative Cycles: Guarantees correctness
        """
        
        self.ax_code.text(0.02, 0.98, code_text, transform=self.ax_code.transAxes,
                         verticalalignment='top', fontfamily='monospace', fontsize=8,
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

def main():
    """Main function to run interactive visualizer"""
    print("=" * 70)
    print("INTERACTIVE DAA ALGORITHMS VISUALIZER")
    print("Design and Analysis of Algorithms - Course Project")
    print("=" * 70)
    
    random.seed(42)
    
    # Create visualizer
    visualizer = InteractiveVisualizer(num_nodes=10, num_files=5)
    
    print("\nSelect algorithm to visualize:")
    print("1. Greedy Algorithm - Replica Selection")
    print("2. Dynamic Programming - Minimum Replicas")
    print("3. Graph Algorithm - Dijkstra's Shortest Path")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        print("\nVisualizing Greedy Algorithm...")
        visualizer.visualize_greedy_replica_selection()
    elif choice == "2":
        print("\nVisualizing Dynamic Programming...")
        visualizer.visualize_dynamic_programming()
    elif choice == "3":
        print("\nVisualizing Graph Algorithm...")
        visualizer.visualize_graph_algorithm()
    else:
        print("Invalid choice. Running Greedy Algorithm by default...")
        visualizer.visualize_greedy_replica_selection()
    
    print("\nVisualization complete!")

if __name__ == "__main__":
    main()
