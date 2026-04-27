"""
Comprehensive Visualization Demo for DAA Project
Shows all available visualization options for the distributed storage system
"""

import matplotlib.pyplot as plt
import networkx as nx
import random
import time
from simulator import DistributedStorageSimulator
from visualization import visualize_cluster, visualize_file_replicas, plot_availability_over_time

def demo_basic_visualization():
    """Demo basic visualization capabilities"""
    print("=" * 60)
    print("DEMO 1: Basic Network Visualization")
    print("=" * 60)
    
    # Create simulator
    random.seed(42)
    target_avail = 0.99
    sim = DistributedStorageSimulator(num_nodes=10, num_files=5, target_availability=target_avail)
    
    # Calculate dynamic replicas
    from replication import calculate_minimum_replicas
    min_replicas, actual_avail = calculate_minimum_replicas(sim.nodes, target_avail)
    print(f"Calculated {min_replicas} replicas needed for {target_avail*100:.1f}% availability")
    
    sim.initial_replica_placement(min_replicas=min_replicas)
    
    print("Showing initial cluster state...")
    print("- Green nodes: Alive and healthy")
    print("- Node labels show ID and current load")
    print("- Edges show network connectivity")
    
    visualize_cluster(sim.nodes, sim.files, "Initial Cluster State")
    
    input("Press Enter to continue to file replica visualization...")
    
    print("\nShowing file replica distribution...")
    print("- Gold nodes: Have the specific file replica")
    print("- Gray nodes: Don't have the replica")
    print("- Orange nodes: Have replica but failed")
    
    visualize_file_replicas(sim.nodes, sim.files[0], f"Replicas for {sim.files[0].id}")
    
    input("Press Enter to continue to simulation...")

def demo_simulation_with_tracking():
    """Demo simulation with availability tracking"""
    print("=" * 60)
    print("DEMO 2: Simulation with Availability Tracking")
    print("=" * 60)
    
    # Create simulator
    random.seed(42)
    target_avail = 0.99
    sim = DistributedStorageSimulator(num_nodes=12, num_files=6, target_availability=target_avail)
    
    # Calculate dynamic replicas
    from replication import calculate_minimum_replicas
    min_replicas, actual_avail = calculate_minimum_replicas(sim.nodes, target_avail)
    print(f"Calculated {min_replicas} replicas needed for {target_avail*100:.1f}% availability")
    
    sim.initial_replica_placement(min_replicas=min_replicas)
    
    print("Running simulation and tracking availability...")
    
    # Run simulation and track availability
    availability_history = []
    for step in range(10):
        print(f"Running step {step + 1}...")
        sim.run_simulation_step()
        status = sim.get_system_status()
        availability_history.append((step + 1, status['system_availability']))
        print(f"  Availability: {status['system_availability']*100:.2f}%")
        print(f"  Alive nodes: {status['alive_nodes']}/{len(sim.nodes)}")
    
    print("\nShowing availability over time...")
    plot_availability_over_time(availability_history)
    
    input("Press Enter to continue to final state visualization...")
    
    print("\nShowing final cluster state...")
    visualize_cluster(sim.nodes, sim.files, "Final Cluster State After Simulation")

def demo_algorithm_comparison():
    """Demo different algorithm parameters"""
    print("=" * 60)
    print("DEMO 3: Algorithm Parameter Comparison")
    print("=" * 60)
    
    # Test different risk thresholds
    thresholds = [0.4, 0.6, 0.8]
    results = {}
    
    for threshold in thresholds:
        print(f"\nTesting with risk threshold = {threshold}")
        random.seed(42)
        target_avail = 0.99
        sim = DistributedStorageSimulator(num_nodes=10, num_files=5, risk_threshold=threshold, target_availability=target_avail)
        
        # Calculate dynamic replicas
        from replication import calculate_minimum_replicas
        min_replicas, actual_avail = calculate_minimum_replicas(sim.nodes, target_avail)
        print(f"  Calculated {min_replicas} replicas needed for {target_avail*100:.1f}% availability")
        
        sim.initial_replica_placement(min_replicas=min_replicas)
        
        # Run simulation
        for step in range(8):
            sim.run_simulation_step()
        
        status = sim.get_system_status()
        results[threshold] = status['system_availability']
        
        print(f"  Final availability: {status['system_availability']*100:.2f}%")
        print(f"  Failed nodes: {status['failed_nodes']}")
        
        # Visualize this configuration
        visualize_cluster(sim.nodes, sim.files, f"Risk Threshold = {threshold}")
    
    # Plot comparison
    plt.figure(figsize=(10, 6))
    thresholds_list = list(results.keys())
    availability_list = [a * 100 for a in results.values()]
    
    plt.bar(range(len(thresholds_list)), availability_list, color=['blue', 'green', 'red'])
    plt.xlabel('Risk Threshold')
    plt.ylabel('Final Availability (%)')
    plt.title('Impact of Risk Threshold on System Availability')
    plt.xticks(range(len(thresholds_list)), [str(t) for t in thresholds_list])
    plt.ylim([90, 100])
    
    # Add value labels on bars
    for i, v in enumerate(availability_list):
        plt.text(i, v + 0.5, f'{v:.2f}%', ha='center')
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    input("Press Enter to continue to advanced demo...")

