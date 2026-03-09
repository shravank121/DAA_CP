"""
OPTIONAL: Network Visualization
Visualizes the distributed cluster using networkx and matplotlib

Note: Requires installation of networkx and matplotlib:
    pip install networkx matplotlib
"""

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Warning: networkx and matplotlib not installed. Visualization disabled.")
    print("Install with: pip install networkx matplotlib")

def visualize_cluster(nodes, files, title="Distributed Storage Cluster"):
    """
    Visualize the distributed storage cluster
    
    Args:
        nodes: List of Node objects
        files: List of File objects
        title: Title for the visualization
    """
    if not VISUALIZATION_AVAILABLE:
        print("Visualization libraries not available")
        return
    
    # Create graph
    G = nx.Graph()
    
    # Add nodes
    for node in nodes:
        G.add_node(node.id, status=node.status, load=node.current_load)
    
    # Add edges (fully connected for simplicity)
    for i, node1 in enumerate(nodes):
        for node2 in nodes[i+1:]:
            if node1.status == "alive" and node2.status == "alive":
                G.add_edge(node1.id, node2.id)
    
    # Set up colors
    node_colors = []
    for node in nodes:
        if node.status == "alive":
            node_colors.append('lightgreen')
        else:
            node_colors.append('red')
    
    # Create layout
    pos = nx.spring_layout(G, seed=42)
    
    # Draw
    plt.figure(figsize=(12, 8))
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=800, alpha=0.9)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    
    # Draw labels
    labels = {node.id: f"N{node.id}\n{node.current_load:.2f}" 
              for node in nodes}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def visualize_file_replicas(nodes, file, title=None):
    """
    Visualize replica distribution for a specific file
    
    Args:
        nodes: List of Node objects
        file: File object to visualize
        title: Optional title
    """
    if not VISUALIZATION_AVAILABLE:
        print("Visualization libraries not available")
        return
    
    if title is None:
        title = f"Replica Distribution for {file.id}"
    
    # Create graph
    G = nx.Graph()
    
    # Add all nodes
    for node in nodes:
        G.add_node(node.id, status=node.status, has_replica=node.id in file.replicas)
    
    # Add edges between nodes with replicas
    replica_nodes = [n for n in nodes if n.id in file.replicas]
    for i, node1 in enumerate(replica_nodes):
        for node2 in replica_nodes[i+1:]:
            G.add_edge(node1.id, node2.id)
    
    # Set up colors
    node_colors = []
    for node in nodes:
        if node.id in file.replicas:
            if node.status == "alive":
                node_colors.append('gold')
            else:
                node_colors.append('orange')
        else:
            if node.status == "alive":
                node_colors.append('lightgray')
            else:
                node_colors.append('darkgray')
    
    # Create layout
    pos = nx.spring_layout(G, seed=42)
    
    # Draw
    plt.figure(figsize=(10, 8))
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=600, alpha=0.9)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.5, width=2)
    
    # Draw labels
    labels = {node.id: f"N{node.id}" for node in nodes}
    nx.draw_networkx_labels(G, pos, labels, font_size=10)
    
    plt.title(title)
    plt.axis('off')
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', 
                   markerfacecolor='gold', markersize=10, label='Has Replica (Alive)'),
        plt.Line2D([0], [0], marker='o', color='w', 
                   markerfacecolor='orange', markersize=10, label='Has Replica (Failed)'),
        plt.Line2D([0], [0], marker='o', color='w', 
                   markerfacecolor='lightgray', markersize=10, label='No Replica (Alive)'),
        plt.Line2D([0], [0], marker='o', color='w', 
                   markerfacecolor='darkgray', markersize=10, label='No Replica (Failed)')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    plt.show()

def plot_availability_over_time(availability_history):
    """
    Plot system availability over simulation time
    
    Args:
        availability_history: List of (time_step, availability) tuples
    """
    if not VISUALIZATION_AVAILABLE:
        print("Visualization libraries not available")
        return
    
    time_steps = [t for t, _ in availability_history]
    availability = [a * 100 for _, a in availability_history]
    
    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, availability, marker='o', linewidth=2, markersize=6)
    plt.xlabel('Time Step')
    plt.ylabel('System Availability (%)')
    plt.title('System Availability Over Time')
    plt.grid(True, alpha=0.3)
    plt.ylim([95, 100])
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    from simulator import DistributedStorageSimulator
    import random
    
    random.seed(42)
    
    # Create simulator
    sim = DistributedStorageSimulator(num_nodes=10, num_files=5)
    sim.initial_replica_placement(min_replicas=3)
    
    # Visualize initial state
    if VISUALIZATION_AVAILABLE:
        visualize_cluster(sim.nodes, sim.files, "Initial Cluster State")
        visualize_file_replicas(sim.nodes, sim.files[0])
    
    # Run simulation and track availability
    availability_history = []
    for step in range(5):
        sim.run_simulation_step()
        status = sim.get_system_status()
        availability_history.append((step + 1, status['system_availability']))
    
    # Visualize final state
    if VISUALIZATION_AVAILABLE:
        visualize_cluster(sim.nodes, sim.files, "Final Cluster State")
        plot_availability_over_time(availability_history)
