import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.NORMAL, "www.cli.co")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
		
    def test_repr(self):
        node = TextNode("This is a text node", TextType.NORMAL, "www.cli.co")
        self.assertTrue("This is a text node" in repr(node))
        self.assertTrue("normal" in repr(node))
        self.assertTrue("www.cli.co" in repr(node))


if __name__ == "__main__":
    unittest.main()