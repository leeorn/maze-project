# import libraries
import numpy as np
import cv2
import timeit
from collections import deque

# Check if the given index is a valid place to explore (inside the boundaries, and not a wall)
# Takes in the image, and index for row and column
# Returns True or False based if the pixel is valid or not
def valid_move(img, row_idx, col_idx):
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

    # grayish color - if lower than that, the pixel is not clear (wall)
    black_treshold = np.array([100, 100, 100])
    if np.all(np.less(img[row_idx][col_idx], black_treshold)):
        return False

    # it's a valid move
    return True

# Node class, just initiate its variables
class Node:
    def __init__(self, row, col, prev):
        self.row_idx = row
        self.col_idx = col
        self.prev = prev

# Find the shortest path between the starting point and end point
# Takes the image, start row and column, and and row and column
# Returns the last node if found the path
def shortest_path(img, start_row, start_col, end_row, end_col):
    # inite a queue (FIFO)
    seen_q2 = np.zeros([img.shape[0], img.shape[1]])
    q = deque()

    # create a node object
    node = Node(start_row, start_col, None, None)
    # append the first node to the queue
    q.append(node)

    # while the queue is not empty, continue looking for the end
    while q:
        # remove the node from the queue
        n = q.popleft()

        # checks if reach the end. if so return the node
        if n.row_idx == end_row and n.col_idx == end_col:
            return n

        # if visited this area, don't visit again
        if seen_q2[n.row_idx][n.col_idx]:
            continue

        # check if can move to left, up, right, down

        # checks left
        if valid_move(img, n.row_idx, n.col_idx - 1):
            q.append(Node(n.row_idx, n.col_idx - 1, n))

        # checks up
        if valid_move(img, n.row_idx - 1, n.col_idx):
            q.append(Node(n.row_idx - 1, n.col_idx, n))

        # checks right
        if valid_move(img, n.row_idx, n.col_idx + 1):
            q.append(Node(n.row_idx, n.col_idx + 1, n))

        # checks down
        if valid_move(img, n.row_idx + 1, n.col_idx):
            q.append(Node(n.row_idx + 1, n.col_idx, n))

        seen_q2[n.row_idx][n.col_idx] = 1

    # if reached here - no path was found
    print("DIDN'T FIND PATH")
    return

# Recolor the image to white and black to make the pixel value more contrast
# Takes the image
# Returns the color imaged
def recolor_img(img):
    # recolor the resized img
    for r in range(img.shape[0]):
        for c in range(img.shape[1]):

            black_treshold = np.array([100, 100, 100])
            # color black
            if np.any(np.less(img[r][c], black_treshold)):
                img[r][c] = (0, 0, 0)

            # color white
            else:
                img[r][c] = (255, 255, 255)

    return img

# Function to color the path from starting to ending position with width w
# Takes the image, the last node and the width of the path want to color
# Returns the image with colored path (green)
def color_path(img, node, w):
    # color the path
    n = node

    while n:
        # Color the pixel green
        img[n.row_idx - w:n1.row_idx + w, n1.col_idx - w:n1.col_idx + w, :] = (0, 255, 0)
        n = n.prev

    # write the img to current folder
    cv2.imwrite("maze.jpg", img_resized)

    return img


#def main(file_name, resize_per, start_r, start_c, end_r, end_c):
    # load the image

resize_per = 50
start_r = 100
start_c = 100

end_r = 410
end_c = 450



pic = cv2.imread('maze.jpg')

    # resize it to X (resize_per) percent
img_resized = resize(pic, resize_per)

    # recolor the maze to white and black
colored_img = recolor_img(img_resized.copy())

    # find shortest path
n = shortest_path2(colored_img, start_r, start_c, end_r, end_c)

if n:
    print("Found path")

        # show the image with the path
    color_path(img_resized, n, 1)


# checks how the get arguments from the command line
if __name__ == 'main':
    # TOOO
    # ask the user for start and end position
    # Show the start and end positions (color with red/blue)
    # If user is happy with the choice, continue to solve the maze

    main() # TODO need to add parameters
