'''
Created on 26 oct. 2014

@author: gilles
'''

from lxml import etree
from sys import argv
from six.moves.urllib.parse import urlparse

class icecast_parser:
    """
    Class to parse icecast's status.xsl page, either directly from the .xsl URL, or given a ip & port
    parse_url is used as "static" to get the info out of a .xsl
    the default constructor can be used to specify the server.
    
    It can be called directly, with URLs to parse as parameters.
    """
    
    # Potentially interesting mountpoints, can be guessed later
    _interesting_mounts = ''
    # IP Adress of server, either from constructor, or from the .xsl URL
    _server_ip = ''
    # Port
    _server_port = 0
    # Name (not DNS) of the server, as reported by Icecast
    _server_name = ''
    
    def __init__(self, ip=None, port=8000):
        """
        Constructor, server name is dynamically requested
        If ip/port not given, one must use parse_url to get things done.
        """
        if ip != None:
            self._server_ip = ip
            self._server_port = port
            self._get_server_name()

    
    def guess_interesting_mounts(self, mountpoints, sep='-'):
        """
        Generic function to find all potential generic mountpoints, i.e. with "separator" in it, left part being the generic name. 
        """
        im = [ m.rpartition(sep)[0] for m in mountpoints.keys() if len(m.rpartition(sep)[0]) > 1]
        return set(im)
    
    def parse_url(self, url):
        """
        urlparse() for the URL, to extract port number & hostname from a URL
        """
        obj = urlparse(url)
        if obj.port == None:
            self._server_port = 80
        else:
            self._server_port = obj.port
            
        self._server_ip = obj.hostname
        
    def _get_server_name(self):
        """
        Use server_version.xsl to determine hostname as set up by the server admin
        This allows to discriminate a server if we have been given it twice using DNS or whatever
        """
        if self._server_ip == '':
            raise Exception('IP is unknown yet')
        else:
            version_url = self._make_version_url()
            parser = etree.HTMLParser()
            tree = etree.parse(version_url, parser)
            server_infos = tree.xpath("/html/body/div[@class='roundbox']/table[1]/tbody/tr[3]")
            server_name = server_infos[0].xpath('td[2]')[0].text
            self._server_name = server_name
    
    def _make_version_url(self):
        """ builds a /server_version.xsl url based on the server info """
        return 'http://' + self._server_ip + ':' + str(self._server_port) + '/' + 'server_version.xsl'
    
    def _make_stats_url(self):
        """ builds a /status.xsl url based on the server info """
        if self._server_ip == '':
            raise Exception('IP is unknown yet')
        
        return 'http://' + self._server_ip + ':' + str(self._server_port) + '/' + 'status.xsl'
        
    def parse_status(self,url=""):
        """
        Parse a /status.xsl URL in order to fetch all the information it gives about all the mountpoints on the server
        This returns a dictionnary with the mountpoint as the key, and a dictionnary as a value, with the info for the mount points.
        It looks like this { 'my_mountpoint': { 'Current Listeners': '3', 'Stream Title': 'My special radio', 'Peak Listeners': '91', ...} }
        """
        
        if url != "" :
            # Fetch the info from the URL, to define server_*
            self.parse_url(url)
            self._get_server_name()
        else:
            url = self._make_stats_url()
        
        parser = etree.HTMLParser()
        tree = etree.parse(url, parser)
        # Extract the relevant part of the HTML code
        sources = tree.xpath('/html/body/div[@class="roundbox"]')
        mountpoints = {}
        
        # For each mountpoints, we'll fetch the mount point name, then the array with all info
        for i in sources:
            # That is where the mountpoint is located
            mountpoint = i.xpath('./div[@class="mounthead"]/h3')[0].text.rpartition('/')[2]
            
            # That's our array with all the info about the mountpoint, and the dictionary to store it
            infos = i.xpath('./div[@class="mountcont"]/table/tbody/tr')
            dinfo = {}
            for lignes in infos:
                info = lignes.xpath('./td')                
                key = info[0].text.rpartition(':')[0]
                value = info[1].text
                dinfo[key] = value
            
            mountpoints[mountpoint] = dinfo
                
                
        return mountpoints    

if __name__ == '__main__':
    if len(argv) > 1:
        for url in argv[1:]:
            print('Treating ', url)
            ip = icecast_parser()
            dic = ip.parse_status(url)
            mounts = ip.guess_interesting_mounts(dic)
            print('interesting: ', mounts)
            print(dic)
            print(ip._server_name)
    else:
        ip = icecast_parser()
        dic = ip.parse_status(url="http://ice.stream.frequence3.net/status.xsl")
        mounts = ip.guess_interesting_mounts(dic)
        print('interesting: ', mounts)
        print(dic)
        
        ip = icecast_parser(ip="ice.stream.frequence3.net", port=80)
        dic = ip.parse_status()
        #ip._get_server_name()
        print(ip._server_name)
        mounts = ip.guess_interesting_mounts(dic)
        print('interesting: ', mounts)
        print(dic)

