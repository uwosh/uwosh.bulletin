from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from uwosh.bulletin.interfaces import ITOCRoot, ITOCAdapter
import interfaces
from uwosh.bulletin.config import *
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
import Products.CMFCore.permissions as CMFCorePermissions
from Products.CMFPlone.browser.navtree import NavtreeStrategyBase, buildFolderTree
from AccessControl import ClassSecurityInfo
import re
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base
##IMG_PATTERN = re.compile(r"""(\<img .*?)src="([^/]+?)"(.*?\>)""", re.IGNORECASE | re.DOTALL)

schema = Schema((

    DateTimeField(
        name='startDate',
        widget=DateTimeField._properties['widget'](
            label="Bulletin Start Date",
            show_hm=False,
            starting_year='2008', #First year to show up in the drop down menu.
            ending_year='2020', #Last year to show up in the drop down menu.
            default_method='getThisYear',
            					
            description="Enter the date this bulletin is active from",
        ),
    ),

    DateTimeField(
        name='completionDate',
        widget=DateTimeField._properties['widget'](
            label="Bulletin Completion Date",
            show_hm=False,
            starting_year='2008', #First year to show up in the drop down menu.
            ending_year='2020', #Last year to show up in the drop down menu.      
            
            description="Enter the date this bulletin is no longer active",
        ),
    ),

    ReferenceField('assocFacultyListing',
        widget=ReferenceWidget(
            label="Faculty Listing",
            description="Select a faculty listing to be associated with this bulletin",
        ),
        relationship="WorksWith",
        vocabulary_display_path_bound=-1,
        allowed_types=('Faculty_Listing',),
        multiValued=0,
        
    ),

))

BulletinSchema = ATFolderSchema.copy() + schema.copy()
BulletinSchema['title'].widget.description = "A generic title for the bulletin(i.e. Graduate Bulletin 2010-2012)"

class Bulletin(ATFolder):
    """
    """

    faculty_listing = ATReferenceFieldProperty('assocFacultyListing')##archetypes fields must be bridged to python properties using ATReferenceFieldProperty not ATFieldProperty

    security = ClassSecurityInfo()

    implements(interfaces.IBulletin, interfaces.IBatchPrintable, ITOCRoot)
    
    archetype_name = 'Bulletin'
    meta_type = 'Bulletin'
    portal_type = "Bulletin"
    _at_rename_after_creation = True

    schema = BulletinSchema

    ##Need a method to get the object and adapt it?

    ##May be causing view-all-pages to drop when try to access it without authentication##security.declareProtected(CMFCorePermissions.View, 'getTOC')
#     def getTOC(self, current=None, root=None):
#         """Get the table-of-contents of this manual. 
        
#         The parameter 'current' gives the object that is the current page or
#         section being viewed. 
        
#         The parameter 'root' gives the root of the manual - if not given, this
#         ReferenceManual object is used, but you can pass in a 
#         ReferenceManualSection instead to root the TOC at this element. The 
#         root element itself is not included in the table-of-contents.
        
#         The return value is a list of dicts, recursively representing the 
#         table-of-contents of this manual. Each element dict contains:
        
#             item        -- a catalog brain for the item (a section or page)
#             numbering   -- The dotted numbering of this item, e.g. 1.3.2
#             depth       -- The depth of the item (0 == top-level item)
#             currentItem -- True if this item corresponds to the object 'current'
#             children    -- A list of dicts
            
#         The list 'children' recursively contains the equivalent dicts for
#         children of each section. If the parameter 'current' is not given, no
#         element will have current == True.
#         """
        
#         if not root:
#             root = self

#         class Strategy(NavtreeStrategyBase):

#             rootPath = '/'.join(root.getPhysicalPath())
#             showAllParents = False

#         strategy = Strategy()
#         query=  {'path'        : '/'.join(root.getPhysicalPath()),
#                  'object_provides' : 'uwosh.bulletin.content.interfaces.IBatchPrintable',
#                  'sort_on'     : 'getObjPositionInParent'}

#         toc = buildFolderTree(self, current, query, strategy)['children']

#         def buildNumbering(nodes, base=""):
#             idx = 1
#             for n in nodes:
#                 numbering = "%s%d." % (base, idx,)
#                 n['numbering'] = numbering
#                 buildNumbering(n['children'], numbering)
#                 idx += 1

#         buildNumbering(toc)
#         return toc


    ##security.declareProtected(CMFCorePermissions.View, 'getTOCSelectOptions')
#     def getTOCSelectOptions(self, current=None):
#         """
#         Calls getTOC then cooks the results into a sequence of dicts:
#             title: tile of section/page, including numbering
#             url:   URL of page
#             current: True if current section/page
#         This is a convenience for creating an option list.
#         """
        
#         def doNodes(nodes):
#             res = []
#             for n in nodes:
#                 item = n['item']
#                 res.append( { 
#                     'title'   : "%s %s" % (n['numbering'], item.Title),
#                     'url'     : item.getURL(),
#                     'current' : n['currentItem'],
#                 } )
#                 if n['children']:
#                     childres = doNodes(n['children'])
#                     if childres:
#                         res = res + childres
#             return res
        
#         return doNodes(self.getTOC(current))


#     ##security.declareProtected(CMFCorePermissions.View, 'getTOCInfo')
#     def getTOCInfo(self, toc):
#         """Get information about a table-of-contents, as returned by getTOC.
        
#         The return value is a dict, containing:

#             tocList    -- A flat list representing the table-of-contents
#             localTOC   -- A toc structure for the contents under the current
#                             item (passed in as 'current' to getTOC())
#             currentIdx -- The index in tocList of 'current'
#             nextIdx    -- The index in tocList of the next item after 'current'
#             prevIdx    -- The index in tocList of the next item before 'current'
#             parentIdx  -- The index in tocList of the parent of 'current'
            
