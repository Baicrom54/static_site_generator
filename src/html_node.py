from block import markdown_to_blocks,BlockType,block_to_block_type
from inline_textnode import text_to_textnodes,TextType,TextNode
import re


class HTMLNODE():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag=tag
        self.value=value
        self.children=children
        self.props=props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:  # Handles None or an empty dictionary
            return ""
        return ' '.join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return f"tag:{self.tag},value:{self.value},children:{self.children},props:{self.props_to_html()}"


class LeafNode(HTMLNODE):
    def __init__(self,tag,value,props={}):
        super().__init__(tag=tag,value=value,props=props)
    
    def to_html(self):
        if self.value==None:
            raise ValueError("All leaf node must have values")
        if self.tag==None:
            return str(self.value)
        else:
            return f"<{self.tag}>{str(self.value)}</{self.tag}>"

    
class ParentNode(HTMLNODE):
    def __init__(self,tag,children,props=None):
        super().__init__(tag=tag,children=children,props=props)
    
    def to_html(self,string_so_far="",):
        if not  self.tag:
            raise ValueError("missing tag")
        if not self.children:
            raise ValueError("missing childrens")
        for c in self.children:

            if isinstance(c,LeafNode):
                if c.tag==None:
                    raise ValueError("missing tag")
                if not c.value:
                    raise ValueError(f"missing value,examined node:{c}")
                if c.props=={}:
                    string_so_far+=f"<{c.tag}>{str(c.value)}</{c.tag}>" if c.tag!="" else f"{str(c.value)}"
                else:
                    string_so_far+=f'<{c.tag} href="{c.props["href"]}">{str(c.value)}</{c.tag}>'


            else:
                string_to_add=""
                string_so_far+=c.to_html(string_to_add)
        return f"<{self.tag}>{string_so_far}</{self.tag}>"

def convert_TextNode_to_HTMLNode(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            node=LeafNode("",text_node.text,) 
        case TextType.BOLD:
            node=LeafNode("b",text_node.text,)
        case TextType.ITALIC:
            node=LeafNode("i",text_node.text,)
        case TextType.CODE:
            node=LeafNode("code",text_node.text)
        case TextType.LINK:
            node=LeafNode("a",text_node.text,{"href":text_node.url})
        case TextType.IMAGE:
            node=LeafNode("img",text_node.text,{"href":text_node.url})
        case _:
            raise Exception("Invalid Node")
    return node


def md_to_html(md):
    title=None
    parent=ParentNode("div",[])
    untyped_blocks= markdown_to_blocks(md)
    for block in untyped_blocks:
        block_type=block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                html_element,title=create_heading_html(block.strip(),title)
            case BlockType.CODE:
                html_element=create_code_block_html(block.strip())
            case BlockType.PARAGRAPH:
                html_element=create_paragraph_htmL(block.strip())
            case BlockType.QUOTE:
                html_element=create_quote_block_html(block.strip())
            case BlockType.ORDERED_LIST:
                html_element=create_ordered_list_html(block.strip())
            case BlockType.UNORDERED_LIST:
                html_element=create_unordered_list_html(block.strip())
        parent.children.append(html_element)
    return parent,title

def create_heading_html(block,title):
    i=0
    while block[i]=="#":
        i+=1
    if i==1 and title==None:
        title=block.replace("# ","")
    heading=ParentNode(f"h{i}",[])
    corrected_block=re.sub(f"^{'#'*i} ","",block)
    return create_inline_html(corrected_block,heading,BlockType.HEADING),title

def split_blocks(block_list):
    split_block_on_newline=lambda block:block if block_to_block_type(block)==BlockType.CODE else block.split("\n")
    adjusted_block_list=list(map(split_block_on_newline,block_list))
    return adjusted_block_list

def create_inline_html(block,parent_node,block_type):
    if block_type==BlockType.CODE:
        node=convert_TextNode_to_HTMLNode(TextNode(block.lstrip(),TextType.TEXT))
        parent_node.children.append(node)
    
    else:
        for t_node in text_to_textnodes(block.strip()):
                if block_type!=BlockType.CODE:
                    node=convert_TextNode_to_HTMLNode(t_node)
                    lst=[line for line in node.value.split("\n") if line.strip()!=""]
                    node.value=" ".join(lst)
                    parent_node.children.append(node)
    return parent_node


def create_code_block_html(block):
    code_block=ParentNode("code",[])
    pre_block=ParentNode("pre",[code_block])
    code_block=create_inline_html(block.replace("```",""),code_block,BlockType.CODE)
    return pre_block

def create_paragraph_htmL(block):
    paragraph_block=ParentNode("p",[])
    return create_inline_html(block,paragraph_block,BlockType.PARAGRAPH)

def create_quote_block_html(block):
    quote_block=ParentNode("blockquote",[])
    return create_inline_html(re.sub("^ ","",block.replace(">",""),flags=re.MULTILINE),quote_block,BlockType.QUOTE)


def create_unordered_list_html(block):
    unordered_list=ParentNode("ul",[])
    list_elements=[el.replace("- ","") for el in block.split("\n")]
    for el in list_elements:
        el_node=ParentNode("li",[])
        unordered_list.children.append(create_inline_html(el,el_node,BlockType.UNORDERED_LIST))
    return unordered_list

def create_ordered_list_html(block):
    ordered_list=ParentNode("ol",[])
    list_elements=[re.sub(r"^\d+\. ","",el) for el in block.split("\n")]
    for el in list_elements:
        el_node=ParentNode("li",[])
        ordered_list.children.append(create_inline_html(el,el_node,BlockType.ORDERED_LIST))
    return ordered_list






        
    
    
    
    


        



    