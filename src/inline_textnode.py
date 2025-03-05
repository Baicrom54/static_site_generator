from enum import Enum
import re


class TextType(Enum):
    TEXT="normal"
    BOLD="bold"
    ITALIC="italic"
    CODE="code"
    LINK="link"
    IMAGE="image"


class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text=text
        self.text_type=text_type
        self.url=url

    def __eq__(self,other):
        if self.text==other.text and self.text_type==other.text_type and self.url==other.url:
            return True 
        else:
            False

    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value},{self.url})"



#Splits text nodes according to their text type returning divided nodes
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list=[]
    for node in old_nodes:
        if node.text_type!= TextType.TEXT:
            new_list.append(node)
        else:
            lst=node.text.split(delimiter)
            if len(lst)%2==0:
                raise Exception(f"untermined block,lst:{lst},old_nodes:{old_nodes}")
            new_list+=[TextNode(el, text_type) if i % 2 == 1 else TextNode(el, TextType.TEXT) for i, el in enumerate(lst)]
    filtered_new_list=[node for node in new_list if node.text.strip()!="" and node.text!="\n"]
    return filtered_new_list


def extract_markdown_images(text):
    md_images=re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return md_images

def extract_markdown_links(text):
    md_links=re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return md_links


def split_nodes_all_delimiters(old_nodes):
    return split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(old_nodes,"**",TextType.BOLD),"_",TextType.ITALIC),"`",TextType.CODE)


def text_to_textnodes(text):
    t=[TextNode(text,TextType.TEXT)]
    textnodes=split_nodes_all_delimiters(split_nodes_image(split_nodes_link(t)))
    return textnodes


def split_nodes_image(old_nodes):
    new_list=[]
    for node in old_nodes:
        if node.text_type!=TextType.TEXT:
            new_list.append(node)
        if node.text_type==TextType.TEXT:
            images=extract_markdown_images(node.text)
            for i in range(0,len(images)):
                image_alt,image_link=images[i][0],images[i][1]
                sections=node.text.split(f"![{image_alt}]({image_link})", 1)
                new_list+=[TextNode(sections[0],TextType.TEXT),TextNode(image_alt,TextType.IMAGE,image_link)]
                node.text=sections[1]
            if node.text!="":
                new_list+=[node]
    return new_list



def split_nodes_link(old_nodes):
    new_list=[]
    for node in old_nodes:
        if node.text_type!=TextType.TEXT:
            new_list.append(node)
        if node.text_type==TextType.TEXT:
            links=extract_markdown_links(node.text)
            for i in range(0,len(links)):
                link_alt,link_link=links[i][0],links[i][1]
                sections=node.text.split(f"[{link_alt}]({link_link})", 1)
                new_list+=[TextNode(sections[0],TextType.TEXT),TextNode(link_alt,TextType.LINK,link_link)]
                node.text=sections[1]
            if node.text!="":
                new_list+=[node]
    return new_list


        

