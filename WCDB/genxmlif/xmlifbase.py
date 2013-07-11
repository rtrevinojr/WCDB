#
# genxmlif, Release 0.8
# file: xmlifbase.py
#
# abstract XML interface class
#
# history:
# 2005-04-25 rl   created
# 2006-08-18 rl   some methods for XML schema validation support added
# 2007-05-25 rl   performance optimization (caching) added, bugfixes for XPath handling
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
import os
import re
from types      import TupleType
from genxmlif   import EMPTY_PREFIX, EMPTY_NAMESPACE, XML_NAMESPACE, XMLNS_NAMESPACE
from xmlifUtils import convertToAbsUrl, processWhitespaceAction, NsNameTupleFactory


_reChild = re.compile('child *::')
_reAttribute = re.compile('attribute *::')


########################################
# define XML interface base class
# All not implemented methods have to be overloaded by the derived class!!
#

class XmlInterfaceBase:

    def __init__(self, verbose):
        self.verbose = verbose
        pass

    ##########################################################
    #  creates a new XML tree (DOM document)
    #  returns the created XML tree
    #  'file' may be a file path or an URI

    def createXmlTree (self, namespace, xmlRootTagName, publicId=None, systemId=None):
        raise NotImplementedError


    ##########################################################
    #  calls the parser for 'file'
    #  returns the respective XML tree for the parsed XML file
    #  'file' may be a file path or an URI

    def parse (self, file, baseUrl="", ownerDoc=None):
        raise NotImplementedError


    ##########################################################
    #  calls the parser for 'text'
    #  returns the respective XML tree for the parsed XML text string

    def parseString (self, text, baseUrl="", ownerDoc=None):
        raise NotImplementedError


    ##########################################################
    #  split 'qName' into prefix and local name

    def splitQName (self, qName):
        raise NotImplementedError


########################################
# define tree wrapper base class
# All not implemented methods have to be overloaded by the derived class!!
#

class TreeWrapperBase:

    def __init__(self, xmlIf, tree):
        self.xmlIf        = xmlIf
        self.tree         = tree

    ##########################################################
    #  inserts the children of the given subTree
    #  before 'nextSibling' ('nextSibling' is not removed!)
    #  returns the extended XML tree (containing children of subTree)

    def insertSubtree (self, nextSiblingWrapper, subTreeWrapper):
        raise NotImplementedError


    ##########################################################
    #  returns root node of given XML tree 'tree'

    def getRootNode (self):
        raise NotImplementedError


    ##########################################################
    #  returns 'tree' of given XML tree

    def getTree (self):
        return self.tree


    ##########################################################
    #  returns a string containing the textual representation of the XML tree

    def printTree (self, printElementValue=1):
        return self.getRootNode().printNode("", deep=1, printElementValue=printElementValue)


    ###############################################################
    # PRIVATE methods
    ###############################################################

    def _createElement (self, tupleOrLocalName):
        raise NotImplementedError


########################################
# define node wrapper base class
# All not implemented methods have to be overloaded by the derived class!!
#

class ElementWrapperBase:

    def __init__(self, xmlIf, treeWrapper, element):
        self.xmlIf           = xmlIf
        self.treeWrapper     = treeWrapper
        self.element         = element


    ##########################################################
    #  attributes of the current node can be accessed via key operator
    
    def __getitem__(self, tupleOrAttrName):
        return self.getAttribute (tupleOrAttrName)

    def __setitem__(self, tupleOrAttrName, attributeValue):
        self.setAttribute (tupleOrAttrName, attributeValue)


