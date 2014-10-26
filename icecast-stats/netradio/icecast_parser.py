'''
Created on 26 oct. 2014

@author: gilles
'''

from lxml import etree
class icecast_parser:
    interesting_mounts = ''
    def guess_interesting_mounts(self, mountpoints, sep='-'):
        im = [ m.rpartition(sep)[0] for m in mountpoints.keys() if len(m.rpartition(sep)[0]) > 1]
        return set(im)
    
    def parse_status(self, url=""):
        parser = etree.HTMLParser()
        tree = etree.parse(url, parser)
        sources = tree.xpath('/html/body/div/div[@class="roundcont"]')
        mountpoints = {}
        for i in sources:
            mountpoint = i.xpath('./div[@class="newscontent"]/div/table/tr/td/h3')[0].text.rpartition('/')[2]
            
            infos = i.xpath('./div[@class="newscontent"]/table/tr')
            dinfo = {}
            for lignes in infos:
                info = lignes.xpath('./td')                
                key = info[0].text.rpartition(':')[0]
                value = info[1].text
                dinfo[key] = value
            
            mountpoints[mountpoint] = dinfo
                
                
        return mountpoints
                
    

if __name__ == '__main__':
    ip = icecast_parser()
    dic = ip.parse_status("http://ice.stream.frequence3.net/status.xsl")
    mounts = ip.guess_interesting_mounts(dic)
    print('interesting: ', mounts)
    print(dic)
