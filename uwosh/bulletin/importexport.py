from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName

def import_all(context):
    
    site = context.getSite()

    if 'bulletins' not in site.objectIds():
        _createObjectByType('Folder', site, id='bulletins', title='Bulletins')
        site['bulletins'].setConstrainTypesMode(1)
        site['bulletins'].setLocallyAllowedTypes(['Bulletin', 'Program', 'Course', 'InfoPage', 'Department', 'Faculty_Listing'])
        site.portal_workflow.doActionFor(site['bulletins'], 'publish')
    
    if 'faculty-profiles' not in site.objectIds():
        _createObjectByType('Large Plone Folder', site, id='faculty-profiles', title='Faculty')
        site['faculty-profiles'].setConstrainTypesMode(1)
        site['faculty-profiles'].setLocallyAllowedTypes(['Faculty', 'Faculty_Listing'])
        site.portal_workflow.doActionFor(site['faculty-profiles'], 'publish')

    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()








