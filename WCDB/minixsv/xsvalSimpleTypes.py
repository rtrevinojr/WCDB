#
# minixsv, Release 0.8
# file: xsvalSimpleTypes.py
#
# class for validation of XML schema simple types
#
# history:
# 2004-09-09 rl   created
# 2006-08-18 rl   W3C testsuite passed for supported features
# 2007-05-24 rl   Features for release 0.8 added, some bugs fixed
#
# Copyright (c) 2004-2007 by Roland Leuthe.  All rights reserved.
#
# --------------------------------------------------------------------
# The minixsv XML schema validator is
#
# Copyright (c) 2004-2007 by Roland Leuthe
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

import sys
import string
import re
import datetime
from decimal             import Decimal
from minixsv             import XSD_NAMESPACE
from genxmlif.xmlifUtils import collapseString, normalizeString, NsNameTupleFactory

###################################################
# Validator class for simple types
###################################################
class XsSimpleTypeVal:

    substMultiCharEscList = (
     (r"[\i-[:]]", "[a-zA-Z_]"),
     (r"\i", "[a-zA-Z_:]"),
     (r"\I", "[^a-zA-Z_:]"),
     (r"[\c-[:]]", "[\w.\-]"),
     (r"\c", "[\w.\-:]"),
     (r"\C", "[^\w.\-:]"),
     (r"\p{Lu}", "[A-Z]"),
     (r"\P{Lu}", "[^A-Z]"),
     (r"\p{Ll}", "[a-z]"),
     (r"\P{Ll}", "[^a-z]"),)

    def __init__ (self, parent):
        self.parent = parent
        self.xmlIf  = parent.xmlIf
        self.xsdNsURI = parent.xsdNsURI
        self.xsdIdDict = parent.xsdIdDict


    ########################################
    # validate given value against simpleType
    #
    def checkSimpleType (self, inputNode, attrName, typeName, attributeValue, returnDict):
        returnDict["BaseTypes"].append(str(typeName))
        if _suppBaseTypeDict.has_key(typeName):
            try:
                _suppBaseTypeDict[typeName] (inputNode, typeName, attributeValue, returnDict)
                returnDict["primitiveType"] = typeName
            except BaseTypeError, errstr:
                raise SimpleTypeError("Value of '%s' (%s) %s" %(attrName, attributeValue, errstr))

        elif self.parent.xsdTypeDict.has_key(typeName):
            typedefNode = self.parent.xsdTypeDict[typeName]
            if typedefNode.getNsName() == (XSD_NAMESPACE, "simpleType"):
                self.checkSimpleTypeDef (inputNode, typedefNode, attrName, attributeValue, returnDict)
            elif (typedefNode.getNsName() == (XSD_NAMESPACE, "complexType") and
                  typedefNode.getFirstChild().getNsName() == (XSD_NAMESPACE, "simpleContent")):
                self.checkSimpleTypeDef (inputNode, typedefNode.getFirstChild(), attrName, attributeValue, returnDict)
            elif typeName != (XSD_NAMESPACE, "anyType"):
                raise SimpleTypeError("Attribute '%s' requires a simple type (2)!" %(attrName))
            
            if typeName == (XSD_NAMESPACE, "ID"):
                if not self.xsdIdDict.has_key(attributeValue):
                    self.xsdIdDict[attributeValue] = inputNode
                else:
                    raise SimpleTypeError("There are multiple occurences of ID value '%s'!" %(attributeValue))
        else:
            # TODO: Fehler im XSD-File => Check muss an anderer Stelle erfolgen
            raise SimpleTypeError("%s uses unknown type '%s'!" %(attrName, str(typeName)))


    ########################################
    # validate given value against simpleType node
    #
    def checkSimpleTypeDef (self, inputNode, xsdElement, attrName, attributeValue, returnDict):
        restrictionElement = xsdElement.getFirstChildNS(self.xsdNsURI, "restriction")
        extensionElement   = xsdElement.getFirstChildNS(self.xsdNsURI, "extension")
        listElement        = xsdElement.getFirstChildNS(self.xsdNsURI, "list")
        unionElement       = xsdElement.getFirstChildNS(self.xsdNsURI, "union")
        if restrictionElement != None:
            self._checkRestrictionTag (inputNode, restrictionElement, attrName, attributeValue, returnDict)
        if extensionElement != None:
            self._checkExtensionTag (inputNode, extensionElement, attrName, attributeValue, returnDict)
        elif listElement != None:
            self._checkListTag (inputNode, listElement, attrName, attributeValue, returnDict)
        elif unionElement != None:
            self._checkUnionTag (inputNode, unionElement, attrName, attributeValue, returnDict)

    ########################################
    # validate given value against restriction node
    #
    def _checkRestrictionTag (self, inputNode, xsdElement, attrName, attributeValue, returnDict):
        # first check against base type
        baseType = xsdElement.getQNameAttribute("base")
        if baseType != NsNameTupleFactory(None):
            self.checkSimpleType (inputNode, attrName, baseType, attributeValue, returnDict)
        else:
            baseTypeNode = xsdElement.getFirstChildNS(self.xsdNsURI, "simpleType")
            self.checkSimpleTypeDef (inputNode, baseTypeNode, attrName, attributeValue, returnDict)

        minExcl = xsdElement.getFirstChildNS(self.xsdNsURI, "minExclusive")
        minIncl = xsdElement.getFirstChildNS(self.xsdNsURI, "minInclusive")
        maxExcl = xsdElement.getFirstChildNS(self.xsdNsURI, "maxExclusive")
        maxIncl = xsdElement.getFirstChildNS(self.xsdNsURI, "maxInclusive")

        if minExcl != None:
            minExclReturnDict = {"BaseTypes":[], "primitiveType":None}
            minExclValue = minExcl.getAttribute("value")
            self.checkSimpleType (inputNode, attrName, baseType, minExclValue, minExclReturnDict)
            if returnDict.has_key("orderedValue") and minExclReturnDict.has_key("orderedValue"):
                if returnDict["orderedValue"] <= minExclReturnDict["orderedValue"]:
                    raise SimpleTypeError ("Value of %s (%s) is <= minExclusive (%s)" %(attrName, attributeValue, minExclValue))
        elif minIncl != None:
            minInclReturnDict = {"BaseTypes":[], "primitiveType":None}
            minInclValue = minIncl.getAttribute("value")
            self.checkSimpleType (inputNode, attrName, baseType, minInclValue, minInclReturnDict)
            if returnDict.has_key("orderedValue") and minInclReturnDict.has_key("orderedValue"):
                if returnDict["orderedValue"] < minInclReturnDict["orderedValue"]:
                    raise SimpleTypeError ("Value of %s (%s) is < minInclusive (%s)" %(attrName, attributeValue, minInclValue))
        if maxExcl != None:
            maxExclReturnDict = {"BaseTypes":[], "primitiveType":None}
            maxExclValue = maxExcl.getAttribute("value")
            self.checkSimpleType (inputNode, attrName, baseType, maxExclValue, maxExclReturnDict)
            if returnDict.has_key("orderedValue") and maxExclReturnDict.has_key("orderedValue"):
                if returnDict["orderedValue"] >= maxExclReturnDict["orderedValue"]:
                    raise SimpleTypeError ("Value of %s (%s) is >= maxExclusive (%s)" %(attrName, attributeValue, maxExclValue))
        elif maxIncl != None:
            maxInclReturnDict = {"BaseTypes":[], "primitiveType":None}
            maxInclValue = maxIncl.getAttribute("value")
            self.checkSimpleType (inputNode, attrName, baseType, maxInclValue, maxInclReturnDict)
            if returnDict.has_key("orderedValue") and maxInclReturnDict.has_key("orderedValue"):
                if returnDict["orderedValue"] > maxInclReturnDict["orderedValue"]:
                    raise SimpleTypeError ("Value of %s (%s) is > maxInclusive (%s)" %(attrName, attributeValue, maxInclValue))

        totalDigitsNode = xsdElement.getFirstChildNS(self.xsdNsURI, "totalDigits")
        if totalDigitsNode != None:
            totalDigitsValue = totalDigitsNode.getAttribute("value")
            if totalDigitsNode.getAttribute("fixed") == "true":
                if len(re.findall("\d" ,attributeValue)) != string.atoi(totalDigitsValue):
                    raise SimpleTypeError ("Total number of digits != %s for %s (%s)" %(totalDigitsValue, attrName, attributeValue))
            else:
                if len(re.findall("\d" ,attributeValue)) > string.atoi(totalDigitsValue):
                    raise SimpleTypeError ("Total number of digits > %s for %s (%s)" %(totalDigitsValue, attrName, attributeValue))

        fractionDigitsNode = xsdElement.getFirstChildNS(self.xsdNsURI, "fractionDigits")
        if fractionDigitsNode != None:
            fractionDigitsValue = fractionDigitsNode.getAttribute("value")
            result = re.search("(?P<intDigits>\d*)(?P<dot>\.)(?P<fracDigits>\d+)" ,attributeValue)
            if result != None:
                numberOfFracDigits = len (result.group('fracDigits'))
            else:
                numberOfFracDigits = 0
            if fractionDigitsNode.getAttribute("fixed") == "true" and numberOfFracDigits != string.atoi(fractionDigitsValue):
                raise SimpleTypeError ("Fraction number of digits != %s for %s (%s)" %(fractionDigitsValue, attrName, attributeValue))
            elif numberOfFracDigits > string.atoi(fractionDigitsValue):
                raise SimpleTypeError ("Fraction number of digits > %s for %s (%s)" %(fractionDigitsValue, attrName, attributeValue))

        if returnDict.has_key("length"):
            lengthNode = xsdElement.getFirstChildNS(self.xsdNsURI, "length")
            if lengthNode != None:
                length = string.atoi(lengthNode.getAttribute("value"))
                if returnDict["length"] != length:
                    raise SimpleTypeError ("Length of %s (%s) must be %d!" %(attrName, attributeValue, length))
            minLengthNode = xsdElement.getFirstChildNS(self.xsdNsURI, "minLength")
            if minLengthNode != None:
                minLength = string.atoi(minLengthNode.getAttribute("value"))
                if returnDict["length"] < minLength:
                    raise SimpleTypeError ("Length of %s (%s) must be >= %d!" %(attrName, attributeValue, minLength))
            maxLengthNode = xsdElement.getFirstChildNS(self.xsdNsURI, "maxLength")
            if maxLengthNode != None:
                maxLength = string.atoi(maxLengthNode.getAttribute("value"))
                if returnDict["length"] > maxLength:
                    raise SimpleTypeError ("Length of %s (%s) must be <= %d!" %(attrName, attributeValue, maxLength))

        whiteSpace = xsdElement.getFirstChildNS(self.xsdNsURI, "whiteSpace")
        if whiteSpace != None:
            returnDict["wsAction"] = whiteSpace.getAttribute("value")
            if returnDict["wsAction"] == "replace":
                normalizedValue = normalizeString(attributeValue)
                if normalizedValue != attributeValue:
                    returnDict["adaptedAttrValue"] = normalizedValue
            elif returnDict["wsAction"] == "collapse":
                collapsedValue = collapseString(attributeValue)
                if collapsedValue != attributeValue:
                    returnDict["adaptedAttrValue"] = collapsedValue

        enumerationElementList = xsdElement.getChildrenNS(self.xsdNsURI, "enumeration")
        if enumerationElementList != []:
            for enumeration in enumerationElementList:
                if returnDict.has_key("adaptedAttrValue"):
                    attributeValue = returnDict["adaptedAttrValue"]
                if enumeration["value"] == attributeValue:
                    break
            else:
                raise SimpleTypeError ("Enumeration value '%s' not allowed!" %(attributeValue))

        patternNode = xsdElement.getFirstChildNS(self.xsdNsURI, "pattern")
        if patternNode != None:
            rePattern = patternNode.getAttribute("value")
            intRePattern = rePattern
            if returnDict.has_key("adaptedAttrValue"):
                attributeValue = returnDict["adaptedAttrValue"]
            try:
                regexObj = re.match(intRePattern, attributeValue)
                if not regexObj or regexObj.end() != len(attributeValue):
                    raise SimpleTypeError ("Value of attribute '%s' does not match pattern '%s'!" %(attrName, rePattern))
            except:
                for multiCharEsc, repl in XsSimpleTypeVal.substMultiCharEscList:
                    intRePattern = string.replace(intRePattern, multiCharEsc, repl)
                regexObj = re.match(intRePattern, attributeValue)
                if not regexObj or regexObj.end() != len(attributeValue):
                    raise SimpleTypeError ("Value of attribute '%s' does not match pattern '%s'!" %(attrName, rePattern))


    ########################################
    # validate given value against list node
    #
    def _checkListTag (self, inputNode, xsdElement, attrName, attributeValue, returnDict):
        if attributeValue != "":
            itemType = xsdElement.getQNameAttribute ("itemType")
            # substitute multiple whitespace characters by a single ' '
            collapsedValue = collapseString(attributeValue)
            returnDict["wsAction"] = "collapse"
            returnDict["adaptedAttrValue"] = collapsedValue

            # divide up attributeValue => store it into list
            attributeList = string.split(collapsedValue, " ")
            for attrValue in attributeList:
                elementReturnDict = {"BaseTypes":[], "primitiveType":None}
                if itemType != (None, None):
                    self.checkSimpleType (inputNode, attrName, itemType, attrValue, elementReturnDict)
                else:
                    itemTypeNode = xsdElement.getFirstChildNS(self.xsdNsURI, "simpleType")
                    self.checkSimpleTypeDef (inputNode, itemTypeNode, attrName, attrValue, elementReturnDict)

            returnDict["BaseTypes"].extend(elementReturnDict["BaseTypes"])
            returnDict["length"] = len(attributeList)
        else:
            returnDict["length"] = 0


    ########################################
    # validate given value against extension node
    #
    def _checkExtensionTag (self, inputNode, xsdElement, attrName, attributeValue, returnDict):
        # first check against base type
        baseType = xsdElement.getQNameAttribute("base")
        if baseType != NsNameTupleFactory(None):
            self.checkSimpleType (inputNode, attrName, baseType, attributeValue, returnDict)
        else:
            baseTypeNode = xsdElement.getFirstChildNS(self.xsdNsURI, "simpleType")
            self.checkSimpleTypeDef (inputNode, baseTypeNode, attrName, attributeValue, returnDict)


    ########################################
    # validate given value against union node
    #
    def _checkUnionTag (self, inputNode, xsdElement, attrName, attributeValue, returnDict):
        memberTypes = xsdElement.getAttribute ("memberTypes")
        if memberTypes != None:
            # substitute multiple whitespace characters by a single ' '
            # divide up attributeValue => store it into list
            for memberType in string.split(collapseString(memberTypes), " "):
                try:
                    self.checkSimpleType (inputNode, attrName, xsdElement.qName2NsName(memberType, useDefaultNs=1), attributeValue, returnDict)
                    return
                except SimpleTypeError, errstr:
                    pass

        # memberTypes and additional type definitions is legal!
        for childSimpleType in xsdElement.getChildrenNS(self.xsdNsURI, "simpleType"):
            try:
                self.checkSimpleTypeDef (inputNode, childSimpleType, attrName, attributeValue, returnDict)
                return
            except SimpleTypeError, errstr:
                pass

        raise SimpleTypeError ("%s (%s) is no valid union member type!" %(attrName, attributeValue))