#         The elements 'currentIdx', 'nextIdx', 'prevIdx' and 'parentIdx' may be
#         None if either the table-of-contents was not constructed with a current
#         item, or if there is no previous/next/parent item. Similarly, 'localTOC' 
#         will be None if the table-of-contents was not constructed with a current 
#         item.
        
#         Each item in the list 'tocList' in the returned dict contains a dict 
#         with keys:
        
#             item       -- A catalog brain repsenting the item
#             numbering  -- The dotted numbering of the item, e.g. 1.3.2.
#             depth      -- The depth of the item (0 = top-level item)
#             current    -- True if this item represents the current page/section
         
#         The parameter 'toc' gives the table of contents, as returned by
#         getTOC() above.
#         """

#         # Let's fake static variables - keep track of what may be our parent
#         global parentIdx, prevIdx, prevDepth, prevWasCurrent

#         parentIdx = None
#         prevIdx = None
#         prevDepth = -1
#         prevWasCurrent = False

#         def addToList(tocInfo, tocItem):
#             item      = tocItem['item']
#             numbering = tocItem['numbering']
#             depth     = tocItem['depth']
#             children  = tocItem['children']
#             isCurrent = tocItem['currentItem']

#             global parentIdx, prevIdx, prevDepth, prevWasCurrent

#             numberingList = numbering.split('.')[:-1]
#             idxList = [int(number) - 1 for number in numberingList]

#             tocInfo['tocList'].append({'item'        : item,
#                                        'numbering'   : numbering,
#                                        'depth'       : depth,
#                                        'currentItem' : isCurrent,
#                                        })

#             currentIdx = len(tocInfo['tocList']) - 1

#             if isCurrent:
#                 prevWasCurrent = True
#                 tocInfo['currentIdx'] = currentIdx
#                 if currentIdx > 0:
#                     tocInfo['prevIdx'] = currentIdx - 1
#                 tocInfo['parentIdx'] = parentIdx
#                 tocInfo['localTOC'] = tocItem['children']
#             elif prevWasCurrent:
#                 prevWasCurrent = False
#                 tocInfo['nextIdx'] = currentIdx

#             for child in children:
#                 addToList(tocInfo, child)

#             # parent index will be item with depth = depth - 1
#             # keep track of potential parents by noting when we move down
#             # one step

#             if depth > prevDepth:
#                 parentIdx = prevIdx
#                 prevDepth = depth

#             prevIdx = currentIdx

#         tocInfo = {'currentIdx' : None,
#                    'nextIdx'    : None,
#                    'prevIdx'    : None,
#                    'parentIdx'  : None,
#                    'tocList'    : [],
#                    'localTOC'   : None}

#         for topLevel in toc:
#             addToList(tocInfo, topLevel)

#         return tocInfo


    ##security.declareProtected(CMFCorePermissions.View, 'addImagePaths')
#     def addImagePaths(self, body, baseurl):
#         """Fixup image paths in section body"""
        
#         # This is a convenience method for use in referencemanual_macros
#         # section_collation macro. It looks in body for img tags
#         # with relative URLs in the src attribute and prepends the baseurl.
#         # TODO: when we not longer need 2.1 compatibility, this belongs in 
#         # a view.
                
#         return IMG_PATTERN.sub(r"""\1src="%s/\2"\3""" % baseurl, body)

#     ##security.declareProtected(CMFCorePermissions.View, 'getAllPagesURL')
#     def getAllPagesURL(self):
#         """ return URL for all pages view """
        
#         return "%s/view-all-pages" % self.absolute_url()###need a seperate view for program or just set root as something different?


#     ##security.declareProtected(CMFCorePermissions.View, 'getNextPreviousParentValue')
#     def getNextPreviousParentValue(self):
#         """ always true """
#         return True


#     ##security.declareProtected(CMFCorePermissions.View, 'Rights')
#     def Rights(self):
#         """ get rights from parent if necessary """
#         if self.Schema().has_key('rights'):
#             return self.getRawRights()
#         else:
#             return self.aq_parent.Rights()


#     ##security.declareProtected(CMFCorePermissions.View, 'Creators')
#     def Creators(self):
#         """ get rights from parent if necessary """
#         if self.Schema().has_key('creators'):
#             return self.getRawCreators()
#         else:
#             return self.aq_parent.Creators()


    def getDescription(self):
        """ Returns the description of the Bulletin
        """
        return self.Description()

#     ##def getPortalState(self):
#     ##    return self.review_state

#     ##security.declareProtected(CMFCorePermissions.View, 'bulletinObject')
#     def bulletinObject(self):
#         """ find manual from sub-object """
#         return self

#     def getFacultyListing(self):
# 	portal_catalog = getToolByName(self, 'portal_catalog')
#         brains = portal_catalog.searchResults({'portal_type':'Faculty', 'sort_on':'sortable_title'})
#         return brains


    def sortByKey(self, listing, sort_key):
        sorted_listing = sorted(listing, key=lambda obj: getattr(obj, sort_key))
        return sorted_listing

    def getColumns(self, brains):
	numOfFac = len(brains)
	colOneLen = int(round(float(numOfFac)/2))
	colOne = brains[:colOneLen]
	colTwo = brains[colOneLen:]
	facCols = [colOne, colTwo]
	return facCols

    def getTOCAdapter(self):
        return ITOCAdapter(self)

#     def isPrivate(self, obj):##may not be neccessary.... 
# 	portal_catalog = getToolByName(self, 'portal_catalog')
#         brains = portal_catalog.searchResults({'Title':obj.Title(), 'review_state':'private'})
#         return brains
        

  
registerType(Bulletin, PRODUCT_NAME)
