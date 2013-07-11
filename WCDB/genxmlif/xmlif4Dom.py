#
# genxmlif, Release 0.8
# file: xmlif4Dom.py
#
# XML interface class to the 4DOM library
#
# history:
# 2005-04-25 rl   created
#
# Copyright (c) 2005-2007 by Roland Leuthe.  All rights reserved.
#
# --------------------------------------------------------------------
# The generix XML interface is
#
# Copyright (c) 2005-2007 by Roland Leuthe
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# the author not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
# ABILITY AND FITNESS.  IN NO EVENT SHALL THE AUTHOR
# BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
# --------------------------------------------------------------------

import urllib
from xml.dom.ext.reader.Sax2   import Reader, XmlDomGenerator
from xmlifUtils                import convertToAbsUrl
from xmlifDom                  import XmlInterfaceDom, TreeWrapperDom, XmlIfBuilderExtensionDom


class XmlInterface4Dom (XmlInterfaceDom):
    #####################################################
    # for description of the interface methods see xmlifbase.py
    #####################################################

    def __init__ (self, verbose):
        XmlInterfaceDom.__init__ (self, verbose)
        if self.verbose:
            print "Using 4Dom interface module..."


    def parse (self, file, baseUrl="", ownerDoc=None):
        absUrl = convertToAbsUrl (file, baseUrl)
        fp     = urllib.urlopen (absUrl)
        return self._parseStream (fp, file, absUrl, ownerDoc)


    def parseString (self, text, baseUrl="", ownerDoc=None):
        import cStringIO
        fp = cStringIO.StringIO(text)
        absUrl = convertToAbsUrl ("", baseUrl)
        return self._parseStream (fp, "", absUrl, ownerDoc)


    def _parseStream (self, fp, file, absUrl, ownerDoc):
        try:
            reader = Reader(validate=0, keepAllWs=0, catName=None, 
                            saxHandlerClass=ExtXmlDomGenerator, parser=None)
            reader.handler.extinit(file, absUrl, reader.parser)
            tree = reader.fromStream(fp, ownerDoc)
        finally:
            fp.close()
        
        return self.treeWrapper(self, tree)



###################################################
# Extended DOM generator class derived from XmlDomGenerator
# extended to store related line numbers, file/URL names and 
# defined namespaces in the node object

class ExtXmlDomGenerator(XmlDomGenerator, XmlIfBuilderExtensionDom):
    def __init__(self, keepAllWs=0):
        XmlDomGenerator.__init__(self, keepAllWs)


    def extinit(self, filePath, absUrl, parser):
        XmlIfBuilderExtensionDom.__init__(self, filePath, absUrl)
        self.parser   = parser


    def startElement(self, name, attribs):
        XmlDomGenerator.startElement(self, name, attribs)

        curNode = self._nodeStack[-1]
        XmlIfBuilderExtensionDom.startElementHandler (self, curNode, self.parser.getLineNumber(), self._namespaces.items())


    def endElement(self, name):
        curNode = self._nodeStack[-1]
        XmlIfBuilderExtensionDom.endElementHandler (self, curNode, self.parser.getLineNumber())
        XmlDomGenerator.endElement(self, name)