###############################################################
#  Base type check functions
###############################################################

reDecimal      = re.compile("[+-]?[0-9]*.?[0-9]+")
reHexBinary    = re.compile("([a-fA-F0-9]{2})*")
reBase64Binary = re.compile("(?P<validBits>[a-zA-Z0-9+/]+)={0,3}")
reQName        = re.compile("[a-zA-Z_:][\w.\-:]*")
reDuration     = re.compile("-?P(?P<years>\d+Y)?(?P<months>\d+M)?(?P<days>\d+D)?(T(?P<hours>\d+H)?(?P<minutes>\d+M)?((?P<seconds>\d+)(?P<fracsec>.\d+)?S)?)?")
reDateTime     = re.compile("(?P<date>\d{4}-\d{2}-\d{2})T(?P<time>\d{2}:\d{2}:\d{2})(?P<offset>Z|[+-]\d{2}:\d{2})?")
reDate         = re.compile("\d{4}-\d{2}-\d{2}")
reTime         = re.compile("(?P<time>\d{2}:\d{2}:\d{2})(?P<offset>Z|[+-]\d{2}:\d{2})?")
reYearMonth    = re.compile("\d{4}-\d{2}")
reMonthDay     = re.compile("--\d{2}-\d{2}")
reMonth        = re.compile("--\d{2}(--)?")
reDay          = re.compile("---\d{2}")


