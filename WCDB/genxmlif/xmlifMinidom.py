#
# genxmlif, Release 0.8
# file: xmlifMinidom.py
#
# XML interface class to Python standard minidom
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

import string
import urllib
from xml.dom.expatbuilder import ExpatBuilderNS
from xmlifUtils           import convertToAbsUrl, NsNameTupleFactory
from xmlifDom             import XmlInterfaceDom, ElementWrapperDom, XmlIfBuilderExtensionDom


class XmlInterfaceMinidom (XmlInterfaceDom):
    #####################################################
    # for description of the interface methods see xmlifbase.py
    #####################################################

    def __init__ (self, verbose):
        XmlInterfaceDom.__init__ (self, verbose)
        self.elementWrapper = ElementWrapperMinidom
        if self.verbose:
            print "Using minidom interface module..."


    def createXmlTree (self, namespace, xmlRootTagName, publicId=None, systemId=None):
        from xml.dom.minidom import getDOMImplementation
        domImpl = getDOMImplementation()
        doctype = domImpl.createDocumentType(xmlRootTagName, publicId, systemId)
        domTree = domImpl.createDocument(namespace, xmlRootTagName, doctype)
        treeWrapperInst = self.treeWrapper(self, domTree)
        treeWrapperInst.getRootNode()._initElement ({}, []) # TODO: namespace handling
        return treeWrapperInst


    def parse (self, file, baseUrl="", ownerDoc=None):
        absUrl = convertToAbsUrl(file, baseUrl)
        fp     = urllib.urlopen (absUrl)
        try:
            builder = ExtExpatBuilderNS(file, absUrl)
            tree = builder.parseFile(fp)
        finally:
            fp.close()

        return self.treeWrapper(self, tree)


    def parseString (self, text, baseUrl="", ownerDoc=None):
        absUrl = convertToAbsUrl ("", baseUrl)
        builder = ExtExpatBuilderNS("", absUrl)
        tree = builder.parseString (text)
        return self.treeWrapper (self, tree)




class ElementWrapperMinidom (ElementWrapperDom):

    def getAttributeDict (self):
        """Return dictionary of attributes"""
        attribDict = {}
        for attrNameNS, attrNodeOrValue in self.element.attributes.itemsNS():
            attribDict[NsNameTupleFactory(attrNameNS)] = attrNodeOrValue
                
        return attribDict


###################################################
# Extended Expat Builder class derived from ExpatBuilderNS
# extended to store related line numbers, file/URL names and 
# defined namespaces in the node object

class ExtExpatBuilderNS (ExpatBuilderNS, XmlIfBuilderExtensionDom):
    def __init__ (self, filePath, absUrl):
        ExpatBuilderNS.__init__(self)
        XmlIfBuilderExtensionDom.__init__(self, filePath, absUrl)

        # set EndNamespaceDeclHandler, currently not used by minidom
        self.getParser().EndNamespaceDeclHandler = self.end_namespace_decl_handler
        self.curNamespaces = []


    def start_element_handler(self, name, attributes):
        ExpatBuilderNS.start_element_handler(self, name, attributes)

        # use attribute format {namespace}localName
        attrList = []
        for i in range (0, len(attributes), 2):
            attrName = attributes[i]
            attrNameSplit = string.split(attrName, " ")
            if len(attrNameSplit) > 1:
                attrName = (attrNameSplit[0], attrNameSplit[1])
            attrList.extend([attrName, attributes[i+1]])
        
        XmlIfBuilderExtensionDom.startElementHandler (self, self.curNode, self.getParser().ErrorLineNumber, self.curNamespaces[:], attrList)


    def end_element_handler(self, name):
        XmlIfBuilderExtensionDom.endElementHandler (self, self.curNode, self.getParser().ErrorLineNumber)
        ExpatBuilderNS.end_element_handler(self, name)


    def start_namespace_decl_handler(self, prefix, uri):
        ExpatBuilderNS.start_namespace_decl_handler(self, prefix, uri)
        self.curNamespaces.insert(0, (prefix, uri))


    def end_namespace_decl_handler(self, prefix):
        assert self.curNamespaces.pop(0)[0] == prefix, "implementation confused"
