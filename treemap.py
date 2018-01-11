from menu import Menu as m
import urllib.request, json
import numpy as np

class TreeMap:
    '''
    Implicit data structure representation of Shopify's API.
    '''
    def __init__(self):
        data = self.initialParser()
        self.trees = {}
        self.visited = {}
        self.menus = []
        self.total = int(data['pagination']['total'])
        self.pages = int(self.total / data['pagination']['per_page'])

    def initialParser(self):
        '''
        Parses page 0 of the Shopify API in order to collect pagination data.
        '''
        with urllib.request.urlopen("https://backend-challenge-summer-2018" +
                ".herokuapp.com/challenges.json?id=1&page=0") as url:
            data = json.loads(url.read().decode())
        return data  

    def appendMenus(self):
        '''
        Appends all menus based on how many pages the API provides, then flattens
        them into one array.
        '''
        for n in range(1, self.pages + 1):
            with urllib.request.urlopen("https://backend-challenge-summer-2018" +
                    ".herokuapp.com/challenges.json?id=1&page=" + str(n)) as url:
                data = json.loads(url.read().decode())
                self.menus.append(data['menus'])
        self.menus = np.array(self.menus)
        self.menus = self.menus.flatten()
        self.visited = self.memoize()

    def memoize(self):
        '''
        Initializes the memoization for parsing.
        '''
        memo = {}
        for n in range(1, self.menus.size + 1):
            memo[n] = False
        return memo

    def parse(self, i):
        '''
        Parses the menu: an array of dictionaries consisting of the keys
        id, data, parent_id, child_ids.

        Note: MENUS is not zero-indexed.
        We want to iterate through the array nonlinearly, by child_ids.
        The parsing will be memoized as a result. Now, if child_ids is
        an empty list or yields a cycle, then we go to the next ID in sequence.
        '''
        k = i + 1
        if not self.visited[k]:
            self.visited[k] = True
            menu_id = self.menus[i]['id']
            data = self.menus[i]['data']
            child_ids = self.menus[i]['child_ids']
            if 'parent_id' in self.menus[i]:
                current_parent = self.menus[i]['parent_id']
                previous_parent = None
                while True:
                    previous_parent = current_parent
                    if 'parent_id' not in self.menus[previous_parent - 1]:
                        current_parent = self.menus[previous_parent - 1]['id']
                        break
                    current_parent = self.menus[previous_parent - 1]['parent_id']
                self.trees[current_parent].appendChildren(child_ids)
            else:
                parent_id = menu_id
                for c in child_ids:
                    if c in self.trees:
                        parent_id = c
                        child_ids.remove(c)
                self.trees[parent_id] = m(menu_id, child_ids)
            for child in child_ids:
                self.parse(child - 1)


        


