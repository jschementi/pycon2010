import unittest

from xamlwriter.node import ErrorNode, Node, OrderedDict, TextNode


class TestNode(unittest.TestCase):
    
    def testConstruction(self):
        node = Node('foo')
        self.assertEqual(node.name, 'foo')
        self.assertEqual(node.attributes, OrderedDict())
        self.assertEqual(node.children, [])
        self.assertEqual(node.parent, None)


    def testEquality(self):
        node = Node('foo')
        self.assertEqual(node, Node('foo'))
        self.assertNotEqual(node, Node('bar'))
        
        node.attributes['foo'] = 'fish'
        node2 = Node('foo')
        self.assertNotEqual(node, node2)
        
        node2.attributes['foo'] = 'fish'
        self.assertEqual(node, node2)
        
        node.children.append(Node('bar'))
        self.assertNotEqual(node, node2)
        
        node2.children.append(Node('bar'))
        self.assertEqual(node, node2)


    def testHash(self):
        self.assertRaises(TypeError, lambda: hash(Node('foo')))


    def testComparison(self):
        node = Node('foo')
        for name in '__gt__ = __lt__ = __ge__ = __le__'.split(' = '):
            method = getattr(node, name)
            self.assertTrue(method(None) is NotImplemented)


    def testToStringSimple(self):
        node = Node('foo')
        self.assertEqual(node.to_string(), '<foo />')


    def testToStringChildren(self):
        node = Node('foo')
        node.children.append(Node('bar'))
        self.assertEqual(node.to_string(), '<foo><bar /></foo>')


    def testToStringAttributes(self):
        node = Node('foo')
        node.attributes['bar'] = 'baz'
        self.assertEqual(node.to_string(), '<foo bar="baz" />')


class TestTextNode(unittest.TestCase):

    def testConstruction(self):
        node = TextNode('some text')
        self.assertEqual(node.data, 'some text')
        
        self.assertFalse(hasattr(node, 'name'))
        self.assertFalse(hasattr(node, 'attributes'))
        self.assertFalse(hasattr(node, 'children'))


    def testEquality(self):
        node = TextNode('some text')
        self.assertEqual(node, TextNode('some text'))
        self.assertNotEqual(node, TextNode('other text'))


    def testHash(self):
        self.assertRaises(TypeError, lambda: hash(TextNode('foo')))


    def testComparison(self):
        node = TextNode('foo')
        for name in '__gt__ = __lt__ = __ge__ = __le__'.split(' = '):
            method = getattr(node, name)
            self.assertTrue(method(None) is NotImplemented)


    def testToString(self):
        node = TextNode('foo')
        self.assertEqual(node.to_string(), 'foo')


class TestErrorNode(unittest.TestCase):
    
    def testErrorNode(self):
        self.assertTrue(issubclass(ErrorNode, Node))



if __name__ == '__main__':
    unittest.main()