def demo_large_scale_simulation():
    """Demo with larger system"""
    print("=" * 60)
    print("DEMO 4: Large-Scale Simulation")
    print("=" * 60)
    
    # Create larger system
    random.seed(42)
    target_avail = 0.99
    sim = DistributedStorageSimulator(num_nodes=20, num_files=10, target_availability=target_avail)
    
    # Calculate dynamic replicas
    from replication import calculate_minimum_replicas
    min_replicas, actual_avail = calculate_minimum_replicas(sim.nodes, target_avail)
    print(f"Calculated {min_replicas} replicas needed for {target_avail*100:.1f}% availability")
    
    sim.initial_replica_placement(min_replicas=min_replicas)
    
    print("Simulating larger system (20 nodes, 10 files)...")
    
    # Track detailed metrics
    availability_history = []
    failed_nodes_history = []
    
    for step in range(15):
        sim.run_simulation_step()
        status = sim.get_system_status()
        availability_history.append(status['system_availability'])
        failed_nodes_history.append(status['failed_nodes'])
        
        if step % 3 == 0:
            print(f"Step {step + 1}: Availability = {status['system_availability']*100:.2f}%, Failed = {status['failed_nodes']}")
    
    # Create comprehensive visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Availability over time
    time_steps = list(range(1, len(availability_history) + 1))
    ax1.plot(time_steps, [a * 100 for a in availability_history], 'b-', linewidth=2)
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('Availability (%)')
    ax1.set_title('System Availability Over Time')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([95, 100])
    
    # Plot 2: Failed nodes over time
    ax2.plot(time_steps, failed_nodes_history, 'r-', linewidth=2, marker='o')
    ax2.set_xlabel('Time Step')
    ax2.set_ylabel('Number of Failed Nodes')
    ax2.set_title('Node Failures Over Time')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Node status distribution
    alive_count = sum(1 for node in sim.nodes if node.status == "alive")
    failed_count = len(sim.nodes) - alive_count
    
    ax3.pie([alive_count, failed_count], labels=['Alive', 'Failed'], 
            colors=['lightgreen', 'red'], autopct='%1.1f%%')
    ax3.set_title('Final Node Status Distribution')
    
    # Plot 4: Load distribution
    loads = [node.current_load for node in sim.nodes if node.status == "alive"]
    ax4.hist(loads, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
    ax4.set_xlabel('Node Load')
    ax4.set_ylabel('Number of Nodes')
    ax4.set_title('Load Distribution Across Alive Nodes')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print(f"\nFinal Statistics:")
    print(f"  Total nodes: {len(sim.nodes)}")
    print(f"  Alive nodes: {alive_count}")
    print(f"  Failed nodes: {failed_count}")
    print(f"  Final availability: {availability_history[-1]*100:.2f}%")
    print(f"  Average load: {sum(loads)/len(loads):.3f}" if loads else "  Average load: N/A")

def demo_real_time_animation():
    """Demo real-time animation (manual version)"""
    print("=" * 60)
    print("DEMO 5: Step-by-Step Animation")
    print("=" * 60)
    
    # Create simulator
    random.seed(42)
    target_avail = 0.99
    sim = DistributedStorageSimulator(num_nodes=8, num_files=4, target_availability=target_avail)
    
    # Calculate dynamic replicas
    from replication import calculate_minimum_replicas
    min_replicas, actual_avail = calculate_minimum_replicas(sim.nodes, target_avail)
    print(f"Calculated {min_replicas} replicas needed for {target_avail*100:.1f}% availability")
    
    sim.initial_replica_placement(min_replicas=min_replicas)
    
    print("Showing step-by-step simulation...")
    print("Each step shows:")
    print("  - Network topology changes")
    print("  - Node failures (red)")
    print("  - High-risk nodes (orange)")
    
    for step in range(5):
        print(f"\n=== Step {step + 1} ===")
        
        # Show current state
        visualize_cluster(sim.nodes, sim.files, f"Step {step + 1}")
        
        # Run simulation step
        sim.run_simulation_step()
        
        # Show status
        status = sim.get_system_status()
        print(f"Availability: {status['system_availability']*100:.2f}%")
        print(f"Alive nodes: {status['alive_nodes']}/{len(sim.nodes)}")
        
        input("Press Enter for next step...")

def main():
    """Main demo function"""
    print("=" * 70)
    print("COMPREHENSIVE VISUALIZATION DEMO")
    print("Design and Analysis of Algorithms - Course Project")
    print("=" * 70)
    
    print("\nThis demo showcases all visualization capabilities:")
    print("1. Basic network visualization")
    print("2. Simulation with tracking")
    print("3. Algorithm parameter comparison")
    print("4. Large-scale simulation")
    print("5. Step-by-step animation")
    
    while True:
        print("\n" + "=" * 50)
        print("Select demo to run:")
        print("1. Basic Visualization")
        print("2. Simulation with Tracking")
        print("3. Algorithm Comparison")
        print("4. Large-Scale Simulation")
        print("5. Step-by-Step Animation")
        print("6. Run All Demos")
        print("0. Exit")
        
        choice = input("\nEnter choice (0-6): ").strip()
        
        if choice == "0":
            print("Exiting demo...")
            break
        elif choice == "1":
            demo_basic_visualization()
        elif choice == "2":
            demo_simulation_with_tracking()
        elif choice == "3":
            demo_algorithm_comparison()
        elif choice == "4":
            demo_large_scale_simulation()
        elif choice == "5":
            demo_real_time_animation()
        elif choice == "6":
            demo_basic_visualization()
            demo_simulation_with_tracking()
            demo_algorithm_comparison()
            demo_large_scale_simulation()
            demo_real_time_animation()
        else:
            print("Invalid choice. Please try again.")
    
    print("\n" + "=" * 70)
    print("Demo complete! Your DAA project visualization capabilities include:")
    print("✓ Real-time network topology visualization")
    print("✓ File replica distribution tracking")
    print("✓ System availability monitoring")
    print("✓ Algorithm parameter comparison")
    print("✓ Large-scale simulation analysis")
    print("✓ Interactive step-by-step animation")
    print("=" * 70)

if __name__ == "__main__":
    main()
