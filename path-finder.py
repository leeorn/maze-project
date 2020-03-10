# import libraries
from collections import deque
import cv2
import numpy as np
import sys


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


# Node class, initiate its variables.
# row and col are the index location in maze prev is the previous node
class Node:
    def __init__(self, row, col, prev):
        self.row_idx = row
        self.col_idx = col
        self.prev = prev


# Find the shortest path between the starting point and endpoint
# Takes the image, start row and column, and row column
# Returns the last node if found the path
def shortest_path(img, start_row, start_col, end_row, end_col):
    # inite a queue (FIFO)
    seen_q2 = np.zeros([img.shape[0], img.shape[1]])
    q = deque()

    # create a node object
    node = Node(start_row, start_col, None)
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


# Function to resize the image
# Takes the image to be resized and by how much (what percent of original)
# returns a pointer the the resized image
def resize(img, per):
    scale_percent = per  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    return resized


# Recolor the image to white and black to make the pixel value more contrast
# Takes the image
# Returns the color imaged
def recolor_img(img):
    # recolor the resized img
    for r in range(img.shape[0]):
        for c in range(img.shape[1]):

            black_threshold = np.array([100, 100, 100])
            # color black
            if np.any(np.less(img[r][c], black_threshold)):
                img[r][c] = (0, 0, 0)

            # color white
            else:
                img[r][c] = (255, 255, 255)

    return img


# Function to color the path from starting to ending position with width w
# Takes the image, the last node and the width of the path want to color
# Returns the image with a colored path (green)
def color_path(img, node, w):
    # color the path
    n = node

    while n:
        # Color the pixel green
        img[n.row_idx - w:n.row_idx + w, n.col_idx - w:n.col_idx + w, :] = (0, 255, 0)
        n = n.prev

    # write the img to current folder
    cv2.imwrite("maze-solved.jpg", img_resized)

    return img


# If a starting/ ending points are black at the beginning, the find path algo won't work.
# This function confirms that the points are valid (although they're hardcoded points, the light condition can change)
# Takes the image and the list of tuples of start and endpoints
def check_valid_pts(img, pt_list):
    black_threshold = np.array([100, 100, 100])
    valid_pts = []

    # goes over each point, check they are above threshold
    for pt in pt_list:
        row_val = pt[0]
        col_val = pt[1]
        # if valid, add them to the valid list
        if np.any(np.greater([row_val][col_val], black_threshold)):
            valid_pts.append((row_val, col_val))

    return valid_pts


# Function to take a picture using Pi camera.
# returns the name of the image that was taken
def take_pic():
    # Uncomment when connected to the Pi! that should take a picture and save at current directory with name 'maze.jpg'
    # import picamera
    # import time
    # import os
    #
    # print("Give the picture file a name:")
    # name = input()
    # name = name+'.img'
    # path = os.getcwd()
    # print(f"A picture name {name} was saved at {path}")
    # camera = picamera.PiCamera()
    #
    # camera.capture(name)
    # camera.close()
    # return name
    pass


def main(file_name, start_r, start_c, end_r, end_c):
    # recolor the maze to white and black
    colored_img = recolor_img(file_name.copy())

    # find shortest path
    n = shortest_path(colored_img, start_r, start_c, end_r, end_c)

    if n:
        print("Found path")

        # color the path we found
        return color_path(file_name, n, 1)

    else:
        return None


# *******************************************************************************
# name = take_pic()

# ** Remove the below line when the pi camera is connect! **
name = 'maze.jpg'

# loads the image
pic = cv2.imread(name)

# the percent of the original image. If changed, all the points (start and end) should be modified
resize_percent = 30

# resize it to X (resize_per) percent
img_resized = resize(pic, resize_percent)

# define the starting and ending points, the values are the pixel location in the maze
# Point A (60,80)
pt_a_row = 60
pt_a_col = 80

# Point B (120,285)
pt_b_row = 120
pt_b_col = 285

# Point C (260, 290)
pt_c_row = 260
pt_c_col = 290

# Point D (270, 230)
pt_d_row = 270
pt_d_col = 230

# copy of the image
img_copy = img_resized.copy()

# color the start and end options
img_copy[pt_a_row:pt_a_row + 5, pt_a_col:pt_a_col + 5, :] = (255, 0, 0)
img_copy[pt_b_row:pt_b_row + 5, pt_b_col:pt_b_col + 5, :] = (255, 0, 0)
img_copy[pt_c_row:pt_c_row + 5, pt_c_col:pt_c_col + 5, :] = (255, 0, 0)
img_copy[pt_d_row:pt_d_row + 5, pt_d_col:pt_d_col + 5, :] = (255, 0, 0)


# Show the user the options, and ask to choose a start and end point
# writing text on the image
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (0, 0, 255)
line_type = 2

# for 'A'
location_of_a = (pt_a_col, pt_a_row)
cv2.putText(img_copy, 'A', location_of_a, font, font_scale, font_color)

# for 'B'
location_of_b = (pt_b_col, pt_b_row)
cv2.putText(img_copy, 'B', location_of_b, font, font_scale, font_color)

# for 'C'
location_of_c = (pt_c_col, pt_c_row)
cv2.putText(img_copy, 'C', location_of_c, font, font_scale, font_color)

# for 'D'
location_of_d = (pt_d_col, pt_d_row)
cv2.putText(img_copy, 'D', location_of_d, font, font_scale, font_color)

print("Please choose starting and ending points, then close the window, and write you decision")

# show resized image and ask where they what to start and end
cv2.imshow("Maze-Image", img_copy)
# wait to close the window
cv2.waitKey(0)
cv2.destroyAllWindows()

print("What is your desire START point?")
start = input()
start = start.lower()
print("What is your desire END point?")
end = input()

start_row = 0
start_col = 0
end_row = 0
end_col = 0
valid_start = True
valid_end = True

# check what start and end point the user gave
if start == 'a':
    start_row = pt_a_row
    start_col = pt_a_col
elif start == 'b':
    start_row = pt_b_row
    start_col = pt_b_col
elif start == 'c':
    start_row = pt_c_row
    start_col = pt_c_col
elif start == 'd':
    start_row = pt_d_row
    start_col = pt_d_col
else:
    # print("Invalid input was provided. Please restart.")
    # sys.exit()
    valid_start = False


if end == 'a':
    end_row = pt_a_row
    end_col = pt_a_col
elif end == 'b':
    end_row = pt_b_row
    end_col = pt_b_col
elif end == 'c':
    end_row = pt_c_row
    end_col = pt_c_col
elif end == 'd':
    end_row = pt_d_row
    end_col = pt_d_col
else:
    # print("Invalid input was provided. Please restart.")
    # sys.exit()
    valid_end = False

if not valid_start or not valid_end:
    print("Invalid inputs were given. Please start 2 different start and end point from the options")
    sys.exit(-1)

print("Working on finding the best path between these points...")

path_img = main(img_resized, start_row, start_col, end_row, end_col)

if np.any(path_img):
    cv2.imshow("Maze-path", path_img)

    # wait to close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

print("Done.")
