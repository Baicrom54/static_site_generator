import unittest
from inline_textnode import TextNode, TextType,split_nodes_delimiter,split_nodes_image,split_nodes_link,extract_markdown_images,extract_markdown_links,text_to_textnodes





class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3=TextNode("This is a text node", TextType.TEXT)
        node4=TextNode("This is  text node", TextType.TEXT)
        node5=TextNode("This is a text node", TextType.TEXT,"www.bootdev")
        self.assertEqual(node, node2)
        self.assertNotEqual(node,node3)
        self.assertNotEqual(node,node4)
        self.assertNotEqual(node,node5)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.__repr__(),f"TextNode({node.text},{node.text_type.value},{node.url})")
        self.assertEqual(node.__repr__(),node2.__repr__())
    



class TestMardownFuncs(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"   
            )
        matches1=extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"   
            )
        matches2=extract_markdown_images(
            "This is text with an ![image(https://i.imgur.com/zjjcJKZ.png)"   
            )
        matches3=extract_markdown_images(
            "This is text with an ![image]https://i.imgur.com/zjjcJKZ.png)"   
            )
        matches4=extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png"   
            )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        self.assertListEqual([],matches1)
        self.assertListEqual([],matches2)
        self.assertListEqual([],matches3)
        self.assertListEqual([],matches4)


    
    
    
class TestTexnodeFunc(unittest.TestCase):    
    def test_split_nodes_delimiter_one_text(self):
        nodo = TextNode("This is a text node", TextType.TEXT)
        t_node_lst=[nodo]
        bold_delimiter="**"
        self.assertEqual(split_nodes_delimiter(t_node_lst,bold_delimiter,TextType.BOLD),t_node_lst)

    def test_split_nodes_delimiter_multiple_types(self):
        nodo = TextNode("This is a text node **bold** `code` _italic_ ", TextType.TEXT)
        nodo_fail=TextNode("This is a fail **",TextType.TEXT)
        t_node_lst=[nodo]
        bold_delimiter="**"
        code_delimiter="`"
        italic_delimiter="_"
        tran1=split_nodes_delimiter(t_node_lst,bold_delimiter,TextType.BOLD)
        tran2=split_nodes_delimiter(tran1,code_delimiter,TextType.CODE)
        tran3=split_nodes_delimiter(tran2,italic_delimiter,TextType.ITALIC)
        for node in tran3:
            print(f"{node.__repr__()}\n")
        self.assertEqual(tran3,[TextNode("This is a text node ",TextType.TEXT),TextNode("bold",TextType.BOLD),TextNode("code",TextType.CODE),TextNode("italic",TextType.ITALIC)])


    def test_extract_markdown_images_one_image(self):
        node0 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        node1=TextNode("and another ![second image](https://i.imgur.com/3elNhQu.png)",TextType.TEXT)
        new_nodes=split_nodes_image([node0,node1])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_images_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_markdown_links_one_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)",TextType.TEXT)
        node1=TextNode("and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)
        new_nodes=split_nodes_link([node,node1])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes
        )


    def test_markdown_links_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text="This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes=text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )












if __name__ == "__main__":
    unittest.main()