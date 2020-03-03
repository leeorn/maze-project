import numpy as np

# create maze 
maze = np.array([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,1]])

maze

class Node3:
    def __init__(self, row, col, prev):
        self.row_idx = row
        self.col_idx = col
        self.prev = prev


def valid_move3(matrix,row_idx, col_idx):
    # less than the row # or col #
    if row_idx < 0 or col_idx < 0:
        return False

    # larger than the # of rows OR # of cols (out of bound)
    if row_idx >= matrix.shape[0] or col_idx >= matrix.shape[1]:
        return False
    
    # if the index is a wall
    if matrix[row_idx][col_idx] != 0:
        return False
    
    # it's a valid move
    return True


from collections import deque
from IPython.core.debugger import set_trace

def shortest_path3(matrix, start_row=1, start_idx=1):
    # inite a queue (FIFO)
    q = deque()
    seen_q = deque()
    # create a node object
    node = Node3(start_row, start_idx, None)
    # append the first node to the queue
    q.append(node)
    
    c = 0
    
    # while the queue is not empty, continue looking for the end
    while q:
        n = q.popleft()
        set_trace()
        if (n.row_idx, n.col_idx) in seen_q:
            continue
        else:
            seen_q.append((n.row_idx, n.col_idx))
        
        # checks if reach the end (the color is read). if so return the node
        if matrix[n.row_idx][n.col_idx] == 1:
            return n
        
        # check if can move to left, up, right, down
        if valid_move3(matrix, n.row_idx, n.col_idx-1): # checks left
            if (n.row_idx, n.col_idx-1) not in seen_q:
                q.append(Node3(n.row_idx, n.col_idx-1, n))
            
        if valid_move3(matrix, n.row_idx+1, n.col_idx): # checks up
            if (n.row_idx+1, n.col_idx) not in seen_q:
                q.append(Node3(n.row_idx+1, n.col_idx, n))
            
        if valid_move3(matrix, n.row_idx, n.col_idx +1): # checks right
            if (n.row_idx, n.col_idx +1) not in seen_q:
                q.append(Node3(n.row_idx, n.col_idx +1, n))
            
        if valid_move3(matrix, n.row_idx-1, n.col_idx): # checks down
            if (n.row_idx-1, n.col_idx) not in seen_q:
                q.append(Node3(n.row_idx-1, n.col_idx , n))
            
        if c == 100:
#             print(c, n.row_idx, n.col_idx)
            c = 0
    
        c += 1
    # if reached here - no path was found
    print("DIDN'T FIND PATH")
    return

n = shortest_path3(maze)