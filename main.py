from treemap import TreeMap as t
import os, codecs, json
import numpy as np

def jsonify(output):
    current_dir = os.getcwd()
    path = current_dir + "/output.json"
    outputFile = open(path, 'w')
    outputFile.write(json.dumps(output, indent=4))
    outputFile.close()

def process(mapping):
    '''
    Process the amount of menus created from parsing.
    We create a dictionary, such that we have two keys VALID_MENUS
    and INVALID_MENUS. Their values yield respective arrays of menus.
    '''
    # initialization
    output = {}
    output['valid_menus'] = []
    output['invalid_menus'] = []
    for key in mapping.trees:
        mapping.trees[key].children.sort()
        if mapping.trees[key].valid:
            output['valid_menus'].append(mapping.trees[key].__dict__())
        else:
            output['invalid_menus'].append(mapping.trees[key].__dict__())
    jsonify(output)
    return output

if __name__ == "__main__":
    mapping = t()
    mapping.appendMenus()
    for i in range(mapping.total):
        mapping.parse(i)
    output = process(mapping)

    

