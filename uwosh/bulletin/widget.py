from Products.Archetypes.Widget import InAndOutWidget
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerWidget

class LiveReferenceWidget(InAndOutWidget):
    _properties = InAndOutWidget._properties.copy()
    _properties.update({
        'macro' : 'liveReference',
        'helper_js': ('skins/bulletin_scripts/liveReference.js',), ##removed 'widgets/js/inandout.js', and just added contents of that file to liveReference,js
        'actb_timeout': 2250, #How long (ms) before the autocomplete times out
        'actb_lim': 5, #How many choices to show at a time
        'actb_firsttext': 0, #Should the auto complete be limited to the
                             #beginning of keyword?
        'actb_filter_bogus': 1, # 1: removes items not in the vocabulary
        ##'actb_expand_onfocus': 1, # expands the dropdown on field focus
        'actb_complete_on_tab': 1, # when set to 0, pressing tab moves the focus to the next widget
        'actb_show_alerts': 0, # when set to 1, warnings are shown when invalid value is typed
        'actb_show_clear_button': 1,
        })

    security = ClassSecurityInfo()

registerWidget(LiveReferenceWidget,
               title='LiveReference',
               description="InAndOutWidget with search capabilities",
               used_for=('Products.Archetypes.Field.LinesField',
                         'Products.Archetypes.Field.ReferenceField',)
               )


