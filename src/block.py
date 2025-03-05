from enum import Enum
import re


class BlockType(Enum):
    HEADING="heading"
    PARAGRAPH="paragraph"
    CODE="code"
    QUOTE="quote"
    UNORDERED_LIST="unordered_list"
    ORDERED_LIST="ordered_list"


def markdown_to_blocks(markdown):
    raw_lst=[block  for block in markdown.split("\n\n")if (block.strip()!="\n" and block.strip()!="")]
    filtered_lst=[strip_blocks(block) if "\n" in block else block for block in raw_lst]
    return filtered_lst

def strip_blocks(block):
    sections=block.split("\n")
    strip_sections=[sect.strip()  for sect in sections if sect.strip()!=""]
    return "\n".join(strip_sections)


def block_to_block_type(block):
        if re.fullmatch(r"(?:^#{1,6} .*$)",block,flags=re.DOTALL):
            return BlockType.HEADING
        if re.fullmatch(r"(?:^`{3}.*`{3}$)",block,flags=re.DOTALL):
            return BlockType.CODE
        if re.fullmatch(r"(?:^>.*(?:\n|$))",block,flags=re.MULTILINE|re.DOTALL):
            return BlockType.QUOTE
        if re.fullmatch(r"(?:^- .*$)",block,flags=re.MULTILINE|re.DOTALL):
            return BlockType.UNORDERED_LIST
        if check_for_ordered_lists(block):
            return BlockType.ORDERED_LIST
        else :
            return BlockType.PARAGRAPH

    
    
    
    
def check_for_ordered_lists(block):
    match=re.findall(r"(?:^(\d+)\. .*$)",block,flags=re.MULTILINE|re.DOTALL)
    if (match):
        for i in range(0,len(match)):
            if int(match[i])!=i+1:
                return False
            i+=1
        return True
    else:
        return False
