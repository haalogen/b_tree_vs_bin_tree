import sys
import numpy as np

class BTreeNode(object):
    def __init__(self, _t, _leaf): 
        """Constructor."""
#        print "BTreeNode.__init__(self, _t, _leaf)"
        # Number of keys storing in the node
        self.n = 0
        # Minimum degree (defines the range for number of keys)
        self.t = _t
        
        # c[0] < k[0] < c[1] < k[1] < ... < k[n-1] < c[n] 
        self.keys = [None] * (2 * self.t - 1)
        self.vals = [None] * (2 * self.t - 1)
        
        # An array of children pointers
        self.c = [BTreeNode] * (2 * self.t) 
        
        self.is_leaf = _leaf
    
    
    def traverse(self):
        """A function to traverse all nodes in a sub-tree rooted with 
        this node."""
#        print "BTreeNode.traverse()"
        # There are n keys and n+1 children, traverse through n keys 
        # and first n children
        idx = 0
        for i in xrange(0, self.n, 1):
            # If this is not leaf, then before printing key[i],
            # traverse the sub-tree rooted with child C[i]
            if not self.is_leaf:
                self.c[i].traverse()
            print self.keys[i],
            
            idx += 1
        
        # Print the sub-tree rooted with last child
        if not self.is_leaf:
            self.c[idx].traverse()
        
#        print
    
    
    
    def search(self, k): # returns None if k is not present
        """A function to search a key in sub-tree rooted with this 
        node."""
        print "BTreeNode.search()"
        # Find the first key greater than or equal to k
        i = 0
        while i < n and k > self.keys[i]:
            i += 1
        
        # If the found key is equal to k, return this node
        if self.keys[i] == k:
            return self
        
        # If key is not found here and this is a leaf node
        if self.is_leaf:
            return None
        
        # Go to the appropriate child
        return self.c[i].search(k)
    
    
    
    def find_key(self, k):
        """A function that returns the index of the first key that is 
        greater or equal to k."""
#        print "BTreeNode.find_key()"
        idx = 0
        while idx < self.n and self.keys[idx] < k:
            idx += 1
        
        return idx
    
    
    def insert_non_full(self, k):
        """A utility function to insert a new key in the sub-tree 
        rooted with this node. The assumption is, the node must be 
        non-full when this function is called."""
#        print "BTreeNode.insert_non_full()"
        t = self.t
        # Initialize index as index of rightmost element
        i = self.n-1
        
        # If this is a leaf
        if self.is_leaf:
            # The following loop does two things
            # a) Finds the location of new key to be inserted
            # b) Moves all greater keys to one place ahead
            while i >= 0 and self.keys[i] > k:
                self.keys[i+1] = self.keys[i]
                i -= 1
            
            # Insert the new key at found location
            self.keys[i+1] = k
            self.n += 1
            
        else: # If this node is not leaf
            # Find the child which is going to have the new key
            while i >= 0 and self.keys[i] > k:
                i -= 1
            
            # See if the found child is full
            if self.c[i+1].n == 2*t-1:
                # If the child is full, then split it
                self.split_child(i+1, self.c[i+1])
                
                # After split, the middle key of C[i] goes up and C[i] 
                # is splitted into two. See which of the two is going 
                # to have the new key
                if self.keys[i+1] < k:
                    i += 1
                
            self.c[i+1].insert_non_full(k)
        
    
    
    def split_child(self, i, y):
        """A utility function to split the child y of this node. i is 
        index of y in child array C[]. The Child y must be full when 
        this function is called."""
