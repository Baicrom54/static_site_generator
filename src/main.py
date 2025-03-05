import shutil
import os
from html_node import md_to_html,ParentNode



def cp_tree_static_to_public():
    public_path="./public"
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
        os.mkdir(public_path)
        path="./static"
        if os.path.exists(path):
            flag=rc_cp_tree(path,public_path)
            print(flag)
        else:
            raise Exception(f"invalid second file path,current path:{path}")
    else:        
        raise Exception(f"invalid first file path,current path:{public_path}")

def rc_cp_tree(source,dest):
    for file in os.listdir(source):
        path=os.path.join(source,file)
        if os.path.isfile(path):
            shutil.copy(path,dest)
        else:
            new_dest=os.path.join(dest,file)
            os.mkdir(new_dest)
            rc_cp_tree(path,new_dest)
    return f"Operation completed successfully"

def generate_page(from_path, template_path, dest_path):
    with open(f"{from_path}","r") as from_file:
        content=from_file.read()
    with open(f"{template_path}","r") as template_file:
        template=template_file.read()
    node,title=md_to_html(content)
    if not title:
        raise Exception("missing title")
    html_content=node.to_html()
    template=template.replace("{{ Content }}",html_content).replace("{{ Title }}",title)
    with open(f"{dest_path}","w") as dest_file:
        dest_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for element in os.listdir(dir_path_content):
        element_path=os.path.join(dir_path_content,element)
        new_dest_dir_path=os.path.join(dest_dir_path,element.replace(".md",".html"))
        if os.path.isfile(element_path):
            generate_page(element_path,template_path,new_dest_dir_path)
        else:
            os.mkdir(new_dest_dir_path)
            generate_pages_recursive(element_path,template_path,new_dest_dir_path)





def main():
   cp_tree_static_to_public()
   generate_pages_recursive("./content","./template.html","./public")


if __name__ == "__main__":
    main()
