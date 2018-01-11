class TreeNode:
    '''
    Representation of a TreeNode.
    '''
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class ShopifyTree:
    '''
    Standard AVL Tree implementation found on the internet. This ensures that the max depth
    will never be past 4, as per request by Shopify.
    
    Link: http://blog.coder.si/2014/02/how-to-implement-avl-tree-in-python.html
    '''
    def __init__(self):
        self.root = None
        self.height = 1
        self.balance = 0
    
    def insert(self, node):
        '''
        Insert a node into the tree. If the value already exists, then it is invalid.
        In the context of Shopify's backend challenge, this means that we have a cycle.
        '''
        if not self.root:
            self.root = TreeNode(node)
            self.root.left = ShopifyTree()
            self.root.right = ShopifyTree()
        elif node < self.root.val:
            self.root.left.insert(node)
        elif node > self.root.val:
            self.root.right.insert(node)
        else:
            return
        self.balancer()
    
    def balancer(self):
        '''
        Balances the BST depending on which cases are satisfied.
        Processed when height is outside the interval [-1, 1].
        '''
        self.setHeight(False)
        self.setBalance(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance < -1:
                if self.root.right.balance > 0:
                    self.root.right.rotateRight()
                    self.setHeight()
                    self.setBalance()
                self.rotateLeft()
                self.setHeight()
                self.setBalance()
            if self.balance > 1:
                if self.root.left.balance < 0:
                    self.root.left.rotateLeft()
                    self.setHeight()
                    self.setBalance()
                self.rotateRight()
                self.setHeight()
                self.setBalance()

    def rotateLeft(self):
        prev = self.root
        new_root = self.root.right.root
        temp = new_root.left.root
        self.root = new_root
        prev.right.root = temp
        new_root.left.root = prev

    def rotateRight(self):
        prev = self.root
        new_root = self.root.left.root
        temp = new_root.right.root
        self.root = new_root
        prev.left.root = temp
        new_root.right.root = prev

    def setHeight(self, memo=True):
        if not self.root:
            self.height = 1
        if memo:
            if not self.root.left:
                self.root.left.setHeight()
            if not self.root.right:
                self.root.right.setHeight()
        self.height = 1 + max(self.root.left.height, self.root.right.height)

    def setBalance(self, memo=True):
        if not self.root:
            self.balance = 0
        if memo:
            if not self.root.left:
                self.root.left.setBalance()
            if not self.root.right:
                self.root.right.setBalance()
        self.balance = self.root.left.height - self.root.right.height
    
