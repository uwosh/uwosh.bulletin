from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from uwosh.bulletin.interfaces import ITOCRoot, ITOCAdapter
from uwosh.bulletin import interfaces
import interfaces
from uwosh.bulletin.config import *
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema
import Products.CMFCore.permissions as CMFCorePermissions
from uwosh.bulletin.widget import LiveReferenceWidget
from Acquisition import aq_base, aq_parent, aq_get


schema = Schema((
    
    StringField(
        name='contactName',
        widget=StringWidget(
            label='Full Name',
        ),
        schemata='Contact Info',
    ),

    StringField(
        name='contactTitle',
        widget=StringWidget(
            label='Title',
        ),
        schemata='Contact Info',
    ),

    StringField(
        name='contactOffice',
        widget=StringWidget(
            label='Office',
        ),
        schemata='Contact Info',
    ),

    StringField(
        name='contactPhone',
        widget=StringWidget(
            label='Telephone',
        ),
        schemata='Contact Info',
        validators=[u'isUSPhoneNumber'],
    ),

    StringField(
        name='contactSite',
        widget=StringWidget(
            label='Web Site',
        ),
        schemata='Contact Info',
    ),

    StringField(
        name='contactEmail',
        widget=StringWidget(
            label='Email',
        ),
        schemata='Contact Info',
        validators=[u'isEmail'],
    ),

    ReferenceField('assocFaculty',
        widget=LiveReferenceWidget(
            label="Faculty",
        ),
        relationship="WorksWith",
        vocabulary_display_path_bound=-1,
        ##allowed_types=('Faculty',),
        vocabulary="getFacultyList",
        multiValued=1,
        
    ),

    TextField(
        name='purpose',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label="Purpose",
        ),
        default_output_type='text/html',
        schemata="Program Info",
    ),

    TextField(
        name='degree',
        allowable_content_types=('text/plain','text/html'),
        widget=TextAreaWidget(
            label="Degree",
        ),
        default_output_type='text/html',
        schemata="Program Info",
    ),

    TextField(
        name='additionalReq',
        allowable_content_types=('text/plain','text/html'),
        widget=RichWidget(
            label="Additional Admissions Requirements/Information",
        ),
        default_output_type='text/html',
        schemata="Program Info",
    ),


    TextField(
        name='degreeReq',
        allowable_content_types=('text/plain','text/html'),
        widget=RichWidget(
            label="Degree Requirements",
        ),
        default_output_type='text/html',
        schemata="Program Info",
    ),

    TextField(
        name='sum_structure',
        allowable_content_types=('text/plain','text/html'),
        widget=TextAreaWidget(
            label="Structure",
        ),
        default_output_type='text/html',
        schemata="Summary",
    ),

    TextField(
        name='sum_apos',
        allowable_content_types=('text/plain','text/html'),
        widget=TextAreaWidget(
            label="Academic Plans of Study",
        ),
        default_output_type='text/html',
        schemata="Summary",
    ),

    TextField(
        name='sum_cr_req',
        allowable_content_types=('text/plain','text/html'),
        widget=TextAreaWidget(
            label="Minimum Unit (Cr.) Requirements",
        ),
        default_output_type='text/html',
        schemata="Summary",
    ),

    TextField(
        name='sum_atc',
        allowable_content_types=('text/plain','text/html'),
        widget=TextAreaWidget(
            label="Admission to Candidacy",
        ),
        default_output_type='text/html',
        schemata="Summary",
    ),

    TextField(
        name='sum_grad_req',
        allowable_content_types=('text/plain','text/html'),
        widget=TextAreaWidget(
            label="Graduation Requirements",
        ),
        default_output_type='text/html',
        schemata="Summary",
    ),

    TextField(
        name='additional_sum_req',
        allowable_content_types=('text/html'),
        widget=TextAreaWidget(
            label="Additional Summary Fields",
	    description='Add any additional summary fields here. Leave a single space between fields and use the following html format for styling consistency:<br/><code> &lt;label class="formQuestion"&gt;F. Summary Field Title&lt;/label&gt;&lt;br/&gt;Summary Field Body Text&lt;br/&gt;&lt;br/&gt;</code>',
        ),
        default_output_type='text/html',
        schemata="Summary",
    ),

))

ProgramSchema =  ATFolderSchema.copy() + schema.copy()
ProgramSchema['title'].widget.label = "Program Title"
ProgramSchema['description'].widget.label = "Program Description"



class Program(ATFolder):##ATBaseContent constructor
    """
    Folderish type to hold Program-related information that should be contained by a Bulletin -> Department type
    """
    
    security = ClassSecurityInfo()

    implements(interfaces.IProgram, interfaces.IBatchPrintable, ITOCRoot)
    
    archetype_name = 'Program'
    meta_type = 'Program'
    portal_type = "Program"
    _at_rename_after_creation = True

    schema = ProgramSchema

    def getDescription(self):
        """ Returns the description of the Program
        """
        return self.Description()

    ##security.declareProtected(CMFCorePermissions.View, 'programObject')
    ##def programObject(self):
    ##    """ find manual from sub-object """
    ##    return self

    def getFacultyList(self):
        """vocabulary method to get vocabulary from the department associated with this program"""
        try:
            pairs = []
            bulletin_obj = aq_parent(aq_parent(self))
            if getattr(bulletin_obj, 'portal_type') == 'Bulletin':
                if bulletin_obj.faculty_listing != []:
                    faculty_listing = bulletin_obj.faculty_listing

                    faculty_vocab = faculty_listing.getAssocFacultyFL()
                    for faculty in faculty_vocab:
                        uid = faculty.UID()
                        label = faculty.title_or_id()
                        pairs.append((uid, label))
                    return DisplayList(pairs)

        except:
            portal_catalog = getToolByName(self, 'portal_catalog')
            all_faculty = portal_catalog.searchResults({'portal_type':'Faculty', 'review_state':'published'})
            faculty_list = [(fac.UID, fac.Title) for fac in all_faculty]##should return a list of tuples
            for faculty in faculty_list:
                pairs.append(faculty)
            ##get all published Faculty from the catalog and return their UIDs and titles
            return DisplayList(pairs)

    def getTOCAdapter(self):
        return ITOCAdapter(self)

    
    
registerType(Program, PRODUCT_NAME)
