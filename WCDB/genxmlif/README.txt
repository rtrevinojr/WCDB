Release Notes for genxmlif, Release 0.8

genxmlif is a generic XML interface package
which currently uses minidom, elementtree or 4DOM as XML parser
Other parsers can be adapted by implementing an appropriate interface class

--------------------------------------------------------------------
 The genxmlif generic XML interface package is

 Copyright (c) 2005-2006 by Roland Leuthe

 By obtaining, using, and/or copying this software and/or its
 associated documentation, you agree that you have read, understood,
 and will comply with the following terms and conditions:

 Permission to use, copy, modify, and distribute this software and
 its associated documentation for any purpose and without fee is
 hereby granted, provided that the above copyright notice appears in
 all copies, and that both that copyright notice and this permission
 notice appear in supporting documentation, and that the name of
 the author not be used in advertising or publicity
 pertaining to distribution of the software without specific, written
 prior permission.

 THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
 TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
 ABILITY AND FITNESS.  IN NO EVENT SHALL THE AUTHOR
 BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
 DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
 WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
 ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
 OF THIS SOFTWARE.
---------------------------------------------------------------------

Contents
========

README.txt
__init__.py
xmlif4Dom.py
xmlifbase.py
xmlifDom.py
xmlifElementTree.py
xmlifMinidom.py
xmlifUtils.py


---------------------------------------------------------------------

Documentation
=============

For documentation how to use genxmlif please refer my homepage

http://www.leuthe-net.de/GenXmlIf.html

---------------------------------------------------------------------

HISTORY:
=======

Changes for Release 0.8
=======================

- Caution, interface changed! Method getXPathList returns now 3 parameters instead of 1 in release 0.7!
- performance optimization (caching, mainly for elementtree interface)
- some bugs fixed


Changes for Release 0.7
=======================

- some special methods for XML schema validation support added
