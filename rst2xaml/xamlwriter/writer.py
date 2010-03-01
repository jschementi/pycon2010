
from docutils.core import publish_string
from docutils.writers import Writer
from xamlwriter.translator import XamlTranslator


class XamlWriter(Writer):
    """Writer to convert a docutils nodetree to a XAML nodetree."""
    
    def __init__(self, flowdocument=True, xclass=True):
        self.flowdocument = flowdocument
        self.xclass = xclass
        Writer.__init__(self)

    supported = ('xaml',)
    output = None

    def translate(self):
        visitor = XamlTranslator(self.document, flowdocument=self.flowdocument, xclass=self.xclass)
        self.document.walkabout(visitor)
        self.output = visitor

settings_overrides = {
    'file_insertion_enabled': False,
}

def publish_xaml(input_data, flowdocument=True, overrides=None, xclass=True):
    config = settings_overrides.copy()
    if overrides is not None:
        config.update(overrides)
    
    writer = XamlWriter(flowdocument=flowdocument, xclass=xclass)
    rv = publish_string(source=input_data, writer=writer,
                        settings_overrides=config)
    return rv.root.to_string()