#++++++++++++ methods concerning the tag name ++++++++++++++++++++++++

    ##########################################################
    #  returns tag name of current node

    def getTagName (self):
        raise NotImplementedError


    ##########################################################
    #  returns local tag name of current node (without namespace)

    def getLocalName (self):
        try:
            return self.element.xmlIfLocalNameCache
        except:
            prefix, localName = self.xmlIf.splitQName (self.getTagName())
            self.element.xmlIfLocalNameCache = localName
        return localName


    ##########################################################
    #  returns namespace URI of tag name of current node

    def getNamespaceURI (self):
        raise NotImplementedError


    ##########################################################
    #  returns a tuple (namespace, localName) of current node
    def getNsName (self):
        try:
            return self.element.xmlIfExtNsNameCache
        except:
            self.element.xmlIfExtNsNameCache = NsNameTupleFactory( (self.getNamespaceURI(), self.getLocalName()) )
            return self.element.xmlIfExtNsNameCache


    ##########################################################
    #  returns the namespace prefix of the current node
    def getPrefix (self):
        return self.getNsPrefix(self.getNsName())

#++++++++++++ methods concerning print support ++++++++++++++++++++++++

    ##########################################################
    #  returns a string containing the textual representation of the XML tree

    def __str__ (self):
        return self.printNode("")

    def printNode (self, indent, deep=0, printElementValue=1):
        patternXmlTagShort = '''\
%(indent)s<%(tagName)s %(attributeString)s/>'''

        patternXmlTagLong = '''\
%(indent)s<%(tagName)s %(attributeString)s>
%(subTreeString)s\
%(elementValueString)s
%(indent)s</%(tagName)s>'''
        
        subTreeStringList = []
        if deep:
            for childNode in self.getChildren():
                subTreeStringList.append (childNode.printNode(indent + "    ", deep, printElementValue))
        subTreeString = string.join (subTreeStringList, "\n")
        
        attributeStringList = []
        for attrName in self.getAttributeList():
            attributeStringList.append ('%s="%s"' %(attrName, self.getAttribute(attrName)))
        attributeString = string.join (attributeStringList)

        tagName = self.getTagName()
        if printElementValue:
            elementValueString = self.getElementValue()
        else:
            elementValueString = ""

        if subTreeString == "" and elementValueString == "":
            printPattern = patternXmlTagShort
        else:
            printPattern = patternXmlTagLong
        return printPattern %vars()


#++++++++++++ methods concerning the parent of the current node ++++++++++++++++++++++++

    ##########################################################
    #  returns parent node of current node

    def getParentNode (self):
        raise NotImplementedError


