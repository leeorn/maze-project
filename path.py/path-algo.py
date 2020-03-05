import numpy as np
import cv2
import timeit


def valid_move2(img, row_idx, col_idx):
    # out of left bound
    if row_idx < 0:
        return False
    # out of upper bound
    if col_idx < 0:
        return False
    # out of right bound
    if row_idx >= img.shape[0]:
        return False
    # out of lower bound
    if col_idx >= img.shape[1]:
        return False

    # grayish color - if lower than that, the box is not clear
    black_treshold = np.array([100, 100, 100])
    if np.all(np.less(img[row_idx][col_idx], black_treshold)):
        return False

    # it's a valid move
    return True


class Node:
    def __init__(self, row, col, prev, color):
        self.row_idx = row
        self.col_idx = col
        self.prev = prev
        self.color = color


from collections import deque

def shortest_path2(img, start_row, start_col, end_row, end_col, size=1):
    # inite a queue (FIFO)
    q = deque()
    seen_q = deque()
    # create a node object
    node = Node(start_row, start_col, None, None)
    # append the first node to the queue
    q.append(node)

    c = 0
    # while the queue is not empty, continue looking for the end
    while q:
        n = q.popleft()

        if c % 10000 == 0:
            print(f"c is {c}, q has {len(q)}, seen_q {len(seen_q)}, curr row, col: {n.row_idx, n.col_idx}")
        c +=1

        # checks if reach the end. if so return the node
        if n.row_idx == end_row and n.col_idx == end_col:
            return n

        if (n.row_idx, n.col_idx) in seen_q:
            continue

        # check if can move to left, up, right, down
        # checks left
        if valid_move2(img, n.row_idx, n.col_idx - 1):
            q.append(Node(n.row_idx, n.col_idx - 1, n, None))

        # checks up
        if valid_move2(img, n.row_idx - 1, n.col_idx):
            q.append(Node(n.row_idx - 1, n.col_idx, n, None))

        # checks right
        if valid_move2(img, n.row_idx, n.col_idx + 1):
            q.append(Node(n.row_idx, n.col_idx + 1, n, None))

        # checks down
        if valid_move2(img, n.row_idx + 1, n.col_idx):
            q.append(Node(n.row_idx + 1, n.col_idx, n, None))

        seen_q.append((n.row_idx, n.col_idx))

    # if reached here - no path was found
    print("DIDN'T FIND PATH")
    return


# algo
# load image
pic = cv2.imread('../new-maze.jpg')

print(type(pic))
# def shortest_path2(img, start_row, start_idx, end_row, end_col, size):

print(("start timeing"))
s = timeit.timeit()
# find shortest path
n = shortest_path2(pic, 15, 15, 690, 920, 1)

print(("end timeing"))
e = timeit.timeit()

print(e-s)