#        print "BTreeNode.split_child()"
        t = self.t
        # Create a new node which is going to store (t-1) keys of y
        z = BTreeNode(y.t, y.is_leaf)
        z.n = t-1
        
        # Copy the last (t-1) keys of y to z
        for j in xrange(0, t-1):
            z.keys[j] = y.keys[j+t]
        
        # Copy the last t children of y to z
        if not y.is_leaf:
            for j in xrange(0, t):
                z.c[j] = y.c[j+t]
        
        # Reduce the number of keys in y
        y.n = t-1
        
        # Since this node is going to have a new child, 
        # create space of new child
        for j in xrange(self.n, i, -1): # j = [n, n-1 .. i+1]
            self.c[j+1] = self.c[j]
        
        # Link the new child to this node
        self.c[i+1] = z
        
        # A key of y will move to this node. Find location of new key 
        # and move all greater keys one space ahead
        for j in xrange(self.n-1, i-1, -1):
            self.keys[j+1] = self.keys[j]
        
        # Copy the middle key of y to this node
        self.keys[i] = y.keys[t-1]
        
        # Increment count of keys in this node
        self.n += 1
        
    
    
    def remove(self, k):
        """A wrapper function to remove the key k in sub-tree rooted 
        with this node."""
#        print "BTreeNode.remove()"
        idx = self.find_key(k)
        
        # The key to be removed is present in this node
        if idx < self.n and self.keys[idx] == k:
            
            if self.is_leaf:
                self.remove_from_leaf(idx)
            else:
                self.remove_from_non_leaf(idx)
        
        else:
            # If this node is a leaf node, then the key is not present 
            # in tree.
            if self.is_leaf:
                print "The key %r does not exist in the tree. \n" % k
                return
            
            # The key to be removed is present in the sub-tree rooted 
            # with this node.
            # The flag indicates whether the key is present in the 
            # sub-tree rooted with the last child of this node
            flag = False
            if idx == self.n:
                flag = True
            
            # If the child where the key is supposed to exist has less 
            # than t keys, we fill that child
            if self.c[idx].n < self.t:
                self.fill(idx)
            
            # If the last child has been merged, it must have merged 
            # with the previous child and so we recurse on the 
            # (idx-1)th child. Else, we recurse on the (idx)th child 
            # which now has at least t keys
            if flag and idx > self.n:
                self.c[idx-1].remove(k)
            else:
                self.c[idx].remove(k)
        
    
    
    
    def remove_from_leaf(self, idx):
        """A function to remove the key present in the idx-th position 
        in this node which is a leaf."""
#        print "BTreeNode.remove_from_leaf()"
        # Move all the keys after the idx-th pos one place backward
        for i in xrange(idx+1, self.n):
            self.keys[i-1] = self.keys[i]
        
        # Reduce the count of keys
        self.n -= 1
        
    
    
    def remove_from_non_leaf(self, idx):
        """A function to remove the key present in the idx-th position 
        in this node which is a non-leaf node."""
#        print "remove_from_non_leaf()"
        k = self.keys[idx]
        
        # If the child that preceeds k (C[idx]) has at least t keys, 
        # find the predecessor 'pred' of k in the sub-tree rooted at 
        # C[idx]. Replace k by pred. Recursively delete pred in C[idx]
        if self.c[idx].n >= self.t:
            pred = self.get_pred(idx)
            self.keys[idx] = pred
            self.c[idx].remove(pred)
            
        # If the child C[idx] has less than t keys, examine C[idx+1].
        # If C[idx+1] has at least t keys, find the successor 'succ' 
        # of k in sub-tree rooted at C[idx+1]. Replace k by succ. 
        # Recursively delete succ in C[idx+1]
        elif self.c[idx+1].n >= self.t:
            succ = self.get_succ(idx)
            self.keys[idx] = succ
            self.c[idx+1].remove(succ)
        
        # If both C[idx] and C[idx+1] have less than t keys, merge k 
        # and all of C[idx+1] into C[idx]. Now C[idx] contains 
        # (less or equal than) 2t-1 keys. Free C[idx+1] and 
        # recursively delete k from C[idx]
        else:
            self.merge(idx)
            self.c[idx].remove(k)
        

    
    
    def get_pred(self, idx):
        """A function to get the predecessor of the key -- where the 
        key is present in the idx-th position in the node."""
