import cv2 as cv
import numpy as np 
import math

image = cv.imread("/home/tim_andrews/workspace/timandrews/Zip_Solver/src/test_image.png",cv.IMREAD_GRAYSCALE)

cv.imshow("Image", image)

cv.waitKey(0)

cv.destroyAllWindows()