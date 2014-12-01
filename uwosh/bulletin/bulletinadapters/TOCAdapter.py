from zope.interface import implements
from zope.component import adapts
from Products.CMFPlone.browser.navtree import NavtreeStrategyBase, buildFolderTree
import re
from uwosh.bulletin.interfaces import *

IMG_PATTERN = re.compile(r"""(\<img .*?)src="([^/]+?)"(.*?\>)""", re.IGNORECASE | re.DOTALL) 

class TOCAdapter(object):
    implements(ITOCAdapter)
    adapts(ITOCRoot)

    def __init__(self, folder):##2nd argument is the object being adapted...
        self.folder = folder


    def getTOC(self, current=None, root=None):##worked with self.folder...
        if not root:
            root = self.folder
            

        class Strategy(NavtreeStrategyBase):

            rootPath = '/'.join(root.getPhysicalPath())
            showAllParents = False

        strategy = Strategy()
        query=  {'path'        : '/'.join(root.getPhysicalPath()),
                 'object_provides' : 'uwosh.bulletin.content.interfaces.IBatchPrintable',
                 'sort_on'     : 'getObjPositionInParent'}
        toc = buildFolderTree(self.folder, current, query, strategy)['children']##looks like here <---causing the problem... something to do with self.context?

        def buildNumbering(nodes, base=""):
            idx = 1
            for n in nodes:
                numbering = "%s%d." % (base, idx,)
                n['numbering'] = numbering
                buildNumbering(n['children'], numbering)
                idx += 1

        buildNumbering(toc)

        return toc

    def getTOCInfo(self, toc):

        # Let's fake static variables - keep track of what may be our parent
        global parentIdx, prevIdx, prevDepth, prevWasCurrent

        parentIdx = None
        prevIdx = None
        prevDepth = -1
        prevWasCurrent = False

        def addToList(tocInfo, tocItem):
            item      = tocItem['item']
            numbering = tocItem['numbering']
            depth     = tocItem['depth']
            children  = tocItem['children']
            isCurrent = tocItem['currentItem']

            global parentIdx, prevIdx, prevDepth, prevWasCurrent

            numberingList = numbering.split('.')[:-1]
            idxList = [int(number) - 1 for number in numberingList]

            tocInfo['tocList'].append({'item'        : item,
                                       'numbering'   : numbering,
                                       'depth'       : depth,
                                       'currentItem' : isCurrent,
                                       })

            currentIdx = len(tocInfo['tocList']) - 1

            if isCurrent:
                prevWasCurrent = True
                tocInfo['currentIdx'] = currentIdx
                if currentIdx > 0:
                    tocInfo['prevIdx'] = currentIdx - 1
                tocInfo['parentIdx'] = parentIdx
                tocInfo['localTOC'] = tocItem['children']
            elif prevWasCurrent:
                prevWasCurrent = False
                tocInfo['nextIdx'] = currentIdx

            for child in children:
                addToList(tocInfo, child)

            # parent index will be item with depth = depth - 1
            # keep track of potential parents by noting when we move down
            # one step

            if depth > prevDepth:
                parentIdx = prevIdx
                prevDepth = depth

            prevIdx = currentIdx

        tocInfo = {'currentIdx' : None,
                   'nextIdx'    : None,
                   'prevIdx'    : None,
                   'parentIdx'  : None,
                   'tocList'    : [],
                   'localTOC'   : None}

        for topLevel in toc:
            addToList(tocInfo, topLevel)

        return tocInfo


    def addImagePaths(self, body, baseurl):
        return IMG_PATTERN.sub(r"""\1src="%s/\2"\3""" % baseurl, body)

