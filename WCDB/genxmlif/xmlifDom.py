#
# genxmlif, Release 0.8
# file: xmlifDom.py
#
# XML interface base class for Python DOM implementations
#
# history:
# 2005-04-25 rl   created
#
# Copyright (c) 2005-2007 by Roland Leuthe.  All rights reserved.
#
# --------------------------------------------------------------------
# The generic XML interface is
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
from types                import TupleType
from genxmlif             import XML_NAMESPACE
from xmlifUtils           import convertToAbsUrl, processWhitespaceAction, NsNameTuple, NsNameTupleFactory, normalizeFilter
from xmlifbase            import XmlInterfaceBase, TreeWrapperBase, ElementWrapperBase, XmlIfBuilderExtensionBase
from xml.dom              import Node


class XmlInterfaceDom (XmlInterfaceBase):
    #####################################################
    # for description of the interface methods see xmlifbase.py
    #####################################################

    def __init__ (self, verbose):
        XmlInterfaceBase.__init__ (self, verbose)
        self.treeWrapper    = TreeWrapperDom
        self.elementWrapper = ElementWrapperDom


    def splitQName (self, qName):
        namespaceEndIndex = string.find (qName, ':')
        if namespaceEndIndex != -1:
            prefix     = qName[:namespaceEndIndex]
            localName  = qName[namespaceEndIndex+1:]
        else:
            prefix     = None
            localName  = qName
        return prefix, localName


#########################################################
# Wrapper class for Document class

class TreeWrapperDom (TreeWrapperBase):

    def getRootNode (self):
        domNode = self.getTree()
        if domNode.nodeType == Node.DOCUMENT_NODE:
            return self.xmlIf.elementWrapper (self.xmlIf, self, domNode.documentElement)
        elif domNode.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
            for node in domNode.childNodes:
                if node.nodeType == Node.ELEMENT_NODE:
                    return self.xmlIf.elementWrapper (self.xmlIf, self, node)
            else:
                return None
        else:
            return None


    def insertSubtree (self, nextSiblingWrapper, subTreeWrapper):
        elementWrapperList = subTreeWrapper.getRootNode().getChildren()
        for elementWrapper in elementWrapperList:
            if nextSiblingWrapper != None:
                self.getRootNode().element.insertBefore(elementWrapper.element, nextSiblingWrapper.element)
            else:
                self.getRootNode().element.appendChild(elementWrapper.element)


    def _createElement (self, tupleOrLocalName):
        if not isinstance(tupleOrLocalName, TupleType):
            elementNode = self.tree.createElement(tupleOrLocalName)
        else:
            elementNode = self.tree.createElementNS(tupleOrLocalName[0], tupleOrLocalName[1])
        return elementNode


    def _createTextNode (self, data):
        return self.tree.createTextNode(data)
    

#########################################################
# Wrapper class for DOM Element class

