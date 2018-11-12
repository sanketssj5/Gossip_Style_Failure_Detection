# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 18:56:38 2018

@author: sanket
"""
#FIRST NODE TO START A GOSSIP
import socket
import nodes
import time
import threading
import json
import copy

'''ONLY CHANGE NODE_NO FOR NEW NODES'''
NODE_NO = 0
NODE_ADDRESS = nodes.node_list[NODE_NO]
FANOUT = nodes.fanout
HEARTBEAT = nodes.heartbeat
NEIGHBORS = []
OTHER_NODES = copy.deepcopy(nodes.node_list)
OTHER_NODES.remove(NODE_ADDRESS)
#extra
members = nodes.memberlist;

#semaphore
sem = threading.Semaphore()

def hb_fun(sock, neighbors, members,):
    try:
        while True:
            time.sleep(HEARTBEAT)
            sem.acquire();
            members[NODE_ADDRESS][0]= members[NODE_ADDRESS][0]+1;
            members[NODE_ADDRESS][1] = time.time();
            d = {}
            nodes.encode_memberlist(members, d)
            msg_json = json.dumps(d)
            for destination in NEIGHBORS:
                try:
                    sock.sendto( msg_json.encode(), destination);
                except ConnectionResetError: #that node closed the connection
                    continue
            sem.release()
    except:
        print("Closed")
    
k=1;
i  = (NODE_NO+1)%len(nodes.node_list) 

while i != NODE_NO and k <= FANOUT:
    NEIGHBORS.append(nodes.node_list[i])
    k = k+1
    i = (i+1)%len(nodes.node_list)
    
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
sock.bind(NODE_ADDRESS);
sock.settimeout(2);

print("Start Gossiping?(yes/no)")
msg = input();
if msg == "yes":
    t1 = threading.Thread(target=hb_fun, args=(sock, NEIGHBORS,members,))
    t1.start()
else:
    exit(0)

t2 = time.time()

try:
    while True:
       try:
           received_data, sender_address = sock.recvfrom(1024); #should be power of two
       except socket.timeout:
           if abs(time.time()-t2) >= nodes.T_Failure:
               print("No one is responding");
               print("Close?")
               raise Exception('No one is responding!');
           else:
              continue;
       except ConnectionResetError:
           #Reciving data corrupted due to forcefully port close at the sender
           #do the timing trick here, and exit the program thereafter
           continue;
       t2 = time.time()
       m = {}
       nodes.decode_memberlist( json.loads( received_data.decode() ), m);
       sem.acquire();
       nodes.compare_members(members, m);
       print("Node No:", NODE_NO,"Address:", NODE_ADDRESS);
       nodes.print_nodes(members)
       print('-'*60);
       sem.release();
except KeyboardInterrupt:
    print('Server closing')
    sock.close()
    t1.join()
except:
    sock.close()
    t1.join()
    input()