#++++++++++++ methods concerning the children of the current node ++++++++++++++++++++++++


    ##########################################################
    #  returns child element nodes (list) of current node
    #  'tagFilter' is optional, 'tagFilter' = '*' must be supported
    #  'tagFilter' may contain also a list of tags

    def getChildren (self, tagFilter=None):
        raise NotImplementedError


    ##########################################################
    #  returns child element nodes (list) of current node
    #  'tagFilter' (localTagName) is optional, 'tagFilter' = '*' must be supported
    #  'tagFilter' may contain also a list of tags
    #  'namespaceURI' has to contain corresponding namespace URI or None

    def getChildrenNS (self, namespaceURI, tagFilter=None):
        return filter (lambda child: child.getNamespaceURI() == namespaceURI,
                       self.getChildren(tagFilter))


    ##########################################################
    #  returns first child element of current node
    #  or None if there is no suitable child element
    #  'tagFilter' (localTagName) is optional, 'tagFilter' = '*' must be supported
    #  'tagFilter' may contain also a list of tags

    def getFirstChild (self, tagFilter=None):
        children = self.getChildren(tagFilter)
        if children != []:
            return children[0]
        else:
            return None


    ##########################################################
    #  returns first child element of current node
    #  or None if there is no suitable child element
    #  'tagFilter' (localTagName) is optional, 'tagFilter' = '*' must be supported
    #  'tagFilter' may contain also a list of tags
    #  'namespaceURI' has to contain corresponding namespace URI or None

    def getFirstChildNS (self, namespaceURI, tagFilter=None):
        children = self.getChildrenNS (namespaceURI, tagFilter)
        if children != []:
            return children[0]
        else:
            return None


    ##########################################################
    #  returns all descendants of current node whose tag match 'tagName'
    #  'tagFilter' (localTagName) is optional, 'tagFilter' = '*' must be supported
    #  'tagFilter' may contain also a list of tags

    def getElementsByTagName (self, tagFilter=None):
        raise NotImplementedError


    ##########################################################
    #  returns all descendants of current node whose tag match 'localName' of the given namespace
    #  'tagFilter' (localTagName) is optional, 'tagFilter' = '*' must be supported
    #  'tagFilter' may contain also a list of tags
    #  'namespaceURI' has to contain corresponding namespace URI

    def getElementsByTagNameNS (self, namespaceURI, filterTag=None):
        return filter (lambda e: e.getNamespaceURI() == namespaceURI,
                       self.getElementsByTagName (filterTag))


    ##########################################################
    #  Append a child node to the children of the current node
    #  If not a element wrapper is given, a new element wrapper is created with tupleOrLocalName
    #  returns the element wrapper of the child element

    def appendChild (self, tupleOrLocalNameOrElement, attributeDict={}):
        raise NotImplementedError


    ##########################################################
    #  Insert a child node before the given reference child of the current node
    #  If not a element wrapper is given, a new element wrapper is created with tupleOrLocalName
    #  returns the element wrapper of the created child

    def insertBefore (self, tupleOrLocalNameOrElement, refChild, attributeDict={}):
        raise NotImplementedError


    ##########################################################
    #  remove given child node from children of current node

    def removeChild (self, childElementWrapper):
        raise NotImplementedError


    ##########################################################
    #  replace child node (include tag) by XML subtree

    def replaceChildBySubtree (self, childElementWrapper, subTreeWrapper):
        self.treeWrapper.insertSubtree (childElementWrapper, subTreeWrapper)
        self.removeChild (childElementWrapper)


#++++++++++++ methods concerning the attributes of the current node ++++++++++++++++++++++++

    ##########################################################
    #  returns dictionary with all attributes of current node

    def getAttributeDict (self):
        raise NotImplementedError


    ##########################################################
    #  returns list with all attributes in the sequence specified in the input XML file

    def getAttributeList (self):
        return self.element.xmlIfExtDict["attributeSequence"][:]    # return a copy!


    ##########################################################
    #  returns attribute value of given tupleOrAttrName
    #  or None if there is no suitable attribute

    def getAttribute (self, tupleOrAttrName):
        raise NotImplementedError


    ##########################################################
    #  returns attribute value if it exists or default value if not

    def getAttributeOrDefault (self, tupleOrAttrName, defaultValue):
        attributeValue = self.getAttribute (tupleOrAttrName)
        if attributeValue == None:
            attributeValue = defaultValue
        return attributeValue


    ##########################################################
    #  returns value of a QName attribute as tuple of namespace and localName

    def getQNameAttribute (self, tupleOrAttrName):
        try:
            return self.element.xmlIfExtQNameAttrCache[tupleOrAttrName]
        except:
            qName = self.getAttribute (tupleOrAttrName)
            nsName = self.qName2NsName(qName, useDefaultNs=1)
            self.element.xmlIfExtQNameAttrCache[tupleOrAttrName] = nsName
            return nsName


    ##########################################################
    #  returns 1 if attribute 'tupleOrAttrName' exists
    #          0 if not

    def hasAttribute (self, tupleOrAttrName):
        raise NotImplementedError


    ##########################################################
    #  sets value of attribute 'tupleOrAttrName' to 'attributeValue'
    #  if the attribute does not yet exist, it will be created

    def setAttribute (self, tupleOrAttrName, attributeValue):
        raise NotImplementedError


    ##########################################################
    #  set attribute value to default if it does not exist

    def setAttributeDefault (self, tupleOrAttrName, defaultValue):
        if not self.hasAttribute(tupleOrAttrName):
            self.setAttribute(tupleOrAttrName, defaultValue)


    ##########################################################
    #  process white spaces of the attribute according to wsAction

    def processWsAttribute (self, tupleOrAttrName, wsAction):
        attributeValue = self.getAttribute(tupleOrAttrName)
        newValue = processWhitespaceAction (attributeValue, wsAction)
        if newValue != attributeValue:
            self.setAttribute(tupleOrAttrName, newValue)
        

