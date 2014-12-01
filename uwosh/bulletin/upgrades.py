from Products.CMFCore.utils import getToolByName
from Acquisition import aq_parent, aq_base
from Products.CMFCore.interfaces import IFolderish

def upgrade_to_0_7(context):
    """ perform upgrade to 0.7 -- Archetypes have changes so we must copy and delete all old items to upgrade to the new format """

    portal_catalog = getToolByName(context, 'portal_catalog')
    urltool = getToolByName(context, "portal_url")
    portal  = urltool.getPortalObject()
    copied_items = []
    not_copied = []

    def listAllBulletins(context):
        """Return all available Bulletin objects in a list"""

        brains = portal_catalog.searchResults(meta_type='Bulletin')
        if brains:
            bulletins = [brain.getObject() for brain in brains]
            return bulletins
        else:
            return []

    def getObjCreateLocation(object):
        physPath = object.getPhysicalPath()
        new_location = [item.replace('_old_object', '') for item in list(physPath)]
        index = list(physPath).index('bulletins')
        objPath = '/'.join(new_location[index:-1])
        return objPath

    def copyItemsInFolderish(folderish):
        """Will copy the items in the folder passed to this method. Recreates the bulletin, program, and department objects but copy and pastes all others"""
        for object in folderish.listFolderContents():
            new_obj_location = portal.restrictedTraverse(getObjCreateLocation(object))

            if IFolderish.providedBy(object):
                new_object = recreateObject(object, new_obj_location)
                if new_object and new_object is not None:
                    copied_items.append(str(new_object.id))
                    copyItemsInFolderish(object)
                else:
                    not_copied.append(str(object.id))
            else:
                if object.wl_isLocked(): 
                    object.wl_clearLocks()
                copied_object = folderish.manage_copyObjects(object.id)
                new_obj_location.manage_pasteObjects(copied_object)

    def recreateObject(object, create_location=None):
        """pass object to recreate and folderish object that will recreate it"""
        if object.wl_isLocked(): 
            object.wl_clearLocks()
        
        object_container = object.aq_parent

        object_type = object.portal_type
        object_id = object.getId()
        object_id_old = object_id + '_old_object'

        if getattr(object_container, 'manage_renameObject', None) != None:
            object_container.manage_renameObject(object_id, object_id_old)
        if create_location is None:
            create_location = object_container
        if getattr(create_location, 'invokeFactory', None) != None:
            create_location.invokeFactory(type_name=object_type, id=object_id)
            new_object = create_location[object_id]
            for field in object.Schema().fields():
                field_id = field.getName()
                if field.getName() == 'id':
                    continue
                field_accessor = field.getAccessor(object)
                field_value = field_accessor()
                if hasattr(new_object, field_id):
                    field.set(new_object, field_value)

            return new_object

    bulletins_folder = context.restrictedTraverse('bulletins')
    bulletins = listAllBulletins(context)
    for bulletin in bulletins:
        bulletin_copy = recreateObject(bulletin)
        copyItemsInFolderish(bulletin)
        bulletins_folder.manage_delObjects(bulletin.getId())
        
    portal_catalog.manage_catalogRebuild()
