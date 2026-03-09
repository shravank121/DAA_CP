"""
File Model for Distributed Storage System
Represents a file stored across multiple nodes
"""

class File:
    def __init__(self, file_id, size, importance_level):
        """
        Initialize a file
        
        Args:
            file_id: Unique identifier for the file
            size: File size in GB
            importance_level: Importance score (higher = more critical)
        """
        self.id = file_id
        self.size = size
        self.importance = importance_level
        self.replicas = []  # List of node_ids where replicas are stored
    
    def add_replica(self, node_id):
        """Add a replica location"""
        if node_id not in self.replicas:
            self.replicas.append(node_id)
            return True
        return False
    
    def remove_replica(self, node_id):
        """Remove a replica location"""
        if node_id in self.replicas:
            self.replicas.remove(node_id)
            return True
        return False
    
    def get_replica_count(self):
        """Get number of replicas"""
        return len(self.replicas)
    
    def __repr__(self):
        return f"File({self.id}, size={self.size}GB, replicas={len(self.replicas)})"