#        print "BTreeNode.get_pred()"
        # Keep moving to the rightmost node until we reach a leaf
        cur = self.c[idx]
        while not cur.is_leaf:
            cur = cur.c[cur.n]
        
        # Returns the last key of the leaf
        return cur.keys[cur.n-1]
    
    
    def get_succ(self, idx):
        """A function to get the successor of the key -- where the 
        key is present in the idx-th position in the node."""
#        print "BTreeNode.get_succ()"
        # Keep moving to the leftmost node starting from C[idx+1] 
        # until we reach a leaf
        cur = self.c[idx+1]
        while not cur.is_leaf:
            cur = cur.c[0]
        
        # Returns the first key of the leaf
        return cur.keys[0]
    
    
    def fill(self, idx):
        """A function to fill up the child node present in the idx-th 
        position in the C[] array if that child has less than t-1 
        keys."""
#        print "BTreeNode.fill()"
        # If the previous child (C[idx-1]) has more than t-1 keys, 
        # borrow a key from that child
        if idx != 0 and self.c[idx-1].n >= self.t:
            self.borrow_from_prev(idx)
        
        # If the next child (C[idx+1]) has more than t-1 keys, 
        # borrow a key from that child
        elif idx != self.n and self.c[idx+1].n >= self.t:
            self.borrow_from_next(idx)
        
        # Merge C[idx] with its sibling. If C[idx] is the last child, 
        # merge it with its' previous sibling. Otherwise, merge it 
        # with its next sibling
        else:
            if idx != self.n:
                self.merge(idx)
            else:
                self.merge(idx-1)
        
    
    
    def borrow_from_prev(self, idx):
        """A function to borrow a key from the C[idx-1]-th node and 
        place it in C[idx]-th node."""
#        print "BTreeNode.borrow_from_prev()"
        child = self.c[idx]
        sibling = self.c[idx-1]
        
        # The last key from C[idx-1] goes up to the parent and 
        # key[idx-1] from parent is inserted as the first key in 
        # C[idx]. Thus, the sibling loses one key and child gains one 
        # key
        
        # Moving all keys in C[idx] one step ahead
        for i in xrange(child.n-1, -1, -1): # i = [n-1 .. 0]
            child.keys[i+1] = child.keys[i]
        
        # If C[idx] is not a leaf, move all its child pointers one 
        # step ahead
        if not child.is_leaf:
            for i in xrange(child.n, -1, -1): # i = [n .. 0]
                child.c[i+1] = child.c[i]
        
        # Setting child's first key equal to keys[idx-1] from the 
        # current node
        child.keys[0] = self.keys[idx-1]
        
        # Moving sibling's last child as C[idx]'s first child
        if not self.is_leaf:
            child.c[0] = sibling.c[sibling.n]
        
        # Moving the key from the sibling to the parent
        # This reduces the number of keys in the sibling
        self.keys[idx-1] = sibling.keys[sibling.n-1]
        
        child.n += 1
        sibling.n -= 1
        
    
    
    def borrow_from_next(self, idx):
        """A function to borrow a key from the C[idx+1]-th node and 
        place it in C[idx]-th node."""
#        print "BTreeNode.borrow_from_next()"
        child = self.c[idx]
        sibling = self.c[idx+1]
        
        # keys[idx] is inserted as the last key in C[idx]
        child.keys[(child.n)] = self.keys[idx]
        
        # Sibling's first child is inserted as the last child 
        # into C[idx]
        if not child.is_leaf:
            child.c[(child.n)+1] = sibling.c[0]
        
        # The first key from sibling is inserted into keys[idx]
        self.keys[idx] = sibling.keys[0]
        
        # Moving all keys in sibling one step behind
        for i in xrange(1, sibling.n):
            sibling.keys[i-1] = sibling.keys[i]
        
        # Moving the child pointers one step behind
        if not sibling.is_leaf:
            for i in xrange(1, sibling.n+1):
                sibling.c[i-1] = sibling.c[i]
            
        # Increasing and decreasing the key count C[idx] and C[idx+1] 
        # respectipvely
        child.n += 1
        sibling.n -= 1
    
    
    def merge(self, idx):
        """A function to merge idx-th child of the node with (idx+1)th 
        child of the node. C[idx+1] is freed after merging."""
