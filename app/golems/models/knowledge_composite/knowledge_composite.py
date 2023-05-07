from pydantic import BaseModel
from typing import List
import json

class Composite(BaseModel):
    name: str
    content: str
    parents: List['Composite'] = []
    children: List['Composite'] = []

    def add(self, child: 'Composite'):
        self.children.append(child)
        child.parents.append(self)

    def update(self, content: str):
        self.content = content

    def to_dict_without_content(self) -> dict:
        return {
            "name": self.name,
            "children": [child.to_dict_without_content() for child in self.children]
        }

    def print_name_tree_json(self) -> None:
        tree_dict = self.to_dict_without_content()
        tree_json = json.dumps(tree_dict, indent=2)
        print(tree_json)

    def print_name_tree(self, level: int = 0) -> None:
        indent = "- " * level
        print(f"{indent}{self.name}")

        for child in self.children:
            child.print_name_tree(level + 1)

    def to_dict(self):
        return {
            "name": self.name,
            "content": self.content,
            "children": [child.to_dict() for child in self.children],
        }
    
    def add_child_to_node(self, keys: List[str], content: str):
        if not keys:
            self.update(content)
            return

        target_key = keys.pop(0)
        for node in self.children:
            if node.name == target_key:
                node.add_child_to_node(keys, content)
                return

        new_child = Composite(name=target_key, content=content)
        self.add(new_child)
        new_child.add_child_to_node(keys, content)


if __name__ == '__main__':
        
    # Example usage
    root = Composite(name="root", content="Root content")

    a = Composite(name="a", content="Content A")
    b = Composite(name="b", content="Content B")
    c = Composite(name="c", content="Content C")
    d = Composite(name="d", content="Content D")
    e = Composite(name="e", content="Content E")
    f = Composite(name="f", content="Content F")
    g = Composite(name="g", content="Content G")

    root.add(a)
    a.add(b)
    a.add(c)
    c.add(d)
    d.add(e)
    d.add(f)
    b.add(g)

    # Update the content of the existing node 'b'
    root.add_child_to_node(["a", "b"], "Updated Content B")

    # Add new nodes to the tree using the list of keys
    root.add_child_to_node(["a", "c", "d", "h"], "Content H")
    root.add_child_to_node(["a", "c", "d", "h", "i"], "Content I")
    root.add_child_to_node(["a", "c", "d", "h", "i", "j"], "Content J")
    root.add_child_to_node(["a", "b", "g", "k"], "Content K")

    # Print the resulting tree
    root.print_name_tree_json()
