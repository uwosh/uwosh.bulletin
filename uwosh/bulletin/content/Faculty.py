from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from uwosh.bulletin.config import *
from Products.ATContentTypes.content.image import ATImage, ATImageSchema
##from Products.ATContentTypes.content.base import ATCTFileContent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

copied_fields = {}
copied_fields['title'] = BaseSchema['title'].copy()
copied_fields['title'].widget.label = "Full Name"

copied_fields['description'] = BaseSchema['description'].copy()
copied_fields['description'].widget.label = "Professional Title"

##copied_fields['image'] = ATImageSchema['image'].copy()
##copied_fields['image'].widget.label = "Faculty Image"
##copied_fields['image'].primary = False
##copied_fields['image'].required = False
##copied_fields['image'].storage = AttributeStorage()

schema = Schema((
    copied_fields['title'],
    copied_fields['description'],

    TextField(
        name='degrees',
        allowable_content_types=('text/plain','text/html'),
        widget=RichWidget(
            label="Degrees",
            description="List Degrees Below",
        ),
        default_output_type='text/html',
    ),

    ImageField(
        name='fac_image',
        widget=ImageWidget(
            label="Image",
            description="Add a faculty image here",
        ),
        storage=AttributeStorage()
    ),

))

FacultySchema = BaseSchema.copy() + schema.copy()

class Faculty(BaseContent, BrowserDefaultMixin):
    
    implements(interfaces.IFaculty, interfaces.IBatchPrintable)
    
    security = ClassSecurityInfo()
    schema = FacultySchema
    portal_type = "Faculty"
    archetype_name = "Faculty"
    meta_type = "Faculty"

    
registerType(Faculty, PRODUCT_NAME)
