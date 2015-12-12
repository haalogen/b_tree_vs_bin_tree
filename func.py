"""Basic functionality of the project "Bin_tree_vs_B_tree"."""
import numpy as np

glob_output = [] # global list for returning bin_tree nodes as list
glob_cmp_cnt = 0


# bin_tree Class
class TreeNode(object):
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.data = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        
    
    def has_left_child(self):
        return self.leftChild
    
    def has_right_child(self):
        return self.rightChild
    
    def is_left_child(self):
        return self.parent and self.parent.leftChild == self
    
    def is_right_child(self):
        return self.parent and self.parent.rightChild == self
    
    def is_root(self):
        return not self.parent
    
    def is_leaf(self):
        return not (self.leftChild or self.rightChild)
    
    def has_any_children(self):
        return self.leftChild or self.rightChild
    
    def has_both_children(self):
        return self.leftChild and self.rightChild
    
    
    def replace_node_data(self, key, value, lc, rc):
        self.key = key
        self.data = value
        self.leftChild = lc
        self.rightChild = rc
        
        if self.has_left_child():
            self.leftChild.parent = self
            
        if self.has_right_child():
            self.rightChild.parent = self
    
    
    def print_tree_node(self, offset):
        current = self
        
        if current.has_left_child():
            current.leftChild.print_tree_node(offset + 1)
                
        if current.has_right_child():
            current.rightChild.print_tree_node(offset + 1)
            
        print "." * offset, current.key, current.data
        
    
    
    def find_successor(self):
        succ = None
        if self.has_right_child():
            succ = self.rightChild.find_min()
            
        else:
            if self.parent:
                if self.is_left_child():
                    succ = self.parent
                    
                else:
                    self.parent.rightChild = None
                    succ = self.parent.find_successor()
                    self.parent.rightChild = self
            
        return succ
    
    
    
    def find_min(self):
        current = self
        while current.has_left_child():
            current = current.leftChild
        
        return current
    
    
    def splice_out(self): # Glue
        if self.is_leaf():
            if self.is_left_child():
                self.parent.leftChild = None
                
            else:
                self.parent.rightChild = None
                
        elif self.has_any_children():
            
            if self.has_left_child():
                if self.is_left_child():
                    self.parent.leftChild = self.leftChild
                    
                else:
                    self.parent.rightChild = self.leftChild
                    
                self.leftChild.parent = self.parent
                
            else: 
                if self.is_left_child():
                    self.parent.leftChild = self.rightChild
                    
                else:
                    self.parent.rightChild = self.rightChild
                    
                self.rightChild.parent = self.parent
                
    


class BinarySearchTree(object):
    def __init__(self):
        global glob_cmp_cnt
        glob_cmp_cnt = 0
        self.root = None
        self.size = 0
    
    
    
    def put(self, key, val=1):
        if self.root:
            self._put(key, val, self.root)
        
        else:
            self.root = TreeNode(key, val)
            self.size += 1
    
    
    def _put(self, key, val, currentNode):
        
        if key == currentNode.key:
            currentNode.data += 1
            
        elif key < currentNode.key:
            if currentNode.has_left_child():
                self._put(key, val, currentNode.leftChild)
                
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
                self.size += 1
                
        else:
            if currentNode.has_right_child():
                self._put(key, val, currentNode.rightChild)
                
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)
                self.size += 1
        
    
    
    def print_tree(self, offset=0):
        current = self.root
        
        if current != None:
            if current.has_left_child():
                current.leftChild.print_tree_node(offset + 1)
                
            if current.has_right_child():
                current.rightChild.print_tree_node(offset + 1)
            
            print "." * offset, current.key, current.data
        
    
    def get_all_nodes(self):
        
        if self.root:
            output = self._get_all_nodes(self.root)
        
        return output
    
    
    def _get_all_nodes(self, currentNode):
        global glob_output
        
        if currentNode.has_left_child():
            self._get_all_nodes(currentNode.leftChild)
            
        if currentNode.has_right_child():
            self._get_all_nodes(currentNode.rightChild)
        
        glob_output.append([currentNode.data, currentNode.key])
        return glob_output
    
    
    def _get(self, key, currentNode):
        global glob_cmp_cnt
        
        if not currentNode:
            return None
            
        elif currentNode.key == key:
            glob_cmp_cnt += 1
            return currentNode
            
        elif key < currentNode.key:
            glob_cmp_cnt += 2
            return self._get(key, currentNode.leftChild)
            
        else:
            return self._get(key, currentNode.rightChild)
    
    
    def delete(self, key):
        if self.size > 1:
            
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size -= 1
                
            else:
                raise KeyError('Error, key not in tree')
                
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
            
        else:
            raise KeyError('Error, key not in tree')
            
    
    
    def remove(self, currentNode):
        
        if currentNode.is_leaf(): # Leaf node
            
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
                
            else:
                currentNode.parent.rightChild = None
                
        elif currentNode.has_both_children(): # Interior node
            succ = currentNode.find_successor()
            succ.splice_out()
            
            currentNode.key = succ.key
            currentNode.data = succ.data
            
        else: # this node has one child
            if currentNode.has_left_child():
              if currentNode.is_left_child():
                  currentNode.leftChild.parent = currentNode.parent
                  currentNode.parent.leftChild = currentNode.leftChild
                  
              elif currentNode.is_right_child():
                  currentNode.leftChild.parent = currentNode.parent
                  currentNode.parent.rightChild = currentNode.leftChild
                  
              else:
                currentNode.replace_node_data( 
                                     currentNode.leftChild.key,
                                     currentNode.leftChild.data,
                                     currentNode.leftChild.leftChild,
                                     currentNode.leftChild.rightChild)
            
            else:
              if currentNode.is_left_child():
                currentNode.rightChild.parent = currentNode.parent
                currentNode.parent.leftChild = currentNode.rightChild
                
              elif currentNode.is_right_child():
                currentNode.rightChild.parent = currentNode.parent
                currentNode.parent.rightChild = currentNode.rightChild
                
              else:
                currentNode.replace_node_data(
                                    currentNode.rightChild.key,
                                    currentNode.rightChild.data,
                                    currentNode.rightChild.leftChild,
                                    currentNode.rightChild.rightChild)


## Testing
#t = BinarySearchTree()

#arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
#np.random.shuffle(arr)

#print "Filling the bin_tree:"
#for item in arr:
#    print "Insert", item
#    t.put(item)
#    t.print_tree()
#    print

#np.random.shuffle(arr)

#print "Clearing the bin_tree:"
#for item in arr:
#    print 'Delete', item
#    t.delete(item)
#    t.print_tree()
#    print