#++++++++++++ methods concerning the content of the current node ++++++++++++++++++++++++

    ##########################################################
    #  returns element value of current node

    def getElementValue (self):
        raise NotImplementedError


    ##########################################################
    #  set the element value of current node

    def setElementValue (self, elementValue):
        raise NotImplementedError


    ##########################################################
    #  process white spaces of the element value according to wsAction

    def processWsElementValue (self, wsAction):
        raise NotImplementedError
        

#++++++++++++ methods concerning the info about the current node in the XML file ++++++++++++++++++++


    ##########################################################
    #  returns the current start line number of the current node in the XML file

    def getStartLineNumber (self):
        return self.element.xmlIfExtDict["startLineNumber"]


    ##########################################################
    #  returns the current end line number of the current node in the XML file

    def getEndLineNumber (self):
        return self.element.xmlIfExtDict["endLineNumber"]


    ##########################################################
    #  returns the absolute URL of the XML file the current node belongs to

    def getAbsUrl (self):
        return self.element.xmlIfExtDict["absUrl"]


    ##########################################################
    #  returns the base URL for the current node

    def getBaseUrl (self):
        return self.element.xmlIfExtDict["baseUrl"]


    ##########################################################
    #  returns the file path of the XML file the current node belongs to

    def getFilePath (self):
        return self.element.xmlIfExtDict["filePath"]

    ##########################################################
    #  returns a string containing file name and line number of the current node
    #  (e.g. to be used for traces or error messages
    
    def getLocation (self, end=0, fullpath=0):
        lineMethod = (self.getStartLineNumber, self.getEndLineNumber)
        pathFunc = (os.path.basename, os.path.abspath)
        return "%s, %d" %(pathFunc[fullpath](self.getFilePath()), lineMethod[end]())


#++++++++++++ miscellaneous methods concerning namespaces ++++++++++++++++++++


    ##########################################################
    #  returns a list of the namespace prefix visible for the current node

    def getCurrentNamespaces (self):
        return self.element.xmlIfExtDict["curNs"]


    ##########################################################
    #  create NsName (namespaceURI and local name) from qName
    def qName2NsName (self, qName, useDefaultNs):
        if qName != None:
            qNamePrefix, qNameLocalName = self.xmlIf.splitQName (qName)
            for prefix, namespaceURI in self.getCurrentNamespaces():
                if qNamePrefix == prefix:
                    if prefix != EMPTY_PREFIX or useDefaultNs:
                        nsName = (namespaceURI, qNameLocalName)
                        break
            else:
                if qNamePrefix == None:
                    nsName = (EMPTY_NAMESPACE, qNameLocalName)
                else:
                    raise ValueError, "Namespace prefix '%s' not bound to a namespace!" %(qNamePrefix)
        else:
            nsName = (None, None)
        return NsNameTupleFactory(nsName)


    ##########################################################
    #  create QName from namespaceURI and localName
    def nsName2QName (self, nsLocalName):
        ns = nsLocalName[0]
        for prefix, namespace in self.getCurrentNamespaces():
            if ns == namespace:
                return "%s:%s" %(prefix, nsLocalName[1])
        else:
            if ns == None:
                return nsLocalName[1]
            else:
                raise LookupError, "Prefix for namespaceURI '%s' not found!" %(ns)


    ##########################################################
    #  evaluate namespace from QName
    def getNamespace (self, qName):
        if qName != None:
            qNamePrefix, qNameLocalName = self.xmlIf.splitQName (qName)
            for prefix, namespaceURI in self.getCurrentNamespaces():
                if qNamePrefix == prefix:
                    namespace = namespaceURI
                    break
            else:
                if qNamePrefix == None:
                    namespace = EMPTY_NAMESPACE
                else:
                    raise LookupError, "Namespace for QName '%s' not found!" %(qName)
        else:
            namespace = EMPTY_NAMESPACE
        return namespace


    ##########################################################
    #  evaluate namespace prefix from NsName
    def getNsPrefix (self, nsLocalName):
        ns = nsLocalName[0]
        for prefix, namespace in self.getCurrentNamespaces():
            if ns == namespace:
                return prefix
        else:
            if ns == None:
                return None
            else:
                raise LookupError, "Prefix for namespaceURI '%s' not found!" %(ns)


