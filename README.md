# Description
Plow Mirroring Problem (PMP) wants to mirror flows in the network. It assumes that each switch has a *mirroring port* and the switch can mirror the traffic of a subset of its **ports** on that port. The goal is to collect the traffic of all flows and we desire to minimize the maximum traffic rate of any mirroring port.

## Inputs
Currently, the algorithm assumes that the network topology is specified on a file named **topo** (change by option `-t`) in the **network** directory. In the first line, the number of switches in the network should be specified. Then, each link of the network should be specified in a single line afterwards. The switches should be named with positive integers and each link is specified with two switches names that are separated with a single space. 

Currently three algorithms are implemented for port mirroring:
1. Optimal: Solves the SPM problem, optimally.
2. PMA: Solves the SPM problem using PMA algorithm.
3. Planck: A POS based approach for mirroring all flows on all switches.

## Outputs
Currently, the algorithm generates the flows randomly (random source and destination with shortest path routing. change number by using option `-f`). The traffic rate of each flow also is randomly chosen in a user specified interval (change by options `-l` and `-u`, respectively). The code generates two auxiliary files in the network folder:

1. flows: In each line of this file a flow is specified. The first number is the **id** of the flow. The second number is the **traffic rate**. Then, a sequence of paired numbers follows. The first number is a **switch id** and the second number is the **port number**. Port numbers are unique locally for each switch, starting from `1`.
2. switches: In each line of this file a **port** is specified. The first number is the switch name. The second number is the **port number**.The remaining numbers are the **flow ids** that pass through that port. 

Algorithm can also read flows from a file in the **network** directory. Its name can be specified via option `-i`. It should have the same format as the *flows* file, described above. Note that, if `-i` is provided the flows are not generated randomly and if not provided the flows are generated randomly. 

Currently, the following results are generated in **solutions** folder:
1. opt: Shows the solution from **optimal** algorithm. In each line, the first number is the **switch id** and the second number is a **port number** that should be mirrored. Note that, multiple ports from a switch can be selected. The last line has a single number that shows the objective value.  
2. df: Shows the solution from **PMA** algorithm in the same format.
3. coverage: Shows the coverage percentage of all algorithm (this is calculated based on the capacity of switches).
4. coverage-cost: Shows the coverage_cost of all algorithm (this is calculated based on the capacity of switches).
5. obj: Shows the objective value (lambda in the SPM problem) of all algorithms.