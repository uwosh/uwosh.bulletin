from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import StringWidget

class AutocompleteWidget(StringWidget):
    security = ClassSecurityInfo()
    
    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro' : "autocomplete",
        'helper_js': ('actb_widget.js',),
        'helper_css': ('actb_widget.css',),
        'actb_timeout': 2250, #How long (ms) before the autocomplete times out
        'actb_lim': 5, #How many choices to show at a time
        'actb_firsttext': 0, #Should the auto complete be limited to the
                             #beginning of keyword?
        'actb_filter_bogus': 1, # 1: removes items not in the vocabulary
        'actb_expand_onfocus': 1, # expands the dropdown on field focus
        'actb_complete_on_tab': 1, # when set to 0, pressing tab moves the focus to the next widget
        'actb_show_alerts': 0, # when set to 1, warnings are shown when invalid value is typed
        'actb_show_clear_button': 1,
        })

    security.declarePrivate('keyword_from_value')
    def keyword_from_value(self, value, instance, field):
        vocab = field.Vocabulary(instance)
        if self.actb_filter_bogus: # delete bogus keywords
            return vocab.getKey(value.strip(), None)
        else: # keep bogus keywords
            return vocab.getKey(value.strip(), value.strip()) # if no keyword, use value
    
    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None, emptyReturnsMarker=False):
        """ process the string into a list """

        value = form.get(field.getName(), None)

        # no value!
        if not value:
            return (field.type=='lines' or field.multiValued) and [] or '', {}
        
        if field.multiValued:
            # make delimiters uniform
            value = value.replace(',', ';')
            
            # get keywords from values
            values = value.split(';');
            result = []
            for value in values:
                keyword = self.keyword_from_value(value, instance, field)
                if keyword and keyword not in result:
                    result.append(keyword)
                
            if field.type!='lines' and field.type!='reference':
                result= ';'.join(result) # make it a string again
        else:
            keyword = self.keyword_from_value(value, instance, field)
            result = keyword and keyword or ''
                
        return result, {}
        

from Products.Archetypes.Registry import registerWidget

registerWidget(AutocompleteWidget,
               title='Autocomplete',
               description="Text field with vocabulary based autocomplete.",
               used_for=('Products.Archetypes.public.StringField',)
               )