#++++++++++++ limited XPath support ++++++++++++++++++++


    ########################################
    # retrieve node list or attribute list for specified XPath
    def getXPathList (self, xPath, namespaceRef=None, useDefaultNs=1, attrIgnoreList=[]):
        if namespaceRef == None: namespaceRef = self
        xPath = _reChild.sub('./', xPath)
        xPath = _reAttribute.sub('@', xPath)
        xPathList = string.split (xPath, "|")
        completeChildDict = {}
        completeChildList = []
        attrNodeList = []
        attrNsNameFirst = None
        for xRelPath in xPathList:
            xRelPath = string.strip(xRelPath)
            descendantOrSelf = 0
            if xRelPath[:3] == ".//":
                descendantOrSelf = 1
                xRelPath = xRelPath[3:]
            xPathLocalStepList = string.split (xRelPath, "/")
            childList = [self,]
            for localStep in xPathLocalStepList:
                localStep = string.strip(localStep)
                stepChildList = []
                if localStep == "":
                    raise IOError ("Invalid xPath '%s'!" %(xRelPath))
                elif localStep == ".":
                    continue
                elif localStep[0] == '@':
                    if len(localStep) == 1:
                        raise ValueError ("Attribute name is missing in xPath!")
                    if descendantOrSelf:
                        childList = self.getElementsByTagName()
                    attrName = localStep[1:]
                    for childNode in childList:
                        if attrName == '*':
                            attrNodeList.append (childNode)
                            attrDict = childNode.getAttributeDict()
                            for attrIgnore in attrIgnoreList:
                                if attrDict.has_key(attrIgnore):
                                    del attrDict[attrIgnore]
                            stepChildList.extend(attrDict.values())
                            try:
                                attrNsNameFirst = attrDict.keys()[0]
                            except:
                                pass
                        else:
                            attrNsName = namespaceRef.qName2NsName (attrName, useDefaultNs=0)
                            if attrNsName[1] == '*':
                                for attr in childNode.getAttributeDict().keys():
                                    if attr[0] == attrNsName[0]:
                                        if attrNodeList == []:
                                            attrNsNameFirst = attrNsName
                                        attrNodeList.append (childNode)
                                        stepChildList.append (childNode.getAttribute(attr))
                            elif childNode.hasAttribute(attrNsName):
                                if attrNodeList == []:
                                    attrNsNameFirst = attrNsName
                                attrNodeList.append (childNode)
                                stepChildList.append (childNode.getAttribute(attrNsName))
                    childList = stepChildList
                else:
                    nsLocalName = namespaceRef.qName2NsName (localStep, useDefaultNs=useDefaultNs)
                    if descendantOrSelf:
                        descendantOrSelf = 0
                        if localStep == "*":
                            stepChildList = self.getElementsByTagName()
                        else:
                            stepChildList = self.getElementsByTagNameNS(nsLocalName[0], nsLocalName[1])
                    else:
                        for childNode in childList:
                            if localStep == "*":
                                stepChildList.extend (childNode.getChildren())
                            else:
                                stepChildList.extend (childNode.getChildrenNS(nsLocalName[0], nsLocalName[1]))
                    childList = stepChildList
            # filter duplicated childs
            for child in childList:
                try:
                    childKey = child.element
                except:
                    childKey = child
                if not completeChildDict.has_key(childKey):
                    completeChildList.append(child)
                    completeChildDict[childKey] = 1
        return completeChildList, attrNodeList, attrNsNameFirst


