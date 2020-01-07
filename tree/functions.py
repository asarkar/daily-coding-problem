import operator
import sys
from typing import TypeVar, Dict, Callable, Tuple

from tree.binary_tree import BinaryTree

T = TypeVar("T")


# LeetCode 250.
# 8. A unival tree (which stands for "universal value") is a tree where all nodes under it have the same value.
#
# Given the root to a binary tree, count the number of unival subtrees.
#
# For example, the following tree has 5 unival subtrees:
#
#    0
#   / \
#  1   0
#     / \
#    1   0
#   / \
#  1   1

def num_unival(node: BinaryTree[T]) -> int:
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return 1
    num_unival_node: int = num_unival(node.left) + num_unival(node.right)

    if all(v.val == node.val for v in filter(None.__ne__, [node.left, node.right])):
        num_unival_node += 1
    return num_unival_node


# 50. Suppose an arithmetic expression is given as a binary tree. Each leaf is an integer and each internal node is
# one of '+', '−', '∗', or '/'.
#
# Given the root to such a tree, write a function to evaluate it.
#
# For example, given the following tree:
#
#     *
#    / \
#   +    +
#  / \  / \
# 3  2  4  5
# You should return 45, as it is (3 + 2) * (4 + 5).

_ops: Dict[str, Callable[[int, int], int]] = {
    "+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv
}


def eval_bintree(node: BinaryTree[str]) -> int:
    return int(node.val) if node.val.isdigit() else _ops[node.val](eval_bintree(node.left), eval_bintree(node.right))


# LeetCode 124.
# 94. Given a binary tree of integers, find the maximum path sum between two nodes. The path must go through at least
# one node and does not need to go through the root.

# ANSWER: Two possibilities:
# 1. Current node is included in the max path and forms a simple path (no split)
# 2. Current node is not included or splits
#
# The answer is the max of the two.
def max_path_sum(root: BinaryTree[int]) -> int:
    def max_sum(node: BinaryTree[int], max_so_far: int) -> Tuple[int, int]:
        if node is None:
            return 0, max_so_far  # None node can't be included in the path, so return 0 for path_max

        (left_path_max, left_tree_max) = max_sum(node.left, max_so_far)
        (right_path_max, right_tree_max) = max_sum(node.right, max_so_far)

        # Consider all possible simple paths
        path_max: int = max(node.val, node.val + max(left_path_max, right_path_max))
        # Consider path_max, because this node may be a single-node tree
        tree_max: int = max(left_tree_max, right_tree_max, path_max, node.val + left_path_max + right_path_max)

        return path_max, tree_max

    return 0 if root is None else max(max_sum(root, root.val))


# 133. Given a node in a binary search tree, return the next bigger element, also known as the inorder successor.
# You can assume each node has a parent pointer.
# ANSWER:
# if node has a right tree, smallest node there
# else if it is a left child, parent node
# else first larger parent node
def inorder_successor(node: BinaryTree[T]) -> T:
    def _smallest(root: BinaryTree[T]) -> BinaryTree[T]:
        y: BinaryTree[T] = root

        while y.left:
            y = y.left

        return y

    if node.right:
        return _smallest(node.right).val
    elif node is node.parent.left:
        return node.parent.val

    x: BinaryTree[T] = node
    while x is x.parent.right:
        x = x.parent

    return x.parent.val


# 135. Given a binary tree, find a minimum path sum from root to a leaf.
#
# For example, the minimum path in this tree is [10, 5, 1, -1], which has sum 15.
# +---+10+---+
# |          |
# 5+---+     5+----+
#      |           |
#      2     +----+1
#            |
#            |
#            -1
def min_path_sum(root: BinaryTree[int]) -> int:
    def min_sum(node: BinaryTree[int], best: int, sum_so_far: int) -> int:
        if node is None:
            return best

        if node.left is None and node.right is None:
            return min(sum_so_far + node.val, best)

        min_left: int = min_sum(node.left, best, sum_so_far + node.val)
        min_right: int = min_sum(node.right, min(min_left, best), sum_so_far + node.val)

        return min(min_left, min_right)

    if root is None:
        return 0
    return min_sum(root, sys.maxsize, 0)


# LeetCode 814.
# 146. Given a binary tree where all nodes are either 0 or 1, prune the tree so that subtrees containing all 0s are
# removed.
#
# For example, given the following tree:
#
#    0
#   / \
#  1   0
#     / \
#    1   0
#   / \
#  0   0
# should be pruned to:
#
#    0
#   / \
#  1   0
#     /
#    1
# We do not remove the tree at the root or its left child because it still has a 1 as a descendant.
def prune_zeros(root: BinaryTree[int]) -> BinaryTree[int]:
    if not root:
        return None
    left: BinaryTree[int] = prune_zeros(root.left)
    right: BinaryTree[int] = prune_zeros(root.right)

    if left is None and right is None and root.val == 0:
        return None
    if left is None:
        root.left = None
    if right is None:
        root.right = None

    return root
