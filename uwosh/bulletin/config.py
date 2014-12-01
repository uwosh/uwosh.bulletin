from Products.CMFCore.permissions import setDefaultRoles

PRODUCT_NAME = "uwosh.bulletin"

ADD_CONTENT_PERMISSIONS = { 
    'Bulletin': 'UWOBulletin: Add Bulletin',
    'Department': 'UWOBulletin: Add Department',
    'Course': 'UWOBulletin: Add Course',   
    'Faculty': 'UWOBulletin: Add Faculty',
    'Faculty_Listing': 'UWOBulletin: Add Faculty_Listing',
    'Program': 'UWOBulletin: Add Program',   
    'InfoPage': 'UWOBulletin: Add InfoPage',    
}

setDefaultRoles('UWOBulletin: Add Bulletin', ('Manager', 'UWOBulletin.Director'))
setDefaultRoles('UWOBulletin: Add Department', ('Manager', 'UWOBulletin.Director', 'UWOBulletin.Staff'))
setDefaultRoles('UWOBulletin: Add Course', ('Manager', 'UWOBulletin.Director', 'UWOBulletin.Staff'))
setDefaultRoles('UWOBulletin: Add Faculty',  ('Manager', 'UWOBulletin.Director', 'UWOBulletin.Staff'))
setDefaultRoles('UWOBulletin: Add Faculty_Listing',  ('Manager', 'UWOBulletin.Director', 'UWOBulletin.Staff'))
setDefaultRoles('UWOBulletin: Add Program', ('Manager', 'UWOBulletin.Director', 'UWOBulletin.Staff'))
setDefaultRoles('UWOBulletin: Add InfoPage', ('Manager', 'UWOBulletin.Director', 'UWOBulletin.Staff'))
