#
# (C) Copyright 2003, 2004 Hewlett-Packard Development Company, L.P.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; version 2 of the License.
#   
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#   
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

# Author: Martin Pool <mbp@hp.com>

"""
tupletree - Convert XML DOM objects to and from tuple trees.

DOM is the standard in-memory representation of XML documents, but it
is very cumbersome for some types of processing where XML encodes
object structures rather than text documents.  Direct mapping to Python
classes may not be a good match either.

tupletrees may be created from an in-memory DOM using
dom_to_tupletree(), or from a string using xml_to_tupletree().

Since the Python XML libraries deal mostly with Unicode strings they
are also returned here.  If plain Strings are passed in they will be
converted by xmldom.

Each node of the tuple tree is a Python 4-tuple, corresponding to an
XML Element (i.e. <tag>):

  (NAME, ATTRS, CONTENTS, None)

The NAME is the name of the element.

The ATTRS are a name-value hash of element attributes.

The CONTENTS is a list of child elements.

The fourth element is reserved.
"""

def ele_to_tupletree(node):
    """Convert a ElementTree to a Tuple"""
    
    name = node.tag
    attrs = {}
    contents = []
    
    contents.append(node.text)
    
    for child in node:
        if str(type(child)) == "<type 'Element'>":
            contents.append(ele_to_tupletree(child))
            
    attrs = node.attrib
    return (name, attrs, contents, None)
    
def xml_to_tupletree(xml_string):
    """Parse XML straight into tupletree."""

    import xml.etree.cElementTree as ElementTree
    ele_xml = ElementTree.fromstring(xml_string)
    return ele_to_tupletree(ele_xml)
