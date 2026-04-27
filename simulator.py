"""
Main Simulation Engine
Orchestrates the distributed storage system simulation
"""

from nodes import Node
from file_model import File
from risk_model import identify_high_risk_nodes, get_all_risk_scores
from replication import (select_replica_nodes, calculate_minimum_replicas, 
                         migrate_replicas_from_risky_nodes)
from failure_simulation import simulate_node_failures, cleanup_failed_node_replicas
from availability import calculate_system_availability, get_availability_report

class DistributedStorageSimulator:
    def __init__(self, num_nodes=10, num_files=5, risk_threshold=0.6, target_availability=0.99):
        """
        Initialize the distributed storage simulator
        
        Args:
            num_nodes: Number of nodes in the cluster
            num_files: Number of files to store
            risk_threshold: Threshold for identifying high-risk nodes
            target_availability: Target system availability (default 99%)
        """
        self.nodes = []
        self.files = []
        self.risk_threshold = risk_threshold
        self.target_availability = target_availability
        self.time_step = 0
        self.events = []
        
        # Initialize nodes and files
        self._initialize_nodes(num_nodes)
        self._initialize_files(num_files)
    
    def _initialize_nodes(self, num_nodes):
        """Create initial set of nodes with varying characteristics"""
        import random
        
        for i in range(num_nodes):
            reliability = random.uniform(0.7, 0.99)
            failure_prob = random.uniform(0.01, 0.15)
            trust_score = random.uniform(0.6, 1.0)
            capacity = random.uniform(50, 200)  # GB
            
            node = Node(
                node_id=i,
                reliability=reliability,
                failure_probability=failure_prob,
                trust_score=trust_score,
                storage_capacity=capacity
            )
            self.nodes.append(node)
        
        self.log_event(f"Initialized {num_nodes} nodes")
    
    def _initialize_files(self, num_files):
        """Create initial set of files"""
        import random
        
        for i in range(num_files):
            size = random.uniform(1, 10)  # GB
            importance = random.uniform(0.5, 1.0)
            
            file = File(
                file_id=f"File_{i}",
                size=size,
                importance_level=importance
            )
            self.files.append(file)
        
        self.log_event(f"Initialized {num_files} files")
    
    def initial_replica_placement(self, min_replicas=3):
        """
        Perform initial replica placement for all files
        """
        self.log_event(f"\n=== Initial Replica Placement ===")
        
        for file in self.files:
            # Select nodes for replicas
            selected_nodes = select_replica_nodes(self.nodes, file, min_replicas)
            
            # Place replicas
            for node_id in selected_nodes:
                node = self.nodes[node_id]
                if node.add_file(file.id, file.size):
                    file.add_replica(node_id)
            
            self.log_event(f"{file.id}: placed {len(file.replicas)} replicas on nodes {file.replicas}")
    
    def run_simulation_step(self):
        """
        Execute one simulation time step
        """
        self.time_step += 1
        self.log_event(f"\n=== Time Step {self.time_step} ===")
        
        # Step 1: Calculate node risk scores
        risk_scores = get_all_risk_scores(self.nodes)
        high_risk_nodes = identify_high_risk_nodes(self.nodes, self.risk_threshold)
        
        if high_risk_nodes:
            self.log_event(f"High-risk nodes detected: {high_risk_nodes}")
            for node_id in high_risk_nodes:
                self.log_event(f"  Node {node_id} risk = {risk_scores[node_id]:.3f}")
        
        # Step 2: Proactive replica migration
        if high_risk_nodes:
            migrations = migrate_replicas_from_risky_nodes(
                self.nodes, self.files, high_risk_nodes
            )
            
            for file_id, from_node, to_node in migrations:
                self.log_event(f"Migrated {file_id}: Node {from_node} -> Node {to_node}")
        
        # Step 3: Simulate node failures
        failed_nodes = simulate_node_failures(self.nodes)
        
        if failed_nodes:
            for node_id in failed_nodes:
                self.log_event(f"Node {node_id} FAILED")
        
        # Step 4: Cleanup failed node replicas
        removed = cleanup_failed_node_replicas(self.nodes, self.files)
        if removed > 0:
            self.log_event(f"Removed {removed} replicas from failed nodes")
        
        # Step 5: Maintain minimum replicas (dynamically calculated)
        self._maintain_replicas()
        
        # Step 6: Calculate and report availability
        system_availability = calculate_system_availability(self.files, self.nodes)
        self.log_event(f"System availability: {system_availability * 100:.2f}%")
        
        # Report individual file availability
        availability_report = get_availability_report(self.files, self.nodes)
        for file_id, avail in availability_report.items():
            if avail < 0.99:  # Only report files with low availability
                self.log_event(f"  {file_id} availability: {avail * 100:.2f}%")
    
    def _maintain_replicas(self):
        """
        Ensure all files maintain minimum replica count (dynamically calculated)
        """
        # Calculate current minimum replicas needed for target availability
        min_replicas, actual_availability = calculate_minimum_replicas(
            self.nodes, self.target_availability
        )
        
        self.log_event(f"Dynamic replica calculation: need {min_replicas} replicas for {self.target_availability*100:.1f}% availability")
        
        for file in self.files:
            current_replicas = file.get_replica_count()
            
            if current_replicas < min_replicas:
                needed = min_replicas - current_replicas
                exclude = set(file.replicas)
                new_nodes = select_replica_nodes(self.nodes, file, needed, exclude)
                
                for node_id in new_nodes:
                    node = self.nodes[node_id]
                    if node.add_file(file.id, file.size):
                        file.add_replica(node_id)
                        self.log_event(f"Created replica of {file.id} on Node {node_id}")
            elif current_replicas > min_replicas + 1:  # Allow some buffer, remove excess if too many
                # Remove excess replicas to save resources (optional optimization)
                excess = current_replicas - min_replicas
                # For now, we'll keep extra replicas for safety
                pass
    
    def log_event(self, message):
        """Log simulation event"""
        self.events.append(message)
        print(message)
    
    def get_system_status(self):
        """
        Get current system status summary
        """
        alive_nodes = sum(1 for n in self.nodes if n.status == "alive")
        failed_nodes = len(self.nodes) - alive_nodes
        total_replicas = sum(f.get_replica_count() for f in self.files)
        avg_availability = calculate_system_availability(self.files, self.nodes)
        
        return {
            "time_step": self.time_step,
            "alive_nodes": alive_nodes,
            "failed_nodes": failed_nodes,
            "total_files": len(self.files),
            "total_replicas": total_replicas,
            "system_availability": avg_availability
        }
