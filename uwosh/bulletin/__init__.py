from Products.Archetypes import atapi
from Products.CMFCore import utils as cmfutils

##import sys, content

ADD_CONTENT_PERMISSION = "Add portal content"

##sys.modules['uwosh.bulletin.content.Department'] = content.College

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    import content

    content_types, constructors, ftis = atapi.process_types(atapi.listTypes('uwosh.bulletin'), 'uwosh.bulletin')

    cmfutils.ContentInit(
        'uwosh.bulletin Content',
        content_types = content_types,
        permission = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti = ftis,
        ).initialize(context)
