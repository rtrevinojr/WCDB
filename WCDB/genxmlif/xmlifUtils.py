#
# genxmlif, Release 0.8
# file: xmlifUtils.py
#
# utility module for genxmlif
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
import re
import os
import urllib
import urlparse
from types import StringTypes, TupleType
from genxmlif import EMPTY_PREFIX, EMPTY_NAMESPACE

######################################################################
# DEFINITIONS
######################################################################

######################################################################
# REGULAR EXPRESSION OBJECTS
######################################################################

_reWhitespace  = re.compile('\s')
_reWhitespaces = re.compile('\s+')

_reSplitUrlApplication = re.compile (r"(file|http|ftp|gopher):(.+)") # "file:///d:\test.xml" => "file" + "///d:\test.xml"


######################################################################
# FUNCTIONS
######################################################################


########################################
# substitute multiple whitespace characters by a single ' '
#
def collapseString (strValue):
    return string.strip(_reWhitespaces.sub(' ', strValue))


########################################
# substitute each whitespace characters by a single ' '
#
def normalizeString (strValue):
    return _reWhitespace.sub(' ', strValue)


########################################
# process whitespace action
#
def processWhitespaceAction (strValue, wsAction):
    if wsAction == "collapse":
        return collapseString(strValue)
    elif wsAction == "replace":
        return normalizeString(strValue)
    else:
        return strValue
    

##########################################################
#  convert input parameter 'fileOrUrl' into a valid URL

def convertToUrl (fileOrUrl):
    matchObject = _reSplitUrlApplication.match(fileOrUrl)
    if matchObject:
        # given fileOrUrl is an absolute URL
        if matchObject.group(1) == 'file':
            path = re.sub(':', '|', matchObject.group(2)) # replace ':' by '|' in the path string
            url = "file:" + path
        else:
            url = fileOrUrl
    elif not os.path.isfile(fileOrUrl):
        # given fileOrUrl is treated as a relative URL
        url = fileOrUrl
    else:
        # local filename
#        url = "file:" + urllib.pathname2url (fileOrUrl)
        url = urllib.pathname2url (fileOrUrl)

    return url


##########################################################
#  convert input parameter 'fileOrUrl' into a valid absolute URL

def convertToAbsUrl (fileOrUrl, baseUrl):
    if fileOrUrl == "" and baseUrl != "":
        absUrl = "file:" + urllib.pathname2url (os.path.join(os.getcwd(), baseUrl, "__NO_FILE__"))
    elif os.path.isfile(fileOrUrl):
        absUrl = "file:" + urllib.pathname2url (os.path.join(os.getcwd(), fileOrUrl))
    else:
        matchObject = _reSplitUrlApplication.match(fileOrUrl)
        if matchObject:
            # given fileOrUrl is an absolute URL
            if matchObject.group(1) == 'file':
                path = re.sub(':', '|', matchObject.group(2)) # replace ':' by '|' in the path string
                absUrl = "file:" + path
            else:
                absUrl = fileOrUrl
        else:
            # given fileOrUrl is treated as a relative URL
            if baseUrl != "":
                absUrl = urlparse.urljoin (baseUrl, fileOrUrl)
            else:
                absUrl = fileOrUrl
#                raise IOError, "File %s not found!" %(fileOrUrl)
    return absUrl

##########################################################
#  normalize filter
def normalizeFilter (filterVar):
    if filterVar == None or filterVar == '*':
        filterVar = ("*",)
    elif not isinstance(filterVar, TupleType):
        filterVar = (filterVar,)
    return filterVar



######################################################################
# CLASSES
######################################################################

######################################################################
# class containing a tuple of namespace prefix and localName
#
class QNameTuple(tuple):
    def __str__(self):
        if self[0] != EMPTY_PREFIX:
            return "%s:%s" %(self[0],self[1])
        else:
            return self[1]
    

def QNameTupleFactory(initValue):
    if isinstance(initValue, StringTypes):
        separatorIndex = string.find (initValue, ':')
        if separatorIndex != -1:
            initValue = (initValue[:separatorIndex], initValue[separatorIndex+1:])
        else:
           initValue = (EMPTY_PREFIX, initValue)
    return QNameTuple(initValue)


######################################################################
# class containing a tuple of namespace and localName
#
class NsNameTuple(tuple):
    def __str__(self):
        if self[0] != EMPTY_NAMESPACE:
            return "{%s}%s" %(self[0],self[1])
        elif self[1] != None:
            return self[1]
        else:
            return "None"


def NsNameTupleFactory(initValue):
    if initValue == None:
        initValue = (EMPTY_NAMESPACE, initValue)
    elif isinstance(initValue, StringTypes):
        namespaceEndIndex = string.find (initValue, '}')
        if namespaceEndIndex != -1:
            initValue = (initValue[1:namespaceEndIndex], initValue[namespaceEndIndex+1:])
        else:
            initValue = (EMPTY_NAMESPACE, initValue)
    return NsNameTuple(initValue)


