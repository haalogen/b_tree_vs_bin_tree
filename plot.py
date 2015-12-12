import matplotlib.pyplot as plt
import numpy as np

fname = 'plot_data.txt'
mat = np.loadtxt(fname)
print mat

word_num = np.zeros(mat.shape[0])
word_num = mat[:, 0]
print word_num

bin_t = mat[:, 1]
print bin_t

b_t = mat[:, 2:].T
print '\n', b_t



fig_tree = plt.figure()
ax_tree = fig_tree.add_subplot(111)
ax_tree.plot(word_num, bin_t, color='k', ls='--', label='BinaryTree', lw=3)

bt_t = [1, 2, 3, 4, 5, 10, 15, 20, 25]
for i in xrange(b_t.shape[0]):
    lbl = 'BTree(t=' + str(bt_t[i]) + ')'
    ax_tree.plot(word_num, b_t[i], ls='-', label=lbl)

ax_tree.legend(loc=2)

label2 = r"max_num_children = $2t$"
limits = ax_tree.axis()
x = 0.4 * (limits[0] + limits[1])
y = 0.8 * (limits[2] + limits[3])
ax_tree.text(x, y, label2, fontsize=14)

ax_tree.set_title("Analysis of Delete operation: Binary Tree VS B-Tree")
ax_tree.set_xlabel("Number of unique words in text")
ax_tree.set_ylabel("Number of CMP operations on keys (CMP_COUNT)")


# plot histogram from b_tree

plt.show()
# saving plots
#fig_tree.savefig("bin_tree_%r_words" % len(count_arr_tree))
