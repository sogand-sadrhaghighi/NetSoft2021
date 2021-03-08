# Description
Selective Flow Mirroring (SFM) is a 2-approximation algorithm for mirroring flows in the network. It assumes that each switch has a *mirroring port* and the switch can mirror the traffic of a subset of its flows on that port. The goal is to collect the traffic of all flows and we desire to minimize the maximum traffic rate of any mirroring port.

## Inputs
Currently, the algorithm assumes that the network topology is specified on a file named **topo** (change by option `-t`) in the **network** directory. In the first line, the number of switches in the network should be specified. Then, each link of the network should be specified in a single line afterwards. The switches should be named with positive integers and each link is specified with two switches names that are separated with a single space. 

Currently the following algorithms are implemented:
1. optimal: Solves the SFM problem, optimally.
2- FMA: Solves the SFM problem using FMA algorithm.
3- Stroboscope: Decide on mirroring locations based on KPS algorithm presented in stroboscope paper.

## Outputs
Currently, the algorithm generates the user specified number of flows randomly (random source and destination with shortest path routing. change number by using option `-f`). The traffic rate of each flow also is randomly chosen from the interval `0.1` to `0.5` (change by options `-l` and `-u`, respectively). The code generates two auxiliary files in the network folder:
1. flows: In each line of this file a flow is specified. The first number is the **id** of the flow. The second number is the **traffic rate**. The remaining numbers are the switch names that are in the path of that flow. 
2. switches: In each line of this file a switch is specified. The first number is the switch name. The remaining numbers are the **flow ids** that pass through that switch. 

Algorithm can also read flows from a file in the **network** directory. Its name can be specified via option `-i`. It should have the same format as the *flows* file, described above. Note that, if `-i` is provided the flows are not generated randomly and if not provided the flows are generated randomly. 

Then, two files are generated in the **solutions** folder:
1. approx: Shows the result of the FSM algorithm. In each line, the first number is the **flow id** and the second number is the switch on which the mirroring for that flow happens. The last line has a signle number that shows the objective value. 
2. opt: Shows the optimal solution. The format is similar to approx file. 
