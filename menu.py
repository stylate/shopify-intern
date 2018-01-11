from shopify_tree import *

class Menu:
    '''
    Data structure representation of Menu, intended for Shopify.
    '''
    def __init__(self, root_id, children=[]):
        self.root_id = root_id
        self.children = []
        self.valid = True
        self.btree = ShopifyTree()
        self.btree.insert(root_id)
        self.appendChildren(children)

    def appendChildren(self, child_ids):
        for node in list(child_ids):
            self.children.append(node)
            if self.cyclic():
                self.valid = False
                break
            self.btree.insert(node)

    def cyclic(self):
        return self.root_id in self.children

    def __dict__(self):
        output = {}
        output['root_id'] = self.root_id
        output['children'] = self.children
        return output

    def __repr__(self):
        return str(self.__dict__())

    def __str__(self):
        return self.__repr__()

    
