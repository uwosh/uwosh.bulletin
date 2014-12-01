from zope.interface import Interface

class IBulletin(Interface):
    """
    marker interface
    """

class IDepartment(Interface):
    """
    marker interface
    """

class IProgram(Interface):
    """
    marker interface
    """

class IInfoPage(Interface):
    """
    marker interface
    """

class ICourse(Interface):
    """
    marker interface
    """

class IFaculty(Interface):
    """
    marker interface
    """

class IFacultyListing(Interface):
    """
    marker interface
    """

class IBatchPrintable(Interface):
    """
    must have interface to be able to pull content into one page for printing
    """


