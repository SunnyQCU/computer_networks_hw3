To run network.py:

- python3 network.py <network_port> <topology_file>
  Ex.
- python3 network.py 50000 topologies/topology.dat

To run the multiple nodes:

- python3 dvr.py <ip_addr> <network_port>
  Ex.
- python3 dvr.py 127.0.0.1 50000

Current issues:
The updating seems to be random and sporadic, so its a matter of chance what info
reaches what node. In other words, alot of messages are lost.