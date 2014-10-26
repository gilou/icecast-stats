'''
Created on 26 oct. 2014

@author: gilles
'''

from dns.resolver import query
from icecast_parser import * 

def get_servers(url="ice.stream.frequence3.net"):
    q = query(url, 'A')
    servers = []
    for rep in q:
        servers.append(rep.to_text())
    
    return servers

def get_stats(servers): 
    pass

if __name__ == '__main__':
    s = get_servers()
    print(s)