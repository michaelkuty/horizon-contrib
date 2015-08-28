
SWITCHABLE_ATTRS = {
    'class': 'switchable',
    'data-slug': 'localsource'
}


def create_switchable_attributes(prefix, input_type, name):
    """Creates attribute dicts for the switchable form

    :type prefix: str
    :param prefix: prefix (environment, template) of field
    :type input_type: str
    :param input_type: field type (file, raw, url)
    :type name: str
    :param name: translated text label to display to user
    :rtype: dict
    :return: an attribute set to pass to form build

        ..code-block::
        for extension in self.extensions:
            attributes = create_switchable_attributes(
                'local',
                '%s' % extension["id"],
                _('Extends'))
            field = forms.ChoiceField(label=_('Extends'),
                                      choices=self.get_extension_choices(),
                                      widget=forms.Select(
                                          attrs=attributes),
                                      required=False)
            self.fields["extension__%s" % extension['id']] = field
    """
    attributes = {'class': 'switched', 'data-switch-on': prefix + 'source'}
    attributes['data-' + prefix + 'source-' + input_type] = name
    return attributes
