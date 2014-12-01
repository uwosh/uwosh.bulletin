from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from uwosh.bulletin.config import *
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFCore.utils import getToolByName

copied_fields = {}
copied_fields['title'] = BaseSchema['title'].copy()
copied_fields['title'].widget.label = "Course Name"

schema = Schema((
    
    StringField(
        name='courseID',
        widget=StringField._properties['widget'](
        label="Course ID",
        ),
        required=1,
        searchable=1,
    ),

    copied_fields['title'],

    StringField(
        name='credits',
        widget=StringField._properties['widget'](
        label="Credits",
        ),
        required=1,
        searchable=1,
    ),

    TextField(
        name='courseDescription',
        allowable_content_types=('text/plain','text/html'),
        widget=RichWidget(
            label="Course Description",
        ),
        default_output_type='text/html',
    ),

    TextField(
        name='coursePrereqs',
        allowable_content_types=('text/plain','text/html'),
        widget=TextAreaWidget(
            label="Course Prerequisites",
        ),
        default_output_type='text/html',
    ),

))

CourseSchema = BaseSchema.copy() + schema.copy()

class Course(BaseContent, BrowserDefaultMixin):
    
    implements(interfaces.ICourse, interfaces.IBatchPrintable)
    
    security = ClassSecurityInfo()
    schema = CourseSchema
    portal_type = "Course"
    archetype_name = "Course"
    meta_type = "Course"

    def getPreviousSibling(self):
        """The node immediately preceding this node.  If
        there is no such node, this returns None."""
        if hasattr(self, 'aq_parent'):
            parent = self.aq_parent
            ids=list(parent.objectIds())
            id=self.id
            if type(id) is not type(''): id=id()
            try: index=ids.index(id)
            except: return None
            if index < 1: return None
            return parent.objectValues()[index-1]
        return None

    def displayCDHeader(self):
        ps = self.getPreviousSibling()
        if ps is None:
            return True
        if hasattr(ps, 'portal_type'):
            if ps.portal_type != 'Course':
                return True
        return False



registerType(Course, PRODUCT_NAME)