#++++++++++++ special XSD validation support ++++++++++++++++++++


    ########################################
    # store / retrieve reference to corresponding XSD node
    def setXsdNode (self, xsdNode):
        self.element.xmlIfExtDict["xsdNode"] = xsdNode

    def getXsdNode (self):
        return self.element.xmlIfExtDict["xsdNode"]
    
    ########################################
    # store / retrieve reference to corresponding XSD attribute node
    def setXsdAttrNode (self, tupleOrAttrName, xsdAttrNode):
        self.element.xmlIfExtDict["xsdAttrNodes"][tupleOrAttrName] = xsdAttrNode

    def getXsdAttrNode (self, tupleOrAttrName):
        try:
            return self.element.xmlIfExtDict["xsdAttrNodes"][tupleOrAttrName]
        except:
            if isinstance(tupleOrAttrName, TupleType):
                if tupleOrAttrName[1] == '*' and len(self.element.xmlIfExtDict["xsdAttrNodes"]) == 1:
                    return self.element.xmlIfExtDict["xsdAttrNodes"].values()[0]
            return None
    

    ###############################################################
    # PRIVATE methods
    ###############################################################

    def _createElement (self, tupleOrLocalName, attributeDict):
        childElement = self.treeWrapper._createElement (tupleOrLocalName)
        childElementWrapper = self.__class__(self.xmlIf, self.treeWrapper, childElement)
        childElementWrapper._initElement (attributeDict, self.element.xmlIfExtDict["curNs"]) # TODO: when to be adapted???)
        return childElementWrapper


    def _initElement (self, attributeDict, curNs):
        self.element.xmlIfChildrenCache = {}
        self.element.xmlIfExtFirstChildCache = {}
        self.element.xmlIfExtQNameAttrCache = {}
        self.element.xmlIfExtDict = {"baseUrl":  None,
                                     "absUrl"  : None,
                                     "filePath": None,
                                     "startLineNumber": None,
                                     "endLineNumber": None,
                                     "curNs"   : curNs[:],
                                     "attributeSequence": [],
                                     "xsdNode": None,
                                     "xsdAttrNodes": {},
                                    }
        for tupleOrAttrName, attrValue in attributeDict.items():
            self.setAttribute (tupleOrAttrName, attrValue)



########################################
# xmlif builder extension base class
#

class XmlIfBuilderExtensionBase:

    def __init__ (self, filePath, absUrl):
        self.filePath = filePath
        self.absUrl   = absUrl
        self.baseUrlStack  = [absUrl,]


    def startElementHandler (self, curNode, startLineNumber, curNs, attributes=[]):
        curNode.xmlIfExtChildrenCache = {}
        curNode.xmlIfExtFirstChildCache = {}
        curNode.xmlIfExtQNameAttrCache = {}
        curNode.xmlIfExtDict = {"baseUrl":  self._getBaseUrl(curNode),
                                "absUrl"  : self.absUrl,
                                "filePath": self.filePath,
                                "startLineNumber": startLineNumber,
                                "curNs"   : curNs,
                                "attributeSequence": [],
                                "xsdNode": None,
                                "xsdAttrNodes":{},
                               }
        curNode.xmlIfExtDict["curNs"].extend ([("xml", XML_NAMESPACE), ("xmlns", XMLNS_NAMESPACE)])
        for i in range (0, len(attributes), 2):
            curNode.xmlIfExtDict["attributeSequence"].append(attributes[i])

        self.baseUrlStack.insert (0, curNode.xmlIfExtDict["baseUrl"])


    def endElementHandler (self, curNode, endLineNumber):
        curNode.xmlIfExtDict["endLineNumber"] = endLineNumber
        self.baseUrlStack.pop (0)


    def _getBaseUrl (self, curNode):
        raise NotImplementedError