class ElementWrapperDom (ElementWrapperBase):

    def getTagName (self):
        return self.element.tagName


    def getLocalName (self):
        # base method replaced (optimized method)
        return self.element.localName


    def getNamespaceURI (self):
        return self.element.namespaceURI


    def getParentNode (self):
        return self.__class__(self.xmlIf, self.treeWrapper, self.element.parentNode)


    def getChildren (self, tagFilter=None):
        tagFilter = normalizeFilter (tagFilter)

        children = filter (lambda e: (e.nodeType == Node.ELEMENT_NODE) and          # - only ELEMENTs
                                     (tagFilter == ("*",) or e.localName in tagFilter), # - if tagFilter given --> check
                           self.element.childNodes)                                 # from element's nodes

        return map(lambda element: self.__class__(self.xmlIf, self.treeWrapper, element), children)


    def getElementsByTagName (self, tagFilter=None):
        tagFilter = normalizeFilter (tagFilter)
        elementList = []
        for tagFlt in tagFilter:
            elementList.extend (self.element.getElementsByTagName(tagFlt))
            
        return map(lambda element: self.__class__(self.xmlIf, self.treeWrapper, element), elementList)


    def getElementsByTagNameNS (self, namespaceURI, tagFilter=None):
        tagFilter = normalizeFilter (tagFilter)
        elementList = []

        for tagFlt in tagFilter:
            elementList.extend (self.element.getElementsByTagNameNS(namespaceURI, tagFlt))
        
        return map(lambda element: self.__class__(self.xmlIf, self.treeWrapper, element), elementList)


    def appendChild (self, tupleOrLocalNameOrElement, attributeDict={}):
        if not isinstance(tupleOrLocalNameOrElement, ElementWrapperDom):
            childElementWrapper = self._createElement (tupleOrLocalNameOrElement, attributeDict)
        else:
            childElementWrapper = tupleOrLocalNameOrElement
        self.element.appendChild (childElementWrapper.element)
        return childElementWrapper


    def insertBefore (self, tupleOrLocalNameOrElement, refChild, attributeDict={}):
        if not isinstance(tupleOrLocalNameOrElement, ElementWrapperDom):
            childElementWrapper = self._createElement (tupleOrLocalNameOrElement, attributeDict)
        else:
            childElementWrapper = tupleOrLocalNameOrElement
        if refChild == None:
            self.element.appendChild (childElementWrapper.element)
        else:    
            self.element.insertBefore (childElementWrapper.element, refChild.element)
        return childElementWrapper


    def removeChild (self, childElementWrapper):
        self.element.removeChild(childElementWrapper.element)


    def getAttributeDict (self):
        """Return dictionary of attributes"""
        attribDict = {}
        for attrNameNS, attrNodeOrValue in self.element.attributes.items():
            attribDict[NsNameTupleFactory(attrNameNS)] = attrNodeOrValue.nodeValue
                
        return attribDict


    def getAttribute (self, tupleOrAttrName):
        if not isinstance(tupleOrAttrName, TupleType):
            tupleOrAttrName = (None, tupleOrAttrName)
        
        if self.element.attributes.has_key (tupleOrAttrName):
            return self.element.getAttributeNS (tupleOrAttrName[0], tupleOrAttrName[1])
        else:
            return None


    def hasAttribute (self, tupleOrAttrName):
        if not isinstance(tupleOrAttrName, TupleType):
            tupleOrAttrName = (None, tupleOrAttrName)

        return self.element.attributes.has_key (tupleOrAttrName)


    def setAttribute (self, tupleOrAttrName, attributeValue):
        if not self.hasAttribute (tupleOrAttrName):
            self.element.xmlIfExtDict["attributeSequence"].append(tupleOrAttrName)

        if self.element.xmlIfExtQNameAttrCache.has_key(tupleOrAttrName):
            del self.element.xmlIfExtQNameAttrCache[tupleOrAttrName]

        if not isinstance(tupleOrAttrName, TupleType):
            tupleOrAttrName = (None, tupleOrAttrName)

        if tupleOrAttrName[0] != None:
            qName = self.nsName2QName(tupleOrAttrName)
        else:
            qName = tupleOrAttrName[1]
        
        self.element.setAttributeNS(tupleOrAttrName[0], qName, attributeValue)
            

    def getElementValue (self):
        elementValueList = ["",]
        elementValueList.extend (map(lambda textNode: textNode.data , self._getChildTextNodes()))
        return string.join (elementValueList, "")


    def setElementValue (self, elementValue):
        if self._getChildTextNodes() == []:
            textNode = self.treeWrapper._createTextNode(elementValue)
            self.element.appendChild (textNode)
        else:
            self._getChildTextNodes()[0].data = elementValue
            if len(self._getChildTextNodes() > 1):
                for textNode in self._getChildTextNodes()[1:]:
                    textNode.data = ""

    
    def processWsElementValue (self, wsAction):
        textNodes = self._getChildTextNodes()
        for textNode in textNodes:
            textNode.data = processWhitespaceAction (textNode.data, wsAction)


    ###############################################################
    # PRIVATE methods
    ###############################################################

    def _getChildTextNodes (self):
        """Return list of TEXT nodes."""
        return filter (lambda e: (e.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE)),        # - only TEXT-NODES
                       self.element.childNodes)                         # from element's child nodes


########################################
# xmlIf builder extension class
#

class XmlIfBuilderExtensionDom (XmlIfBuilderExtensionBase):
    
    def _getBaseUrl (self, curNode):
        if curNode.attributes.has_key ((XML_NAMESPACE, "base")):
            return convertToAbsUrl (curNode.getAttributeNS (XML_NAMESPACE, "base"), self.baseUrlStack[0])
        else:
            return self.baseUrlStack[0]

