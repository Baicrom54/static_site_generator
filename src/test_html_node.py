import unittest
from html_node import HTMLNODE,LeafNode,ParentNode,md_to_html

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props={
        "href": "https://www.google.com",
        "target": "_blank",}
        node0=HTMLNODE()
        node1=HTMLNODE(tag="<a>",value="Hey Node",props=props)
        self.assertEqual( 'href="https://www.google.com" target="_blank"',node1.props_to_html())
        self.assertEqual("",node0.props_to_html())
        self.assertEqual(f"tag:<a>,value:Hey Node,children:None,props:{node1.props_to_html()}",node1.__repr__())

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node1 = LeafNode("a", "Hello, world!")
        node2=LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node1.to_html(), "<a>Hello, world!</a>")
        self.assertEqual(node2.to_html(), "<h1>Hello, world!</h1>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_one_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    
    def test_to_html_with_multiple_childrens(self):
        child_node1 = LeafNode("span", "child")
        child_node2=LeafNode("a","link")
        parent_node = ParentNode("div", [child_node1,child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><a>link</a></div>")

    def test_to_html_with_one_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild")
        grandchild_node2=LeafNode("a","link")
        child_node = ParentNode("span", [grandchild_node1,grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><a>link</a></span></div>",
        )
    
    def test_to_html_with_multiple_parents_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild")
        grandchild_node2=LeafNode("a","link")
        child_node1 = ParentNode("span", [grandchild_node1])
        child_node2=ParentNode("p",[grandchild_node2])
        parent_node = ParentNode("div", [child_node1,child_node2])
        print(f"reuslt:{parent_node.to_html()}")
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><p><a>link</a></p></div>",
        )

class TestMdToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """

        node,title = md_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """

        node,title = md_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md="""
            ### This is **bolded** heading
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here
            """
        node,title = md_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is <b>bolded</b> heading text in a p tag here</h3><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_quotes(self):
        md = """
            > This is a quote block
            > It can span multiple lines
            > And contain **bold** or _italic_ text
            """

        node,title = md_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote block It can span multiple lines And contain <b>bold</b> or <i>italic</i> text</blockquote></div>",
        )
    def test_unordered_list(self):
        md = """
                - Item 1
                - Item 2
                - Item 3 with **bold** text
                - Item 4 with _italic_ text
                - Item 5 with `code` text
                """

        node,title= md_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3 with <b>bold</b> text</li><li>Item 4 with <i>italic</i> text</li><li>Item 5 with <code>code</code> text</li></ul></div>"
            )

    def test_ordered_list(self):
            md = """
                1. First item
                2. Second item
                3. Third item with **bold** text
                4. Fourth item with _italic_ text
                5. Fifth item with `code` text
                """

            node,title = md_to_html(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ol><li>First item</li><li>Second item</li><li>Third item with <b>bold</b> text</li><li>Fourth item with <i>italic</i> text</li><li>Fifth item with <code>code</code> text</li></ol></div>"
            )
            

        
