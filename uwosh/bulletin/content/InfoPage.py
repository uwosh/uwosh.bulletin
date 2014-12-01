from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from uwosh.bulletin.config import *
from Products.ATContentTypes.content.document import ATDocument, ATDocumentSchema

InfoPageSchema = ATDocumentSchema.copy()
InfoPageSchema['title'].widget.label = "Info Page Title"
InfoPageSchema['text'].widget.label = "Info Page Body Text"

class InfoPage(ATDocument):
    
    implements(interfaces.IInfoPage, interfaces.IBatchPrintable)
    
    security = ClassSecurityInfo()
    schema = InfoPageSchema
    portal_type = "InfoPage"
    archetype_name = "InfoPage"
    meta_type = "InfoPage"

    
registerType(InfoPage, PRODUCT_NAME)
