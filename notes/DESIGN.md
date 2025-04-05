The design of the protocol is as follows:

We first initialize our routing table and neighbors
table. The routing table is a dictionary with the
keys being the node names, and the value being a
tuple with the cost and the hopping node (i.e, the
node it must hop through to reach the key node)

The neighbors table is just a dictionary with the
keys being the neighboring node names, and the value
being only the cost to reach said neighbor. The
neighbors table does not change, while the routing
table doee. The purpose of the neighbors table
is to reference from when calculating the cost
of getting to another node in:
new_cost = cost_to_sender + sender_cost_to_dest
where cost_to_sender is simply the cost to reach the
neighbor (the sender).

Afterward, we end up in the main while loop which
runs forever. The steps is as follows:

1. Send distance vector to every neighbor

This is so the neighbors can update their current
routing table.

2. Receive the messages from neighbors

This is so that the current node can update its own
routing table

3. Process every message and update routing_table accordingly

Go through every single distance vector received and
update the current node distance vector

4. Log the new routing_table if it was updated.

This logging is for record keeping as per the
assignment requirements

For the message processing, there is only one
type of message. The message's purpose is to
simply transmit a node's distance vector.
Its structure is a 4-byte header + json file.

The 4-byte header contains the length of the json
file, while the json file itself contains two field:
The sending node, and the distance vector from the node.

Because multiple nodes could be sending at the same
time, the receiving process must also process
messages as well. To do this, the receive function
simply receives a reasonably large size (4096 bytes)
all at once, which minimizes the possibility of any
message being truncated. Then, it uses the file
length information (which is always 4 bytes long)
to extract the rest of the json file in its exact
size.

It goes over each received distance vector and
updates the shortest route in the routing table.
If any updates occur, the updated bool becomes
True, and at the very end we log the new
routing table. We then time.sleep() for
one second to give time to every node to
process and send their messages. It also
limits unnecessary spinning.
