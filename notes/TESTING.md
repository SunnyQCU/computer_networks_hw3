Test 1:
topology file: topology_ez.dat
A simple two node graph used to simply test the
init_tables(), seeing if the initial tables are set.

Result:
log_A.txt has B:1:B, which is correct
log_B.txt has A:1:A, which is correct

Both nodes got the neighboring nodes in their .txt,
indicating routing_table is successful.

Test 2:
topology file: topology_five.dat
A medium complexity 5 node graph. The main thing to
check for is the path between A and B, whose
direct connection is 7, but the indirect path 
goes through 3 links and has a cost of 6.

The log_A.txt indicates this (B:6:E), indicating
that the shortest path was successfully propagated through the network

Test 3:
topology file: topology_nine.dat
A complicated 9 node graph. Some notable links to check for
is A to I (should be 6), and A to F (should be 5). The logs
from log_A.txt show I:6:B and F:5:B, indicating success.



