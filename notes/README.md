-- COMPILATION AND RUNNING --

To run network.py:

- python3 network.py <network_port> <topology_file>
  For example:
- python3 network.py 50000 topologies/topology.dat

To run the multiple nodes:

- python3 dvr.py <ip_addr> <network_port>
  For example
- python3 dvr.py 127.0.0.1 50000
  Run this command on N different terminals, where N is the number of nodes present
  in the network.

Run the network.py before running the multiple nodes.

-- CODE STRUCTURE --
The structure of my code is quite simple.
First, i get the initial message and initialize two tables: routing_table and neighbors_table.

Routing_table will contain the distance to every node, as well as what node the current node must pass through in order to reach the destination node.

The neighbors_table only contains the distance to every neighboring node, and is used to calculate the cost_to_sender value in update_routing_table used to calculate the total cost.

After initialization, the code enters a while True loop which follow these steps:

1. Send distance vector to every neighbor
2. Receive the messages from neighbors
3. Process every message and update routing_table accordingly
4. Log the new routing_table if it was updated.

I used a while True loop since it more accurately reflects how real nodes operate (they don't just stop responding when tables are converged)

I also made 5 different functions, which do the following:

- init_table(): Initialize the tables
- send_dv(): Send distance vectors to all the neighbors
- receive_dv(): Receive and process multiple dv messages
- update_routing_table(): Updates the routing table
- log_routing_table(): Logs to a txt file

More information about these functions can be found in dvr.py itself.

Code already works
Remaining things to do:

Finish TESTING.md
Clean up main code
