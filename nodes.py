"""
Node Model for Distributed Storage System
Represents a storage node in the distributed cluster
"""

class Node:
    def __init__(self, node_id, reliability, failure_probability, trust_score, storage_capacity):
        """
        Initialize a storage node
        
        Args:
            node_id: Unique identifier for the node
            reliability: Probability node stays alive (0-1)
            failure_probability: Probability of failure per time step
            trust_score: Trust level of the node (0-1)
            storage_capacity: Maximum storage capacity in GB
        """
        self.id = node_id
        self.reliability = reliability
        self.failure_probability = failure_probability
        self.trust_score = trust_score
        self.storage_capacity = storage_capacity
        self.current_load = 0.0  # Current storage usage (0-1)
        self.status = "alive"  # "alive" or "failed"
        self.stored_files = []  # List of file_ids stored on this node
        self.failure_history = 0  # Number of past failures
        
    def add_file(self, file_id, file_size):
        """Add a file to this node"""
        if self.status == "alive" and file_id not in self.stored_files:
            self.stored_files.append(file_id)
            self.current_load += file_size / self.storage_capacity
            return True
        return False
    
    def remove_file(self, file_id, file_size):
        """Remove a file from this node"""
        if file_id in self.stored_files:
            self.stored_files.remove(file_id)
            self.current_load -= file_size / self.storage_capacity
            self.current_load = max(0, self.current_load)  # Prevent negative load
            return True
        return False
    
    def mark_failed(self):
        """Mark node as failed"""
        self.status = "failed"
        self.failure_history += 1
    
    def has_capacity(self, file_size):
        """Check if node has capacity for a file"""
        return self.status == "alive" and (self.current_load + file_size / self.storage_capacity) <= 1.0
    
    def __repr__(self):
        return f"Node({self.id}, status={self.status}, load={self.current_load:.2f}, reliability={self.reliability:.2f})"
