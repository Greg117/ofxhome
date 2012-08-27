import urllib
from datetime import datetime
from xml.dom.minidom import parseString

API_URL='http://www.ofxhome.com/api.php'

class OFXHome:

    @staticmethod
    def lookup(id):
        """
        Get financial institution OFX info given an ofxhome.com 'id'

        Returns: Institution

        bank = OFXHome.lookup('456')
        print bank.name _ bank.url _ bank.fid
        """
        return Institution(_xml_request({ 'lookup': id }))

    @staticmethod
    def all():
        """
        List every available bank that ofxhome.com knows about

        Returns: InstitutionList

        See also: OFXHome.search()
        """
        return search()

    @staticmethod
    def search(name=None):
        """
        Search for a financial institution by name.

        Returns: InstitutionList

        If no name is provided , or a name of None is provided then
        it is the same as calling OFXHome.all().  Note that passing a
        string of '' will not be the same thing and will result in no
        results.

        banks = OFXHome.search('America')
        for res in banks:
            print res.id _ res.name

            bank = OFXHome.lookup(res.id)
            print bank.name _ bank.url _ bank.fid
        """
        if name is None:
            params = { 'all': 'yes' }
        else:
            params = { 'search': name }
        return InstitutionList(_xml_request(params))

def _attr(node,name):
    return node.getAttribute(name)

def _text(parent,name):
    rc = []
    for node in parent.getElementsByTagName(name)[0].childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def _xml_request(params=None):
    encoded = urllib.urlencode(params)
    xml = urllib.urlopen("%s?%s" % (API_URL,encoded)).read()
    return xml

#---------------------------------------------
class InstitutionList:
    def __init__(self,xml):
        self.xml = xml
        self.xml_parsed = parseString(self.xml)

    @staticmethod
    def from_file(file):
        return InstitutionList(open(file,'r').read())

    def list(self):
        root = self.xml_parsed.documentElement
        data = []
        for node in root.getElementsByTagName('institutionid'):
            yield { 'name': _attr(node,'name'), 'id': _attr(node,'id') }

    def __iter__(self):
        return self.list()

    def __str__(self):
        return self.xml
#---------------------------------------------
class Institution:
    def __init__(self,xml):

        dom = parseString(xml)
        root = dom.documentElement

        self.id = _attr(root,'id')
        self.name = _text(root,'name')
        self.fid = _text(root,'fid')
        self.org = _text(root,'org')
        self.url = _text(root,'url')
        self.brokerid = _text(root,'brokerid')
        self.ofxfail = _text(root,'ofxfail')
        self.sslfail = _text(root,'sslfail')
        self.lastofxvalidation = datetime.strptime(_text(root,'lastofxvalidation'),"%Y-%m-%d %H:%M:%S")
        self.lastsslvalidation = datetime.strptime(_text(root,'lastsslvalidation'),"%Y-%m-%d %H:%M:%S")

        self.xml = xml

    @staticmethod
    def from_file(file):
        return Institution(open(file,'r').read())
