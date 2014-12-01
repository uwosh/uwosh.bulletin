from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from uwosh.bulletin.interfaces import ITOCRoot, ITOCAdapter
from uwosh.bulletin import interfaces
import interfaces
from uwosh.bulletin.config import *
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
import Products.CMFCore.permissions as CMFCorePermissions

DepartmentSchema =  ATFolderSchema.copy()
DepartmentSchema['title'].widget.title = "College Name"
DepartmentSchema['title'].widget.description = "" 



class Department(ATFolder):
    """
    Folderish type to hold Department/College-related information that should be contained by a Bulletin type
    """ 
   
    security = ClassSecurityInfo()

    implements(interfaces.IDepartment, interfaces.IBatchPrintable, ITOCRoot)
    
    archetype_name = 'Department'
    meta_type = 'Department'
    portal_type = "Department"
    _at_rename_after_creation = True

    schema = DepartmentSchema

    def getDescription(self):
        """ Returns the description of the Department
        """
        return self.Description()

    ##security.declareProtected(CMFCorePermissions.View, 'DepartmentObject')
    ##def DepartmentObject(self):
    ##    """ find manual from sub-object """
    ##    return self

    ##def getAssocFacultyListing(self):
    ##    return Bulletin.getAssocFacultyListing(self)##have to explicitly write call to parents getAssocFacultyListing because we deleted it from the Department schema so it could not be set on that level... still needs to be called and acquisition isn't cutting it for some odd reason...

#     def getFacultyList(self):##put Faculty List into an adapter as well? make these individual content types and make a bulletin adapter for all the extra functionality?##doing the faculty_list calculation here rather than on program... this method is for just populating the vocab
#         """vocabulary method to get vocabulary from the bulletin associated with this program"""
#         ##use acquisition to get the associated faculty listing
#         pairs = []
#         parent_obj = self.aq_parent
#         if hasattr(parent_obj, 'getAssocFacultyListing'):
#             faculty_listing = parent_obj.getAssocFacultyListing()##get the faculty listing grouping
#         elif hasattr(parent_obj, 'faculty_listing'):
#             faculty_listing = parent_obj.faculty_listing
#         else:
#             portal_catalog = getToolByName(self, 'portal_catalog')
#             all_faculty = portal_catalog.searchResults({'portal_type':'Faculty', 'review_state':'published'})
#             faculty_list = [(fac.UID, fac.Title) for fac in all_faculty]##should return a list of tuples
#             for faculty in faculty_list:
#                 pairs.append(faculty)
#             ##get all published Faculty from the catalog and return their UIDs and titles
#             return DisplayList(pairs)
        
#         faculty_vocab = faculty_listing.getAssocFacultyFL()
#         for faculty in faculty_vocab:
#             uid = faculty.UID()
#             label = faculty.title_or_id()
#             pairs.append((uid, label))
#         return DisplayList(pairs)

    def getTOCAdapter(self):
        return ITOCAdapter(self)

registerType(Department, PRODUCT_NAME)
