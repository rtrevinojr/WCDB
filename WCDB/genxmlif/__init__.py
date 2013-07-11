#
# genxmlif, Release 0.8
# file: __init__.py
#
# genxmlif package file
#
# history:
# 2005-04-25 rl   created
#
# Copyright (c) 2005-2006 by Roland Leuthe.  All rights reserved.
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


######################################################################
# PUBLIC DEFINITIONS
######################################################################


# supported XML interfaces

XMLIF_MINIDOM     = "XMLIF_MINIDOM"
XMLIF_4DOM        = "XMLIF_4DOM"
XMLIF_ELEMENTTREE = "XMLIF_ELEMENTTREE"



# namespace definitions

EMPTY_PREFIX    = None

EMPTY_NAMESPACE = None
XML_NAMESPACE   = "http://www.w3.org/XML/1998/namespace"
XMLNS_NAMESPACE = "http://www.w3.org/2000/xmlns/"


# definition of genxmlif path 

import os
GENXMLIF_DIR = os.path.dirname(__file__)


########################################
# central function to choose the XML interface to be used
#

def chooseXmlIf (xmlIf, verbose=0):
    if xmlIf == XMLIF_MINIDOM:
        import xmlifMinidom
        return xmlifMinidom.XmlInterfaceMinidom(verbose)

    elif xmlIf == XMLIF_4DOM:
        import xmlif4Dom
        return xmlif4Dom.XmlInterface4Dom(verbose)

    elif xmlIf == XMLIF_ELEMENTTREE:
        import xmlifElementTree
        return xmlifElementTree.XmlInterfaceElementTree(verbose)

    else:
        raise AttributeError, "Unknown XML interface: %s" %(xmlIf)

