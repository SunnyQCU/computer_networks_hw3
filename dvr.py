""""
Columbia University - CSEE 4119 Computer Network
Assignment 3 - Distance Vector Routing

dvr.py - the Distance Vector Routing (DVR) program announces its distance vector to its neighbors and 
updates its routing table based on the received routing vectors from its neighbors
"""
import sys
import socket
import time

#my imports
import os
import json
import shutil

class NetworkInterface():
    """
    DO NOT EDIT.
    
    Provided interface to the network. In addition to typical send/recv methods,
    it also provides a method to receive an initial message from the network, which
    contains the costs to neighbors. 
    """
    def __init__(self, network_port, network_ip):
        """
        Constructor for the NetworkInterface class.

        Parameters:
            network_port : int
                The port the network is listening on.
            network_ip : str
                The IP address of the network.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((network_ip, network_port))
        self.init_msg = self.sock.recv(4096).decode() # receive the initial message from the network
        
    def initial_costs(self): 
        """
        Return the initial message received from the network in following format:
        <node_id>. <neighbor_1>:<cost_1>,...,<neighbor_n>:<cost_n>

        node_id is the unique identifier for this node, i.e., dvr.py instance. 
        Neighbor_i is the unique identifier for direct neighbor nodes. All identifiers
        and costs are specified in the topology file.
        """
        return self.init_msg
    
    def send(self, message):
        """
        Send a message to all direct neigbors.

        Parameters:
            message : bytes
                The message to send.
        
        Returns:
            None
        """
        message_len = len(message)
        packet = message_len.to_bytes(4, byteorder='big') + message
        self.sock.sendall(packet)
    
    def recv(self, length):
        """
        Receive a message from neighbors. Behaves exactly like socket.recv()

        Parameters:
            length : int
                The length of the message to receive.
        
        Returns:
            bytes
                The received message.
        """
        return self.sock.recv(length)
    
    def close(self):
        """
        Close the socket connection with the network.
        """
        self.sock.close()

def init_tables(init_costs):
    """
    Takes the init_costs and initializes the routing table and neighbors table

    Parameters:
        init_costs : string
            The current node and initial costs to each neighboring node

    Returns:
        The current node and the routing table
    """
    routing_table = {}
    neighbors_table = {}
    
    curr_node, neighbors = init_costs.split('.')
    curr_node = curr_node.strip()
    routing_table[curr_node] = (0, curr_node)

    for entry in neighbors.split(','):
        neighbor, cost = entry.split(':')

        neighbor = neighbor.strip()
        cost = cost.strip()

        routing_table[neighbor] = (int(cost), neighbor)
        neighbors_table[neighbor] = int(cost)

    return curr_node, routing_table, neighbors_table

def send_dv(net_interface, curr_node, routing_table):
    """
    Sends the distance vector to every neighbor

    Parameters:
        net_interface:
            The net interface object that provides the send() function
        curr_node:
            The sending node
        routing_table:
            The table to send
    """
    dv_to_send = {dest: cost for dest, (cost, _) in routing_table.items()}

    message = {
        "sender": curr_node,
        "dv": dv_to_send
    }
    packet = json.dumps(message).encode()

    packet_size = len(packet) 
    packet = packet_size.to_bytes(4, byteorder='big') + packet

    net_interface.send(packet)

def receive_dv(net_interface):
    """
    Receives multiple messages at a time

    Parameters:
        net_interface:
            The net interface object that provides the recv() function
    
    Returns:
        The list of messages
    """
    data = net_interface.recv(4096)
    messages = []
    buffer = data

    while len(buffer) >= 4:
        header = buffer[:4]
        packet_size = int.from_bytes(header, byteorder='big')

        if len(buffer) < 4 + packet_size:
            break

        payload = buffer[4:4 + packet_size]
        try:
            message = json.loads(payload.decode())
            messages.append(message)
        except Exception as e:
            pass

        buffer = buffer[4 + packet_size:]

    return messages

def update_routing_table(routing_table, neighbors_table, sender, dv):
    """
    Updates this node's routing table based on received table from
    a neighbor

    Parameters:
        routing_table:
            The current node's routing_table
        sender:
            The sending node's name
        dv: 
            The sending node's distance vector
        neighbors_table:
            The current node's neighbors_table
    
    Returns:
        The updated routing_table
    """
    updated = False

    cost_to_sender = neighbors_table[sender]

    for dest, sender_cost_to_dest in dv.items():
        if dest == sender:
            continue

        new_cost = cost_to_sender + sender_cost_to_dest

        # Bellman-Ford algorithm
        if dest not in routing_table or new_cost < routing_table[dest][0]:
            routing_table[dest] = (new_cost, sender) # (cost, hop)
            updated = True
    
    return updated 

def log_routing_table(log_file, routing_table, curr_node):
    """
    Logs the routing table to a specified file

    Parameters:
        log_file:
            The file to log to
        routing_table:
            The routing_table to log
        curr_node:
            The current node, so log_routing knows which node to omit printing
    """
    entries = []

    for dest in sorted(routing_table.keys()):
        if dest == curr_node:
            continue 
        cost, next_hop = routing_table[dest]
        entries.append(f"{dest}:{cost}:{next_hop}")
    
    log_line = " ". join(entries)

    log_file.write(log_line + "\n")
    log_file.flush()

if __name__ == '__main__':
    network_ip = sys.argv[1] # the IP address of the network
    network_port = int(sys.argv[2]) # the port the network is listening on
 
    net_interface = NetworkInterface(network_port, network_ip) # initialize the network interface
    
    # get the initial costs to your neighbors to help initialize your vector and table. Format is:
    # <node_id>. <neighbor_1>:<cost_1>,...,<neighbor_n>:<cost_n>
    init_costs = net_interface.initial_costs() 

    """Below is an example of how to use the network interface and log. Replace it with your distance vector routing protocol"""

    curr_node, routing_table, neighbors_table = init_tables(init_costs)

    log_file = open(f"log_{curr_node}.txt", "w")
    log_routing_table(log_file, routing_table, curr_node)

    while True:
        send_dv(net_interface, curr_node, routing_table)

        messages = receive_dv(net_interface)

        updated = False

        for msg in messages:
            sender = msg["sender"]
            dv = msg["dv"]
            if update_routing_table(routing_table, neighbors_table, sender, dv):
                updated = True

        if updated:
            log_routing_table(log_file, routing_table, curr_node)
        
        time.sleep(1)