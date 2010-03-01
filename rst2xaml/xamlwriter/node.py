
# requires either Python 2.6 or the odict module
try:
    from odict import OrderedDict
except ImportError:
    from xamlwriter.modules.odict import OrderedDict

    
not_implemented = lambda *_: NotImplemented


class Node(object):
    def __init__(self, name):
        self.name = name
        self.attributes = OrderedDict()
        self.children = []
        self.parent = None


    def __eq__(self, other):
        return (type(other) == type(self) and
                self.name == other.name and
                dict(self.attributes) == dict(other.attributes) and
                self.children == other.children)


    def __ne__(self, other):
        return not self == other
    
    __gt__ = __lt__ = __ge__ = __le__ = not_implemented
    
    __hash__ = None


    def to_string(self):
        attribute_string = "".join(' %s="%s"' % (key, value) for key, value in 
                                    self.attributes.items())
        name = self.name
        if not self.children:
            return '<%s />' % (name + attribute_string)
        children_string = "".join(node.to_string() for node in self.children)
        return '<%s>%s</%s>' % (name + attribute_string, children_string, self.name)

    # Hmmm...
    __repr__ = to_string


class TextNode(object):
    
    def __init__(self, data):
        self.data = data
    
    def __eq__(self, other):
        return (type(other) == type(self) and
                self.data == other.data)
    
    def __ne__(self, other):
        return not self == other
    
    __gt__ = __lt__ = __ge__ = __le__ = not_implemented
    
    __hash__ = None


    def to_string(self):
        return self.data

    # Hmmm...
    __repr__ = to_string



class ErrorNode(Node):
    pass
