from Products.CMFCore.utils import getToolByName

def getFacultyListing(self):
    portal_catalog = getToolByName(self, 'portal_catalog')
    brains = portal_catalog.searchResults({'portal_type':'Faculty'})
    return brains