def _checkAnySimpleType (inputNode, simpleType, attributeValue, returnDict):
    # TODO: Nothing to check??
    returnDict["length"] = len(attributeValue)

def _checkStringType (inputNode, simpleType, attributeValue, returnDict):
    # TODO: all valid??
    returnDict["length"] = len(attributeValue)

def _checkAnyUriType (inputNode, simpleType, attributeValue, returnDict):
    # TODO: any checks??
    if attributeValue[0:2] == '##':
        raise BaseTypeError("is not a valid URI!")
    returnDict["adaptedAttrValue"] = collapseString(attributeValue)
    returnDict["length"] = len(attributeValue)

def _checkDecimalType (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    regexObj = reDecimal.match(attributeValue)
    if not regexObj or regexObj.end() != len(attributeValue):
        raise BaseTypeError("is not a decimal value!")
    try:
        value = Decimal(attributeValue)
        returnDict["orderedValue"] = value
        returnDict["adaptedAttrValue"] = attributeValue
        returnDict["wsAction"] = "collapse"
    except:
        raise BaseTypeError("is out of range for validation!")

def _checkFloatType (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    if attributeValue not in ("INF", "-INF", "NaN"):
        try:
            value = float(attributeValue)
            returnDict["orderedValue"] = value
            returnDict["adaptedAttrValue"] = attributeValue
            returnDict["wsAction"] = "collapse"
        except:
            raise BaseTypeError("is not a float value!")

def _checkHexBinaryType (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    regexObj = reHexBinary.match(attributeValue)
    if not regexObj or regexObj.end() != len(attributeValue):
        raise BaseTypeError("is not a hexBinary value (each byte is represented by 2 characters)!")
    returnDict["length"] = len(attributeValue) / 2
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"

def _checkBase64BinaryType (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    regexObj = reBase64Binary.match(attributeValue)
    if not regexObj or regexObj.end() != len(attributeValue):
        raise BaseTypeError("is not a base64Binary value (6 bits are represented by 1 character)!")
    returnDict["length"] = (len(regexObj.group("validBits")) * 6) / 8
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"

def _checkBooleanType (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    if attributeValue not in ("true", "false", "1", "0"):
        raise BaseTypeError("is not a boolean value!")
    if attributeValue in ("true", "1"):
        returnDict["orderedValue"] = "__BOOLEAN_TRUE__"
    else:
        returnDict["orderedValue"] = "__BOOLEAN_FALSE__"
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"

def _checkQNameType (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    regexObj = reQName.match(attributeValue)
    if not regexObj or regexObj.end() != len(attributeValue):
        raise BaseTypeError("is not a QName!")
    try:
        inputNode.getNamespace(attributeValue)
    except LookupError:
        raise BaseTypeError("is not a valid QName (namespace prefix unknown)!")
    # TODO: It is not clear, what the length of a QName is!
    # returnDict["length"] = len(attributeValue)
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"

def _checkDurationType (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    regexObj = reDuration.match(attributeValue)
    if not regexObj or regexObj.end() != len(attributeValue) or attributeValue[-1] == "T":
        raise BaseTypeError("is not a valid duration value!")
    sign = ""
    if attributeValue[0] == "-": sign = "-"
    days = 0
    seconds = 0
    microseconds = 0
    if regexObj.group("years") != None:
        days = days + (int(sign + regexObj.group("years")[:-1]) * 365)
    if regexObj.group("months") != None:
        days = days + (int(sign + regexObj.group("months")[:-1]) * 30)
    if regexObj.group("days") != None:
        days = days + int(sign + regexObj.group("days")[:-1])
    if regexObj.group("hours") != None:
        seconds = seconds + int(sign + regexObj.group("hours")[:-1]) * 3600
    if regexObj.group("minutes") != None:
        seconds = seconds + (int(sign + regexObj.group("minutes")[:-1]) * 60)
    if regexObj.group("seconds") != None:
        seconds = seconds + int(sign + regexObj.group("seconds"))
    if regexObj.group("fracsec") != None:
        microseconds = int(Decimal(sign + regexObj.group("fracsec")[:-1]) * 1000000)
    try:
        timeDeltaObj = datetime.timedelta(days=days, seconds=seconds, microseconds=microseconds)
    except ValueError, errstr:
        raise BaseTypeError("is invalid (%s)!" %(errstr))
    returnDict["orderedValue"] = timeDeltaObj
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"
    
def _checkDateTimeType (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    regexObj = reDateTime.match(attributeValue)
    if not regexObj or regexObj.end() != len(attributeValue):
        raise BaseTypeError("is not a dateTime value!")
    date = regexObj.group("date")
    time = regexObj.group("time")
    offset = regexObj.group("offset")
    try:
        if offset != None:
            tz = TimezoneFixedOffset(offset)
        else:
            tz = None
        dtObj = datetime.datetime(int(date[0:4]),int(date[5:7]),int(date[8:10]),
                                  int(time[0:2]),int(time[3:5]),int(time[6:8]), 0, tz)
    except ValueError, errstr:
        raise BaseTypeError("is invalid (%s)!" %(errstr))
    returnDict["orderedValue"] = dtObj
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"
    
def _checkDateType (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    regexObj = reDate.match(attributeValue)
    if not regexObj or regexObj.end() != len(attributeValue):
        raise BaseTypeError("is not a date value!")
    try:
        dateObj = datetime.date(int(attributeValue[0:4]),int(attributeValue[5:7]),int(attributeValue[8:10]))
    except ValueError, errstr:
        raise BaseTypeError("is invalid (%s)!" %(errstr))
    returnDict["orderedValue"] = dateObj
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"
    
def _checkTimeType (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    regexObj = reTime.match(attributeValue)
    if not regexObj or regexObj.end() != len(attributeValue):
        raise BaseTypeError("is not a time value!")
    time = regexObj.group("time")
    offset = regexObj.group("offset")
    try:
        if offset != None:
            tz = TimezoneFixedOffset(offset)
        else:
            tz = None
        timeObj = datetime.time(int(time[0:2]),int(time[3:5]),int(time[6:8]), 0, tz)
    except ValueError, errstr:
        raise BaseTypeError("is invalid (%s)!" %(errstr))
    returnDict["orderedValue"] = timeObj
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"
    
def _checkYearMonth (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    regexObj = reYearMonth.match(attributeValue)
    if not regexObj or regexObj.end() != len(attributeValue):
        raise BaseTypeError("is not a gYearMonth value!")
    try:
        dateObj = datetime.date(int(attributeValue[0:4]),int(attributeValue[5:7]),1)
    except ValueError, errstr:
        raise BaseTypeError("is invalid (%s)!" %(errstr))
    returnDict["orderedValue"] = dateObj
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"

def _checkMonthDay (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    regexObj = reMonthDay.match(attributeValue)
    if not regexObj or regexObj.end() != len(attributeValue):
        raise BaseTypeError("is not a gMonthDay value!")
    try:
        dateObj = datetime.date(2004, int(attributeValue[2:4]),int(attributeValue[5:7]))
    except ValueError, errstr:
        raise BaseTypeError("is invalid (%s)!" %(errstr))
    returnDict["orderedValue"] = dateObj
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"
    
def _checkYear (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    try:
        year = int(attributeValue)
        if year < 1 or year > 9999:
            raise BaseTypeError("is not a valid gYear value!")
    except:
        raise BaseTypeError("is not a gYear value!")
    returnDict["orderedValue"] = year
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"

def _checkMonth (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    regexObj = reMonth.match(attributeValue)
    if not regexObj or regexObj.end() != len(attributeValue):
        raise BaseTypeError("is not a gMonth value!")
    month = int(attributeValue[2:4])
    if month < 1 or month > 12:
        raise BaseTypeError("is invalid (month must be in 1..12)!")
    returnDict["orderedValue"] = month
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"

def _checkDay (inputNode, simpleType, attributeValue, returnDict):
    attributeValue = collapseString(attributeValue)
    regexObj = reDay.match(attributeValue)
    if not regexObj or regexObj.end() != len(attributeValue):
        raise BaseTypeError("is not a gDay value!")
    day = int(attributeValue[3:5])
    if day < 1 or day > 31:
        raise BaseTypeError("is invalid (day must be in 1..31)!")
    returnDict["orderedValue"] = day
    returnDict["adaptedAttrValue"] = attributeValue
    returnDict["wsAction"] = "collapse"

########################################
# timezone class
#
class TimezoneFixedOffset(datetime.tzinfo):
    def __init__(self, offset):
        if offset == "Z":
            self.__offset = datetime.timedelta(0)
        else:
            self.__offset = datetime.timedelta(hours=int(offset[0:3]), 
                                               minutes=int(offset[0] + offset[4:5]))

    def utcoffset(self, dt):
        return self.__offset
    def tzname(self, dt):
        return None

    def dst(self, dt):
        return datetime.timedelta(0)

########################################
# define own exception for XML schema validation errors
#
class SimpleTypeError (StandardError):
    pass

class BaseTypeError (StandardError):
    pass


########################################
# Base type dictionaries
#
_suppBaseTypeDict = {(XSD_NAMESPACE, "anySimpleType"):    _checkAnySimpleType,
                     (XSD_NAMESPACE, "string"):           _checkStringType,
                     (XSD_NAMESPACE, "anyURI"):           _checkAnyUriType,
                     (XSD_NAMESPACE, "decimal"):          _checkDecimalType,
                     (XSD_NAMESPACE, "float"):            _checkFloatType,
                     (XSD_NAMESPACE, "double"):           _checkFloatType,
                     (XSD_NAMESPACE, "hexBinary"):        _checkHexBinaryType,
                     (XSD_NAMESPACE, "base64Binary"):     _checkBase64BinaryType,
                     (XSD_NAMESPACE, "boolean"):          _checkBooleanType,
                     (XSD_NAMESPACE, "QName"):            _checkQNameType,
                     (XSD_NAMESPACE, "NOTATION"):         _checkQNameType,
                     (XSD_NAMESPACE, "duration"):         _checkDurationType,
                     (XSD_NAMESPACE, "dateTime"):         _checkDateTimeType,
                     (XSD_NAMESPACE, "date"):             _checkDateType,
                     (XSD_NAMESPACE, "time"):             _checkTimeType,
                     (XSD_NAMESPACE, "gYearMonth"):       _checkYearMonth,
                     (XSD_NAMESPACE, "gMonthDay"):        _checkMonthDay,
                     (XSD_NAMESPACE, "gYear"):            _checkYear,
                     (XSD_NAMESPACE, "gMonth"):           _checkMonth,
                     (XSD_NAMESPACE, "gDay"):             _checkDay,
                    }

