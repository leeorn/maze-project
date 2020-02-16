import cv2
import numpy as np

black_square = np.zeros([300,300], dtype=np.uint8)

# create white square
black_square[75:175, 75:175] == 255

ret, thresh = cv2.threshold(black_square, 127, 255, 0)

img, con, hie = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

color = cv2.cvtColor(black_square, cv2.COLOR_GRAY2BGR)

black_square = cv2.drawContours(color, con, -1, (0,255,0), 2)

cv2.waitKey(0)
cv2.destroyAllWindows()


