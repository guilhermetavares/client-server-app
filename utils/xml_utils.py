'''
Copy to http://blog.luiscoms.com.br/python/converter-dicionario-para-xml.lcs
'''

from xml.dom import minidom
from collections import Mapping


def dict2element(root, structure, doc, cdatalist=[], attrlist=[]):
    """
    Gets a dictionary like structure and converts its
    content into xml elements. After that appends
    resulted elements to root element. If root element
    is a string object creates a new elements with the
    given string and use that element as root.
    This function returns a xml element object.
    """
    assert isinstance(structure, Mapping), 'Structure must be a mapping object'

    # if root is a string make it a element
    if isinstance(root, str):
        root = doc.createElement(root)

    for key, value in iter(structure.items()):
        el = doc.createElement(str(key))
        if isinstance(value, Mapping):
            dict2element(el, value, doc, cdatalist, attrlist)
        elif isinstance(value, list):
            for item in value:
                item_el = doc.createElement(str(key))
                dict2element(item_el, item, doc, cdatalist, attrlist)
                root.appendChild(item_el)

            continue
        else:
            value = str(value) if value is not None else ''
            if key in cdatalist:
                value = doc.createCDATASection(value)
            elif key in attrlist:
                root.setAttribute(key, value)
                continue
            else:
                value = doc.createTextNode(value)
            el.appendChild(value)
        root.appendChild(el)

    return root


def dict2xml(structure, tostring=False, cdatalist=[], attrlist=[]):
    """
    Gets a dict like object as a structure and returns a corresponding minidom
    document object.
    If str is needed instead of minidom, tostring parameter can be used
    Restrictions:
    Structure must only have one root.
    Structure must consist of str or dict objects (other types will
    converted into string)
    """
    # This is main function call. which will return a document
    assert len(structure) == 1, 'Structure must have only one root element'
    assert isinstance(
        structure, Mapping), 'Structure must be a mapping object such as dict'

    root_element_name, value = next(iter(structure.items()))
    impl = minidom.getDOMImplementation()
    doc = impl.createDocument(None, str(root_element_name), None)
    dict2element(doc.documentElement, value, doc, cdatalist, attrlist)
    return doc.toxml() if tostring else doc