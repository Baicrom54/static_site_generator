from block import BlockType,block_to_block_type,markdown_to_blocks
import unittest

class TestBlocksFunc(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            """
        md1="""
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items

            """
        md2="""
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
            
            
            """
        blocks = markdown_to_blocks(md)
        blocks1=markdown_to_blocks(md1)
        blocks2=markdown_to_blocks(md2)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        self.assertEqual(
            blocks1,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        self.assertEqual(
            blocks2,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        heading_block="## Heading\n Bho"
        code_block="```code\n other code```"
        quote_block=">Sono\n>Un\n>quote block"
        unordered_list="- Ciao\n - Sono\n - Francesco"
        ordered_list="1. Ciao\n 2. Sono\n 3. Francesco"
        paragraph_block="Ciao sono\n Francesco"
        self.assertEqual(block_to_block_type(heading_block),BlockType.HEADING)
        self.assertEqual(block_to_block_type(code_block),BlockType.CODE)
        self.assertEqual(block_to_block_type(quote_block),BlockType.QUOTE)
        self.assertEqual(block_to_block_type(unordered_list),BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(ordered_list),BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(paragraph_block),BlockType.PARAGRAPH)
