import collections
import operator
from typing import Sequence, MutableSequence, Tuple, Iterable, Mapping, Callable, List, Deque


# LeetCode 56.
# 77. Given a list of possibly overlapping intervals, return a new list of intervals where all overlapping intervals
# have been merged.
# The input list is not necessarily ordered in any way.
# For example, given [(1, 3), (5, 8), (4, 10), (20, 25)], you should return [(1, 3), (4, 10), (20, 25)].
#
# ANSWER: Sort intervals by end time and merge when current interval starts after the previous one and ends before the
# previous one, or current interval starts before the previous one.
#
# Time and space complexities: O(n), since we may put every interval at least once on the stack.
def merge_overlapping_intervals(intervals: Iterable[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
    sorted_intervals: List[Tuple[int, int]] = sorted(intervals, key=lambda x: x[1])
    stack: List[Tuple[int, int]] = []

    def should_merge() -> bool:
        return len(stack) >= 2 and ((stack[-2][0] <= stack[-1][0] <= stack[-2][1]) or (stack[-1][0] <= stack[-2][0]))

    def merge() -> None:
        a: Tuple[int, int] = stack.pop()
        b: Tuple[int, int] = stack.pop()
        stack.append((min(a[0], b[0]), a[1]))

    for x in sorted_intervals:
        while should_merge():
            merge()

        stack.append(x)

    while should_merge():
        merge()

    return stack


# 128. The Tower of Hanoi is a puzzle game with three rods and n disks, each a different size.
#
# All the disks start off on the first rod in a stack. They are ordered by size, with the largest disk on the bottom
# and the smallest one at the top.
#
# The goal of this puzzle is to move all the disks from the first rod to the last rod while following these rules:
#
# You can only move one disk at a time.
# A move consists of taking the uppermost disk from one of the stacks and placing it on top of another stack.
# You cannot place a larger disk on top of a smaller disk.
# Write a function that prints out all the steps necessary to complete the Tower of Hanoi. You should assume that
# the rods are numbered, with the first rod being 1, the second (auxiliary) rod being 2, and the last (goal) rod
# being 3.
#
# For example, with n = 3, we can do this in 7 moves:
#
# Move 1 to 3
# Move 1 to 2
# Move 3 to 2
# Move 1 to 3
# Move 2 to 1
# Move 2 to 3
# Move 1 to 3

# Find the largest rectangular area possible in a given histogram where the largest rectangle can be made of a number
# of contiguous bars. For simplicity, assume that all bars have same width and the width is 1 unit.
# For example, consider the following histogram with 7 bars of heights {6, 2, 5, 4, 5, 1, 6}. The largest possible
# rectangle possible is 12 (consisting of the bars 5, 4, 5).
def largest_area_in_hist(hist: Sequence[int]) -> int:
    if not hist:
        return 0

    # Each item j on the stack represents the end of the area at j. Where does that area start? After stack[j - 1],
    # (index stack[j - 1] + 1) because the previous area ends at stack[j - 1], or if the stack is empty, at index 0.
    # The following invariant hold for the stack:
    # For i, j in [0, len(stack)), i > j, hist[stack[i]] >= hist[stack[j]]
    stack: MutableSequence[int] = []
    largest_area: int = -1

    def current_area(i: int) -> int:
        area: int = -1
        while stack and hist[stack[-1]] > (hist[i] if i < len(hist) else -1):
            j: int = stack.pop()
            width: int = i - ((stack[-1] + 1) if stack else 0)
            area = max(area, width * hist[j])
        return area

    for i, v in enumerate(hist):
        if stack and hist[stack[-1]] > v:
            largest_area = max(largest_area, current_area(i))
        stack.append(i)

    return max(largest_area, current_area(len(hist)))


# LeetCode 678.
# You're given a string consisting solely of (, ), and *. * can represent either a (, ), or an empty string.
# Determine whether the parentheses are balanced.
#
# For example, (()* and (*) are balanced. )*( is not balanced.
#
# ANSWER: Time and space complexities: O(n), since each character is pushed and popped at most once.
def is_valid_parenthesis_str(s: str) -> bool:
    left_parens: MutableSequence[int] = []
    asterisks: MutableSequence[int] = []

    for i, ch in enumerate(s):
        if ch == "(":
            left_parens.append(i)
        elif ch == ")":
            if left_parens:
                left_parens.pop()
            # treat * as left paren
            elif asterisks:
                asterisks.pop()
            else:  # found unmatched right paren
                return False
        else:
            asterisks.append(i)

    while left_parens and asterisks:
        # treat * as right paren
        if left_parens[-1] < asterisks[-1]:
            left_parens.pop()
            asterisks.pop()
        else:  # found unmatched left paren
            break

    return not left_parens


# 154. Implement a stack API using only a heap. A stack implements the following methods:
#
# push(item), which adds an element to the stack
# pop(), which removes and returns the most recently added element (or throws an error if there is nothing on the stack)
# Recall that a heap has the following operations:
#
# push(item), which adds a new key to the heap
# pop(), which removes and returns the max value of the heap
#
# ANSWER: Maintain a monotonically increasing counter, and push (counter, value) to the heap. Increment counter.

# LeetCode 150.
# 163. Given an arithmetic expression in Reverse Polish Notation, write a program to evaluate it.
#
# The expression is given as a list of numbers and operands. For example: [5, 3, '+'] should return 5 + 3 = 8.
#
# For example, [15, 7, 1, 1, '+', '-', '/', 3, '*', 2, 1, 1, '+', '+', '-'] should return 5, since it is equivalent
# to ((15 / (7 - (1 + 1))) * 3) - (2 + (1 + 1)) = 5.
#
# You can assume the given expression is always valid.
def eval_rpn(tokens: List[str]) -> int:
    operand_stack: MutableSequence[int] = []
    ops: Mapping[str, Callable[[int, int], int]] = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv  # floordiv gives 6 // -132 = -1, but we want 0
    }

    for x in tokens:
        if x not in ops:
            operand_stack.append(int(x))
        elif len(operand_stack) > 1:
            op1: int = operand_stack.pop()
            op2: int = operand_stack.pop()
            result: int = ops[x](op2, op1) if x != "/" else int(ops[x](op2, op1))
            operand_stack.append(result)

    return operand_stack.pop()


# 180. Given a stack of N elements, interleave the first half of the stack with the second half reversed using only one
# other queue. This should be done in-place.
#
# Recall that you can only push or pop from a stack, and enqueue or dequeue from a queue.
#
# For example, if the stack is [1, 2, 3, 4, 5], it should become [1, 5, 2, 4, 3]. If the stack is [1, 2, 3, 4],
# it should become [1, 4, 2, 3].
#
# Hint: Try working backwards from the end state.
#
# ANSWER: At each iteration, we transfer all elements between the first and the last from the stack to the queue.
# We then push the first and the last elements back to the stack, and transfer all the elements from the queue back
# to the stack. Since this reverses the input order of the elements, we need to also reverse the order in which the
# first and the last elements are inserted in the stack at each iteration.
# At each iteration, two elements are put in their goal position; we repeat the above process with the remaining
# elements.
# At the end, the stack contains the elements in the reverse order of what we want. We transfer them to the queue,
# which gives us the desired answer.
#
# Time complexity: We reduce the problem size by 2 at each iteration, and there are n // 2 iteration.
# The number of stack and queue operations at each iteration is given by (n - i), where 0 <= i < n // 2.
# = n * n // 2 - (1 + 2 + ... + n // 2 - 1)
# = n * n // 2 - (n // 2 - 1) * (n // 2) / 2
# = O(n^2)
def interleave(stack: Deque[int]) -> Sequence[int]:
    queue: Deque[int] = collections.deque()
    n = len(stack)

    for i in range(n // 2):
        first = None
        last = None
        for j in range(i, n - i):
            x = stack.popleft()
            if j == i:
                first = x
            elif j == n - i - 1:
                last = x
            else:
                queue.append(x)

        if i % 2 == 0:
            stack.appendleft(first)
            stack.appendleft(last)
        else:
            stack.appendleft(last)
            stack.appendleft(first)

        while queue:
            stack.appendleft(queue.popleft())

    while stack:
        queue.append(stack.pop())

    return queue
