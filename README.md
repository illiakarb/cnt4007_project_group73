CNT4007 Project 1 Members - Team 73

1. Isaac Probst
2. Illia Karbivnychyi
3. Kerwin Larrobis
4.  

IMPORTANT NOTE FOR ORDER OF IMPLEMENTATION:

1. parseConfig.py 
(reads Common.cfg and PeerInfo.cfg for all other files)

2. log.py
2. buildMessage.py
2. parseMessage.py
2. fileStates.py
Writes log events, builds message types, parses incoming messages, and tracks bitfield/choke status.


3. processFile.py 
3. manageChoke.py
Reads/writes to peer folders, runs unchoke timers.

4. server.py 
4. client.py
Listens to incoming TCP connections, and connects to earlier peers.

5. peerProcess.py

Main entry point, run as "peerProcess.py" per the rubric.




# NOTE: PLEASE LET US KNOW WHAT CHANGES ARE BEING MADE, OR COMMIT QUICKLY TO AVOID OVERWRITING> 

