import argparse
from Node_Tree import Tree
import json

parser = argparse.ArgumentParser(prog="xml-json-converter", description="XMl/JSON converter")
parser.add_argument("path_to_data", type=str,  help="path to file to be converted")
parser.add_argument("path_to_convert", type=str, help="path to file to be saved converted data")
parser.add_argument("-m", "--mode", type=str, default="output",
                    help="if mode is path then path_to_convert is required"
                         ",converted data should be saved in path_to_convert_file,"
                         "if mode is print converted data should be printed in console")
parser_args = parser.parse_args()
if parser_args.path_to_data.endswith(".json"):
    with open(parser_args.path_to_data) as js_file:
        new_data = json.load(js_file)
    tree1 = Tree.build_tree_for_json(new_data)
    if parser_args.mode == "output":
        print(tree1.result())
    elif parser_args.mode == "path":
        tree1.write(parser_args.path_to_convert)
    else:
        print("Wrong mode argument")
elif parser_args.path_to_data.endswith(".xml"):
    with open(parser_args.path_to_data) as xml_file:
        new_data = xml_file.read()
    tree1 = Tree.build_tree_for_xml(new_data)
    if parser_args.mode == "output":
        print(str(tree1.result()))
    elif parser_args.mode == "path":
        tree1.write(parser_args.path_to_convert)
    else:
        print("Wrong mode argument")
