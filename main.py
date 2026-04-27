"""
Main Entry Point for Distributed Storage Simulation
Run this file to execute the simulation
"""

from simulator import DistributedStorageSimulator
import random

def main():
    """
    Main simulation driver
    """
    # Set random seed for reproducibility
    random.seed(42)
    
    print("=" * 70)
    print("PREDICTIVE SECURE FILE REPLICATION IN DISTRIBUTED SYSTEMS")
    print("Design and Analysis of Algorithms - Course Project")
    print("=" * 70)
    
    # Configuration
    NUM_NODES = 15
    NUM_FILES = 8
    RISK_THRESHOLD = 0.6
    SIMULATION_STEPS = 10
    TARGET_AVAILABILITY = 0.99  # 99% target availability
    
    # Initialize simulator
    print(f"\nConfiguration:")
    print(f"  Nodes: {NUM_NODES}")
    print(f"  Files: {NUM_FILES}")
    print(f"  Risk Threshold: {RISK_THRESHOLD}")
    print(f"  Target Availability: {TARGET_AVAILABILITY*100:.1f}%")
    print(f"  Simulation Steps: {SIMULATION_STEPS}")
    
    simulator = DistributedStorageSimulator(
        num_nodes=NUM_NODES,
        num_files=NUM_FILES,
        risk_threshold=RISK_THRESHOLD,
        target_availability=TARGET_AVAILABILITY
    )
    
    # Calculate dynamic minimum replicas based on target availability
    print(f"\nCalculating optimal replica count for {TARGET_AVAILABILITY*100:.1f}% availability...")
    
    # Import the dynamic calculation function
    from replication import calculate_minimum_replicas
    
    # Calculate minimum replicas needed for target availability
    min_replicas, actual_availability = calculate_minimum_replicas(
        simulator.nodes, TARGET_AVAILABILITY
    )
    
    print(f"  Calculated minimum replicas: {min_replicas}")
    print(f"  Expected availability with {min_replicas} replicas: {actual_availability*100:.2f}%")
    
    # Perform initial replica placement with dynamic replica count
    simulator.initial_replica_placement(min_replicas=min_replicas)
    
    # Run simulation
    print("\n" + "=" * 70)
    print("STARTING SIMULATION")
    print("=" * 70)
    
    for step in range(SIMULATION_STEPS):
        simulator.run_simulation_step()
    
    # Final summary
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)
    
    status = simulator.get_system_status()
    print(f"\nFinal System Status:")
    print(f"  Time Steps: {status['time_step']}")
    print(f"  Alive Nodes: {status['alive_nodes']}/{NUM_NODES}")
    print(f"  Failed Nodes: {status['failed_nodes']}")
    print(f"  Total Files: {status['total_files']}")
    print(f"  Total Replicas: {status['total_replicas']}")
    print(f"  System Availability: {status['system_availability'] * 100:.2f}%")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