#        print "BTreeNode.merge()"
        child = self.c[idx]
        sibling = self.c[idx+1]
        t = self.t
        
        # Pulling a key from the current node and inserting it into 
        # (t-1)th position of C[idx]
        child.keys[t-1] = self.keys[idx]
        
        # Copying the keys from C[idx+1] to C[idx] at the end
        for i in xrange(0, sibling.n):
            child.keys[i+t] = sibling.keys[i]
        
        # Copying the child pointers from C[idx+1] to C[idx]
        if not child.is_leaf:
            for i in xrange(0, sibling.n+1): # i = [0 .. n]
                child.c[i+t] = sibling.c[i]
        
        # Moving all keys after idx in the current node one step before
        # -- to fill the gap created by moving keys[idx] to C[idx]
        for i in xrange(idx+1, self.n):
            self.keys[i-1] = self.keys[i]
        
        # Moving the child pointers after (idx+1) in the current node 
        # one step before
        for i in xrange(idx+2, self.n+1):
            self.c[i-1] = self.c[i]
        
        # Updating the key count of child and the current node
        child.n += sibling.n+1
        self.n -= 1
        
        # Freeing the memory occupied by sibling
        del sibling
    
    
    



class BTree(object):
    def __init__(self, _t):
        """Constructor (Initializes tree as empty)."""
        self.root = None # Pointer to the root node
        self.t = _t # Minimum degree
    
    
    def traverse(self):
        if self.root != None:
            self.root.traverse()
    
    
    def search(self, k):
        """A function to search a key in this tree."""
        if self.root == None:
            return None
        else:
            return self.root.search(k)
    
    
    def insert(self, k):
        """The main function that inserts a new key in this B-Tree."""
        # If tree is empty
        if self.root == None:
            # Allocate memory for root
            self.root = BTreeNode(self.t, True)
            self.root.keys[0] = k # Insert keys
            self.root.n = 1 # Update number of keys in root
            
        else: # If tree is not empty
            
            # If root is full, then tree grows in height
            if self.root.n == 2*self.t - 1:
                # Allocate memory for new root
                s = BTreeNode(self.t, False)
                
                # Make old root as child of new root
                s.c[0] = self.root
                
                # Split the old root and move one key to the new root
                s.split_child(0, self.root)
                
                # New root has two children now. Decide which of the 
                # two children is going to have new key
                i = 0
                if s.keys[0] < k:
                    i += 1
                s.c[i].insert_non_full(k)
                
                # Change root
                self.root = s
                
            else: # If root is not full, call insert_non_full for root
                self.root.insert_non_full(k)
                
    
    
    def remove(self, k):
        """The main function that removes a new key in this B-Tree."""
        if not self.root:
            print "The tree is empty\n"
            return
        
        # Call the remove function for root
        self.root.remove(k)
        
        # If the root node has 0 keys, make its first child as the new 
        # root if it has a child, otherwise set root as None
        if self.root.n == 0:
            tmp = self.root
            
            if self.root.is_leaf:
                self.root = None
            else:
                self.root = self.root.c[0]
            
            # Free the old root
            del tmp
        


def main():
    
    t = BTree(2)
    
    
    for i in xrange(10):
        t.insert(i)
        t.traverse()
        print
    
    arr = range(10)
    np.random.shuffle(arr)
    for i in arr:
        t.remove(i)
        print "Removed %r: " % i
        t.traverse()
        print
    
#    print "Traversal of tree constructed is"
    


if __name__ == '__main__':
    sys.exit(main())

