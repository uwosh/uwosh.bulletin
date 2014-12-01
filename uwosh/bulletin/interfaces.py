from zope.interface import Interface

class ITOCRoot(Interface):
    """
    allows a folderish object to be used as a TOC root
    """


class ITOCAdapter(Interface):
    """
    adapter that allows for a folderish object with the IBatchPrintable interface to be aggregated on one page for
    printing or viewing
    """

    def getTOC(self, current=None, root=None):
        """
        takes the current object or an object to be passed as the root of the table of contents
        and iterates over the folder structure returning a table of contents for the item
        """

    def getTOCInfo(self, toc):
        """Get information about a table-of-contents, as returned by getTOC.
        
        The return value is a dict, containing:

            tocList    -- A flat list representing the table-of-contents
            localTOC   -- A toc structure for the contents under the current
                            item (passed in as 'current' to getTOC())
            currentIdx -- The index in tocList of 'current'
            nextIdx    -- The index in tocList of the next item after 'current'
            prevIdx    -- The index in tocList of the next item before 'current'
            parentIdx  -- The index in tocList of the parent of 'current'
            
        The elements 'currentIdx', 'nextIdx', 'prevIdx' and 'parentIdx' may be
        None if either the table-of-contents was not constructed with a current
        item, or if there is no previous/next/parent item. Similarly, 'localTOC' 
        will be None if the table-of-contents was not constructed with a current 
        item.
        
        Each item in the list 'tocList' in the returned dict contains a dict 
        with keys:
        
            item       -- A catalog brain repsenting the item
            numbering  -- The dotted numbering of the item, e.g. 1.3.2.
            depth      -- The depth of the item (0 = top-level item)
            current    -- True if this item represents the current page/section
         
        The parameter 'toc' gives the table of contents, as returned by
        getTOC() above.
        """

    def addImagePaths(self, body, baseurl):
        """Fixup image paths in section body

        # This is a convenience method for use in referencemanual_macros
        # section_collation macro. It looks in body for img tags
        # with relative URLs in the src attribute and prepends the baseurl.
        # TODO: when we not longer need 2.1 compatibility, this belongs in
        # a view.
        """
