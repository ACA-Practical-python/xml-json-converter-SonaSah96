import json


class Node:
    def __init__(self, name, value=None, parent=None, metadata=None, child_list=None):
        self.name = name
        self.value = value
        self.parent = parent
        if metadata is None:
            self.metadata = {}
        else:
            self.metadata = metadata
        if child_list is None:
            self.child_list = []
        else:
            self.child_list = child_list
        if self.parent:
            self.parent.add_child(node_1=self)

    def add_child(self, node_1):
        if node_1 not in self.child_list:
            self.child_list.append(node_1)


class Tree:
    def __init__(self, root, tree_type):
        self.root = root
        self.tree_type = tree_type

    @staticmethod
    def __build_tree_for_json_rec(data, parent_1):
        for key1, val in data.items():
            if isinstance(val, dict):
                new_one_3 = Node(name=key1, parent=parent_1)
                Tree.__build_tree_for_json_rec(data=val, parent_1=new_one_3)
            elif isinstance(val, list):
                new_one_4 = Node(name=key1, parent=parent_1)
                for item in range(len(val)):
                    Node(f"{key1}_sub", value=val[item], parent=new_one_4, metadata={"id": item})
            else:
                Node(name=key1, value=val, parent=parent_1)
        return Tree(root=parent_1, tree_type="json")

    @staticmethod
    def build_tree_for_json(data):
        root_1 = Node(name=tuple(data.keys())[0])
        return Tree.__build_tree_for_json_rec(data, root_1)

    @staticmethod
    def build_tree_for_xml(data):
        root_1 = None
        data = f"{data}<".strip()
        list_of_data = list(data)
        stack_for_parents = []
        stack = []
        while list_of_data:
            while list_of_data[1] != "<":
                stack.append(list_of_data.pop(1))
            list_of_data.pop(0)
            str_stack = "".join(stack)
            str_stack = str_stack.strip()
            if str_stack[0] != "/":
                if str_stack[-1] == ">":
                    name_1 = str_stack[:-1]
                    if not stack_for_parents:
                        root_1 = Node(name=name_1, value=None, parent=None)
                        stack_for_parents.append(root_1)
                    else:
                        par = Node(name=name_1, value=None, parent=stack_for_parents[-1])
                        stack_for_parents.append(par)
                else:
                    val_idx = str_stack.index(">")
                    val = str_stack[(val_idx + 1):]
                    if "id=" in str_stack:
                        new_stack = str_stack.split()
                        name_1 = new_stack[0]
                        id_part = new_stack[1][3:]
                        par_1 = Node(name=name_1, value=val, parent=stack_for_parents[-1],
                                     metadata={"id": id_part})
                    else:
                        name_1 = str_stack[:val_idx]
                        par_1 = Node(name=name_1, value=val, parent=stack_for_parents[-1])
                    stack_for_parents.append(par_1)
            else:
                name_2 = str_stack[1:-1]
                stack_for_parents = [item for item in stack_for_parents if item.name != name_2]
            stack.clear()
            if len(list_of_data) == 1:
                list_of_data.clear()
        return Tree(root=root_1, tree_type="xml")

    @staticmethod
    def __json_to_xml_rec(node_1, spc):
        xml = ""
        if node_1.child_list:
            xml += " " * spc + f"<{node_1.name}>\n"
            spc += 1
            for item in node_1.child_list:
                xml += Tree.__json_to_xml_rec(item, spc)
            spc -= 1
            xml += " " * spc + f"</{node_1.name}>\n"
        else:
            if node_1.value and node_1.metadata:
                xml += " " * spc + f"<{node_1.name} id={node_1.metadata['id']}>{node_1.value}</{node_1.name}>\n"
            else:
                xml += " " * spc + f"<{node_1.name}>{node_1.value}</{node_1.name}>\n"
        return xml

    def json_to_xml(self):
        node_1 = self.root
        return self.__json_to_xml_rec(node_1, 1)

    @staticmethod
    def __xml_to_json_rec(node_1):
        new_data = {}
        for item in node_1.child_list:
            key = item.name
            if item.value:
                new_data[key] = item.value
            else:
                # if obj doesnt have value = > obj is parent
                if item.child_list[0].metadata:
                    new_list = []
                    for item1 in item.child_list:
                        new_list.append(item1.value)
                    new_data[key] = new_list
                else:
                    val = Tree.__xml_to_json_rec(item)
                    new_data[key] = val
        return new_data

    def xml_to_json(self):
        node = self.root
        root_1 = self.__xml_to_json_rec(node)
        return {node.name: root_1}

    def result(self):
        if self.tree_type == "json":
            return self.json_to_xml()
        else:
            return self.xml_to_json()

    def write(self, path):
        ready_data = self.result()
        with open(path, "w") as fd:
            if isinstance(ready_data, dict):
                json.dump(ready_data, fd)
            else:
                fd.write(ready_data)
