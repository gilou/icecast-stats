#! /usr/bin/env python3
'''
Created on 26 oct. 2014

@author: gilles
'''

from dns.resolver import query
from icecast_parser import * 
from joblib import Parallel, delayed
import json
import sys

def get_servers(url="ice.stream.frequence3.net"):
    q = query(url, 'A')
    servers = []
    for rep in q:
        servers.append(rep.to_text())
    
    return servers

def get_single(server):
    ip = icecast_parser(ip=server, port=80)
    values = ip.parse_status()
    infos = { value:key for value,key in values.items() }
    return infos
    
    
def get_stats(servers,prefix=''):
    execut = Parallel(n_jobs=len(servers), backend="threading")(
                                            delayed(get_single)(s) for s in servers
    
    )
    # [ {srv1: { 'mount' : { infos...}, 'mount2' { infos }, ... } ], { srv2: { ...} } ]
    valeurs = {}
    
    for serv in execut:
            for cle, valeur in serv.items():
                radio = cle.rpartition('-')[0]
                if radio == '':
                    radio = cle.rpartition('.')[0]
                if len(radio) > 1 and not (prefix != '' and radio != prefix) :
                    titre = valeur['Currently playing']
                    if titre == None:
                        continue
                    titre = titre.rstrip()
                    if radio in valeurs.keys():
                            if(valeurs[radio]['title']) != titre:
                                continue
                            valeurs[radio]['listeners_count'] = valeurs[radio]['listeners_count'] + int(valeur['Listeners (current)'])
                    else:
                        valeurs[radio] = { 'title': titre, 'listeners_count': int(valeur['Listeners (current)']) }
    
    print(json.dumps(valeurs, sort_keys=True, indent=4))
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        for radio in sys.argv[1:]:
            get_stats(get_servers(), prefix=radio)
    else:
        get_stats(get_servers())
