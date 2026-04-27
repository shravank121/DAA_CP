"""
Enhanced Visual Simulator for Distributed Storage System
Real-time animation of the distributed cluster with DAA algorithms in action
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import numpy as np
from simulator import DistributedStorageSimulator
import random
from collections import deque

class VisualSimulator:
    def __init__(self, num_nodes=12, num_files=6, risk_threshold=0.6, target_availability=0.99):
        """
        Initialize the visual simulator
        
        Args:
            num_nodes: Number of nodes in the cluster
            num_files: Number of files to store
            risk_threshold: Threshold for identifying high-risk nodes
            target_availability: Target system availability (default 99%)
        """
        self.simulator = DistributedStorageSimulator(num_nodes, num_files, risk_threshold, target_availability)
        self.num_nodes = num_nodes
        self.num_files = num_files
        self.target_availability = target_availability
        
        # Animation data
        self.availability_history = deque(maxlen=50)
        self.risk_history = deque(maxlen=50)
        self.migration_events = deque(maxlen=10)
        self.failure_events = deque(maxlen=10)
        
        # Set up the figure and subplots
        self.fig = plt.figure(figsize=(20, 14))
        self.fig.suptitle('Distributed Storage System - Real-time Simulation', fontsize=18, fontweight='bold')
        
        # Create subplots with better spacing
        gs = self.fig.add_gridspec(3, 3, hspace=0.4, wspace=0.4, left=0.08, right=0.95, top=0.93, bottom=0.06)
        self.ax_network = self.fig.add_subplot(gs[:2, :2])  # Main network view
        self.ax_availability = self.fig.add_subplot(gs[0, 2])  # Availability chart
        self.ax_risk = self.fig.add_subplot(gs[1, 2])  # Risk heatmap
        self.ax_events = self.fig.add_subplot(gs[2, :])  # Event log
        
        # Initialize plots
        self._setup_plots()
        
    def _setup_plots(self):
        """Set up initial plot configurations"""
        # Network plot setup
        self.ax_network.set_title('Network Topology & File Replicas')
        self.ax_network.axis('off')
        
        # Availability plot setup
        self.ax_availability.set_title('System Availability')
        self.ax_availability.set_xlabel('Time Step')
        self.ax_availability.set_ylabel('Availability (%)')
        self.ax_availability.set_ylim([95, 100])
        self.ax_availability.grid(True, alpha=0.3)
        
        # Risk heatmap setup
        self.ax_risk.set_title('Node Risk Levels')
        self.ax_risk.set_xlabel('Node ID')
        self.ax_risk.set_ylabel('Risk Score')
        
        # Event log setup
        self.ax_events.set_title('System Events')
        self.ax_events.axis('off')
        
    def _get_network_layout(self):
        """Calculate network layout with better spacing"""
        G = nx.Graph()
        
        # Add nodes
        for node in self.simulator.nodes:
            G.add_node(node.id)
        
        # Add edges between alive nodes
        for i, node1 in enumerate(self.simulator.nodes):
            for node2 in self.simulator.nodes[i+1:]:
                if node1.status == "alive" and node2.status == "alive":
                    G.add_edge(node1.id, node2.id)
        
        # Use spring layout with better parameters for spacing
        pos = nx.spring_layout(G, 
                              seed=42, 
                              k=3.0,  # Optimal distance between nodes
                              iterations=50,  # More iterations for better layout
                              threshold=1e-6)  # Convergence threshold
        
        # If we have disconnected nodes, arrange them in a circle
        if len(G.edges()) == 0 or len(pos) < len(self.simulator.nodes):
            # Create a circular layout for all nodes
            circle_pos = nx.circular_layout(G, scale=2.0, seed=42)
            pos.update(circle_pos)
        
        return pos
    
    def _draw_network(self):
        """Draw the network topology with nodes and file replicas"""
        self.ax_network.clear()
        self.ax_network.set_title('Network Topology & File Replicas', fontsize=14, fontweight='bold')
        self.ax_network.axis('off')
        
        pos = self._get_network_layout()
        
        # Draw edges with labels
        G = nx.Graph()
        for node in self.simulator.nodes:
            G.add_node(node.id)
        for i, node1 in enumerate(self.simulator.nodes):
            for node2 in self.simulator.nodes[i+1:]:
                if node1.status == "alive" and node2.status == "alive":
                    G.add_edge(node1.id, node2.id)
        
        nx.draw_networkx_edges(G, pos, alpha=0.3, width=2, ax=self.ax_network)
        
        # Draw nodes with different colors based on status and risk
        node_colors = []
        node_sizes = []
        risk_scores = get_all_risk_scores(self.simulator.nodes)
        
        for node in self.simulator.nodes:
            risk = risk_scores.get(node.id, 0)
            
            if node.status == "failed":
                node_colors.append('red')
                node_sizes.append(600)  # Smaller nodes to reduce overlap
            elif risk > 0.7:
                node_colors.append('darkorange')  # High risk
                node_sizes.append(700)  # Smaller nodes
            elif risk > 0.5:
                node_colors.append('gold')  # Medium risk
                node_sizes.append(650)  # Smaller nodes
            else:
                node_colors.append('lightgreen')  # Low risk
                node_sizes.append(600)  # Smaller nodes
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=node_sizes, alpha=0.8, 
                              edgecolors='black', linewidths=1, ax=self.ax_network)
        
        # Draw node labels with more information
        labels = {}
        for node in self.simulator.nodes:
            risk = risk_scores.get(node.id, 0)
            status = "FAIL" if node.status == "failed" else "ALIVE"
            labels[node.id] = f"N{node.id}\n{status}\nRisk:{risk:.2f}"
        
        nx.draw_networkx_labels(G, pos, labels, font_size=7, ax=self.ax_network)
        
        # Draw file replicas as small circles around nodes
        file_colors = ['blue', 'green', 'purple', 'brown', 'pink', 'cyan']
        legend_files = []
        for file_idx, file in enumerate(self.simulator.files):
            color = file_colors[file_idx % len(file_colors)]
            legend_files.append((file.id, color))
            
            for replica_node_id in file.replicas:
                if replica_node_id < len(pos):
                    # Draw a small circle around the node
                    x, y = pos[replica_node_id]
                    # Offset the replica circles to avoid overlap - increased distance
                    offset_angle = (file_idx * 60) % 360
                    offset_r = 0.15  # Increased from 0.08 to 0.15
                    offset_x = x + offset_r * np.cos(np.radians(offset_angle))
                    offset_y = y + offset_r * np.sin(np.radians(offset_angle))
                    circle = plt.Circle((offset_x, offset_y), 0.025, color=color, alpha=0.8)
                    self.ax_network.add_patch(circle)
        
        # Add comprehensive legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen', 
                      markersize=10, label='Low Risk (≤0.5)'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gold', 
                      markersize=10, label='Medium Risk (0.5-0.7)'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='darkorange', 
                      markersize=10, label='High Risk (>0.7)'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                      markersize=10, label='Failed')
        ]
        
        # Add file legend
        for file_id, color in legend_files:
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                            markerfacecolor=color, markersize=8, label=f'{file_id}'))
        
        self.ax_network.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.02, 0.98), 
                              ncol=2, fontsize=8)
        
        # Set axis limits to ensure all nodes and replicas are visible
        if pos:
            x_coords = [p[0] for p in pos.values()]
            y_coords = [p[1] for p in pos.values()]
            
            # Add padding for replicas
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            
            x_padding = (x_max - x_min) * 0.3
            y_padding = (y_max - y_min) * 0.3
            
            self.ax_network.set_xlim(x_min - x_padding, x_max + x_padding)
            self.ax_network.set_ylim(y_min - y_padding, y_max + y_padding)
    
    def _draw_availability(self):
        """Draw availability over time chart"""
        self.ax_availability.clear()
        self.ax_availability.set_title('System Availability', fontsize=12, fontweight='bold')
        self.ax_availability.set_xlabel('Time Step', fontsize=10)
        self.ax_availability.set_ylabel('Availability (%)', fontsize=10)
        self.ax_availability.set_ylim([95, 100.1])
        self.ax_availability.grid(True, alpha=0.3)
        
        if len(self.availability_history) > 1:
            time_steps = list(range(len(self.availability_history)))
            availability = [a * 100 for a in self.availability_history]
            
            # Draw line with markers
            self.ax_availability.plot(time_steps, availability, 'b-', linewidth=3, 
                                    marker='o', markersize=6, markerfacecolor='blue', 
                                    markeredgecolor='darkblue', markeredgewidth=1)
            
            # Add current value text with background
            if availability:
                current_availability = availability[-1]
                self.ax_availability.text(0.02, 0.98, f'Current: {current_availability:.2f}%', 
                                         transform=self.ax_availability.transAxes, 
                                         verticalalignment='top', fontsize=10, fontweight='bold',
                                         bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', 
                                                 alpha=0.8, edgecolor='blue'))
                
                # Add trend indicator
                if len(availability) >= 2:
                    trend = availability[-1] - availability[-2]
                    trend_symbol = "↑" if trend > 0 else "↓" if trend < 0 else "→"
                    trend_color = 'green' if trend > 0 else 'red' if trend < 0 else 'gray'
                    self.ax_availability.text(0.02, 0.88, f'Trend: {trend_symbol} {trend:.3f}%', 
                                             transform=self.ax_availability.transAxes, 
                                             verticalalignment='top', fontsize=9, color=trend_color,
                                             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                                     alpha=0.8, edgecolor=trend_color))
    
    def _draw_risk_heatmap(self):
        """Draw risk heatmap for all nodes"""
        self.ax_risk.clear()
        self.ax_risk.set_title('Node Risk Levels', fontsize=12, fontweight='bold')
        self.ax_risk.set_xlabel('Node ID', fontsize=10)
        self.ax_risk.set_ylabel('Risk Score', fontsize=10)
        
        risk_scores = get_all_risk_scores(self.simulator.nodes)
        node_ids = list(range(len(self.simulator.nodes)))
        risks = [risk_scores.get(i, 0) for i in node_ids]
        
        # Create color map based on risk levels
        colors = []
        for risk in risks:
            if risk > 0.7:
                colors.append('red')
            elif risk > 0.5:
                colors.append('darkorange')
            elif risk > 0.3:
                colors.append('gold')
            else:
                colors.append('lightgreen')
        
        bars = self.ax_risk.bar(node_ids, risks, color=colors, alpha=0.8, 
                               edgecolor='black', linewidth=1)
        self.ax_risk.set_ylim([0, 1.1])
        
        # Add risk threshold line with label
        self.ax_risk.axhline(y=0.6, color='darkred', linestyle='--', alpha=0.7, linewidth=2)
        self.ax_risk.text(0.02, 0.62, 'Risk Threshold', transform=self.ax_risk.transAxes,
                         fontsize=8, color='darkred', fontweight='bold')
        
        # Add value labels on bars with better positioning
        for bar, risk in zip(bars, risks):
            height = bar.get_height()
            self.ax_risk.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                             f'{risk:.2f}', ha='center', va='bottom', fontsize=8, 
                             fontweight='bold', color='darkblue')
        
        # Add grid for better readability
        self.ax_risk.grid(True, alpha=0.3, axis='y')
        
        # Set x-axis ticks to be integers
        self.ax_risk.set_xticks(node_ids)
        self.ax_risk.set_xticklabels([f'N{i}' for i in node_ids], fontsize=8)
    
    def _draw_events(self):
        """Draw recent system events"""
        self.ax_events.clear()
        self.ax_events.set_title('System Events Log', fontsize=12, fontweight='bold')
        self.ax_events.axis('off')
        
        # Combine recent events
        all_events = list(self.migration_events) + list(self.failure_events)
        all_events.sort(key=lambda x: x[0], reverse=True)  # Sort by time (most recent first)
        
        if all_events:
            event_text = "Recent System Events:\n" + "="*60 + "\n"
            for i, (time_step, event) in enumerate(all_events[:10]):  # Show last 10 events
                event_text += f"[T{time_step:2d}] {event}\n"
            
            self.ax_events.text(0.02, 0.98, event_text, transform=self.ax_events.transAxes,
                              verticalalignment='top', fontfamily='monospace', fontsize=10,
                              bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', 
                                      alpha=0.9, edgecolor='black'))
        else:
            self.ax_events.text(0.5, 0.5, 'No events recorded yet', 
                              transform=self.ax_events.transAxes,
                              horizontalalignment='center', verticalalignment='center',
                              fontsize=12, style='italic', color='gray')
    
    def update_frame(self, frame):
        """Update animation frame"""
        # Run simulation step
        self.simulator.run_simulation_step()
        
        # Get current status
        status = self.simulator.get_system_status()
        
        # Update history
        self.availability_history.append(status['system_availability'])
        
        # Check for migration events (simplified - in real implementation, you'd track this)
        if frame % 2 == 0:  # Simulate some events
            self.migration_events.append((frame, f"Replica migration detected"))
        
        if random.random() < 0.1:  # Simulate failure events
            failed_nodes = [n.id for n in self.simulator.nodes if n.status == "failed"]
            if failed_nodes:
                self.failure_events.append((frame, f"Node {failed_nodes[0]} failed"))
        
        # Update all plots
        self._draw_network()
        self._draw_availability()
        self._draw_risk_heatmap()
        self._draw_events()
        
        # Update main title with current stats
        self.fig.suptitle(
            f'Distributed Storage System - Time Step: {frame} | '
            f'Availability: {status["system_availability"]*100:.2f}% | '
            f'Alive Nodes: {status["alive_nodes"]}/{self.num_nodes}',
            fontsize=14, fontweight='bold'
        )
        
        return self.ax_network, self.ax_availability, self.ax_risk, self.ax_events
    
    def run_animation(self, interval=4000, frames=15):
        """
        Run the animated simulation
        
        Args:
            interval: Delay between frames in milliseconds (increased for explanation time)
            frames: Number of simulation steps to run
        """
        # Initialize with replica placement
        self.simulator.initial_replica_placement(min_replicas=3)
        
        print(f"\nAnimation Settings:")
        print(f"  - Time between steps: {interval/1000:.1f} seconds")
        print(f"  - Number of frames: {frames}")
        print(f"  - Total duration: {interval*frames/1000:.1f} seconds")
        print("\nStarting animation...")
        
        # Create animation
        anim = animation.FuncAnimation(
            self.fig, self.update_frame, frames=frames,
            interval=interval, blit=False, repeat=True
        )
        
        plt.tight_layout()
        plt.show()
        
        return anim

# Import required functions
from risk_model import get_all_risk_scores

def main():
    """Main function to run the visual simulator"""
    print("=" * 70)
    print("VISUAL DISTRIBUTED STORAGE SIMULATOR")
    print("Design and Analysis of Algorithms - Course Project")
    print("=" * 70)
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Create visual simulator
    print("\nInitializing visual simulator...")
    visual_sim = VisualSimulator(
        num_nodes=12,
        num_files=6,
        risk_threshold=0.6,
        target_availability=0.99
    )
    
    print("Starting animated simulation...")
    print("The visualization will show:")
    print("  - Network topology with node status and risk levels")
    print("  - File replica distribution (colored circles)")
    print("  - System availability over time")
    print("  - Node risk heatmap")
    print("  - Real-time event log")
    print("\nClose the window to stop the simulation.")
    
    # Run animation with longer interval for explanation
    anim = visual_sim.run_animation(interval=4000, frames=12)
    
    print("\nSimulation complete!")

if __name__ == "__main__":
    main()
