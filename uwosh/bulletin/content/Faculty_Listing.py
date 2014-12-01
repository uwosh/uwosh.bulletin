from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from uwosh.bulletin.config import *
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from uwosh.bulletin.widget import LiveReferenceWidget

schema = Schema((
    
    ReferenceField('assocFacultyFL',
        widget=LiveReferenceWidget(
            label="Faculty",
        ),
        relationship="WorksWith",
        vocabulary_display_path_bound=-1,
        allowed_types=('Faculty',),
        multiValued=1,
        
    ),

))

FacultyListingSchema = BaseSchema.copy() + schema.copy()
FacultyListingSchema['title'].widget.description = "A descriptive title for the faculty listing(i.e. Faculty Listing 2010-2012)"

class Faculty_Listing(BaseContent, BrowserDefaultMixin):
    """   
    A container for groupings of faculty members
    """
   
    security = ClassSecurityInfo()

    implements(interfaces.IFacultyListing)
    
    archetype_name = 'Faculty_Listing'
    meta_type = 'Faculty_Listing'
    portal_type = "Faculty_Listing"
    _at_rename_after_creation = True

    schema = FacultyListingSchema

    def sortFacultyListing(self):
	portal_catalog = getToolByName(self, 'portal_catalog')
        brains = portal_catalog.searchResults({'portal_type':'Faculty', 'sort_on':'sortable_title'})##if this path doesn't work get self.absolute_url()...{'query':'./'}...'path':'./',
        return brains
    
registerType(Faculty_Listing, PRODUCT_NAME)
