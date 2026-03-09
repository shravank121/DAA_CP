# Quick Start Guide

## Running the Simulation

### Basic Simulation
Run the main simulation with default parameters:
```bash
python main.py
```

This will:
- Create 15 nodes with random characteristics
- Initialize 8 files
- Place 3 replicas per file
- Run 10 simulation time steps
- Display system events and availability metrics

### Test Individual Algorithms
Run the algorithm test suite:
```bash
python test_algorithms.py
```

This demonstrates:
- Algorithm 1: Risk calculation with sample nodes
- Algorithm 2: Replica selection with scoring
- Algorithm 3: Minimum replica calculation for different availability targets
- Algorithm 6: Availability calculation with examples

### Optional Visualization
If you have networkx and matplotlib installed:
```bash
pip install networkx matplotlib
python visualization.py
```

This will show:
- Network graph of the cluster
- Node status (green=alive, red=failed)
- Replica distribution for files
- Availability trends over time

## Customizing the Simulation

Edit `main.py` to change parameters:

```python
# Configuration
NUM_NODES = 15              # Number of nodes in cluster
NUM_FILES = 8               # Number of files to store
RISK_THRESHOLD = 0.6        # Risk threshold (0-1)
SIMULATION_STEPS = 10       # Number of time steps
MIN_REPLICAS = 3            # Minimum replicas per file
```

## Understanding the Output

### Initial Placement
```
File_0: placed 3 replicas on nodes [9, 1, 7]
```
Shows which nodes store each file's replicas.

### Risk Detection
```
High-risk nodes detected: [3, 7]
  Node 3 risk = 0.652
  Node 7 risk = 0.701
```
Nodes with risk > threshold are flagged for migration.

### Migration Events
```
Migrated File_2: Node 3 → Node 9
```
Replicas moved from risky nodes to safer nodes.

### Failure Events
```
Node 7 FAILED
Removed 2 replicas from failed nodes
```
Node failures and cleanup operations.

### Availability Metrics
```
System availability: 99.87%
  File_4 availability: 98.50%
```
Overall system and individual file availability.

## Project Structure

```
project/
├── main.py                    # Entry point - run this
├── simulator.py               # Main simulation engine
├── nodes.py                   # Node class definition
├── file_model.py             # File class definition
├── risk_model.py             # Algorithm 1: Risk calculation
├── replication.py            # Algorithms 2, 3, 4: Replication logic
├── failure_simulation.py     # Algorithm 5: Failure simulation
├── availability.py           # Algorithm 6: Availability calculation
├── test_algorithms.py        # Algorithm demonstrations
├── visualization.py          # Optional network visualization
├── README.md                 # Project documentation
├── COMPLEXITY_ANALYSIS.md    # Algorithm complexity analysis
├── QUICKSTART.md            # This file
└── requirements.txt          # Dependencies (optional)
```

## Key Algorithms

1. **Risk Calculation** - O(N): Predicts node failures
2. **Replica Selection** - O(N log N): Chooses optimal nodes
3. **Minimum Replicas** - O(N log N): Calculates required replicas
4. **Replica Migration** - O(F × N log N): Proactive replication
5. **Failure Simulation** - O(N): Simulates node failures
6. **Availability Calculation** - O(F × R): Computes reliability

## Example Scenarios

### High Availability System
```python
NUM_NODES = 20
MIN_REPLICAS = 5
RISK_THRESHOLD = 0.5
```
More nodes, more replicas, lower risk tolerance.

### Resource-Constrained System
```python
NUM_NODES = 10
MIN_REPLICAS = 2
RISK_THRESHOLD = 0.7
```
Fewer resources, higher risk tolerance.

### Long-Term Simulation
```python
SIMULATION_STEPS = 50
```
Observe system behavior over extended period.

## Troubleshooting

### No output or errors
- Ensure Python 3.6+ is installed
- Check all .py files are in the same directory

### Import errors
- All files should be in the same folder
- No external dependencies required for basic simulation

### Visualization not working
- Install optional dependencies: `pip install networkx matplotlib`
- Or skip visualization and use text output only

## Next Steps

1. Run `python main.py` to see the simulation in action
2. Run `python test_algorithms.py` to understand each algorithm
3. Modify parameters in `main.py` to experiment
4. Read `COMPLEXITY_ANALYSIS.md` for algorithm details
5. Check `README.md` for comprehensive documentation

## Tips for Course Project

- Focus on explaining the algorithms in your report
- Include complexity analysis from COMPLEXITY_ANALYSIS.md
- Show sample output from test_algorithms.py
- Discuss trade-offs between availability and resource usage
- Explain how proactive migration improves reliability
- Compare different parameter configurations

## Questions?

Review the documentation:
- README.md - Project overview and architecture
- COMPLEXITY_ANALYSIS.md - Detailed algorithm analysis
- Code comments - Implementation details
