'''
Created on 26 oct. 2014

@author: gilles
'''

from dns.resolver import query
from icecast_parser import * 
from joblib import Parallel, delayed
from math import sqrt
import json

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
    
    
def get_stats(servers):
    execut = Parallel(n_jobs=len(servers), backend="threading")(
                                            delayed(get_single)(s) for s in servers
    
    )
    # [ {srv1: { 'mount' : { infos...}, 'mount2' { infos }, ... } ], { srv2: { ...} } ]
    valeurs = {}
    
    for serv in execut:
            for cle, valeur in serv.items():
                radio = cle.rpartition('-')[0]
                if len(radio) > 1:
                    if radio in valeurs.keys():
                            if(valeurs[radio]['title']) != valeur['Current Song']:
                                continue
                            valeurs[radio]['listeners_count'] = valeurs[radio]['listeners_count'] + int(valeur['Current Listeners'])
                    else:
                        valeurs[radio] = { 'title': valeur['Current Song'], 'listeners_count': int(valeur['Current Listeners']) }
    
    print(json.dumps(valeurs, sort_keys=True, indent=4))
    
if __name__ == '__main__':
    get_stats(get_servers())