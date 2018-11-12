# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 02:47:14 2018

@author: sanket
"""

import json
import time

'''here we are first getting data from json file'''
with open('file.json', 'r') as f:
    distros_dict = json.load(f)

fanout = distros_dict['fanout']
heartbeat = distros_dict['heartbeat']
T_Failure = distros_dict['T_Failure']

'''node_list contains all the participating nodes'''
node_list = []
for node in distros_dict['nodes']:
    IP = node['IP']
    PORT = node['PORT']
    node_list.append((IP, PORT));

'''memberlist is the advanced version of node_list, it will contain each node
    along with hearbeat counter and the last time when the heartbeat was updated
    by that node'''
memberlist = {}
for node in node_list:
    memberlist[node] = [0, 0]
    
'''this function encodes the memberlist to specific format required by json'''
def encode_memberlist(memberlist, target):
    for key in memberlist:
        target[key[0]+':'+str(key[1])] = memberlist[key]

'''this function decodes the memberlist from the json format'''
def decode_memberlist(memberlist, target):
    for key in memberlist:
       a = key.split(':')
       target[tuple((a[0],int(a[1])))] = memberlist[key]

'''print all the members along with there hearbeat counter and last update time'''
def print_nodes(members):
     i = 0;
     for node in members:
         print(i,"->",node," Hcount:", members[node][0],
               " LastUpdated:", time.strftime("%H:%M:%S", time.localtime(members[node][1])))
         i= i+1;

'''this function will compare my view of the member 
   list and my neighbor's view of the member list'''
def compare_members(members, received_members):
    i = 0;
    for node in members:
        #check for the recent update
        if members[node][0] < received_members[node][0]:
            #print("updated..",node,": ", members[node][0], "->", received_members[node][0])
            members[node][0] = received_members[node][0]
            members[node][1] = received_members[node][1]
        #failure detection
        if ( time.time()-members[node][1] )>= T_Failure and (members[node][0] != 0):
            print('x'*20,'FAILED->',i,':',node,'x'*20)
        i=i+1;