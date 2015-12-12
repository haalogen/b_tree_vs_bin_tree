import func as fu
import b_tree_deletion as btree
import re
import matplotlib.pyplot as plt
import numpy as np
import sys

def main():
    TIMES = 100 # number of experiments to calc avg values
    T = 5 # minimum degree of BTree: max_num_children == 2*T
    if len(sys.argv) >= 2:
        TIMES = int(sys.argv[1])
    if len(sys.argv) >= 3:
        T = int(sys.argv[2])
    
#    -George_Orwell
#    1984_small
#    read the text; parse it into words
    text = None
    fname = 'texts/1984-George_Orwell.txt'
    with open(fname, 'r') as f:
        text = f.read().lower()
    
#    replaces anything that is not a lowercase letter, space or 
#    apostrophe with a space
    text = re.sub('[^a-z]+', " ", text)
    words = text.split()
    
    
#    1) fill the bin_tree
    bin_tree = fu.BinarySearchTree()
    
    
    for word in words:
        bin_tree.put(word)
    
    
    bin_tree_stat = bin_tree.get_all_nodes()
    
    bin_tree_stat.sort(reverse=True)
    
    unique_words = []
    for item in bin_tree_stat:
        unique_words.append(item[1])
    
    
    count_arr_tree = []
    for item in bin_tree_stat:
        count_arr_tree.append(item[0])
    
    np.random.shuffle(unique_words)
    
    
    for item in unique_words:
        bin_tree.delete(item)
    
    bin_tree_cmp_cnt = 0
    fu.glob_cmp_cnt = 0
    for t in xrange(TIMES):
        bin_t = fu.BinarySearchTree()
        
        np.random.shuffle(unique_words)
        for item in unique_words:
            bin_t.put(item)
        
        np.random.shuffle(unique_words)
        for item in unique_words:
            bin_t.delete(item)
        
        bin_tree_cmp_cnt += fu.glob_cmp_cnt
        fu.glob_cmp_cnt = 0
    
    bin_tree_cmp_cnt /= 1.0*TIMES
    print "BinTree avg:", bin_tree_cmp_cnt
    
    
    
    
    # 2) fill the b_tree
    btree.glob_cmp_cnt = 0
    btree_cmp_cnt = 0
    for i in xrange(TIMES):
        bt = btree.BTree(T)
        
        np.random.shuffle(unique_words)
        for word in unique_words:
            bt.insert(word)
    
        np.random.shuffle(unique_words)
        for word in unique_words:
            bt.remove(word)
        
        btree_cmp_cnt += btree.glob_cmp_cnt
        btree.glob_cmp_cnt = 0
    
    btree_cmp_cnt /= 1.0*TIMES
    print "Btree_", T ,"avg:", btree_cmp_cnt
    
    
    
    
    
    
#    plot histogram from bin_tree
    fig_tree = plt.figure()
    ax_tree = fig_tree.add_subplot(111)
    ax_tree.plot(range(len(count_arr_tree)), count_arr_tree, color='r')
    
    label2 = "BinTree. Top 20 most popular words:\n"
    for i in range(20):
        label2 += str(bin_tree_stat[i]) + '\n'
    label2 += '\n'
    
    limits = ax_tree.axis()
    x = 0.6 * (limits[0] + limits[1])
    y = 0.2 * (limits[2] + limits[3])
    ax_tree.text(x, y, label2, fontsize=10)
    
    
    # plot histogram from b_tree
    
    # saving plots
    fig_tree.savefig("bin_tree_%r_words" % len(count_arr_tree))
    
if __name__ == '__main__':
    main()


