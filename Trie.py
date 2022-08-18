# Trie

class node:
    def __init__(self,value=''):
        self.node = value
        self.children = {}
        self.endofword = False
        self.wordmentions = 0

class Trie:
    def __init__(self,list1):
        self.root = node() # The root node is set up as an empty node.
        for i in list1:
            self.insert(i) # Inserts each string into the data structure.

    def insert(trie, string):
        if string != '':
            node1 = trie.root # Starts inserting the string into the root
            for char in string: 
                # Iterates over each character in the string, 
                # following preexisting branches in the trie or creating new nodes.
                if char in node1.children.keys(): # Follows a preexisting branch from the node to the next character in the string.
                    node1 = node1.children[char]
                else:
                    node1.children[char] = node(char) # Creates a node and follows it.
                    node1 = node1.children[char]
            node1.endofword = True
    
    def query(trie, string):
        print()
        node1 = trie.root
        if node1.children == {}: # Trie is empty.
            print('Trie is empty.')
        else:
            for i,char in enumerate(string):
                if char not in node1.children: # Entire string is not in trie.
                    print('No matches, sorry.')
                    break
                else:
                    node1 = node1.children[char]
                    if i == len(string) - 1: # Last character in string.
                        # Two cases.
                        if node1.children == {}: # Zero branches left --> end of word branch.
                            print(f'There is a match: {string}')
                        
                        else: # One or more branches. These indicate that the query was an incomplete word.
                            print('Matches:\n')
                            for i in trie._quasidisplay(node1): # Looks at each string stored in node1's subtrie. 
                                # the appropriate match would be the query, save the last letter, and the string put together.
                                match = string[:-1] + i
                                print(f'{match}')
    
    def delete(trie, string):
        if string != '':
            if string not in trie._quasidisplay(): # string not in trie.
                print('Deletion operation unsuccessful: not in trie.')
            else:
                string_ = string
                while string_: # This, until stopped by special cases, loops through characters in the string 

                    node1 = trie.root

                    for char in string_[:-1]:
                        node1 = node1.children[char]

                    node2 = node1.children[string_[-1]]
                    # Here, node2 is the node at the end of the string, and node1 is its parent.

                    if node2.children != {}: # If node2 has children nodes, then it is at the end of a subset of a larger word.
                        # Deleting node2 will also delete its children
                        # which will delete other unintended words. 
                        # Instead, we can change its status as the end of a word, 
                        # since that is the only proof in the data structure that there was that word.
                        node2.endofword = False
                        break
                    
                    elif (not node2.endofword) or string_ == string: # This will delete node2 if it is not the end of a word or if it is one of the leaf nodes of the trie.
                        breakafterthis = False
                        if len(node1.children.keys()) != 1: # This checks whether node1, node2's parent, has more than one branch. 
                            # If this is true, we should stop deleting after deleting node2 to save the words in the other branches.
                            breakafterthis = True
                        del node1.children[string_[-1]] # Deletes node2
                        if breakafterthis:
                            break
                    
                    elif (node2.endofword and (not string_ == string)): 
                        # This tests whether node2 has reached the end of another word, 
                        # in which case the deletion algorithm should stop deleting nodes.
                        break
                    string_ = string_[:-1]

    def display(trie,node_ = None):
        addBig = False
        
        if node_ == None: # Default node case, should describe the root node.
            node_ = trie.root
            addBig = True
            print()
            print('Words in trie:',sorted(trie._quasidisplay()))
            print()
        
        if len(node_.children.keys()) not in [0,1]: # 2 or more branches - prints out the number of children.
            nodename = node_.node if node_ != trie.root else 'ROOT NODE'
            print(f'{nodename} - branches: {len(node_.children.keys())}')
            print()
        elif node_.children == {}: # End of word
            print(node_.node)
            print()
        else: # The chain continues.
            print(node_.node)
        branch = 1
        for _,i in node_.children.items():
            if len(node_.children.keys()) != 1:
                print('-----------------------------')
                prefix = 'Big ' if addBig else ''
                print(f'{prefix}Branch {branch}\n')
            trie.display(i)
            branch += 1

    def _quasidisplay(trie,node_ = None): # This is a private function. 
        # This goes through every level of the trie and finally returns the strings stored in the trie as a list.
        
        if node_ == None: # Default node case, should describe the root node.
            node_ = trie.root
        
        if node_.children == {}: # The node in question is at the end of the branch (word). 
            # This is the base case for the recursion involved in this function.
            return [node_.node]
        
        else: # One or more branches from the node in question. 
            # What this section does is consider all of the node's children to be roots of their own subtries. 
            # It then evaluates the strings contained in all the subtries combined (using recursion) and simply adds the starting node's own value to the start of each string.
            list1 = []

            if node_.endofword: # This indicates the possibility that even though the node is not at the end of a branch, it still is at the end of a word.
                # The node also represents a separate string that contributes to a word in its own right. 
                # So, it should be appended to the list of strings.
                list1.append(node_.node)
            
            for _,i in node_.children.items():
                list1 = list1 + [node_.node + x for x in trie._quasidisplay(i)] # Appends the strings stored in each subtrie, with the starting node's value added to the front of each.
            return list1

list1 = [i for i in '''jewel
protect
delicate
lamp
end
sidewalk
peck
faded
shape
entertaining
entertained
circle
beef
ear
smile
imperfect
gullible
nail
unruly
hollow
hysterical
axiomatic
pull
thunder
label
stop
store
needless
easy'''.splitlines()]

trie = Trie(list1)
choice = input("Would you like to insert an element into the trie ('i'), query the trie ('q'), delete an element from the trie ('d') or do nothing ('n')? After the operation, I will display the trie. ")
if choice.lower()[0] == 'i':
    trie.insert(input('\nEnter string to be inserted: '))
elif choice.lower()[0] == 'q':
    trie.query(input('\nEnter query: '))
elif choice.lower()[0] == 'd':
    trie.delete(input('\nEnter string to be deleted: '))

trie.display()